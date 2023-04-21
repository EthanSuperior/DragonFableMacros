"""
Basis of Code comes from Martin Lee's imagesearch.py
code src: https://github.com/drov0/python-imagesearch
https://brokencode.io/how-to-easily-image-search-with-python/
"""
import os
import platform

from scipy.ndimage import center_of_mass, generate_binary_structure, label
import applescript
from pynput import mouse
import time
import numpy as np
from PIL import Image, ImageChops, ImageFilter

import cv2
import pyautogui as pyag

pyag.FAILSAFE = True

hwnd = 0

REDUCE_FACTOR = 1
BOUNDS = {0,0,25,0}
SLOT_TO_SELL = 56
MAX_SLOTS = 60
SAVE_PATH = 'C:/Users/Evan Chase/Desktop/Files/Programming/DragonFableLite/Images'

_is_retina = False
if platform.system() == "Darwin":
    import subprocess
    _is_retina = subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True) == 0


def getWinRect():
    if 'Windows' in platform.platform():
        import win32gui
        return win32gui.GetWindowRect(win32gui.GetForegroundWindow())
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
        import win32gui
        win32gui.FindWindow(className, winName)

def resizeWin(pos = getRelPos(), size=None):
    if size is None:
        rect = getWinRect()
        size = (rect[2]-rect[0], (rect[3]-rect[1]))
    if 'Windows' in platform.platform():
        import win32gui
        wH = win32gui.GetForegroundWindow()
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
        import win32gui
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
    pos = RelToAbs((x, y))
    pyag.mouseDown(*pos, button='left')
    sleep(.1)
    pyag.mouseUp(*pos, button='left')

def getRelMousePos():
    return AbsToRel(pyag.position())

def typeKeys(*keys):
    interval = 0
    if type(keys[-1]) is float:
        interval = keys[-1]
        keys = list(*keys[:-1])
    else: keys = list(*keys)

    pyag.typewrite(''.join(keys), interval)


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

def RegionGrab(area):
    ss = _region_grabber(RelToAbs(area))
    im = Image.fromarray(np.array(ss)[..., -2::-1], 'RGB')
    return im

def ImageCheck(pathList, area, timeout=0):
    if ImageSearch(pathList, area, timeout) != [-1, -1]: return True
    else: return False

def ImgGoneCheck(pathList, area, timeout=3):
    startT = time.time()
    while ImageCheck(pathList, area, 0):
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

_currX,_currY = 0, 0
def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        if pressed: print('{}{}, [{}]'.format('m.Click', getRelMousePos(), pyag.position()))
    else:
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
    pyag.moveTo(*RelToAbs(start))
    pyag.dragTo(*RelToAbs(end), button='left')

def mask_image(img_in, img_mask):
    diff_img = ImageChops.difference(img_in.convert('RGB'), img_mask.convert('RGB'))
    diff_img = diff_img.convert('L').filter(ImageFilter.MedianFilter(size=5)).point(lambda i: i * 255)
    return diff_img.convert('1')

def largest_in_mask(diff_img, min_size = 0):
    labels, labels_nb = label(np.array(diff_img), generate_binary_structure(2, 2))
    areas = [*np.bincount(labels.flat)[1:]]
    if len(areas) == 0 or (m_area:=max(areas)) < min_size: return None
    return center_of_mass(labels, labels=labels, index=areas.index(m_area)+1)[::-1]

def on_move(x, y):
    if x < 10 and y < 10: listener.stop()

def moveMouse(x, y):
    pyag.moveTo(*RelToAbs((x, y)))

if __name__ == '__main__':
    os.chdir(SAVE_PATH)
    with mouse.Listener(on_click=on_click,on_move=on_move) as listener:
        listener.join()
