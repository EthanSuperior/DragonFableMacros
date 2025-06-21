"""
Original basis of code comes from Martin Lee's imagesearch.py
code src: https://github.com/drov0/python-imagesearch
https://brokencode.io/how-to-easily-image-search-with-python/
"""

import math
import time
import numpy as np
import cv2

from utils import UTILS
from api_lib import API

folder_dir = "ScreenCaps"
exe_path = "C:/Users/User/Downloads/Evolved DragonFable Launcher/evolved-dragonfable-launcher.exe"


class GUI:
    @staticmethod
    def MousePosition():
        return UTILS.ToRatio(API.MousePosition())

    @staticmethod
    def CaptureRegion(area):
        return API.WindowCapture().crop(UTILS.ToRelative(area))

    @staticmethod
    def SaveRegion(area, name=""):
        GUI.CaptureRegion(area).save(f"{folder_dir}/{name}#{area}.png", "png")
        GUI.DrawGizmo(area)

    @staticmethod
    def CheckImage(path, precision=0.8):
        if not path:
            return False
        # Load template image
        template = cv2.imread(path, 0)
        if template is None:
            raise FileNotFoundError(f"Image file not found: {path}")
        # Convert relative ratios to absolute pixels
        area = UTILS.AreaFromPath(path)
        size = UTILS.GetSize(area)
        expanded_area = UTILS.AddBuffer(area, 0.02)
        expanded_size = UTILS.GetSize(expanded_area)
        # expand_area = (area[0] - 0.002, area[1] - 0.002, area[2] + 0.002, area[3] + 0.002)
        im = API.WindowCapture().crop(UTILS.ToRelative(expanded_area))
        img_gray = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2GRAY)

        # Resize grabbed image to same realative sizes
        width = math.ceil(template.shape[1] * (expanded_size[0] / size[0]))
        height = math.ceil(template.shape[0] * (expanded_size[1] / size[1]))
        img_gray = cv2.resize(img_gray, (width, height), interpolation=cv2.INTER_AREA)
        # Match template
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        return max_val >= precision

    @staticmethod
    def AwaitImg(*paths, timeout=3, interval=0.01):
        """
        Wait for one of several images to appear
        timeout=-1 will run forever
        interval is how often to check
        """
        startT = time.time()
        while timeout == -1 or time.time() - startT <= timeout:
            for path in paths:
                if GUI.CheckImage(path):
                    return path
            time.sleep(interval)
        for path in paths:
            if GUI.CheckImage(path):
                return path
        return None

    @staticmethod
    def AwaitNotImg(*paths, timeout=3, interval=0.01):
        """
        Wait for an image to disappear
        """
        startT = time.time()
        while timeout == -1 or time.time() - startT <= timeout:
            for path in paths:
                if not GUI.CheckImage(path):
                    return path
            time.sleep(interval)
        for path in paths:
            if not GUI.CheckImage(path):
                return path
        return None

    @staticmethod
    def ClickIf(path, timeout=3, interval=0.01):
        if not path:
            return False
        if GUI.AwaitImg(path, timeout=timeout, interval=interval) is not None:
            GUI.MouseClick(UTILS.MidPt(UTILS.AreaFromPath(path)))
            return True
        return False

    @staticmethod
    def MouseClick(pos):
        API.MouseClick(UTILS.ToAbsolute(pos))

    @staticmethod
    def TypeKeys(keys, interval=0.01):
        API.TypeKey(keys[0])
        for key in keys[1:]:
            time.sleep(interval)
            API.TypeKey(key)

    @staticmethod
    def DrawGizmo(area, color="#94d6fe"):  # NOTE COLOR IS IN BGR SPACE
        API.DrawDebug(UTILS.ToAbsolute(area), API.ColorFromHex(color))

    @staticmethod
    def DrawDebugGrid():
        GUI.DrawGizmo((0, 0, 1, 1))
        for y in np.linspace(0, 1, 50)[1:-1]:
            for x in np.linspace(0, 1, 50)[1:-1]:
                GUI.DrawGizmo((x, y), "#FF0")
