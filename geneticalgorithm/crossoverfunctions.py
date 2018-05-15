import numpy as np
from geneticalgorithm.crossoverfunctor import CrossoverFunctor

class OnePointCrossover(CrossoverFunctor):
    def crossover(self, a, b):
        aNew = a.flatten()
        bNew = b.flatten()
        cx = np.random.randint(1, len(aNew) - 1)
        aNew = np.concatenate([np.split(aNew, [cx])[0], np.split(bNew, [cx])[1]]).reshape(a.shape)
        return aNew

    def getparameters(self):
        return {

        }

    def setparameter(self, key, value):
        return False

