
class Model():
    def __init__(self, output_layer, fitness_function):
        self.output_layer = output_layer
        self.fitness_function = self.__wrap_fitness(fitness_function)

    def __wrap_fitness(self, fitness_function):
        def inner(population):
            self.current_uses = self.current_uses + len(population)
            return fitness_function(population)
        return inner

    def run(self, initial_population, stopping_criterion, subscribers = []):
        self.generation = 1
        self.current_uses = 0
        population = initial_population
        fitness = self.fitness_function(population)
        try:
            while not stopping_criterion(population, fitness, current_uses=self.current_uses):
                self.output_layer.resetcache()
                population = self.output_layer.forward(population, fitness)
                fitness = self.fitness_function(population)
                for s in subscribers:
                    s.notify(self.generation, population, fitness, current_uses=self.current_uses)
                self.generation = self.generation + 1
        except KeyboardInterrupt:
            pass  
        return population, fitness