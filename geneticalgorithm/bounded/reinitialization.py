from geneticalgorithm.bounded.boundedmutationfunctor import BoundedMutationFunctor

class Reinitialization(BoundedMutationFunctor):

    def __init__(self, inner, lower_boundary, upper_boundary, generator):
        super(Reinitialization, self).__init__(inner, lower_boundary, upper_boundary)
        self.generator = generator

    def mutate(self, original):
        new = self.inner.mutate(original)
        if self._isoutside(new):
            new = self.generator.generate(1)[0]
            return new