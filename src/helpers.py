import numpy as np


def get_locations(match, threshold):
    return np.where(match >= threshold)


def is_match(match, threshold):
    flag = False
    if np.amax(match) > threshold:
        flag = True
    return flag
