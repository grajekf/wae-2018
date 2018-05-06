import numpy as np

def clipped_uniform_integer_mutation_generator(rate, variance, max_below, max_above):
    def mutate(original):
        return np.clip(original + np.random.randint(-variance, variance, size=original.shape) *
                    np.random.choice([0, 1], size=original.shape, p=[1 - rate, rate]), max_below, max_above)
    return mutate