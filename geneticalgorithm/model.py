
class Model():
    def __init__(self, output_layer, fitness_function):
        self.output_layer = output_layer
        self.fitness_function = fitness_function

    def run(self, initial_population, stopping_criterion, subscribers = []):
        self.generation = 1
        population = initial_population
        fitness = self.fitness_function(population)
        try:
            while not stopping_criterion(population, fitness):
                self.output_layer.resetcache()
                population = self.output_layer.forward(population, fitness)
                fitness = self.fitness_function(population)
                self.generation = self.generation + 1
                for s in subscribers:
                    s.notify(self.generation, population, fitness)
        except KeyboardInterrupt:
            pass  
        return population, fitness