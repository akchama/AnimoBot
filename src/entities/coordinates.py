"""
this is the class to get coordinates and also check if the coordinates has changed
so we can know if the player is moving or not
"""
import time

from windowcapture import WindowCapture
from cv2 import cv2 as cv


class Coordinates:
    MOVEMENT_STOPPED_THRESHOLD = 0.975

    OFFSET_X = 0
    OFFSET_Y = 3

    WIDTH = 75
    HEIGHT = 20

    win_cap: WindowCapture = None

    coordinate_img = None
    prev_coordinate_img = None

    def __init__(self, win_cap):
        self.win_cap = win_cap
        self.OFFSET_X = int((win_cap.w - self.WIDTH) / 2)

    def get_area(self, img):
        return img[
               self.OFFSET_Y: self.OFFSET_Y + self.HEIGHT,
               self.OFFSET_X: self.OFFSET_X + self.WIDTH,
               ]

    def get_area_points(self):
        return (self.OFFSET_X, self.OFFSET_Y), (
            self.OFFSET_X + self.WIDTH, self.OFFSET_Y + self.HEIGHT)

    def has_changed(self):
        # if we haven't stored a screenshot to compare to, do that first
        self.coordinate_img = self.get_area(self.win_cap.screenshot)
        if self.prev_coordinate_img is None:
            self.prev_coordinate_img = self.coordinate_img
            return False

        # give some time to the player to move
        time.sleep(2)

        # compare the old screenshot to the new screenshot
        result = cv.matchTemplate(self.coordinate_img, self.prev_coordinate_img, cv.TM_CCOEFF_NORMED)
        # we only care about the value when the two screenshots are laid perfectly over one
        # another, so the needle position is (0, 0). since both images are the same size, this
        # should be the only result that exists anyway
        similarity = result[0][0]
        print('Movement detection similarity: {}'.format(similarity))

        if similarity >= self.MOVEMENT_STOPPED_THRESHOLD:
            # pictures look similar, so we've probably stopped moving
            print('Movement detected stop')
            return False

        # looks like we're still moving.
        # use this new screenshot to compare to the next one
        self.prev_coordinate_img = self.coordinate_img.copy()
        return True
