"""
Basis of Code comes from Martin Lee's imagesearch.py
code src: https://github.com/drov0/python-imagesearch
https://brokencode.io/how-to-easily-image-search-with-python/
"""

import os
import platform

from ctypes import windll

if "Windows" in platform.platform():
    import win32api
    import win32con
    import win32process
    import win32ui
    import win32gui

    # import pytesseract as pyocr
import applescript
from pynput import mouse
import time
import numpy as np
from PIL import Image

import cv2
import pyautogui as pyag

pyag.FAILSAFE = False
hwnd = 0

REDUCE_FACTOR = 1
BOUNDS = {0, 0, 25, 0}
SLOT_TO_SELL = 56
MAX_SLOTS = 60


_is_retina = False
if platform.system() == "Darwin":
    import subprocess

    _is_retina = (
        subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True) == 0
    )


def _imagesearcharea(image, x1, y1, x2, y2, precision=0.8, im=None):
    x1, x2, y1, y2 = x1 - 1, x2 + 1, y1 - 1, y2 + 1
    if im is None:
        im = _region_grabber(region=(x1, y1, x2, y2))
        if _is_retina:
            im.thumbnail((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
        # im.save('testarea.png') usefull for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    # width = int(template.shape[1] * REDUCE_FACTOR)
    # height = int(template.shape[0] * REDUCE_FACTOR)
    # template = cv2.resize(template, (width, height), interpolation = cv2.INTER_AREA)
    if template is None:
        raise FileNotFoundError("Image file not found: {}".format(image))

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


def _region_grabber(region):
    import mss

    if _is_retina:
        region = [n * 2 for n in region]
    x1 = region[0]
    y1 = region[1]
    width = region[2]
    height = region[3]

    region = x1, y1, width, height
    with mss.mss() as sct:
        return sct.grab(region)


def getHWND():
    global hwnd
    if "Windows" in platform.platform():
        if hwnd == win32gui.GetForegroundWindow():
            return 0
        return hwnd if hwnd != 0 else win32gui.GetForegroundWindow()
    else:
        return 0


def printWin():
    if not "Windows" in platform.platform():
        return
    print("'" + win32gui.GetWindowText(getHWND()) + "'")


def GetAllWindows():
    hwnd_list = []

    def enum_window_callback(hwnd, hwnd_list):
        if win32gui.IsWindowVisible(hwnd):
            hwnd_list.append(
                {
                    "hwnd": hwnd,
                    "class": win32gui.GetClassName(hwnd),
                    "text": win32gui.GetWindowText(hwnd),
                }
            )

    win32gui.EnumWindows(enum_window_callback, hwnd_list)
    return hwnd_list


def DrawRel(area):
    import win32ui

    hwnd = getHWND()
    hdc = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(hdc)
    # Create a brush or pen and draw a rectangle
    pen = win32ui.CreatePen(0, 3, 0x0000FF)
    dcObj.SelectObject(pen)
    dcObj.Rectangle(area)
    # Cleanup
    dcObj.DeleteDC()
    win32gui.ReleaseDC(hwnd, hdc)


def getWinRect():
    if "Windows" in platform.platform():
        global hwnd
        wH = hwnd if hwnd != 0 else win32gui.GetForegroundWindow()
        return win32gui.GetWindowRect(wH)
    else:
        f_pr = applescript.tell.app(
            "System Events", "get name of process 1 where frontmost is true"
        ).out
        applescript.tell.app(f"{f_pr}", "activate")

        def get_command_string(app, command, argument=None):
            argument = (" to " + argument) if argument is not None else ""
            return f'tell application process "{app}"\n\t{command} of window 1{argument}\nend tell'

        pos = applescript.tell.app(
            "System Events", get_command_string(f_pr, "get position")
        ).out.split(",")
        size = applescript.tell.app(
            "System Events", get_command_string(f_pr, "get size")
        ).out.split(",")
        return [int(pos[0]), int(pos[1]), int(size[0]), int(size[1])]


# 1385, 769
def getRelPos():
    return getWinRect()[:2]


def setHWND(i):
    global hwnd
    hwnd = i


def assignWin(className, winName):
    if "Windows" in platform.platform():
        global hwnd
        hwnd = win32gui.FindWindow(className, winName)


def resizeWin(pos=getRelPos(), size=None):
    if size is None:
        rect = getWinRect()
        size = (rect[2] - rect[0], (rect[3] - rect[1]))
    if "Windows" in platform.platform():
        global hwnd
        wH = hwnd if getHWND() != 0 else win32gui.GetForegroundWindow()
        win32gui.MoveWindow(wH, *pos, *size, True)
    else:
        f_pr = applescript.tell.app(
            "System Events", "get name of process 1 where frontmost is true"
        ).out
        applescript.tell.app(f"{f_pr}", "activate")

        def get_command_string(app, command, argument=None):
            argument = (" to " + argument) if argument is not None else ""
            return f'tell application process "{app}"\n\t{command} of window 1{argument}\nend tell'

        applescript.tell.app(
            "System Events",
            get_command_string(f_pr, "set position", "{" + str(pos[0]) + ", " + str(pos[1]) + "}"),
        ).out.split(",")
        applescript.tell.app(
            "System Events",
            get_command_string(f_pr, "set size", "{" + str(size[0]) + ", " + str(size[1]) + "}"),
        ).out.split(",")


def focusWin(className, winName):
    if "Windows" in platform.platform():
        win32gui.SetForegroundWindow(win32gui.FindWindow(className, winName))
    else:
        f_pr = applescript.tell.app(
            "System Events", "get name of process 1 where frontmost is true"
        ).out
        applescript.tell.app({f_pr}, "activate")


def RelToAbs(pos):
    relX, relY = getRelPos()
    if len(pos) == 2:
        return pos[0] + relX, pos[1] + relY
    else:
        return pos[0] + relX, pos[1] + relY, pos[2] + relX, pos[3] + relY


def AbsToRel(pos):
    relX, relY = getRelPos()
    if len(pos) == 2:
        return pos[0] - relX, pos[1] - relY
    else:
        return pos[0] - relX, pos[1] - relY, pos[2] - relX, pos[3] - relY


def Click(x, y):  # (72, 38) vs (63, 0) (-9, -38) -9, -13
    wH = getHWND()
    if wH != 0:
        l_pram = win32api.MAKELONG(int(x - 9), int(y - 38))
        win32gui.PostMessage(wH, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_pram)
        win32gui.PostMessage(wH, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, l_pram)
    else:
        # mP = pyag.position()
        pos = RelToAbs((x, y))
        # pos = list(posR)
        # pos[1] += 38 * REDUCE_FACTOR
        pyag.mouseDown(*pos, button="left")
        sleep(0.1)
        pyag.mouseUp(*pos, button="left")
        # pyag.moveTo(*mP)


def ClickBtn(pathList, area, confirmPathList=None, confirmArea=None, disappear=True, timeout=3):
    if confirmArea is None:
        confirmArea = area
    if confirmPathList is None:
        confirmPathList = pathList

    def mid(a, b):
        return a + ((b - a) / 2)

    if ImageCheck(pathList, area, timeout):
        Click(mid(area[0], area[2]), mid(area[1], area[3]))
        if disappear and ImgGoneCheck(confirmPathList, confirmArea, timeout):
            return True
        elif ImageSearch(confirmPathList, confirmArea, timeout):
            return True
    return False


def getRelMousePos():
    return AbsToRel(pyag.position())


def typeKeys(*keys):
    wH = getHWND()
    interval = 0
    if type(keys[-1]) is float:
        interval = keys[-1]
        keys = list(*keys[:-1])
    else:
        keys = list(*keys)

    if wH != 0:
        currThread, outThread = (
            win32api.GetCurrentThreadId(),
            win32process.GetWindowThreadProcessId(wH)[0],
        )
        win32process.AttachThreadInput(currThread, outThread, 1)
        for k in keys:
            v_key = {
                " ": 0x20,
                "0": 0x30,
                "1": 0x31,
                "2": 0x32,
                "3": 0x33,
                "4": 0x34,
                "5": 0x35,
                "6": 0x36,
                "7": 0x37,
                "8": 0x38,
                "9": 0x39,
                "a": 0x41,
                "b": 0x42,
                "c": 0x43,
                "d": 0x44,
                "e": 0x45,
                "f": 0x46,
                "g": 0x47,
                "h": 0x48,
                "i": 0x49,
                "j": 0x4A,
                "k": 0x4B,
                "l": 0x4C,
                "m": 0x4D,
                "n": 0x4E,
                "o": 0x4F,
                "p": 0x50,
                "q": 0x51,
                "r": 0x52,
                "s": 0x53,
                "t": 0x54,
                "u": 0x55,
                "v": 0x56,
                "w": 0x57,
                "x": 0x58,
                "y": 0x59,
                "z": 0x5A,
            }
            char_id, capital = ord(k.lower()), k.isupper()
            prev = win32gui.SetFocus(wH)
            if not capital:
                win32api.PostMessage(wH, win32con.WM_KEYDOWN, char_id, 0)
            else:
                win32api.PostMessage(wH, win32con.WM_CHAR, char_id, 0)
                win32api.PostMessage(wH, win32con.WM_DEADCHAR, char_id, 0)
            win32gui.SetFocus(prev)
            sleep(interval)
        win32process.AttachThreadInput(currThread, outThread, 0)
    else:
        pyag.typewrite("".join(keys), interval)


"""
def imgToText(img):
    return pyocr.image_to_string(img)

def readText(area):
    img = RegionGrab(area)
    img_rgb = np.array(img)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img = img.convert('L')
    #Try 'L' or convert('L'),
    # img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    img.save('../Blah.png', 'png')
    text = pyocr.image_to_string(img, config='-l eng --psm 8 -c tessedit_char_whitelist=0123456789')
    return text
"""


def winScreenGrab():
    wH = getHWND()
    if wH != 0:
        left, top, right, bot = win32gui.GetWindowRect(wH)
        w, h = right - left, bot - top

        hwndDC = win32gui.GetWindowDC(wH)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)
        windll.user32.PrintWindow(wH, saveDC.GetSafeHdc(), 2)
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            "RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1
        )

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(wH, hwndDC)
        return im
    else:
        return pyag.screenshot().crop(getWinRect()).convert("RGB")


def RegionGrab(area):
    wH = getHWND()
    if wH != 0:
        left, top, right, bot = win32gui.GetWindowRect(wH)
        w, h = right - left, bot - top

        hwndDC = win32gui.GetWindowDC(wH)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)
        windll.user32.PrintWindow(wH, saveDC.GetSafeHdc(), 2)
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        im = Image.frombuffer(
            "RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1
        )
        im = im.crop(area)
        im.save("../currImg.png", "png")
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(wH, hwndDC)
    else:
        ss = _region_grabber(RelToAbs(area))
        im = Image.fromarray(np.array(ss)[..., -2::-1], "RGB")
    return im


def ImageCheck(pathList, area, timeout=0):
    if ImageSearch(pathList, area, timeout) != [-1, -1]:
        return True
    else:
        return False


def ImgGoneCheck(pathList, area, timeout=3):
    startT = time.time()
    while ImageCheck(pathList, area):
        if timeout != -1 and time.time() - startT > timeout:
            return False
    return True


def ImageSearch(pathList, area, timeout=0):
    absArea = RelToAbs(area)
    startT = time.time()
    if type(pathList) is str:
        pathList = [pathList]
    while True:
        im = RegionGrab(area)
        for path in pathList:
            if (r := _imagesearcharea(path, *absArea, im=im)) != [-1, -1]:
                return r
        if timeout == 0 or (timeout != -1 and time.time() - startT > timeout):
            return [-1, -1]


def ClickImage(path, area, timeout=3):
    pos = ImageSearch(path, area, timeout)

    def mid(a, b):
        return a + ((b - a) / 2)

    if pos != [-1, -1]:
        Click(mid(area[0], area[2]), mid(area[1], area[3]))


def get_mid(area):
    def mid(a, b):
        return a + ((b - a) / 2)

    x1, y1, x2, y2 = area
    return mid(x2, x1), mid(y2, y1)


def give_me_mid(click, area):
    gX, gY = click
    x1, y1, x2, y2 = area
    if not (x1 < gX < x2) or not (y1 < gY < y2):
        return None
    xDi = max(gX - x1, x2 - gX)
    yDi = max(gY - y1, y2 - gY)
    return int(gX - xDi), int(gY - yDi), int(gX + xDi), int(gY + yDi)


def sleep(secs):
    time.sleep(secs)


# parameter must be a PIL image
def send_to_clipboard(image):
    if not "Windows" in platform.platform():
        return
    from io import BytesIO

    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    import win32clipboard

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def moveMouse(x, y):
    pyag.moveTo(*RelToAbs((x, y)))


def forceAwake():
    pyag.moveRel(1, 0)
    pyag.moveRel(-1, 0)


def reposition():
    import win32gui

    winds = []

    def enum_windows_callback(i, winds):
        if (
            win32gui.GetClassName(i) == "Chrome_WidgetWin_1"
            and win32gui.GetWindowText(i) == ""
            and win32gui.GetParent(i) == 0
        ):
            winds.append(i)

    win32gui.EnumWindows(enum_windows_callback, winds)
    sleep(0.1)
    print(winds)
    if not winds:
        return False
    global hwnd
    hwnd = winds[0]
    pos = getRelPos()
    resizeWin((min(pos[0], 654), min(pos[1], 158)), (1274, 880))
    return True


def screenshot(showMenu=False, saveTo=None):
    img_in = winScreenGrab().crop((70, 38, 1206, 870 if showMenu else 718)).convert("RGB")
    if saveTo is not None:
        img_in.save(saveTo + "_SS.png", "png")
    return img_in


def openApp():
    import platform

    if "Windows" in platform.platform():
        import win32gui

        while not reposition():
            if win32gui.FindWindow(None, "GameLauncher on Artix Entertainment v.212") == 0:
                os.startfile("C:\\Program Files\\Artix Game Launcher\\Artix Game Launcher.exe")
                sleep(3)
            global hwnd
            hwnd = win32gui.FindWindow(None, "GameLauncher on Artix Entertainment v.212")
            Click(362, 471)
            sleep(2)
            Click(564, 800)
            sleep(7)
    login()


def login():
    reposition()
    area = (513, 590, 733, 664)
    area = give_me_mid(get_mid(area), area)
    RegionGrab(area).save(f"ScreenCaps/{area}.png", "png")
    ClickImage("UI/LoginButton.png", (513, 590, 733, 664), -1)
    Click(618, 625)
    ImageSearch("UI/CharShadia.png", (748, 190, 1176, 312), -1)
    Click(948, 237)
    ImageSearch("UI/Launch.png", (154, 651, 470, 744), -1)
    Click(312, 695)
