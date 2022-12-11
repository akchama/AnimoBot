from helpers import background_screenshot, get_locations
from cv2 import cv2


class Bot:
    def __init__(self):
        self.running = False

    def start(self):
        img_buffer = background_screenshot('Terror Of Sea')
        oyster_img = cv2.imread('../img/oyster.jpg', cv2.IMREAD_UNCHANGED)

        while True:
            match = cv2.matchTemplate(img_buffer, oyster_img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
            w = oyster_img.shape[1]
            h = oyster_img.shape[0]
            print(max_loc)
            y_loc, x_loc = get_locations(match, 0.6)  # 0.6 is accuracy threshold

            rectangles = []
            for (x, y) in zip(x_loc, y_loc):
                rectangles.append([int(x), int(y), int(w), int(h)])
                rectangles.append([int(x), int(y), int(w), int(h)])

            rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

            for (x, y, w, h) in rectangles:
                cv2.rectangle(img_buffer, (x, y), (x + w, y + h), (0, 255, 255), 1)
            cv2.imshow("real", img_buffer)

        cv2.waitKey()
