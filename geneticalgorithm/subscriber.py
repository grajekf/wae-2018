from abc import ABC

class Subscriber(ABC):
    def notify(self, generation, population, fitness):
        pass