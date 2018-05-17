from geneticalgorithm.mutationfunctor import MutationFunctor
from abc import ABC
import numpy as np

class BoundedMutationFunctor(MutationFunctor, ABC):

    def __init__(self, inner, lower_boundary, upper_boundary):
        self.inner = inner
        self.lower_boundary = lower_boundary
        self.upper_boundary = upper_boundary

    def _isoutside(self, chromosome):
        return np.logical_or(chromosome < self.lower_boundary, chromosome > self.upper_boundary).any()

    def getparameters(self):
        return {**{
            "bounded_mutation_function":type(self.inner).__name__
        },
        **self.inner.getparameters(),
        **self._getparameters()}

    def _getparameters(self):
        return {}

    def setparameter(self, key, value):
        changed = False
        if key == "bounded_mutation_function":
            self.inner = value
            changed = True
        changed = changed or self._setparameter(key, value) or self.inner.setparameter(key, value)
        return changed 

    def _setparameter(self, key, value):
        return False
