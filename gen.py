#!/usr/bin/env python3
import argparse
from heapq import nlargest

import numpy as np
from PIL import Image
from keras import backend as K
from keras.applications import inception_v3
from keras.preprocessing import image
from geneticalgorithm.model import Model
from geneticalgorithm.crossover import CrossoverLayer
import geneticalgorithm.crossoverfunctions
from geneticalgorithm.mutation import MutationLayer
import geneticalgorithm.mutationfunctions
from geneticalgorithm.elitism import ElitismLayer
from geneticalgorithm.selectionfunctions import tournament_generator, repeat
from geneticalgorithm.populationgenerator import UniformClippedPopulationGenerator
from mysubcribers import Printer


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



def to_model_image(image):
    img = np.copy(image)
    img /= 255.0
    img -= 0.5
    img *= 2.0
    return img


def fitness_change_original_generator(model_input_layer, model_output_layer, original_image, original_classes):
    cost_function = model_output_layer[:, :]
    grab_cost_from_model = K.function([model_input_layer, K.learning_phase()], [cost_function])
    def fitness_function(population):
        class_probabilities = grab_cost_from_model([to_model_image(population), 0])[0]
        probs_original = np.array([class_probabilities[:, i] for i in range(len(class_probabilities[0])) if i in original_classes])
        probs_other = np.array([class_probabilities[:, i] for i in range(len(class_probabilities[0])) if i not in original_classes])
        # print(class_probabilities)
        max_other_classes = np.array([max(p) for p in probs_other.T])  # highest probability other then original classes
        max_original_classes = np.array([max(p) for p in probs_original.T]) # highest probability of original classes
        fitness = max_other_classes - max_original_classes + 1.0
        return fitness
    return fitness_function


def stopping_when_more_likely_by(stopping_value):
    def stopping(population, fitness):
        return max(fitness) >= 1 + stopping_value
    return stopping



def args(p=None):
    parser = argparse.ArgumentParser() if p is None else p
    parser.add_argument('input', metavar='INPUT_FILE', type=str, help='Input image path')
    parser.add_argument('-o', metavar='OUTPUT_FILE', default=OUTPUTFILE, help='Output image path', type=str)
    parser.add_argument('-p', metavar='POPULATIONSIZE', default=POPULATIONSIZE, help='Population size', type=int)
    parser.add_argument('-mr', metavar='MUTATIONRATE', default=MUTATIONRATE, help='Chance to mutate [0 - 1]',
                        type=float)
    parser.add_argument('-mv', metavar='MUTATIONVARIANCE', default=MUTATIONVARIANCE, help='Maximal mutation distance',
                        type=int)
    parser.add_argument('-c', metavar='MAXCHANGE', default=MAXCHANGE, help='Maximal distance from original value',
                        type=int)
    parser.add_argument('-ca', metavar='CLASSESTOAVOID', default=CLASSESTOAVOID, help='Number of best classes to avoid',
                        type=int)
    parser.add_argument('-e', metavar='ELITISM', default=ELITISM,
                        help='Number of best images to pass without change to next generation', type=int)
    parser.add_argument('-f', metavar='FINISHCONDITION', default=FINISH,
                        help='Finish when max(other class) - max(classes to avoid) is bigger than this value',
                        type=float)
    parser.add_argument('-ts', metavar='TOURNAMENT_SIZE', default=TOURNAMENTSIZE, help='Size of tournament in selection', type=int)

    if p is None:
        args = parser.parse_args()
        return args


def predict_classes(model, image, top_count=5):
    input_image_extended = np.expand_dims(image, axis=0)
    predictions = model.predict(input_image_extended)
    predicted_classes = inception_v3.decode_predictions(predictions, top=top_count)
    results = []
    for i in range(top_count):
        _, name, confidence = predicted_classes[0][i]
        results.append({'className': name, 'probability': float(confidence)})
    return results

def build_genetic_model(inception_input, inception_output, original_image, original_classes,
        population_size, tournament_size, elitism_count, mutation_rate, mutation_variance, max_change_below, max_change_above):
    elitism = ElitismLayer(None, elitism_count) if elitism_count > 0 else None
    crossover = CrossoverLayer(None, 
        geneticalgorithm.crossoverfunctions.one_point_crossover, 
        repeat(tournament_generator(tournament_size)),
        population_size - elitism_count)
    first_layer = [crossover, elitism] if elitism is not None else crossover
    mutation = MutationLayer(first_layer, 
        geneticalgorithm.mutationfunctions.clipped_uniform_integer_mutation_generator(mutation_rate, mutation_variance, max_change_below, max_change_above))
    return Model(mutation, fitness_change_original_generator(inception_input, inception_output, original_image, original_classes))


def run(args, hook=None):
    inp, out, population_size, mutation_rate, mutation_variance, max_change, classes_to_avoid, elitism, finish, tournament_size = args.input, args.o, args.p, args.mr, args.mv, args.c, args.ca, args.e, args.f, args.ts

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

    predictions = np.argsort(predictions, axis=1)
    original_classes = predictions[0][-classes_to_avoid:]

    genetic_alg = build_genetic_model(model_input_layer, model_output_layer, input_image, original_classes, 
        population_size, tournament_size, elitism, mutation_rate, mutation_variance, max_change_below, max_change_above)
    
    
    initial_population = UniformClippedPopulationGenerator(input_image, max_change, 0, 255).generate(population_size)

    population, fitness = genetic_alg.run(initial_population, stopping_when_more_likely_by(finish), subscribers=[Printer()])  

    hacked_image = max(list(zip(population, fitness)), key=lambda p: p[1])[0]
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

    # prob = 0

    # population = create_initial_population(input_image, population_size, 1, max_change, max_change_below,
    #                                        max_change_above)
    # generation = 1
    # try:
    #     while prob <= 1.0 + finish:  # We want to end when another class is more likely than orignal
    #         scaled_population = to_model_image(population)
    #         probs = grab_cost_from_model([scaled_population, 0])[0]

    #         costs, prob, objectiveFunction = cost_change_original(population, probs, input_image, original_classes,
    #                                                               CHANGEEXPONENT)

    #         if elitism > 0:
    #             elite = [p[0] for p in nlargest(elitism, list(zip(population, costs)), key=lambda p: p[1])]
    #         population = [mutate(crossover(*get_parents(population, costs, tournament_generator(TOURNAMENTSIZE))),
    #                              mutation_rate, mutation_variance, max_change_below, max_change_above)
    #                       for i in range(len(population) - elitism)]
    #         if elitism > 0:
    #             population = np.concatenate([elite, population])

    #         # calculate stats
    #         best = float(np.max(objectiveFunction))
    #         mean = float(np.mean(objectiveFunction))
    #         median = float(np.median(objectiveFunction))
    #         worst = float(np.min(objectiveFunction))
    #         bestSpecimen = population[np.argmax(objectiveFunction)]
    #         predictedClasses = predict_classes(model, to_model_image(bestSpecimen))
    #         if hook is not None:
    #             print('calling hook')
    #             hook({
    #                 'objectiveFunction': {
    #                     'best': best,
    #                     'worst': worst,
    #                     'mean': mean,
    #                     'median': median
    #                 },
    #                 'generation': generation,
    #                 'bestSpecimen': {
    #                     'data': Image.fromarray(bestSpecimen.astype(np.uint8)),
    #                     'predictions': predictedClasses
    #                 }
    #             })

    #         generation += 1
    # except KeyboardInterrupt:
    #     pass

    # hacked_image = max(list(zip(population, costs)), key=lambda p: p[1])[0]

    # # Save the hacked image!
    # im = Image.fromarray(hacked_image.astype(np.uint8))
    # im.save(out)

    # hacked_image = to_model_image(hacked_image)
    # hacked_image_extended = np.expand_dims(hacked_image, axis=0)

    # predictions = model.predict(hacked_image_extended)

    # predicted_classes = inception_v3.decode_predictions(predictions)
    # print(predicted_classes[0])
    # _, name, confidence = predicted_classes[0][0]
    # print("This is a {} with {:.4}% confidence!".format(name, confidence * 100))


if __name__ == '__main__':
    run(args(), lambda data: print(data))
