import collections
from geneticalgorithm.layer import Layer
class Model():
    class CollectLayer(Layer):

        def _dowork(self, population, fitness):
            return population


    def __init__(self, output_layers, fitness_function, parameter_adjusters = []):
        self.output_layer = Model.CollectLayer(output_layers)
        self.fitness_function = self.__wrap_fitness(fitness_function)
        self.parameter_adjusters = parameter_adjusters

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
            while not stopping_criterion(population, fitness, current_uses=self.current_uses, generation=self.generation):
                self.output_layer.resetcache()
                population = self.output_layer.forward(population, fitness)
                fitness = self.fitness_function(population)
                for s in subscribers:
                    s.notify(self.generation, population, fitness, current_fitness_uses=self.current_uses, layer_parameters=self.output_layer.getparameters())
                for parameter_adjuster in self.parameter_adjusters:
                    parameter_adjuster.adjust(self.output_layer, population, fitness, self.generation, fitness_function=self.fitness_function)
                self.generation = self.generation + 1
        except KeyboardInterrupt:
            pass
        for s in subscribers:
            s.on_finish()
        return population, fitness