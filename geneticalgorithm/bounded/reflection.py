from geneticalgorithm.bounded.boundedmutationfunctor import BoundedMutationFunctor
import numpy as np


class Reflection(BoundedMutationFunctor):
    def mutate(self, original):
        new = self.inner.mutate(original)
        while self._isoutside(new):
            self.__reflect(new)
        return new


    def __reflect(self, chromosome):
        lower_filtered = self.lower_boundary[np.where(chromosome < self.lower_boundary)]
        upper_filtered = self.upper_boundary[np.where(chromosome > self.upper_boundary)]
        chromosome[np.where(chromosome < self.lower_boundary)] = 2 * lower_filtered - chromosome[np.where(chromosome < self.lower_boundary)]
        chromosome[np.where(chromosome > self.upper_boundary)] = 2 * upper_filtered - chromosome[np.where(chromosome > self.upper_boundary)]