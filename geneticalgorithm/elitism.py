from geneticalgorithm.layer import Layer
from heapq import nlargest

class ElitismLayer(Layer):
    def __init__(self, inputs, elitism_count):
        super(ElitismLayer, self).__init__(inputs)
        self.elitism_count = elitism_count
    
    def _dowork(self, population, costs):
        return [p[0] for p in nlargest(self.elitism_count, list(zip(population, costs)), key=lambda p: p[1])]