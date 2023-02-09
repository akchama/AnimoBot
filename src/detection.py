import cv2
import cv2 as cv
from threading import Thread, Lock

from helpers import get_locations


class Detection:
    # threading properties
    stopped = True
    lock = None
    rectangles = []
    # properties
    # cascade = None
    _screenshot = None
    _oyster_img = None

    def __init__(self):  # you can pass cascade file path here in the future
        # create a thread lock object
        self.lock = Lock()
        # load the trained model
        # self.cascade = cv.CascadeClassifier(model_file_path)
        self._oyster_img = cv2.imread(
            "../img/oyster1.jpg", cv2.IMREAD_UNCHANGED
        )

    def update(self, screenshot):
        self.lock.acquire()
        self._screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            if self._screenshot is not None:
                # do object detection
                # to use cascade classifier
                # rectangles = self.cascade.detectMultiScale(self.screenshot)

                # to use matchTemplate
                # do object detection
                match = cv2.matchTemplate(
                    self._screenshot, self._oyster_img, cv2.TM_CCOEFF_NORMED
                )
                w = self._oyster_img.shape[1]
                h = self._oyster_img.shape[0]
                print("Detection.run")
                y_loc, x_loc = get_locations(
                    match, 0.8
                )  # accuracy threshold

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

                # lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()
