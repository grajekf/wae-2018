#!/usr/bin/env python3
import numpy as np
from keras.preprocessing import image
from keras.applications import inception_v3
from keras import backend as K
from PIL import Image
from heapq import nlargest
import argparse

POPULATIONSIZE = 100
MUTATIONRATE = 0.05
MUTATIONVARIANCE = 6
TOURNAMENTSIZE = 4
MAXCHANGE = 15
CHANGEEXPONENT = 0
ELITISM = 0
CLASSESTOAVOID = 5
FINISH = 0.7
OUTPUTFILE = "hacked-image.png"

def mutate(original, rate, variance, max_below, max_above):
    return np.clip(original + np.random.randint(-variance, variance, size = original.shape) * 
                    np.random.choice([0, 1], size = original.shape, p = [1 - rate, rate]), max_below, max_above)

def crossover(a, b):
    aNew = a.flatten()
    bNew = b.flatten()
    cx = np.random.randint(1, len(aNew) - 1)
    aNew = np.concatenate([np.split(aNew, [cx])[0], np.split(bNew, [cx])[1]]).reshape(a.shape)
    return aNew

def create_initial_population(original, size, rate, variance, max_below, max_above):
    return [mutate(original, rate, variance, max_below, max_above) for i in range(size)]

def tournament_generator(tournament_size):
    def select_tournament(population_with_costs):
        return max([population_with_costs[i] for i in np.random.choice(len(population_with_costs), tournament_size)], key=lambda p: p[1])[0]
    return select_tournament

def get_parents(population, costs, parent_generator):
    return (parent_generator(list(zip(population, costs))), parent_generator(list(zip(population, costs))))

def costs_pixel_amount(original, population, costs, exponent):
    return [((p.size - np.count_nonzero((p - original).round(5))) / p.size)**exponent * c for p, c in zip(population, costs)]

def to_model_image(image):
    img = np.copy(image)
    img /= 255.0
    img -= 0.5
    img *= 2.0 
    return img  

def cost_change_original(population, probs, original_image, original_classes, exponent):
    probs_original = np.array([probs[:, i] for i in range(len(probs[0])) if i in original_classes])
    probs_other = np.array([probs[:, i] for i in range(len(probs[0])) if i not in original_classes])
    costs = np.array([max(p) for p in probs_other.T]) #highest probability other then original
    org_max = np.array([max(p) for p in probs_original.T])
    costs = org_max - costs
    prob = 1 - min(costs)
    costs = 1 - costs #Because the ga always needs to maximize
    return costs_pixel_amount(original_image, population, costs, exponent), prob

def cost_fake_another(population, probs, original_image, fake_class, exponent):
    costs = probs[:, fake_class]
    prob = max(costs)
    return costs_pixel_amount(original_image, population, costs, exponent), prob    

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='INPUT_FILE', type=str, help='Input image path')
    parser.add_argument('-o', metavar='OUTPUT_FILE', default=OUTPUTFILE, help='Output image path', type=str)
    parser.add_argument('-p', metavar='POPULATIONSIZE', default=POPULATIONSIZE, help='Population size', type=int)
    parser.add_argument('-mr', metavar='MUTATIONRATE', default=MUTATIONRATE, help='Chance to mutate [0 - 1]', type=float)
    parser.add_argument('-mv', metavar='MUTATIONVARIANCE', default=MUTATIONVARIANCE, help='Maximal mutation distance', type=int)
    parser.add_argument('-c', metavar='MAXCHANGE', default=MAXCHANGE, help='Maximal distance from original value', type=int)
    parser.add_argument('-ca', metavar='CLASSESTOAVOID', default=CLASSESTOAVOID, help='Number of best classes to avoid', type=int)
    parser.add_argument('-e', metavar='ELITISM', default=ELITISM, help='Number of best images to pass without change to next generation', type=int)
    parser.add_argument('-f', metavar='FINISHCONDITION', default=FINISH, help='Finish when max(other class) - max(classes to avoid) is bigger than this value', type=float)
    args = parser.parse_args()
    return args.input, args.o, args.p, args.mr, args.mv, args.c, args.ca, args.e, args.f

def main():
    inp, out, population_size, mutation_rate, mutation_variance, max_change, classes_to_avoid, elitism, finish = args()
    model = inception_v3.InceptionV3()
    model_input_layer = model.layers[0].input
    model_output_layer = model.layers[-1].output

    img = image.load_img(inp, target_size=(299, 299))
    input_image = image.img_to_array(img)


    img_scaled = to_model_image(input_image)

    max_change_below = np.clip(input_image - max_change, 0, 255)
    max_change_above = np.clip(input_image + max_change, 0, 255)

    input_image_extended = np.expand_dims(img_scaled, axis=0)

    predictions = model.predict(input_image_extended)

    predicted_classes = inception_v3.decode_predictions(predictions)
    print(predicted_classes[0])
    _, name, confidence = predicted_classes[0][0]
    print("This is a {} with {:.4}% confidence!".format(name, confidence * 100))

    predictions = np.argsort(predictions, axis=1)
    original_classes = predictions[0][-classes_to_avoid:]
    print(original_classes)
    # class_to_fake = 751 #racer

    cost_function = model_output_layer[:, :]
    grab_cost_from_model = K.function([model_input_layer, K.learning_phase()], [cost_function])

    prob = 0

    population = create_initial_population(input_image, population_size, 1, max_change, max_change_below, max_change_above)
    # print(population)


    try:
        while prob <= 1.0 + finish: #We want to end when another class is more likely than orignal
            scaled_population = to_model_image(population)
            probs = grab_cost_from_model([scaled_population, 0])[0]
            costs, prob = cost_change_original(population, probs, input_image, original_classes, CHANGEEXPONENT)

            if elitism > 0:
                elite = [p[0] for p in nlargest(elitism, list(zip(population, costs)), key=lambda p: p[1])]
            population = [mutate(crossover(*get_parents(population, costs, tournament_generator(TOURNAMENTSIZE))), 
                                    mutation_rate, mutation_variance, max_change_below, max_change_above) 
                            for i in range(len(population) - elitism)]
            if elitism > 0:
                population = np.concatenate([elite, population])

            print("Best fitness: {:.8}".format(prob))
    except KeyboardInterrupt:
        pass

    hacked_image = max(list(zip(population, costs)), key=lambda p: p[1])[0]

    # Save the hacked image!
    im = Image.fromarray(hacked_image.astype(np.uint8))
    im.save(out)

    hacked_image = to_model_image(hacked_image)
    hacked_image_extended = np.expand_dims(hacked_image, axis=0)

    predictions = model.predict(hacked_image_extended)

    predicted_classes = inception_v3.decode_predictions(predictions)
    print(predicted_classes[0])
    _, name, confidence = predicted_classes[0][0]
    print("This is a {} with {:.4}% confidence!".format(name, confidence * 100))

if __name__ == '__main__':
    main()