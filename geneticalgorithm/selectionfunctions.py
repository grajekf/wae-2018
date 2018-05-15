import numpy as np
from geneticalgorithm.selectionfunctor import SelectionFunctor

class TournamentSelection(SelectionFunctor):
    def __init__(self, torunament_size):
        self.tournament_size = torunament_size

    def _select(self, population, fitness):
        population_with_fitness = list(zip(population, fitness))
        return max([population_with_fitness[i] for i in np.random.choice(len(population_with_fitness), self.tournament_size)],
                   key=lambda p: p[1])[0]   
    
    def select(self, population, fitness):
        return self._select(population, fitness), self._select(population, fitness)

    def getparameters(self):
        return {
            'tournament_size': self.tournament_size
        }

    def setparameter(self, key, value):
        changed = False
        if key == "tournament_size":
            self.tournament_size = value
            changed = True
        return changed



# def tournament_generator(tournament_size):
#     def select_tournament(population, fitness):
#         population_with_fitness = list(zip(population, fitness))
#         return max([population_with_fitness[i] for i in np.random.choice(len(population_with_fitness), tournament_size)],
#                    key=lambda p: p[1])[0]

#     return select_tournament


# def repeat(fun, n = 2):
#     def inner(population, fitness):
#         return [fun(population, fitness) for i in range(n)]
#     return inner
