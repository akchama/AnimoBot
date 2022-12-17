import sys
import threading

from detection import Detection
from helpers import background_screenshot
from cv2 import cv2
from time import time, sleep
import keyboard


class Bot:
    @property
    def debug(self):
        return not sys.gettrace() is None

    def __init__(self):
        self.running = False
        self.update_image = threading.Thread(target=self.update_image)
        self.detector = Detection()

    def start(self):
        self.running = True

        self.update_image.start()
        self.detector.start()
        while True:
            if self.detector._screenshot is not None:
                print("Update game logic")
                self.update()
                sleep(0.3)

            # Press q to quit program
            if cv2.waitKey(1) & 0xFF == ord("q"):
                # stop bot thread
                self.running = False
                self.update_image.join()
                self.detector.stop()
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                sys.exit()

    def update(self):
        self.running = True
        rectangles = self.detector.rectangles

        for (x, y, w, h) in rectangles:
            cv2.rectangle(self.detector._screenshot, (x, y), (x + w, y + h), (0, 255, 255), 1)
            # cv2.putText(self.detector._screenshot, 'Oyster', (x, y), cv2.FONT_HERSHEY_SIMPLEX,
            #             1, (255, 0, 0), 2, cv2.LINE_AA)

        print("updating screen capture")
        cv2.imshow("Game", self.detector._screenshot)
        cv2.waitKey(1)

    def update_image(self):
        while self.running:
            self.detector.update(background_screenshot('Terror Of Sea'))
            print("Bot.update_image")
            sleep(0.3)
        print("Exit")
