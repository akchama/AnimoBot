"""
ID area of the window
"""

# id text
ID_OFFSET_X = 415 + 47
ID_OFFSET_Y = 365 + 65

ID_X = 30
ID_Y = 25


def get_id_area(img):
    return img[
           ID_OFFSET_Y: ID_OFFSET_Y + ID_Y,
           ID_OFFSET_X: ID_OFFSET_X + ID_X,
           ]


def get_id_area_points():
    return (ID_OFFSET_X, ID_OFFSET_Y), (ID_OFFSET_X + ID_X, ID_OFFSET_Y + ID_Y)
