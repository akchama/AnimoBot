import time
from random import randint

import pyautogui

from windowcapture import WindowCapture


class Map:
    win_cap: WindowCapture = None

    def __init__(self, win_cap):
        self.win_cap = win_cap

    def click_random_position(self):
        print("Clicking random position on minimap")
        # click a random position on the screen
        x = randint(0, self.win_cap.w)
        y = randint(0, self.win_cap.h)
        x, y = self.get_screen_position((x, y))
        pyautogui.moveTo(x=x, y=y)
        time.sleep(1.250)
        pyautogui.click()

    def get_screen_position(self, pos):
        return pos[0] + self.win_cap.offset_x, pos[1] + self.win_cap.offset_y
