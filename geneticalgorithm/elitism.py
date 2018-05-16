from geneticalgorithm.layer import Layer
from heapq import nlargest

class ElitismLayer(Layer):
    def __init__(self, inputs, elitism_count, name = None, save_inputs=False):
        super(ElitismLayer, self).__init__(inputs, name, save_inputs)
        self.elitism_count = elitism_count
    
    def _dowork(self, population, costs):
        return [p[0] for p in nlargest(self.elitism_count, list(zip(population, costs)), key=lambda p: p[1])]

    def _getparameters(self):
        return {
            "elitism_count": self.elitism_count, 
        }
    
    def _setparameter(self, key, value):
        changed = False
        if key == "elitism_count":
            self.elitism_count = value
            changed = True
        return changed