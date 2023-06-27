"""
Basis of Code comes from Martin Lee's imagesearch.py
code src: https://github.com/drov0/python-imagesearch
https://brokencode.io/how-to-easily-image-search-with-python/
"""
import os
import platform

from ctypes import windll

if 'Windows' in platform.platform():
    import win32api
    import win32con
    import win32process
    import win32ui
    import win32gui
    import pytesseract as pyocr
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
BOUNDS = {0,0,25,0}
SLOT_TO_SELL = 56
MAX_SLOTS = 60



_is_retina = False
if platform.system() == "Darwin":
    import subprocess
    _is_retina = subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True) == 0

def _imagesearcharea(image, x1, y1, x2, y2, precision=0.8, im=None):
    x1, x2, y1, y2 = x1-1,x2+1,y1-1,y2+1
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
        raise FileNotFoundError('Image file not found: {}'.format(image))

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


def _region_grabber(region):
    import mss
    if _is_retina: region = [n * 2 for n in region]
    x1 = region[0]
    y1 = region[1]
    width = region[2]
    height = region[3]

    region = x1, y1, width, height
    with mss.mss() as sct:
        return sct.grab(region)

def getHWND():
    global hwnd
    if 'Windows' in platform.platform():
        if hwnd == win32gui.GetForegroundWindow(): return 0
        return hwnd if hwnd !=0 else win32gui.GetForegroundWindow()
    else: return 0

def printWin():
    if not 'Windows' in platform.platform(): return
    print("\'"+win32gui.GetWindowText(getHWND())+"\'")

def getWinRect():
    if 'Windows' in platform.platform():
        global hwnd
        wH = hwnd if hwnd !=0 else win32gui.GetForegroundWindow()
        return win32gui.GetWindowRect(wH)
    else:
        f_pr = applescript.tell.app('System Events', 'get name of process 1 where frontmost is true').out
        applescript.tell.app(f'{f_pr}', 'activate')
        def get_command_string(app, command, argument=None):
            argument = (' to ' + argument) if argument is not None else ''
            return f'tell application process "{app}"\n\t{command} of window 1{argument}\nend tell'
        pos = applescript.tell.app('System Events', get_command_string(f_pr, 'get position')).out.split(',')
        size = applescript.tell.app('System Events', get_command_string(f_pr, 'get size')).out.split(',')
        return [int(pos[0]),int(pos[1]),int(size[0]), int(size[1])]
# 1385, 769
def getRelPos():
    return getWinRect()[:2]

def assignWin(className, winName):
    if 'Windows' in platform.platform():
        global hwnd
        hwnd = win32gui.FindWindow(className, winName)

def resizeWin(pos = getRelPos(), size=None):
    if size is None:
        rect = getWinRect()
        size = (rect[2]-rect[0], (rect[3]-rect[1]))
    if 'Windows' in platform.platform():
        global hwnd
        wH = hwnd if getHWND() != 0 else win32gui.GetForegroundWindow()
        win32gui.MoveWindow(wH, *pos, *size, True)
    else:
        f_pr = applescript.tell.app('System Events', 'get name of process 1 where frontmost is true').out
        applescript.tell.app(f'{f_pr}', 'activate')
        def get_command_string(app, command, argument=None):
            argument = (' to ' + argument) if argument is not None else ''
            return f'tell application process "{app}"\n\t{command} of window 1{argument}\nend tell'
        applescript.tell.app('System Events', get_command_string(f_pr, 'set position', '{'+str(pos[0])+', '+str(pos[1])+'}')).out.split(',')
        applescript.tell.app('System Events', get_command_string(f_pr, 'set size', '{'+str(size[0])+', '+str(size[1])+'}')).out.split(',')

def focusWin(className, winName):
    if 'Windows' in platform.platform():
        win32gui.SetForegroundWindow(win32gui.FindWindow(className, winName))
    else:
        f_pr = applescript.tell.app('System Events', 'get name of process 1 where frontmost is true').out
        applescript.tell.app({f_pr}, 'activate')

def RelToAbs(pos):
    relX, relY = getRelPos()
    if len(pos) == 2: return pos[0]+relX, pos[1]+relY
    else: return pos[0]+relX, pos[1]+relY, pos[2]+relX, pos[3]+relY

def AbsToRel(pos):
    relX, relY = getRelPos()
    if len(pos) == 2: return pos[0]-relX, pos[1]-relY
    else: return pos[0]-relX, pos[1]-relY, pos[2]-relX, pos[3]-relY

def Click(x, y): #(72, 38) vs (63, 0) (-9, -38) -9, -13
    wH = getHWND()
    if wH != 0:
        l_pram = win32api.MAKELONG(int(x-9), int(y-38))
        win32gui.PostMessage(wH, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_pram)
        win32gui.PostMessage(wH, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, l_pram)
    else:
        # mP = pyag.position()
        pos = RelToAbs((x, y))
        # pos = list(posR)
        # pos[1] += 38 * REDUCE_FACTOR
        pyag.mouseDown(*pos, button='left')
        sleep(.1)
        pyag.mouseUp(*pos, button='left')
        # pyag.moveTo(*mP)

def getRelMousePos():
    return AbsToRel(pyag.position())

def typeKeys(*keys):
    wH = getHWND()
    interval = 0
    if type(keys[-1]) is float:
        interval = keys[-1]
        keys = list(*keys[:-1])
    else: keys = list(*keys)

    if wH != 0:
        currThread, outThread = win32api.GetCurrentThreadId(), win32process.GetWindowThreadProcessId(wH)[0]
        win32process.AttachThreadInput(currThread, outThread, 1)
        for k in keys:
            v_key = {'<':0x25, '>':0x27, '\t':0x09}
            char_id, capital = ord(k.upper()), k.isupper()
            if k in v_key: char_id = v_key[k]
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
        pyag.typewrite(''.join(keys), interval)
'''
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
'''
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

        im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(wH, hwndDC)
        return im
    else: return pyag.screenshot().crop(getWinRect()).convert('RGB')

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
        im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        im = im.crop(area)
        im.save('../currImg.png', 'png')
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(wH, hwndDC)
    else:
        ss = _region_grabber(RelToAbs(area))
        im = Image.fromarray(np.array(ss)[..., -2::-1], 'RGB')
    return im

def ImageCheck(pathList, area, timeout=0):
    """
    Returns where an image exists in an area
    :param pathList: name of image to look for
    :param area: area to look within
    :param timeout: time to spend looking
    :return: True if the image is there, otherwise false.
    """
    return ImageSearch(pathList, area, timeout) != [-1, -1]

def ImgGoneCheck(pathList, area, timeout=3):
    startT = time.time()
    while ImageCheck(pathList, area):
        if timeout != -1 and time.time() - startT > timeout: return False
    return True

def ImageSearch(pathList, area, timeout=0):
    absArea = RelToAbs(area)
    startT = time.time()
    if type(pathList) is str: pathList = [pathList]
    while True:
        im = RegionGrab(area)
        for path in pathList:
            if (r := _imagesearcharea(path, *absArea, im=im)) != [-1, -1]: return r
        if timeout == 0 or (timeout != -1 and time.time() - startT > timeout): return [-1, -1]

def ClickImage(path, area, timeout = 3):
    pos = ImageSearch(path, area, timeout)
    def mid(a, b): return a + ((b-a)/2)
    if pos != [-1, -1]: Click(mid(area[0], area[2]), mid(area[1], area[3]))

def get_mid(area):
    def mid(a, b): return a + ((b - a) / 2)
    x1, y1, x2, y2 = area
    return mid(x2, x1), mid(y2, y1)

def give_me_mid(click, area):
    gX, gY = click
    x1, y1, x2, y2 = area
    if not(x1<gX<x2) or not(y1<gY<y2): return None
    xDi = max(gX-x1, x2-gX)
    yDi = max(gY-y1, y2-gY)
    return int(gX - xDi), int(gY - yDi), int(gX + xDi), int(gY + yDi)

def sleep(secs):
    time.sleep(secs)

# parameter must be a PIL image
def send_to_clipboard(image):
    if not 'Windows' in platform.platform(): return
    from io import BytesIO
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

    import win32clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

startT = None
_currX,_currY = 0, 0
midClicked = 0
def on_click(x, y, button, pressed):
    global startT, midClicked
    if button == mouse.Button.left:
        if pressed:
            if startT is None:
                startT = time.time()
            else:
                if midClicked: return
                dT = int((time.time() - startT)*1000)/1000
                startT = time.time()
                # print('{}{}'.format('m.Click', getRelMousePos()))
                print('m.sleep({})\nm.Click{}'.format(dT, getRelMousePos()))
    elif button == mouse.Button.middle:
        if midClicked:
            startT = time.time()
        else:
            print('battle((classID, "Single"))')
        midClicked = (midClicked + 1) % 4
    else:
        if midClicked: return
        global _currX,_currY
        if pressed:
            print('{} RC at {}'.format('Pressed', getRelMousePos()))
            _currX, _currY = getRelMousePos()
        else:
            print('{} RC at {}'.format('Released', getRelMousePos()))
            x,y = getRelMousePos()
            if abs(_currX-x) + abs(_currY-y) >= 10:
                area = (min(_currX,x), min(_currY,y), max(_currX,x), max(_currY,y))
                area = give_me_mid(get_mid(area), area)
                RegionGrab(area).save(f'ScreenCaps/{area}.png','png')

def drag(start, end):
    wH = getHWND()
    if wH != 0:
        x, y = start
        l_pram = win32api.MAKELONG(int(x - 9), int(y - 38))
        win32gui.PostMessage(wH, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_pram)
        x, y = end
        l_pram = win32api.MAKELONG(int(x - 9), int(y - 38))
        win32gui.PostMessage(wH, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, l_pram)
    else:
        pyag.moveTo(*RelToAbs(start))
        pyag.dragTo(*RelToAbs(end), button='left')

def on_move(x, y):
    if x < 10 and y < 10: listener.stop()

def moveMouse(x, y):
    pyag.moveTo(*RelToAbs((x, y)))

def forceAwake():
    pyag.moveRel(1, 0)
    pyag.moveRel(-1, 0)

if __name__ == '__main__':
    pyag.FAILSAFE = True
    os.chdir('C:/Users/Evan Chase/Desktop/Files/ProgrammingGit/College/Fall 2023/DragonFable/Images')
    assignWin('Chrome_WidgetWin_1', '')
    with mouse.Listener(on_click=on_click,on_move=on_move) as listener:
        listener.join()


