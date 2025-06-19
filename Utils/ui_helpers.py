import macro_utils as m_ui
import time


def SetUp(src):
    if False:
        useForegroundWin()
    else:
        m_ui.assignWin("Chrome_WidgetWin_1", "Evolved DragonFable Launcher")
    from pathlib import Path
    import os

    os.chdir(f"C:/Users/User/Desktop/Programing/DragonFableMacros/Images/{Path(src).stem}")


def useForegroundWin():
    import win32gui

    time.sleep(2)
    m_ui.setHWND(win32gui.GetForegroundWindow())


# Get Region from img/src
def img_area(path):
    coords_str = path.split("#")[-1].split(")")[0].strip("(")
    return tuple(map(int, coords_str.split(",")))


# Wait for one of several images to appear
# timeout=-1 will halt forever
# interval is how often to check
def AwaitImg(*paths, timeout=3, interval=0.01):
    areas = [img_area(p) for p in paths]
    startT = time.time()
    while timeout == -1 or time.time() - startT <= timeout:
        for path, area in zip(paths, areas):
            if m_ui.ImageSearch(path, area, timeout) != [-1, -1]:
                return True
        time.sleep(interval)
    return False


def Check(*paths):
    for path in paths:
        if m_ui.ImageSearch(path, img_area(path), 0) != [-1, -1]:
            return True
    return False


# Wait for an image to disappear
def AwaitNotImg(*paths, timeout=3, interval=0.01):
    areas = [img_area(p) for p in paths]
    startT = time.time()
    while timeout == -1 or time.time() - startT <= timeout:
        for path, area in zip(paths, areas):
            if m_ui.ImageSearch(path, area, timeout) == [-1, -1]:
                return True
        time.sleep(interval)
    return False


def ClickIf(path, timeout=3, interval=0.01):
    if AwaitImg(path, timeout=timeout, interval=interval):
        m_ui.ClickImage(path, img_area(path), 0)
        return True
    return False


def MouseClick(x, y):
    m_ui.Click(x, y)


def Press(k):
    m_ui.typeKeys(k)
