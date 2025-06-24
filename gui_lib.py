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
        return cv2.minMaxLoc(res)[1] >= precision

    def MatchMask(path):
        mask_img = cv2.imread(path, 0)
        if mask_img is None:
            raise FileNotFoundError(f"Image file not found: {path}")
        # Convert relative ratios to absolute pixels
        area = UTILS.AreaFromPath(path)
        size = list(mask_img.shape[:2])[::-1]
        # expand_area = (area[0] - 0.002, area[1] - 0.002, area[2] + 0.002, area[3] + 0.002)
        im = API.WindowCapture().crop(UTILS.ToRelative(area))
        scrn_img = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2GRAY)
        scrn_img = cv2.resize(scrn_img, size, interpolation=cv2.INTER_AREA)
        template_mask = cv2.threshold(mask_img, 1, 255, cv2.THRESH_BINARY)[1]

        res = cv2.matchTemplate(mask_img, scrn_img, cv2.TM_CCOEFF_NORMED, mask=template_mask)
        print(cv2.minMaxLoc(res)[1])
        return cv2.minMaxLoc(res)[1] >= 0.95

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
    def MouseClick(pos, times=1):
        pos = UTILS.ToAbsolute(pos)
        API.MouseClick(pos)
        for _ in range(times - 1):
            time.sleep(0.1)
            API.MouseClick(pos)

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


if __name__ == "__main__":
    import cv2
    import numpy as np
    import dearpygui.dearpygui as dpg
    import time
    from threading import Timer

    # ------ Image Preprocessing Filters ------ #
    def apply_contour(img):
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        objects = []
        height, width = img.shape[:2]
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h

            area = w * h
            aspect_ratio = w / float(h)

            if area < 3000 or area > 0.3 * width * height:
                continue  # Too small or too big
            if aspect_ratio < 0.2 or aspect_ratio > 3.5:
                continue
            objects.append((x, y, w, h))
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img, objects

    def apply_blur(img, k):
        return cv2.GaussianBlur(img, (k * 2 + 1, k * 2 + 1), 0)

    def apply_canny(img, min_thresh, max_thresh):
        return cv2.Canny(img, min_thresh, max_thresh)

    def apply_adaptive_threshold(img, block_size, C):
        return cv2.adaptiveThreshold(
            img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, (block_size * 2 + 3), C
        )

    def apply_morphology(img, k):
        kernel = np.ones((k, k), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    def apply_median_blur(img, k):
        return cv2.medianBlur(img, k * 2 + 1)

    def apply_bilateral_filter(img, d, sigmaColor, sigmaSpace):
        return cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)

    def apply_histogram_equalization(img):
        return cv2.equalizeHist(img)

    def apply_clahe(img, clipLimit, tileGridSize):
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(tileGridSize, tileGridSize))
        return clahe.apply(img)

    # ------ Pipeline Config ------ #
    FILTERS = {
        "Blur": {"func": apply_blur, "params": {"k": 3}},
        "Median Blur": {"func": apply_median_blur, "params": {"k": 3}},
        "Bilateral Filter": {
            "func": apply_bilateral_filter,
            "params": {"d": 9, "sigmaColor": 75, "sigmaSpace": 75},
        },
        "Canny": {"func": apply_canny, "params": {"min_thresh": 100, "max_thresh": 200}},
        "Adaptive Threshold": {
            "func": apply_adaptive_threshold,
            "params": {"block_size": 5, "C": 5},
        },
        "Morphology": {"func": apply_morphology, "params": {"k": 5}},
        "Histogram Equalization": {"func": apply_histogram_equalization, "params": {}},
        "CLAHE": {"func": apply_clahe, "params": {"clipLimit": 2.0, "tileGridSize": 8}},
    }

    pipeline = []

    # Capture the initial image to determine dimensions

    img_init = np.array(GUI.CaptureRegion((0, 0, 1, 0.807)).convert("RGB"))
    img_h, img_w = img_init.shape[:2]
    texture_data = img_init.astype(np.float32) / 255.0

    # ------ Debounce ------ #
    debounce_timer = None

    def debounce_process():
        global debounce_timer
        if debounce_timer:
            debounce_timer.cancel()
        debounce_timer = Timer(0.3, process_image)
        debounce_timer.start()

    # ------ UI ------ #
    dpg.create_context()
    dpg.create_viewport(title="Filter Pipeline Builder", width=img_w + 400, height=max(img_h, 720))
    with dpg.font_registry():
        big_font = dpg.add_font("C:/Windows/Fonts/segoeui.ttf", 40)  # Path for Windows default font
    dpg.bind_font(big_font)
    with dpg.window(label="Filters", width=400, height=img_h, pos=(0, 0), no_title_bar=True):
        dpg.add_text("Drag filters to rearrange")

        with dpg.group(horizontal=True):
            dpg.add_text("Add Filter")
            dpg.add_combo(list(FILTERS.keys()), callback=lambda s, a: add_filter(a))
            dpg.add_button(label="Clear", callback=lambda: clear_pipeline())

        filter_list = dpg.add_child_window(height=img_h - 180, width=-1, tag="filter_list")

    with dpg.texture_registry():
        dpg.add_raw_texture(
            img_w,
            img_h,
            texture_data.flatten(),
            tag="processed_texture",
            format=dpg.mvFormat_Float_rgb,
        )
    with dpg.window(label="Image", width=img_w, height=img_h, pos=(400, 0), no_title_bar=True):
        dpg.add_image("processed_texture")

    def add_filter(name):
        if name not in FILTERS:
            return
        filter_id = dpg.generate_uuid()
        params = FILTERS[name]["params"].copy()

        with dpg.collapsing_header(
            label=name,
            parent="filter_list",
            tag=filter_id,
            default_open=False,
            drag_callback=None,
            drop_callback=None,
        ):
            with dpg.group(horizontal=True, parent=filter_id):
                # Text inputs for each parameter in header
                for key, val in params.items():
                    input_id = f"{filter_id}_{key}_input"
                    dpg.add_input_int(
                        label=f"{key}:",
                        default_value=val,
                        width=180,
                        step=None,
                        callback=lambda s, a, u=filter_id, k=key: update_param(u, k, a),
                        tag=input_id,
                    )

            with dpg.group(horizontal=False, parent=filter_id):
                # Optional: sliders or more advanced config below the header
                for key, val in params.items():
                    slider_id = f"{filter_id}_{key}_slider"
                    dpg.add_slider_int(
                        label=f"{key} (slider)",
                        default_value=val,
                        min_value=1,
                        max_value=100,
                        width=300,
                        callback=lambda s, a, u=filter_id, k=key, input_ref=f"{filter_id}_{key}_input": sync_input_and_update(
                            u, k, a, input_ref
                        ),
                        tag=slider_id,
                    )

        pipeline.append({"id": filter_id, "name": name, "params": params})
        debounce_process()

    def move_filter_up(filter_id):
        idx = next((i for i, f in enumerate(pipeline) if f["id"] == filter_id), None)
        if idx is not None and idx > 0:
            pipeline[idx], pipeline[idx - 1] = pipeline[idx - 1], pipeline[idx]
            dpg.move_item(filter_id, parent="filter_list", before=pipeline[idx]["id"])
            debounce_process()

    def move_filter_down(filter_id):
        idx = next((i for i, f in enumerate(pipeline) if f["id"] == filter_id), None)
        if idx is not None and idx < len(pipeline) - 1:
            pipeline[idx], pipeline[idx + 1] = pipeline[idx + 1], pipeline[idx]
            dpg.move_item(filter_id, parent="filter_list", before=pipeline[idx + 1]["id"])
            debounce_process()

    def sync_input_and_update(filter_id, param_name, value, input_id):
        dpg.set_value(input_id, value)
        update_param(filter_id, param_name, value)

    def update_param(filter_id, param_name, value):
        for step in pipeline:
            if step["id"] == filter_id:
                step["params"][param_name] = value
                break
        debounce_process()

    def clear_pipeline():
        for step in pipeline:
            dpg.delete_item(step["id"])
        pipeline.clear()
        debounce_process()

    def process_image():
        img = np.array(GUI.CaptureRegion((0, 0, 1, 0.807)).convert("RGB"))
        channels = cv2.split(img)  # Split into R, G, B channels

        processed_channels = []
        for channel in channels:
            channel_gray = cv2.cvtColor(cv2.merge([channel, channel, channel]), cv2.COLOR_BGR2GRAY)

            for step in pipeline:
                name = step["name"]
                params = step["params"]
                try:
                    channel_gray = FILTERS[name]["func"](channel_gray, **params)
                except Exception as e:
                    print(f"Error applying {name}: {e}")

            channel_gray, objects = apply_contour(channel_gray)
            processed_channels.append(channel_gray)

        # Merge processed R, G, B channels
        merged_img = cv2.merge(processed_channels)
        img_rgb_f32 = merged_img.astype(np.float32) / 255.0
        dpg.set_value("processed_texture", img_rgb_f32.flatten())

    # Run the GUI
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
