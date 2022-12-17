# detection.py
import cv2
from threading import Thread, Lock

from helpers import get_locations


class Detection:
    rectangles = []

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
        self._oyster_img = cv2.imread('../img/oyster.jpg', cv2.IMREAD_UNCHANGED)

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
                match = cv2.matchTemplate(self._screenshot, self._oyster_img, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
                w = self._oyster_img.shape[1]
                h = self._oyster_img.shape[0]
                print("Detection.run")
                y_loc, x_loc = get_locations(match, 0.8)  # 0.6 is accuracy threshold

                rectangles = []
                for (x, y) in zip(x_loc, y_loc):
                    rectangles.append([int(x), int(y), int(w), int(h)])
                    rectangles.append([int(x), int(y), int(w), int(h)])

                rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

                # lock the thread while updating the results
                self._lock.acquire()
                self.rectangles = rectangles
                self._lock.release()
