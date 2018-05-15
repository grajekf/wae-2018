from geneticalgorithm.layer import Layer
import numpy as np

class MutationLayer(Layer):

    def __init__(self, inputs, mutation_function, name = None, save_inputs=False):
        super(MutationLayer, self).__init__(inputs, name, save_inputs)
        self.mutation_function = mutation_function

    def _dowork(self, population, fitness):
        return np.array([self.mutation_function.mutate(genom) for genom in population])

    def _getparameters(self):
        return {**{
            "mutation_function": type(self.mutation_function).__name__, 
        },
        **self.mutation_function.getparameters()
        }
    
    def _setparameter(self, key, value):
        changed = False
        if key == "mutation_function":
            self.mutation_function = value
            changed = True
        changed = changed or self.mutation_function.setparameter(key, value)
        return changed

