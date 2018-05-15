from geneticalgorithm.parametrisable import Parametrisible
from abc import ABC

class MutationFunctor(Parametrisible, ABC):
    def mutate(self, original):
        pass