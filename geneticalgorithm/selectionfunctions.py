import numpy as np


def tournament_generator(tournament_size):
    def select_tournament(population, fitness):
        population_with_fitness = list(zip(population, fitness))
        return max([population_with_fitness[i] for i in np.random.choice(len(population_with_fitness), tournament_size)],
                   key=lambda p: p[1])[0]

    return select_tournament


def repeat(fun, n = 2):
    def inner(population, fitness):
        return [fun(population, fitness) for i in range(n)]
    return inner
