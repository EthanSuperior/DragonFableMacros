import dearpygui.dearpygui as dpg
import cv2
import numpy as np
from threading import Timer
from gui_lib import GUI

# Load your images
# from gui_lib import GUI

# print(GUI.MatchMask("top_dlg_mask#(0.360, 0.005, 0.640, 0.035).png"))
# exit()
# img1 = cv2.imread("Images/ScreenCaps/00-13-05#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
# img2 = cv2.imread("Images/ScreenCaps/00-13-11#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
# img3 = cv2.imread("Images/ScreenCaps/00-13-18#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
# img1 = cv2.imread("Images/ScreenCaps/01-40-22#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
# img2 = cv2.imread("Images/ScreenCaps/01-40-31#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
# img3 = cv2.imread("Images/ScreenCaps/01-40-36#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
# img4 = cv2.imread("Images/ScreenCaps/01-40-39#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
# img5 = cv2.imread("Images/ScreenCaps/01-41-14#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
# img6 = cv2.imread("Images/ScreenCaps/01-42-58#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
# img7 = cv2.imread("Images/ScreenCaps/01-43-05#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)

# Apply bitwise AND step by step to find intersection
# imgs = [img1, img2, img3, img5, img6, img7]  # Check that all images are the same shape
# assert all(
#     img.shape == imgs[0].shape for img in imgs
# ), "All images must be the same size and channels"

# # Stack all images into shape: (N, H, W) for grayscale or (N, H, W, C) for color
# stacked = np.stack(imgs, axis=0)

# # Check equality across all images
# match_mask = np.all(stacked == stacked[0], axis=0)  # shape: (H, W, 3)
# match_mask = np.all(match_mask, axis=-1)  # shape: (H, W)
# # If color image: reduce to per-pixel match by checking all channels
# result = imgs[0].copy()
# result[~match_mask] = [0, 0, 0]
# # Crop: keep top 20% and center 80% width
# height, width = result.shape[:2]
# Top cnt text....
# left = int(width * 0.36)
# top = int(height * 0.005)
# right = int(width * 0.64)
# bottom = int(height * 0.035)
# left = int(width * 0.36)
# top = int(height * 0.740)
# right = int(width * 0.64)
# bottom = int(height * 0.830)

# cropped = result[top:bottom, left:right]

# # Save or show result
# cv2.imwrite("dlg_mask#(0.360, 0.740, 0.640, 0.830).png", cropped)
# template_mask = cv2.threshold(cropped, 1, 255, cv2.THRESH_BINARY)[1]

# GUI.CaptureRegion((0.36, 0.005, 0.64, 0.035)).save("dlg_act(0.360, 0.005, 0.640, 0.035).png", "png")
# cv2.imshow("Result", template_mask)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# quit()
dpg.create_context()


def get_capture():
    """Capture the screen region and return it as a PIL Image."""
    return np.array(GUI.CaptureRegion((0, 0, 1, 0.807)).convert("RGB"))


img_init = get_capture()
img_h, img_w = img_init.shape[:2]


# region --- Filters
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


def apply_output(img, color):
    # img = cv2.merge(img)
    img_rgb_f32 = img.astype(np.float32) / 255.0
    dpg.set_value("processed_texture", img_rgb_f32.flatten())
    return img


# endregion


# --- Filter Pipeline
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
    "Output": {"func": apply_output, "params": {"color": "RGB"}},
}
pipeline = {}

# endregion


# region --- DearPyGui Callbacks
def on_drop(dropped_wnd, dragged_id):
    payload_type = dpg.get_drag_payload_type()
    if payload_type != "FILTER_REORDER":
        return  # Ignore unrelated drags like sliders
    print(f"Dropped {dragged_id} before {dropped_wnd}")
    dragged_wnd = dpg.get_item_parent(dragged_id)
    parent_wnd = dpg.get_item_parent(dropped_wnd)
    if dragged_wnd and dpg.does_item_exist(dragged_wnd):
        dpg.move_item(dragged_wnd, parent=parent_wnd, before=dropped_wnd)


def clear_pipeline():
    print("Clearing pipeline")
    out = pipeline.pop(dpg.get_alias_id("output"))
    for wnd in pipeline:
        dpg.delete_item(wnd)
    pipeline.clear()
    pipeline[dpg.get_alias_id("output")] = out
    debounce_process()


def update_param(wnd_id, key, value, sender):
    pipeline[wnd_id]["params"][key] = value
    other = sender[:-5] + ("slide" if sender.endswith("input") else "input")
    dpg.set_value(other, value)
    debounce_process()


def process_image():
    img = get_capture()
    for id in dpg.get_item_children("list")[1]:
        if not dpg.does_item_exist(id):
            continue
        filter = pipeline[id]["filter_type"]
        try:
            img = FILTERS[filter]["func"](img, **pipeline[id]["params"])
        except Exception as e:
            print(f"Error applying {filter}: {e}")


debounce_timer = None


def debounce_process():
    global debounce_timer
    if debounce_timer:
        debounce_timer.cancel()
    debounce_timer = Timer(0.3, process_image)
    debounce_timer.start()


# endregion


# region --- DearPyGui Layout
def add_filter(filter_type="Blur"):
    if filter_type not in FILTERS:
        return
    h_id = dpg.generate_uuid()
    params = FILTERS[filter_type]["params"].copy()
    print(f"Adding {filter_type} filter")
    with dpg.child_window(
        autosize_x=True, auto_resize_y=True, drop_callback=on_drop, parent="list"
    ) as wnd:
        with dpg.collapsing_header(label=filter_type, tag=h_id):
            with dpg.drag_payload(drag_data=h_id, payload_type="FILTER_REORDER"):
                dpg.add_text("Drag to rearrange before")
            for key in params:
                with dpg.group(horizontal=True):
                    dpg.add_text(f"{key}:")
                    callback = lambda s, a: update_param(wnd, key, a, s)
                    dpg.add_input_int(
                        step=-2,
                        step_fast=-2,
                        default_value=int(params[key]),
                        callback=callback,
                        width=100,
                        tag=f"{wnd}_{key}_input",
                    )
                    dpg.add_slider_int(
                        default_value=int(params[key]),
                        min_value=1,
                        max_value=100,
                        width=400,
                        callback=callback,
                        tag=f"{wnd}_{key}_slide",
                    )
        dpg.move_item_down("output")
        pipeline[wnd] = {"filter_type": filter_type, "params": params}
    debounce_process()


dpg.create_viewport(title="Filter Pipeline Builder", width=img_w + 600, height=img_h)
with dpg.font_registry():
    big_font = dpg.add_font("C:/Windows/Fonts/segoeui.ttf", 40)  # Path for Windows default font
dpg.bind_font(big_font)
with dpg.texture_registry():
    dpg.add_raw_texture(
        img_w,
        img_h,
        (img_init.astype(np.float32) / 255.0).flatten(),
        tag="processed_texture",
        format=dpg.mvFormat_Float_rgb,
    )
with dpg.window(
    label="Image",
    width=img_w,
    height=img_h,
    pos=(600, 0),
    no_title_bar=True,
    no_move=True,
    no_resize=True,
):
    dpg.add_image("processed_texture")
with dpg.window(
    label="Filters",
    width=600,
    height=img_h,
    pos=(0, 0),
    no_title_bar=True,
    no_move=True,
    no_resize=True,
):
    with dpg.group(horizontal=True):
        dpg.add_text("Add")
        dpg.add_combo(list(FILTERS.keys()), callback=lambda s, a: add_filter(a))
        dpg.add_button(label="Clear", callback=lambda: clear_pipeline())
    with dpg.child_window(autosize_y=True, width=-1, tag="list"):
        with dpg.child_window(
            autosize_x=True, auto_resize_y=True, drop_callback=on_drop, tag="output"
        ) as wnd:
            with dpg.collapsing_header(label=f"Output", default_open=False):
                pass
            pipeline[dpg.get_alias_id(wnd)] = {"filter_type": "Output", "params": {"color": "RGB"}}
dpg.setup_dearpygui()
dpg.show_viewport()
debounce_process()
dpg.start_dearpygui()
dpg.destroy_context()
# endregion
