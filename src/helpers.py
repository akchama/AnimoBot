import win32ui
import numpy as np
import win32gui
from ctypes import windll


def background_screenshot(window_name):
    hwnd = win32gui.FindWindow(None, window_name)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    print(result)

    # bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    imcv = np.frombuffer(bmpstr, dtype=np.uint8).reshape((h, w, 4))[:, :, :3]
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        return np.array(imcv)
    return False


def get_locations(match, threshold):
    return np.where(match >= threshold)
