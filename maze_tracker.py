from ctypes import windll

windll.shcore.SetProcessDpiAwareness(2)
import dearpygui.dearpygui as dpg

MAZE_SIZE = 10

pos_x, pos_y = 0, 0
old_pos_x, old_pos_y = pos_x, pos_y

DIRS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}

maze = {}
# maze[(pos_x, pos_y)] = {"char": " ", "events": set(), "explored": True}

tile_conn = {
    "╋": {"N", "E", "S", "W"},
    "┫": {"N", "S", "W"},
    "┣": {"N", "S", "E"},
    "┳": {"S", "E", "W"},
    "┻": {"N", "E", "W"},
    "┃": {"N", "S"},
    "━": {"E", "W"},
    "┏": {"S", "E"},
    "┓": {"S", "W"},
    "┗": {"N", "E"},
    "┛": {"N", "W"},
    " ": {"N", "E", "S", "W"},
    "╸": {"W"},
    "╺": {"E"},
    "╹": {"N"},
    "╻": {"S"},
}

dpg.create_context()
with dpg.theme() as grid_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)
        dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, 0, 0)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, -34)
        dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5, 0.5)
        dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0, 0))
        dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)

with dpg.theme() as border_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 3.0)
        dpg.add_theme_color(dpg.mvThemeCol_Border, (255, 0, 0, 255))

with dpg.theme() as circle_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 3.0)
        dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 128, 64, 255))

with dpg.theme() as evnt_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, -4)


def refresh_grid():
    for y in range(MAZE_SIZE):
        for x in range(MAZE_SIZE):
            key = (x, y)
            tile = maze.get(key)
            theme = 0
            if key == (pos_x, pos_y):
                theme = border_theme
            else:
                theme = grid_theme
            if tile:
                label = tile["char"]
                if "⊛" in tile["events"]:
                    theme = circle_theme
            else:
                label = " "
            dpg.set_item_label(f"cell_{x}_{y}", label)
            dpg.bind_item_theme(f"cell_{x}_{y}", theme)


def set_tile(sender, app_data, user_data):
    global maze, pos_x, pos_y
    maze[(pos_x, pos_y)] = {"char": user_data, "events": set(), "links": tile_conn.get(user_data)}
    if user_data == " ":
        del maze[(pos_x, pos_y)]
    refresh_grid()


def trigger_event(sender, app_data, user_data):
    from actions import ACT

    global maze, pos_x, pos_y, old_pos_x, old_pos_y
    tile = maze.get((pos_x, pos_y))
    if not tile:
        return
    events = tile["events"]
    if user_data in events:
        events.remove(user_data)
        print(f"Removed circle")
    elif user_data == "⊛":
        events.add(user_data)
        print(f"Marked circle")
    elif user_data == "·":
        ACT.MouseClick((0.512, 0.512))
    elif user_data == "⚠":
        ACT.MouseClick((0.512, 0.592))
        ACT.Sleep(0.1)
        ACT.MouseClick((0.5, 0.5))
        ACT.Battle("ChaosWeaver", ("3 6v", "78"))
        ACT.MouseClick((0.512, 0.592))
        if sender == 0 and app_data == 0:
            trigger_event(sender, app_data, "a")
    elif user_data == "a":
        possibilities = list(tile["links"].copy())
        for dir, delta in DIRS.items():
            if delta == (old_pos_x - pos_x, old_pos_y - pos_y):
                possibilities.remove(dir)
        if len(possibilities) == 1:
            move_player(sender, app_data, possibilities[0])
    elif user_data == "◌":
        ACT.MouseClick((0.512, 0.592))
        ACT.Sleep(0.1)
        ACT.MouseClick((0.5, 0.5))  # Drag is: 0,200,200,200,0
        ACT.Battle("ChaosWeaver", ("49tv0", "978"))
        ACT.MouseClick((0.512, 0.592))
    refresh_grid()


def move_player(sender, app_data, user_data):
    global pos_x, pos_y, old_pos_x, old_pos_y
    dx, dy = DIRS[user_data]
    nx, ny = pos_x + dx, pos_y + dy
    if 0 <= nx < MAZE_SIZE and 0 <= ny < MAZE_SIZE:
        old_tile = maze.get((pos_x, pos_y))
        if old_tile:
            if user_data in old_tile.get("links"):
                old_pos_x, old_pos_y = pos_x, pos_y
                pos_x, pos_y = nx, ny
                if "⊛" in old_tile["events"]:
                    print(f"Circle {user_data}")
                else:
                    from actions import ACT

                    if user_data.lower()[0] == "n":
                        ACT.MouseClick((0.5, 0.03))
                    elif user_data.lower()[0] == "s":
                        ACT.MouseClick((0.5, 0.81))
                    elif user_data.lower()[0] == "e":
                        ACT.MouseClick((0.98, 0.58))
                    elif user_data.lower()[0] == "w":
                        ACT.MouseClick((0.01, 0.58))
                refresh_grid()
            else:
                print(f"Can't move {user_data} hits a wall")
        else:
            print("Please mark the current tile before moving on")
    else:
        print(f"Cannot move {user_data} outside maze boundaries")


def on_key_press(sender, app_data):
    movement_keybinds = {dpg.mvKey_W: "N", dpg.mvKey_A: "W", dpg.mvKey_S: "S", dpg.mvKey_D: "E"}
    event_keybinds = {
        dpg.mvKey_Spacebar: "⚠",
        627: "⚠",
        625: "⊛",
        525: "·",
        623: "◌",
        dpg.mvKey_Decimal: "a",
    }  # *624
    set_tile_keybinds = {
        dpg.mvKey_NumPad7: "┏",
        dpg.mvKey_NumPad8: "┳",
        dpg.mvKey_NumPad9: "┓",
        dpg.mvKey_NumPad4: "┣",
        dpg.mvKey_NumPad5: "╋",
        dpg.mvKey_NumPad6: "┫",
        dpg.mvKey_NumPad1: "┗",
        dpg.mvKey_NumPad2: "┻",
        dpg.mvKey_NumPad3: "┛",
        dpg.mvKey_NumPad0: "━",
        626: "┃",
        624: " ",
    }
    tile_or_move_keybinds = {
        dpg.mvKey_Up: ("N", "╻"),
        dpg.mvKey_Left: ("W", "╺"),
        dpg.mvKey_Down: ("S", "╹"),
        dpg.mvKey_Right: ("E", "╸"),
    }

    def move_or_tile(a, b, v):
        if (pos_x, pos_y) in maze:
            move_player(a, b, v[0])
        else:
            set_tile(a, b, v[1])

    keybinds_function_map = [
        (movement_keybinds, move_player),
        (set_tile_keybinds, set_tile),
        (event_keybinds, trigger_event),
        (tile_or_move_keybinds, move_or_tile),
    ]
    for keybinds, func in keybinds_function_map:
        for k, v in keybinds.items():
            if app_data == k:
                return func(0, 0, v)
    if app_data != 655:
        print(app_data)


with dpg.handler_registry():
    dpg.add_key_press_handler(callback=on_key_press, parent="main_window")

size = 60
with dpg.font_registry():
    with dpg.font("./JetBrainsMonoNL-Regular.ttf", 128) as unicode_font:
        # Add extra unicode ranges for box drawing and symbols
        dpg.add_font_range(0x2190, 0x21FF)  # Arrows
        dpg.add_font_range(0x2200, 0x22FF)  # Math Operators (⊙ etc.)
        dpg.add_font_range(0x2300, 0x23FF)  # Misc Technical (· etc.)
        dpg.add_font_range(0x2500, 0x259F)  # Box/Block Elements
        dpg.add_font_range(0x25A0, 0x25FF)  # Geometric Shapes (● ◎ ◉ ⊙)
        dpg.add_font_range(0x2600, 0x26FF)  # Miscellaneous Symbols (☀ ⚔ ⛃ ⛩ ⚙ etc.)
        dpg.add_font_range(0x2700, 0x27BF)  # Dingbats (✓ ✔ ✘ ✦ etc.)
        dpg.add_font_range(0x2B00, 0x2BFF)  # Misc Symbols & Arrows (⮞ ⮌ etc.)
        dpg.bind_font(unicode_font)
    with dpg.font("./JetBrainsMonoNL-Regular.ttf", 64) as unicode_font_small:
        dpg.add_font_range(0x2190, 0x2BFF)

# TODO: Allow non 10x10 grids
# TODO: Allow a start besides 0,0 ie allow -/- coords
dpg.create_viewport(title="Maze Tracker", width=(10 * size) + 50, height=17 * size)
with dpg.window(
    label="main_window",
    width=(10 * size) + 20,
    height=1200,
    pos=(0, 0),
    no_title_bar=True,
    no_move=True,
    no_resize=True,
):
    dpg.bind_theme(grid_theme)
    with dpg.group(horizontal=False):

        def c(_a, _b, pos):
            global pos_x, pos_y, old_pos_x, old_pos_y
            old_pos_x, old_pos_y = pos
            pos_x, pos_y = pos
            refresh_grid()

        for y in range(MAZE_SIZE):
            with dpg.group(horizontal=True):
                for x in range(MAZE_SIZE):
                    dpg.add_button(
                        label="",
                        width=size,
                        height=size,
                        tag=f"cell_{x}_{y}",
                        user_data=(x, y),
                        callback=c,
                    )
    with dpg.group(horizontal=True, tag="div"):
        dpg.bind_item_font("div", unicode_font_small)
        dpg.add_separator(label="CTRLS (0, 0)", tag="ctrls")
    for i, line in enumerate("┏┳┓\n┣╋┫┃\n┗┻┛__╻_\n━ __╺╹╸".split("\n")):  # ╺━╸╻╹
        with dpg.group(horizontal=True):
            for ch in line:
                if ch == "_":
                    dpg.add_spacer(width=size, height=size)
                else:
                    dpg.add_button(
                        label=ch, width=size, height=size, callback=set_tile, user_data=ch
                    )
            if i < len("⚠⊛·◌"):
                v = "⚠⊛·◌"[i]
                dpg.add_spacer(width=(size * (9 - len(line))))
                dpg.add_button(
                    label=v,
                    width=size,
                    height=size,
                    callback=trigger_event,
                    user_data=v,
                    tag=v,
                )
                dpg.bind_item_font(v, unicode_font_small)
                dpg.bind_item_theme(v, evnt_theme)
# ◎◉●◊✓✶⚡

dpg.setup_dearpygui()
dpg.show_viewport()
refresh_grid()
dpg.start_dearpygui()
dpg.destroy_context()
