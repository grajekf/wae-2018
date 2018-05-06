from geneticalgorithm.subscriber import Subscriber
import numpy as np

class Printer(Subscriber):
    def notify(self, generation, population, fitness):
        print(f"Generation: {generation}, Min fitness: {np.min(fitness)}, Avg fitness: {np.average(fitness)}, Max fitness: {np.max(fitness)}")