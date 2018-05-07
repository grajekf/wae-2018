from geneticalgorithm.layer import Layer
import collections
import numpy as np

class CrossoverLayer(Layer):

    def __init__(self, inputs, crossover_function, selection_function, children_count):
        super(CrossoverLayer, self).__init__(inputs)
        self.crossover_function = crossover_function
        self.selection_function = selection_function
        self.children_count = children_count
    
    def _dowork(self, population, fitness):
        new_population = []
        
        while len(new_population) < self.children_count:
            parents = self.selection_function(population, fitness)
            child = self.crossover_function(*parents)
            new_population.append(child)

        new_population = np.array(new_population)
        return new_population