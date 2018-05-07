from geneticalgorithm.subscriber import Subscriber
import numpy as np
from PIL import Image
from utils import to_model_image, predict_classes
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize


class Printer(Subscriber):
    def notify(self, generation, population, fitness):
        print(
            f"Generation: {generation}, Min fitness: {np.min(fitness)}, Avg fitness: {np.average(fitness)}, Max fitness: {np.max(fitness)}")


class ServerHook(Subscriber):

    def __init__(self, hook, model):
        self.hook = hook
        self.model = model

    def notify(self, generation, population, fitness):
        pca = PCA(n_components=2)
        flattened_population = list(map(lambda x: x.flatten(), list(population)))
        transformed_population = list(map(lambda x: {'x' : float(x[0]), 'y' : float(x[1]) }, pca.fit_transform(flattened_population)))
        best = float(np.max(fitness))
        mean = float(np.mean(fitness))
        median = float(np.median(fitness))
        worst = float(np.min(fitness))
        bestSpecimen = population[np.argmax(fitness)]
        predictedClasses = predict_classes(self.model, to_model_image(bestSpecimen))
        if self.hook is not None:
            print('calling hook')
            self.hook({
                'objectiveFunction': {
                    'best': best,
                    'worst': worst,
                    'mean': mean,
                    'median': median
                },
                'generation': generation,
                'bestSpecimen': {
                    'data': Image.fromarray(bestSpecimen.astype(np.uint8)),
                    'predictions': predictedClasses
                },
                'population': transformed_population
            })
