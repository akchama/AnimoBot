import time

import cv2 as cv

import vision
from bot import AnimoBot, BotState
from detection import Detection
from entities.coordinates import Coordinates
from entities.map import Map
from entities.message import Message
# from entities.minimap import MiniMap
from windowcapture import WindowCapture

DEBUG = True

# initializations
win_cap = WindowCapture("Terror of Sea", sleep_time=0.5)

detector = Detection(sleep_time=0.5)
detector.coordinates = Coordinates(win_cap)
detector.message = Message(win_cap)
detector.map = Map(win_cap)

bot = AnimoBot(
    (win_cap.offset_x, win_cap.offset_y), (win_cap.w, win_cap.h), detector
)

win_cap.start()  # capture screenshots
detector.start()  # detect targets
bot.start()  # main bot logic

# This loop updates stuff
while True:
    # if we don't have a screenshot yet, don't run the code below this point yet
    if win_cap.screenshot is None:
        continue

    # give detector the current screenshot to search for objects in
    detector.update(win_cap.screenshot)

    # update the bot with the data it needs right now
    if bot.state == BotState.INITIALIZING:
        # while bot is waiting to start, go ahead and start giving it some targets to work
        # on right away when it does start
        targets = vision.get_click_points(detector.targets)
        bot.update_targets(targets)
        print("Bot initializing...")
    elif bot.state == BotState.SEARCHING:
        # when searching for something to click on next, the bot needs to know what the click
        # points are for the current detection results. it also needs an updated screenshot
        # to verify the hover tooltip once it has moved the mouse to that position
        targets = vision.get_click_points(detector.targets)
        bot.update_targets(targets)
        bot.update_screenshot(win_cap.screenshot)
        time.sleep(0.5)
    elif bot.state == BotState.ATTACKING:
        # nothing is needed while we wait for the attack to finish
        print("Bot attacking...")
        pass

    if DEBUG:
        # draw the detection results onto the original image
        detection_image = vision.draw_rectangles(
            win_cap.screenshot, detector.targets, detector.features
        )
        # display the images
        cv.imshow("Matches", detection_image)

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord("q"):
        win_cap.stop()
        detector.stop()
        bot.stop()
        cv.destroyAllWindows()
        break
    elif key == ord("r"):
        bot.state = BotState.SEARCHING

print("Done.")
