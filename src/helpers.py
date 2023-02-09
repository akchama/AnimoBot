import numpy as np


def get_locations(match, threshold):
    return np.where(match >= threshold)
