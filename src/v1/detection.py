# detection.py
import cv2
from threading import Thread, Lock

import numpy as np
import pyautogui

from helpers import get_locations, get_screen_position


class Detection:
    rectangles = []
    targets = []

    # threading properties
    _running = False
    _lock = None

    # properties
    _screenshot = None
    _oyster_img = None

    def __init__(self):
        # create a thread lock object
        self._lock = Lock()
        # load the image
        self._oyster_img = cv2.imread(
            "../../img/oyster1.png", cv2.IMREAD_UNCHANGED
        )

    def update(self, screenshot):
        self._lock.acquire()
        self._screenshot = screenshot
        self._lock.release()

    def start(self):
        self._running = True
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self._running = False

    def run(self):
        while self._running:
            if self._screenshot is not None:
                # do object detection
                match = cv2.matchTemplate(
                    self._screenshot, self._oyster_img, cv2.TM_CCOEFF_NORMED
                )
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
                w = self._oyster_img.shape[1]
                h = self._oyster_img.shape[0]
                print("Detection.run")
                y_loc, x_loc = np.where(match >= 0.8)

                rectangles = []
                for x, y in zip(x_loc, y_loc):
                    rectangles.append([int(x), int(y), int(w), int(h)])
                    rectangles.append([int(x), int(y), int(w), int(h)])

                rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
                print(weights)

                for x, y, w, h in rectangles:
                    cv2.rectangle(
                        self._screenshot,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 255),
                        1,
                    )
                    # cv2.putText(self.detector._screenshot, 'Oyster', (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                    #             1, (255, 0, 0), 2, cv2.LINE_AA)

                print("updating screen capture")
                if len(rectangles) > 0:
                    self.targets = rectangles
                    self.move_to_next_target()
                    cv2.imshow("Game", self._screenshot)
                cv2.waitKey(1)

                # lock the thread while updating the results
                self._lock.acquire()
                self.rectangles = rectangles
                self._lock.release()
            else:
                print("ERROR: Image None")

    def move_to_next_target(self):
        target_pos = self.targets[0]
        screen_x, screen_y = get_screen_position(target_pos)
        print("Moving mouse to x:{} y:{}".format(screen_x, screen_y))

        current_pos = pyautogui.position()
        # move the mouse
        pyautogui.moveTo(x=screen_x, y=screen_y)
        pyautogui.moveTo(x=current_pos.x, y=current_pos.y)
