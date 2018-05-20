import numpy as np
from geneticalgorithm.mutationfunctor import MutationFunctor

class UniformIntegerMutation(MutationFunctor):

    def __init__(self, mutation_rate, mutation_variance):
        self.mutation_rate = mutation_rate
        self.mutation_variance = mutation_variance

    def mutate(self, original):
        # noise = (np.random.random(size=original.shape) < self.mutation_rate) * np.random.random_integers(-self.mutation_variance, self.mutation_variance, size=original.shape)
        noise = (np.random.random(size=original.shape) < self.mutation_rate) * np.random.choice(range(-self.mutation_variance, self.mutation_variance + 1), size=original.shape)
        return original +  noise

    def getparameters(self):
        return {
            'mutation_rate': self.mutation_rate,
            'mutation_variance': self.mutation_variance
        }

    def setparameter(self, key, value):
        changed = False
        if key == "mutation_rate":
            self.mutation_rate = value
            changed = True
        if key == "mutation_variance":
            self.mutation_variance = value
            changed = True
        return changed