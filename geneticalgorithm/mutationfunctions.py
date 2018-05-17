import numpy as np
from geneticalgorithm.mutationfunctor import MutationFunctor

class UniformIntegerMutation(MutationFunctor):

    def __init__(self, mutation_rate, mutation_variance):
        self.mutation_rate = mutation_rate
        self.mutation_variance = mutation_variance

    def mutate(self, original):
        return original + np.random.randint(-self.mutation_variance, self.mutation_variance, size=original.shape) * np.random.choice([0, 1], size=original.shape, p=[1 - self.mutation_rate, self.mutation_rate])

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