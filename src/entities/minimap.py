import time
from random import randint

import pyautogui

from windowcapture import WindowCapture


class MiniMap:
    # Map offsite from right: 212
    # Map offsite from top: 249

    # coordinates of top left corner of minimap
    OFFSET_X_FROM_RIGHT = 204
    OFFSET_Y_FROM_TOP = 116

    # minimap size
    WIDTH = 135
    HEIGHT = 135

    win_cap: WindowCapture = None

    def __init__(self, win_cap):
        self.win_cap = win_cap
        self.x = win_cap.w - self.OFFSET_X_FROM_RIGHT
        self.y = self.OFFSET_Y_FROM_TOP

    def click_random_position(self):
        print("Clicking random position on minimap")
        # click a random position on the screen
        x = randint(0, self.WIDTH)
        y = randint(0, self.HEIGHT)
        x, y = self.get_screen_position((x, y))
        pyautogui.moveTo(x=x, y=y)
        time.sleep(1.250)
        pyautogui.click()

    def click_next_target(self):
        screen_x, screen_y = self.get_screen_position(target_pos)
        print("Moving mouse to x:{} y:{}".format(screen_x, screen_y))
        pyautogui.moveTo(x=screen_x, y=screen_y)

        # short pause to let the mouse movement complete and allow
        time.sleep(1.250)
        
        print("Click on target at x:{} y:{}".format(screen_x, screen_y))
        pyautogui.click()

    def get_screen_position(self, pos):
        return \
            pos[0] + self.win_cap.offset_x + self.win_cap.w - self.OFFSET_X_FROM_RIGHT, \
            pos[1] + self.win_cap.offset_y + self.OFFSET_Y_FROM_TOP
