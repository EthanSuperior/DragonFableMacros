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

img_init = np.array(GUI.CaptureRegion((0, 0, 1, 0.807)).convert("RGB"))
img_h, img_w = img_init.shape[:2]
texture_data = img_init.astype(np.float32) / 255.0


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
}
pipeline = {}

# region --- Debounce
debounce_timer = None


def debounce_process():
    global debounce_timer
    if debounce_timer:
        debounce_timer.cancel()
    debounce_timer = Timer(0.3, process_image)
    debounce_timer.start()


# endregion


# region --- DearPyGui Callbacks
def on_drop(dropped_wnd, dragged_id):
    dragged_wnd = dpg.get_item_parent(dragged_id)
    parent_wnd = dpg.get_item_parent(dropped_wnd)
    if dragged_wnd and dpg.does_item_exist(dragged_wnd):
        dpg.move_item(dragged_wnd, parent=parent_wnd, before=dropped_wnd)


def clear_pipeline():
    for step in pipeline:
        dpg.delete_item(step["id"])
    pipeline.clear()
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


def process_image():
    img = np.array(GUI.CaptureRegion((0, 0, 1, 0.807)).convert("RGB"))
    channels = cv2.split(img)  # Split into R, G, B channels

    processed_channels = []
    for channel in channels:
        channel_gray = cv2.cvtColor(cv2.merge([channel, channel, channel]), cv2.COLOR_BGR2GRAY)

        for id in dpg.get_all_items("filter_list")[1]:
            print(f"Processing step ID: {id}")
            step = pipeline[id]
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


# endregion


# region --- DearPyGui Layout
def add_filter(filter_type="Blur"):
    if filter_type not in FILTERS:
        return
    h_id = dpg.generate_uuid()
    params = FILTERS[filter_type]["params"].copy()

    with dpg.child_window(
        autosize_x=True, auto_resize_y=True, drop_callback=on_drop, parent=filter_list
    ) as wnd:
        with dpg.collapsing_header(label=filter_type, tag=h_id):
            with dpg.drag_payload(drag_data=h_id):
                dpg.add_text("Drag to rearrange before")
            with dpg.group(horizontal=True, parent=h_id):
                # Text inputs for each parameter in header
                for key, val in params.items():
                    input_id = f"{h_id}_{key}_input"
                    dpg.add_input_int(
                        label=f"{key}:",
                        default_value=val,
                        width=180,
                        step=None,
                        callback=lambda s, a, u=h_id, k=key: update_param(u, k, a),
                        tag=input_id,
                    )
            with dpg.group(horizontal=False, parent=h_id):
                # Optional: sliders or more advanced config below the header
                for key, val in params.items():
                    slider_id = f"{h_id}_{key}_slider"
                    dpg.add_slider_int(
                        label=f"{key} (slider)",
                        default_value=val,
                        min_value=1,
                        max_value=100,
                        width=300,
                        callback=lambda s, a, u=h_id, k=key, input_ref=f"{h_id}_{key}_input": sync_input_and_update(
                            u, k, a, input_ref
                        ),
                        tag=slider_id,
                    )
    pipeline[h_id] = {"id": h_id, "filter_type": filter_type, "params": params}

    dpg.move_item(wnd, parent=filter_list, before="output")
    debounce_process()


with dpg.window(label="Filters", width=400, height=img_h, pos=(0, 0), no_title_bar=True):
    with dpg.group(horizontal=True):
        dpg.add_text("Add Filter")
        dpg.add_combo(list(FILTERS.keys()), callback=lambda s, a: add_filter(a))
        dpg.add_button(label="Clear", callback=lambda: clear_pipeline())
    filter_list = dpg.add_child_window(height=img_h - 180, width=-1, tag="filter_list")

    h_id = dpg.generate_uuid()
    with dpg.child_window(
        autosize_x=True, auto_resize_y=True, drop_callback=on_drop, parent=filter_list, tag="output"
    ):
        with dpg.collapsing_header(label=f"Output", tag=h_id, default_open=False):
            dpg.add_text("This is inside the collapsible content.")
            dpg.add_input_text(label="Input something")
            dpg.add_button(label="Another Action")

dpg.create_viewport(title="Filter Pipeline Builder", width=img_w + 400, height=max(img_h, 720))
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
# endregion
