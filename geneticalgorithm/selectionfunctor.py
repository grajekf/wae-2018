from geneticalgorithm.parametrisable import Parametrisible
from abc import ABC

class SelectionFunctor(Parametrisible, ABC):
    def select(self, population, fitness):
        pass