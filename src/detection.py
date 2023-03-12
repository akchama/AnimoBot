from threading import Thread, Lock
from time import sleep

import cv2
import numpy as np
from pytesseract import pytesseract

from entities.coordinates import Coordinates
from entities.message import Message
from helpers import get_locations, is_match

pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class Detection:
    TOP_BAR_OFFSET = 29

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

        # load oyster img
        _oyster_img = cv2.imread("../img/1.png", cv2.IMREAD_UNCHANGED)

        # resize oyster image
        scale_percent = 30  # percent of original size
        width = int(_oyster_img.shape[1] * scale_percent / 100)
        height = int(_oyster_img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(_oyster_img, dim, interpolation=cv2.INTER_AREA)
        # cv2.imshow("resized", resized)
        self._oyster_img = resized

        self._text_img = cv2.imread("../img/text.jpg", cv2.IMREAD_UNCHANGED)

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
                # TODO: you can write your own time/iterations calculation to determine how fast this is
                restricted_text_area = self.message.get_area(
                    self._screenshot
                )  # return area to be scanned for text
                text = pytesseract.image_to_string(restricted_text_area)
                if text != "":
                    print(text)

                # do object detection
                template = self._oyster_img[:, :, 0:3]
                alpha = self._oyster_img[:, :, 3]
                alpha = cv2.merge([alpha, alpha, alpha])

                h = self._screenshot.shape[0]
                sea_area = self._screenshot[self.TOP_BAR_OFFSET:h - 67, :]
                match = cv2.matchTemplate(
                    sea_area, template, cv2.TM_CCORR_NORMED, mask=alpha
                )

                w = self._oyster_img.shape[1]
                h = self._oyster_img.shape[0]
                y_loc, x_loc = get_locations(match, 0.94)  # accuracy threshold

                rectangles = []
                for x, y in zip(x_loc, y_loc):
                    rectangles.append([int(x), int(y + self.TOP_BAR_OFFSET), int(w), int(h)])
                    rectangles.append([int(x), int(y + self.TOP_BAR_OFFSET), int(w), int(h)])

                rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

                # lock the thread while updating the results
                self.lock.acquire()
                self.targets = rectangles
                self.features = [
                    self.message.get_area_points(),
                    self.coordinates.get_area_points()
                ]
                self.lock.release()
                sleep(self.sleep_time)
