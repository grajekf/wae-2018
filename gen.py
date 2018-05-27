#!/usr/bin/env python3
import argparse
from heapq import nlargest
import cProfile

import numpy as np
from PIL import Image
from keras import backend as K
from keras.applications import inception_v3
from keras.preprocessing import image
from utils import to_model_image
from geneticalgorithm.model import Model
from geneticalgorithm.crossover import CrossoverLayer
from geneticalgorithm.crossoverfunctions import OnePointCrossover
from geneticalgorithm.mutation import MutationLayer
from geneticalgorithm.mutationfunctions import UniformIntegerMutation
from geneticalgorithm.elitism import ElitismLayer
from geneticalgorithm.selectionfunctions import TournamentSelection
from geneticalgorithm.populationgenerator import UniformClippedPopulationGenerator
from geneticalgorithm.stopconditions import budget_stopcondition_generator, patience_stopcondition_generator
from geneticalgorithm.onefifthmutationadjuster import OneFifthMutationAdjuster
from mysubcribers import Printer, ServerHook, Logger, PopulationVisualizer
from geneticalgorithm.bounded.conservatism import Conservatism
from geneticalgorithm.bounded.projection import Projection
from geneticalgorithm.bounded.resampling import Resampling
from geneticalgorithm.bounded.reinitialization import Reinitialization
from geneticalgorithm.bounded.reflection import Reflection


POPULATIONSIZE = 70
MUTATIONRATE = 0.05
MUTATIONVARIANCE = 5
TOURNAMENTSIZE = 4
MAXCHANGE = 15
CHANGEEXPONENT = 0
ELITISM = 0
CLASSESTOAVOID = 5
FINISH = 0.7
ALPHA = 1
PATIENCE = 100000
BOUNDSTRATEGY = "projection"
OUTPUTFILE = "hacked-image.png"


def fitness_change_original_generator(model_input_layer, model_output_layer, original_image, original_classes):
    cost_function = model_output_layer[:, :]
    grab_cost_from_model = K.function(
        [model_input_layer, K.learning_phase()], [cost_function])

    def fitness_function(population):
        class_probabilities = grab_cost_from_model(
            [to_model_image(population), 0])[0]
        probs_original = np.array([class_probabilities[:, i] for i in range(
            len(class_probabilities[0])) if i in original_classes])
        probs_other = np.array([class_probabilities[:, i] for i in range(
            len(class_probabilities[0])) if i not in original_classes])
        # highest probability other then original classes
        max_other_classes = np.array([max(p) for p in probs_other.T])
        # highest probability of original classes
        max_original_classes = np.array([max(p) for p in probs_original.T])
        fitness = max_other_classes - max_original_classes + 1.0
        return fitness
    return fitness_function


def stopping_when_more_likely_by(stopping_value):
    def stopping(population, fitness, **kwargs):
        return max(fitness) >= 1 + stopping_value
    return stopping


def stop_condition(finish, budget, patience):
    value_condition = stopping_when_more_likely_by(finish)
    patience_condition = patience_stopcondition_generator(patience)
    if budget is None:
        def inner_no_budget(population, fitness, **kwargs):
            return value_condition(population, fitness, **kwargs) or patience_condition(population, fitness, **kwargs)
        return inner_no_budget
    budget_condition = budget_stopcondition_generator(budget)

    def inner(population, fitness, **kwargs):
        return budget_condition(population, fitness, **kwargs) or value_condition(population, fitness, **kwargs) or patience_condition(population, fitness, **kwargs)
    return inner


def args(p=None):
    parser = argparse.ArgumentParser() if p is None else p
    parser.add_argument('input', metavar='INPUT_FILE',
                        type=str, help='Input image path')
    parser.add_argument('-o', metavar='OUTPUT_FILE',
                        default=OUTPUTFILE, help='Output image path', type=str)
    parser.add_argument('-p', metavar='POPULATIONSIZE',
                        default=POPULATIONSIZE, help='Population size', type=int)
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
    parser.add_argument('-l', metavar='LOG_FILE',
                        default=None, help='Log file path', type=str)
    parser.add_argument('-ts', metavar='TOURNAMENT_SIZE', default=TOURNAMENTSIZE,
                        help='Size of tournament in selection', type=int)
    parser.add_argument('-b', metavar='BUDGET',
                        help='Number of fitness function evaluations the algorithm can use', type=int)
    parser.add_argument('-bs', metavar='BOUNDSTRATEGY', default=BOUNDSTRATEGY, help='Strategy to use for chromosome outside of allowed range',
                        type=str)
    parser.add_argument('-pat', metavar='PATIENCE', default=PATIENCE,
                        help='How many generations to go without improvement', type=int)
    parser.add_argument('-vp', action='store_true',
                        help='Should the population be visualized at the end of the algorithm')
    # parser.add_argument('-a', metavar='ALPHA', default=ALPHA, help='Factor used to adjust mutation variance according to the one fifth rule',
    #                     type=float)

    if p is None:
        args = parser.parse_args()
        return args


def bound_strategy_from_arg(bound_strategy, mutation, lower, upper, generator):
    if bound_strategy == "resampling":
        return Resampling(mutation, lower, upper)
    if bound_strategy == "conservatism":
        return Conservatism(mutation, lower, upper)
    if bound_strategy == "projection":
        return Projection(mutation, lower, upper)
    if bound_strategy == "reflection":
        return Reflection(mutation, lower, upper)
    if bound_strategy == "reinitialization":
        return Reinitialization(mutation, lower, upper, generator)
    return mutation


def build_genetic_model(inception_input, inception_output, original_image, original_classes,
                        population_size, tournament_size, elitism_count, mutation_rate, mutation_variance, max_change_below, max_change_above, bound_strategy,
                        generator):
    elitism = ElitismLayer(None, elitism_count) if elitism_count > 0 else None
    crossover = CrossoverLayer(None,
                               OnePointCrossover(),
                               TournamentSelection(tournament_size),
                               population_size - elitism_count)
    first_layer = crossover
    mutation = MutationLayer(first_layer,
                             bound_strategy_from_arg(bound_strategy, UniformIntegerMutation(mutation_rate, mutation_variance), max_change_below, max_change_above, generator))
    return Model(mutation if elitism is None else [mutation, elitism], fitness_change_original_generator(inception_input, inception_output, original_image, original_classes))


def run(args, hook=None):
    inp, out, population_size, mutation_rate, mutation_variance, max_change, classes_to_avoid, elitism, finish, log_file, tournament_size, budget, bound_strategy, patience, visualize_population = args.input, args.o, args.p, args.mr, args.mv, args.c, args.ca, args.e, args.f, args.l, args.ts, args.b, args.bs, args.pat, args.vp

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
    print(predicted_classes)

    predictions = np.argsort(predictions, axis=1)
    original_classes = predictions[0][-classes_to_avoid:]

    population_generator = UniformClippedPopulationGenerator(
        input_image, max_change, 0, 255)

    genetic_alg = build_genetic_model(model_input_layer, model_output_layer, input_image, original_classes,
                                      population_size, tournament_size, elitism, mutation_rate, mutation_variance, max_change_below, max_change_above, bound_strategy,
                                      population_generator)

    initial_population = population_generator.generate(population_size)
    subscribers = [Printer() if hook is None else ServerHook(hook, model)]
    if visualize_population:
        subscribers.append(PopulationVisualizer())
    if log_file is not None:
        subscribers.append(Logger(
            log_file, model, classes_to_avoid=classes_to_avoid, max_change=max_change))

    population, fitness = genetic_alg.run(
        initial_population, stop_condition(finish, budget, patience), subscribers)
    # cProfile.runctx("genetic_alg.run(initial_population, stop_condition(finish, budget, patience), subscribers)", globals(), locals())

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


if __name__ == '__main__':
    run(args(), None)
