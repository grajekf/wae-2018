import numpy as np


def one_point_crossover(a, b):
    aNew = a.flatten()
    bNew = b.flatten()
    cx = np.random.randint(1, len(aNew) - 1)
    aNew = np.concatenate([np.split(aNew, [cx])[0], np.split(bNew, [cx])[1]]).reshape(a.shape)
    return aNew
