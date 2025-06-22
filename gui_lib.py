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


def nothing(x):
    pass


if __name__ == "__main__":
    # Convert to grayscale again
    img = cv2.cvtColor(np.array(GUI.CaptureRegion((0, 0, 1, 0.807))), cv2.COLOR_BGR2GRAY)

    cv2.namedWindow("DEV GUI")
    # Create trackbars for parameters
    cv2.createTrackbar("E Blur", "DEV GUI", 0, 1, nothing)
    cv2.createTrackbar("Blur Kernel", "DEV GUI", 4, 36, nothing)  # 4
    # cv2.createTrackbar("E Resize", "DEV GUI", 0, 1, nothing)
    # cv2.createTrackbar("Scale Down", "DEV GUI", 1, 8, nothing)
    cv2.createTrackbar("E AdapThresh 1", "DEV GUI", 0, 1, nothing)
    cv2.createTrackbar("Block Size", "DEV GUI", 5, 500, nothing)
    cv2.createTrackbar("C", "DEV GUI", 1, 45, nothing)
    cv2.createTrackbar("E Canny", "DEV GUI", 0, 1, nothing)
    cv2.createTrackbar("Min Thresh", "DEV GUI", 400, 4000, nothing)  # 1280
    cv2.createTrackbar("Max Thresh", "DEV GUI", 400, 8000, nothing)  # 2256
    cv2.createTrackbar("E AdapThresh 2", "DEV GUI", 0, 1, nothing)
    cv2.createTrackbar("Block Size_2", "DEV GUI", 5, 251, nothing)
    cv2.createTrackbar("C_2", "DEV GUI", 1, 45, nothing)
    cv2.createTrackbar("E Morphology", "DEV GUI", 0, 1, nothing)
    cv2.createTrackbar("Morph Kernel", "DEV GUI", 40, 160, nothing)  # 90
    # cv2.createTrackbar("E Contour Detection", "DEV GUI", 0, 1, nothing)
    cv2.createTrackbar("E Area Contours", "DEV GUI", 0, 1, nothing)
    cv2.createTrackbar("Min Area", "DEV GUI", 4, 4000, nothing)
    cv2.createTrackbar("Max Area", "DEV GUI", 100, 8000, nothing)
    cv2.createTrackbar("E Ratio Contour", "DEV GUI", 0, 1, nothing)
    cv2.createTrackbar("Min Ratio", "DEV GUI", 0, 99, nothing)  # 1280
    cv2.createTrackbar("Max Ratio", "DEV GUI", 0, 99, nothing)  # 2256

    cv2.namedWindow("Render")
    # Loop to update the image
    while True:
        # Get current positions of trackbars
        # pow_2 = cv2.getTrackbarPos("Scale Down", "DEV GUI")  # 8
        blur_k = cv2.getTrackbarPos("Blur Kernel", "DEV GUI")  # 2
        block_size = cv2.getTrackbarPos("Block Size", "DEV GUI")
        C = cv2.getTrackbarPos("C", "DEV GUI")
        threshold1 = cv2.getTrackbarPos("Min Thresh", "DEV GUI")  # 0
        threshold2 = max(cv2.getTrackbarPos("Max Thresh", "DEV GUI"), threshold1)  # 3067
        block_size_2 = cv2.getTrackbarPos("Block Size_2", "DEV GUI")  # 251
        C_2 = cv2.getTrackbarPos("C_2", "DEV GUI")  # 5
        morph_k = cv2.getTrackbarPos("Morph Kernel", "DEV GUI")  # 0
        min_area = cv2.getTrackbarPos("Min Area", "DEV GUI")
        max_area = cv2.getTrackbarPos("Max Area", "DEV GUI")
        min_ratio = cv2.getTrackbarPos("Min Ratio", "DEV GUI")  # 1280
        max_ratio = cv2.getTrackbarPos("Max Ratio", "DEV GUI")  # 2256

        is_Resize = False  # cv2.getTrackbarPos("E Resize", "DEV GUI")
        is_Blur = cv2.getTrackbarPos("E Blur", "DEV GUI")
        is_AdapThresh = cv2.getTrackbarPos("E AdapThresh 1", "DEV GUI")
        is_Canny = cv2.getTrackbarPos("E Canny", "DEV GUI")
        is_AdapThresh2 = cv2.getTrackbarPos("E AdapThresh 2", "DEV GUI")
        is_Morphology = cv2.getTrackbarPos("E Morphology", "DEV GUI")
        is_ContourDetect = True  # cv2.getTrackbarPos("E Contour Detection", "DEV GUI")
        is_Area = cv2.getTrackbarPos("E Area Contours", "DEV GUI")
        is_Ratio = cv2.getTrackbarPos("E Ratio Contour", "DEV GUI")

        h, w = img.shape[:2]
        up_img = img.copy()
        if is_Blur:
            blur_k = (blur_k * 2) + 1
            up_img = cv2.GaussianBlur(up_img, (blur_k, blur_k), 0)
        if is_Resize:
            w = w // (2**pow_2)
            h = h // (2**pow_2)
            up_img = cv2.resize(up_img, (w, h), interpolation=cv2.INTER_AREA)
        # Apply Gaussian blur

        # Adaptive thresholding
        x, y = cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV
        if is_AdapThresh:
            up_img = cv2.adaptiveThreshold(up_img, 255, x, y, (block_size * 2) + 3, C)
        if is_Canny:
            up_img = cv2.Canny(up_img, threshold1, threshold2, apertureSize=5)
        if is_AdapThresh2:
            up_img = cv2.adaptiveThreshold(up_img, 255, x, y, (block_size_2 * 2) + 3, C_2)

        # Morphology
        if is_Morphology:
            kernel = np.ones((morph_k, morph_k), np.uint8)
            up_img = cv2.morphologyEx(up_img, cv2.MORPH_CLOSE, kernel)

        # Find contours
        if is_ContourDetect:
            contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            up_img = cv2.cvtColor(up_img, cv2.COLOR_GRAY2BGR)

            for c in contours:
                x, y, cw, ch = cv2.boundingRect(c)
                area = cw * ch
                aspect_ratio = w / float(h)
                if is_Area and (area < min_area or area > max_area):
                    continue  # too small
                if is_Ratio and (
                    aspect_ratio > (max_ratio + 1) / 100 or aspect_ratio < (min_ratio + 1) / 100
                ):
                    continue  # weird shape
                if h < 30 or w < 30:
                    continue  # avoid slivers
                cv2.rectangle(up_img, (x, y), (x + cw, y + ch), (0, 255, 0), 2)

        if is_Resize:
            w = w * (2**pow_2)
            h = h * (2**pow_2)
            up_img = cv2.resize(up_img, (w, h), interpolation=cv2.INTER_AREA)
        # Show image
        # cv2.resizeWindow("DEV GUI", 1000, 500)
        cv2.imshow("Render", up_img)

        # Break on ESC key
        if cv2.waitKey(1) & 0xFF == 27:
            break
        # time.strftime("%H-%M-%S") + ".png"

    cv2.destroyAllWindows()
    # height, width = img.shape[:2]
    # width = width // 4
    # height = height // 4
    # img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    # img = cv2.GaussianBlur(img, (blur_gauss, blur_gauss), 0)
    # img = cv2.adaptiveThreshold(
    #     img,
    #     255,
    #     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #     cv2.THRESH_BINARY_INV,  # Invert to make objects white
    #     block_size,
    #     C,  # blockSize, C (tweakable)
    # )

    # # Close gaps in edges to better group parts of the same object
    # kernel = np.ones((kern, kern), np.uint8)
    # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    # # contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # # objects = []
    # # for cnt in contours:
    # #     x, y, w, h = cv2.boundingRect(cnt)
    # #     area = w * h

    # #     area = w * h
    # #     aspect_ratio = w / float(h)

    # #     if area < 3000 or area > 0.3 * width * height:
    # #         continue  # Too small or too big
    # #     if aspect_ratio < 0.2 or aspect_ratio > 3.5:
    # #         continue
    # #     objects.append((x, y, w, h))
    # #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # cv2.imwrite("Gray_" + name, img)
