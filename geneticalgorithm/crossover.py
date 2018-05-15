from geneticalgorithm.layer import Layer
import collections
import numpy as np

class CrossoverLayer(Layer):

    def __init__(self, inputs, crossover_function, selection_function, children_count, name = None, save_inputs=False):
        super(CrossoverLayer, self).__init__(inputs, name, save_inputs)
        self.crossover_function = crossover_function
        self.selection_function = selection_function
        self.children_count = children_count
    
    def _dowork(self, population, fitness):
        new_population = []
        
        while len(new_population) < self.children_count:
            parents = self.selection_function.select(population, fitness)
            child = self.crossover_function.crossover(*parents)
            new_population.append(child)

        new_population = np.array(new_population)
        return new_population

    def _getparameters(self):
        return {**{
            "crossover_function": type(self.crossover_function).__name__, 
            "selection_function": type(self.selection_function).__name__
        },
        **self.crossover_function.getparameters(),
        **self.selection_function.getparameters() }
    
    def _setparameter(self, key, value):
        changed = False
        if key == "crossover_function":
            self.crossover_function = value
            changed = True
        if key == "selection_function":
            self.selection_function = value
            changed = True
        changed = changed or self.crossover_function.setparameter(key, value) or self.selection_function.setparameter(key, value)
        return changed