from geneticalgorithm.subscriber import Subscriber
import numpy as np
import pandas as pd
from PIL import Image
from utils import to_model_image, predict_classes
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
import json
import base64
import pickle
import matplotlib.pyplot as plt


class Printer(Subscriber):
    def notify(self, generation, population, fitness, **kwargs):
        print(
            "Generation: %d, Min fitness: %f, Avg fitness: %f, Max fitness: %f, Fitness function uses: %d" % (
                generation, np.min(fitness), np.average(fitness), np.max(fitness), kwargs['current_fitness_uses']))


class PopulationVisualizer(Subscriber):

    def __init__(self, path=None):
        self.path = path
        self.points = []
        self.pca = PCA(n_components=2)

    def notify(self, generation, population, fitness, **kwargs):
        self.points += list(self.pca.fit_transform(
            list(map(lambda x: x.flatten(), list(population)))))

    def on_finish(self):
        # with open(self.path, 'wb') as f:
        #     pickle.dump(self.points, f)
        plt.scatter(list(map(lambda x: x[0], self.points)), list(
            map(lambda x: x[1], self.points)), s=2)
        plt.plot()
        plt.show()


class Logger(Subscriber):
    def __init__(self, path, model, **kwargs):
        self.path = path
        self.model = model
        self.static_parameters = kwargs

    def notify(self, generation, population, fitness, **kwargs):
        best = float(np.max(fitness))
        mean = float(np.mean(fitness))
        median = float(np.median(fitness))
        worst = float(np.min(fitness))
        population_size = len(population)
        mean_speciman = np.average(population, axis=0)
        std_population = np.average(
            np.sqrt(np.sum(np.square(population - mean_speciman), axis=1)))
        bestSpecimen = population[np.argmax(fitness)]
        predictedClasses = predict_classes(
            self.model, to_model_image(bestSpecimen))

        df = pd.DataFrame(
            columns=["Generation", "Fitness function uses", "Best fitness", "Average fitness", "Median fitness",
                     "Worst Fitness", "Population size", "Std Population",
                     "Predicted class 1", "Probability 1", "Predicted class 2", "Probability 2", "Predicted class 3",
                     "Probability 3", "Predicted class 4", "Probability 4",
                     "Predicted class 5", "Probability 5", *
                     kwargs["layer_parameters"].keys(),
                     *self.static_parameters.keys()])
        df.loc[len(df)] = [generation, kwargs["current_fitness_uses"], best, mean, median, worst, population_size,
                           std_population,
                           *[a for b in predictedClasses for _,
                               a in b.items()], *kwargs["layer_parameters"].values(),
                           *self.static_parameters.values()]
        with open(self.path, 'a') as f:
            df.to_csv(f, index=False, header=f.tell() == 0)


class ServerHook(Subscriber):

    def __init__(self, hook, model):
        self.hook = hook
        self.model = model

    def notify(self, generation, population, fitness, **kwargs):
        pca = PCA(n_components=2)
        flattened_population = list(
            map(lambda x: x.flatten(), list(population)))
        transformed_population = list(
            map(lambda x: {'x': float(x[0]), 'y': float(x[1])}, pca.fit_transform(flattened_population)))
        best = float(np.max(fitness))
        mean = float(np.mean(fitness))
        median = float(np.median(fitness))
        worst = float(np.min(fitness))
        bestSpecimen = population[np.argmax(fitness)]
        predictedClasses = predict_classes(
            self.model, to_model_image(bestSpecimen))
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
