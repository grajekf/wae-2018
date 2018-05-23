from abc import ABC

class Subscriber(ABC):
    def notify(self, generation, population, fitness, **kwargs):
        pass

    def on_finish(self):
        pass