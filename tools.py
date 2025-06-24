import dearpygui.dearpygui as dpg


import cv2
import numpy as np

# Load your images
from gui_lib import GUI

print(GUI.MatchMask("top_dlg_mask#(0.360, 0.005, 0.640, 0.035).png"))
exit()
# img1 = cv2.imread("Images/ScreenCaps/00-13-05#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
# img2 = cv2.imread("Images/ScreenCaps/00-13-11#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
# img3 = cv2.imread("Images/ScreenCaps/00-13-18#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
img1 = cv2.imread("Images/ScreenCaps/01-40-22#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
img2 = cv2.imread("Images/ScreenCaps/01-40-31#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
img3 = cv2.imread("Images/ScreenCaps/01-40-36#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
img4 = cv2.imread("Images/ScreenCaps/01-40-39#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
img5 = cv2.imread("Images/ScreenCaps/01-41-14#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
img6 = cv2.imread("Images/ScreenCaps/01-42-58#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)
img7 = cv2.imread("Images/ScreenCaps/01-43-05#(0, 0, 1, 1).png", cv2.IMREAD_COLOR)

# Apply bitwise AND step by step to find intersection
imgs = [img1, img2, img3, img5, img6, img7]  # Check that all images are the same shape
assert all(
    img.shape == imgs[0].shape for img in imgs
), "All images must be the same size and channels"

# Stack all images into shape: (N, H, W) for grayscale or (N, H, W, C) for color
stacked = np.stack(imgs, axis=0)

# Check equality across all images
match_mask = np.all(stacked == stacked[0], axis=0)  # shape: (H, W, 3)
match_mask = np.all(match_mask, axis=-1)  # shape: (H, W)
# If color image: reduce to per-pixel match by checking all channels
result = imgs[0].copy()
result[~match_mask] = [0, 0, 0]
# Crop: keep top 20% and center 80% width
height, width = result.shape[:2]
# Top cnt text....
# left = int(width * 0.36)
# top = int(height * 0.005)
# right = int(width * 0.64)
# bottom = int(height * 0.035)
left = int(width * 0.36)
top = int(height * 0.740)
right = int(width * 0.64)
bottom = int(height * 0.830)

cropped = result[top:bottom, left:right]

# Save or show result
cv2.imwrite("dlg_mask#(0.360, 0.740, 0.640, 0.830).png", cropped)
template_mask = cv2.threshold(cropped, 1, 255, cv2.THRESH_BINARY)[1]

# GUI.CaptureRegion((0.36, 0.005, 0.64, 0.035)).save("dlg_act(0.360, 0.005, 0.640, 0.035).png", "png")
cv2.imshow("Result", template_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()


quit()
dpg.create_context()

is_expanded = {"state": True}


def toggle_section():
    is_expanded["state"] = not is_expanded["state"]
    dpg.configure_item("collapsible_content", show=is_expanded["state"])
    dpg.set_value("toggle_btn", "▼ Collapse" if is_expanded["state"] else "▶ Expand")


# --- Theme: Flat transparent buttons (no default button look)
with dpg.theme() as flat_button_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 0))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 0, 0, 0))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 0, 0, 0))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0)
        dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 4)

# --- Theme: Header background hover effect
with dpg.theme() as header_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (50, 50, 50, 255))  # Default grey
        dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0, 0))

with dpg.theme() as header_hover_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (70, 70, 90, 255))  # Highlight color


def hover_handler(sender, app_data, user_data, *args, **kwargs):
    print(args=(sender, app_data, user_data, args, kwargs))
    dpg.bind_item_theme("header_bg", header_hover_theme)


def unhover_handler(sender, app_data, user_data):
    dpg.bind_item_theme("header_bg", header_theme)


# --- Layout
with dpg.window(label="Styled Collapsing Header", width=440, height=320):

    # Header with background and hover logic
    with dpg.child_window(border=False, autosize_x=True, height=35, tag="header_bg"):
        dpg.bind_item_theme("header_bg", header_theme)

        with dpg.handler_registry():
            dpg.add_item_hover_handler(tag="header_bg", callback=hover_handler)
            # dpg.add_item_("header_bg", callback=unhover_handler)

        with dpg.group(horizontal=True):
            dpg.add_button(label="▼ Collapse", tag="toggle_btn", callback=toggle_section)
            dpg.add_spacer(width=10)
            dpg.add_button(label="Header Button", callback=lambda: print("Header button clicked"))
            dpg.bind_item_theme(dpg.last_item(), flat_button_theme)
            dpg.bind_item_theme("toggle_btn", flat_button_theme)

    dpg.add_spacer(height=-5)  # Gap between header and content

    # Collapsible content with border
    with dpg.child_window(tag="collapsible_content", autosize_x=True, autosize_y=True, border=True):
        dpg.add_text("This is inside the collapsible content.")
        dpg.add_input_text(label="Input something")
        dpg.add_button(label="Another Action")

dpg.create_viewport(title="Final Custom Collapsing Header", width=460, height=340)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
