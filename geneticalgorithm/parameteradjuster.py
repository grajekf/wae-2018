from abc import ABC

class ParameterAdjuster(ABC):

    def adjust(self, layer_graph, population, fitness, generation, **kwargs):
        pass