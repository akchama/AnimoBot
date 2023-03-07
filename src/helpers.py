import numpy as np

from bot import AnimoBot


def get_locations(match, threshold):
    return np.where(match >= threshold)


def get_text_area(img):
    return img[
        AnimoBot.MESSAGE_OFFSET_Y : AnimoBot.MESSAGE_OFFSET_Y + AnimoBot.MESSAGE_Y,
        10 : AnimoBot.window_w - 10,
    ]


def get_id_area(img):
    return img[
        AnimoBot.ID_OFFSET_Y : AnimoBot.ID_OFFSET_Y + AnimoBot.ID_Y,
        AnimoBot.ID_OFFSET_X : AnimoBot.ID_OFFSET_X + AnimoBot.ID_X,
    ]


def get_text_area_points():
    return [
        10,  # X1
        AnimoBot.MESSAGE_OFFSET_Y,  # Y1
        AnimoBot.window_w - 10,  # X2
        AnimoBot.MESSAGE_OFFSET_Y + AnimoBot.MESSAGE_Y,  # Y2
    ]


def get_id_area_points():
    return [
        AnimoBot.ID_OFFSET_X,  # X1
        AnimoBot.ID_OFFSET_Y,  # Y1
        AnimoBot.ID_OFFSET_X + AnimoBot.ID_X,  # X2
        AnimoBot.ID_OFFSET_Y + AnimoBot.ID_Y,  # Y2
    ]


def is_match(match, threshold):
    flag = False
    if np.amax(match) > threshold:
        flag = True
    return flag
