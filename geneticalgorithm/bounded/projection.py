from geneticalgorithm.bounded.boundedmutationfunctor import BoundedMutationFunctor
import numpy as np

class Projection(BoundedMutationFunctor):

    def mutate(self, original):
        new = self.inner.mutate(original)
        return np.clip(new, self.lower_boundary, self.upper_boundary)