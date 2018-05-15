from abc import ABC
import collections
import itertools
import numpy as np
from geneticalgorithm.parametrisable import Parametrisible
from functools import reduce

class Layer(Parametrisible, ABC):
    def __init__(self, inputs):
        if inputs is None:
            inputs = []
        if not isinstance(inputs, collections.Iterable):
            inputs = [inputs]
        self.inputs = inputs
        self.cached_population = None
    

    def forward(self, population, fitness):
        if self.cached_population is not None:
            return self.cached_population
        if len(self.inputs) > 0:
            new_population = []
            for i in self.inputs:
                new_population.extend(i.forward(population, fitness))
            population = np.array(new_population)
        population = self._dowork(population, fitness)
        self.cached_population = population
        return population

    def _dowork(self, population, fitness):
        pass

    def getparameters(self):
        params = {}
        for i in self.inputs:
            params = {**params, **i.getparameters()}
        params = {**params, **self._getparameters()}
        return params

    def _getparameters(self):
        pass

    def setparameter(self, key, value):
        changed = self._setparameter(key, value)
        for i in self.inputs:
            changed = changed or i.setparameter(key, value)
        return changed


    def _setparameter(self, key, value):
        pass
    
    def resetcache(self):
        self.cached_population = None
        for i in self.inputs:
            i.resetcache()