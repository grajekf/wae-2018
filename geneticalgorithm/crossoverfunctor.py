from geneticalgorithm.parametrisable import Parametrisible
from abc import ABC

class CrossoverFunctor(Parametrisible, ABC):
    def crossover(self, a, b):
        pass