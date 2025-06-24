import dearpygui.dearpygui as dpg

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
