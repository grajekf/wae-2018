from geneticalgorithm.parameteradjuster import ParameterAdjuster
import numpy as np


class OneFifthMutationAdjuster(ParameterAdjuster):

    def __init__(self, alpha):
        self.alpha = alpha

    def adjust(self, layer_graph, population, fitness, generation, **kwargs):
        fitness_function = kwargs["fitness_function"]
        parameters = layer_graph.getparameters()
        mutation_inputs = parameters["mutation_inputs"]
        mutation_inputs_fitness = fitness_function(mutation_inputs)
        mutation_variance = parameters["mutation_variance"]
        success_probability = np.sum(fitness > mutation_inputs_fitness) / len(fitness)
        if success_probability > 0.2:
            layer_graph.setparameter("mutation_variance", mutation_variance * self.alpha)
        if success_probability < 0.2:
            layer_graph.setparameter("mutation_variance", mutation_variance / self.alpha)
