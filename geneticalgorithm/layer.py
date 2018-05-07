from abc import ABC
import collections
import itertools
import numpy as np
from functools import reduce

class Layer(ABC):
    def __init__(self, inputs):
        # self.outputs = []
        if inputs is None:
            inputs = []
        if not isinstance(inputs, collections.Iterable):
            inputs = [inputs]
        # for i in inputs:
        #     inputs._addoutput(i)
        self.inputs = inputs
        self.cached_population = None
    
    # def _addoutput(self, output):
    #     self.outputs.append(output)

    def forward(self, population, fitness):
        if self.cached_population is not None:
            return self.cached_population
        if len(self.inputs) > 0:
            new_population = []
            for i in self.inputs:
                new_population.extend(i.forward(population, fitness))
            population = np.array(new_population)
            # print(population.shape)
        population = self._dowork(population, fitness)
        self.cached_population = population
        return population

    def _dowork(self, population, fitness):
        pass
    
    def resetcache(self):
        self.cached_population = None
        for i in self.inputs:
            i.resetcache()