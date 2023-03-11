from windowcapture import WindowCapture


class Message:
    OFFSET_X = 0
    OFFSET_Y = 108

    HEIGHT = 18
    HORIZONTAL_OFFSET = 10

    win_cap: WindowCapture = None

    def __init__(self, win_cap):
        self.win_cap = win_cap

    def get_area(self, img):
        return img[
               self.OFFSET_Y: self.OFFSET_Y + self.HEIGHT,
               self.HORIZONTAL_OFFSET: self.win_cap.w - self.HORIZONTAL_OFFSET,
               ]

    def get_area_points(self):
        return (10, self.OFFSET_Y), (self.win_cap.w - 10, self.OFFSET_Y + self.HEIGHT)
