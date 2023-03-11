class MiniMap:
    # Map offsite from right: 212
    # Map offsite from top: 249

    # coordinates of top left corner of minimap
    OFFSET_X_FROM_RIGHT = 212
    OFFSET_Y_FROM_TOP = 249

    # minimap size
    WIDTH = 135
    HEIGHT = 135

    def __init__(self, win_cap):
        self.x = win_cap.w - self.OFFSET_X_FROM_RIGHT
        self.y = self.OFFSET_Y_FROM_TOP

    def click_random_position(self):
        pass
