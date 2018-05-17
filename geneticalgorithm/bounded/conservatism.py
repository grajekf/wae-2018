from geneticalgorithm.bounded.boundedmutationfunctor import BoundedMutationFunctor

class Conservatism(BoundedMutationFunctor):

    def mutate(self, original):
        new = self.inner.mutate(original)
        return original if self._isoutside(new) else new