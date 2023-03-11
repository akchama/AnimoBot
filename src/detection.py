from threading import Thread, Lock
from time import sleep

import cv2
from pytesseract import pytesseract

from entities.coordinates import Coordinates
from entities.message import Message
from helpers import get_locations, is_match

pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class Detection:
    # threading properties
    stopped = True
    lock = None
    targets = []
    features = []
    # properties
    # cascade = None
    _screenshot = None
    _oyster_img = None
    _id_img = None

    message: Message = None
    coordinates: Coordinates = None

    def __init__(self, sleep_time):  # you can pass cascade file path here in the future
        # create a thread lock object
        self.lock = Lock()
        # load the trained model
        # self.cascade = cv.CascadeClassifier(model_file_path)
        self._oyster_img = cv2.imread("../img/oyster1.jpg", cv2.IMREAD_UNCHANGED)
        self._text_img = cv2.imread("../img/text.jpg", cv2.IMREAD_UNCHANGED)
        self._id_img = cv2.imread("../img/id.jpg", cv2.IMREAD_UNCHANGED)

        self.sleep_time = sleep_time

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

    # this runs in a separate thread
    def run(self):
        while not self.stopped:
            if self._screenshot is not None:
                # # TODO: you can write your own time/iterations calculation to determine how fast this is
                restricted_text_area = self.message.get_area(
                    self._screenshot
                )  # return area to be scanned for text
                text = pytesseract.image_to_string(restricted_text_area)
                print(text)
                # do object detection

                # to use cascade classifier
                # rectangles = self.cascade.detectMultiScale(self.screenshot)

                # to use matchTemplate
                match = cv2.matchTemplate(
                    self._screenshot, self._oyster_img, cv2.TM_CCOEFF_NORMED
                )

                w = self._oyster_img.shape[1]
                h = self._oyster_img.shape[0]
                y_loc, x_loc = get_locations(match, 0.8)  # accuracy threshold

                rectangles = []
                for x, y in zip(x_loc, y_loc):
                    rectangles.append([int(x), int(y), int(w), int(h)])
                    rectangles.append([int(x), int(y), int(w), int(h)])

                rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

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
                self.targets = rectangles
                self.features = [self.message.get_area_points(), self.coordinates.get_area_points()]
                self.lock.release()
                sleep(self.sleep_time)

    def coordinate_changed(self):
        pass
