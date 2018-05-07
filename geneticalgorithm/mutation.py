from geneticalgorithm.layer import Layer
import numpy as np

class MutationLayer(Layer):

    def __init__(self, inputs, mutation_function):
        super(MutationLayer, self).__init__(inputs)
        self.mutation_function = mutation_function

    def _dowork(self, population, fitness):
        return np.array([self.mutation_function(genom) for genom in population])

