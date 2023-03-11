import numpy as np

from bot import AnimoBot


def get_locations(match, threshold):
    return np.where(match >= threshold)


def get_text_area(img):
    return img[
        AnimoBot.MESSAGE_OFFSET_Y : AnimoBot.MESSAGE_OFFSET_Y + AnimoBot.MESSAGE_Y,
        10 : AnimoBot.window_w - 10,
    ]


def get_text_area_points():
    return [
        10,  # X1
        AnimoBot.MESSAGE_OFFSET_Y,  # Y1
        AnimoBot.window_w - 10,  # X2
        AnimoBot.MESSAGE_OFFSET_Y + AnimoBot.MESSAGE_Y,  # Y2
    ]


def is_match(match, threshold):
    flag = False
    if np.amax(match) > threshold:
        flag = True
    return flag
