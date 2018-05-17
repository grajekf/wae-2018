from geneticalgorithm.bounded.boundedmutationfunctor import BoundedMutationFunctor

#Do not recommend it, most often the while loop goes on forever
class Resampling(BoundedMutationFunctor):

    def mutate(self, original):
        new = self.inner.mutate(original)
        while self._isoutside(new):
            new = self.inner.mutate(original)
        return new