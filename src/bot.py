import sys

from helpers import background_screenshot, get_locations
from cv2 import cv2
from time import time, sleep
import keyboard


class Bot:
    @property
    def debug(self):
        return not sys.gettrace() is None

    def __init__(self):
        self.running = False
        self.game_img_buffer = background_screenshot('Terror Of Sea')
        self.oyster_img = cv2.imread('../img/oyster.jpg', cv2.IMREAD_UNCHANGED)

    def update(self):
        self.running = True
        match = cv2.matchTemplate(self.game_img_buffer, self.oyster_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        w = self.oyster_img.shape[1]
        h = self.oyster_img.shape[0]
        print(max_loc)
        y_loc, x_loc = get_locations(match, 0.8)  # 0.6 is accuracy threshold

        rectangles = []
        for (x, y) in zip(x_loc, y_loc):
            rectangles.append([int(x), int(y), int(w), int(h)])
            rectangles.append([int(x), int(y), int(w), int(h)])

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        for (x, y, w, h) in rectangles:
            cv2.rectangle(self.game_img_buffer, (x, y), (x + w, y + h), (0, 255, 255), 1)
            cv2.putText(self.game_img_buffer, 'OpenCV', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 0), 2, cv2.LINE_AA)

        print("updating screen capture")
        cv2.imshow("Game", self.game_img_buffer)
        cv2.waitKey(1)

    def update_image(self):
        while True:
            self.game_img_buffer = background_screenshot('Terror Of Sea')
            print("Update game img")
            sleep(0.3)
