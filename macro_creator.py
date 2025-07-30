import time
import platform
from pynput import mouse, keyboard

from Macro.utils import UTILS
from actions import ACT
from Macro.gui_lib import GUI, folder_dir


class HANDLERS:
    startT = time.time()
    prev = (0, 0)
    alt_pressed = False
    shift_pressed = False
    keyboard_listener = None
    mouse_listener = None

    @staticmethod
    def on_left_click(pressed):
        if pressed:
            return
        if HANDLERS.startT is None:
            HANDLERS.startT = time.time()
        else:
            dT = round(time.time() - HANDLERS.startT, 3)
            HANDLERS.startT = time.time()
            print(f"ACT.Sleep({dT})")
        pos = GUI.MousePosition()
        print(f"ACT.MouseClick({pos})")
        if HANDLERS.alt_pressed:
            print(f'ACT.Battle("ChaosWeaver", 1)')
            ACT.Battle("ChaosWeaver", 1)
            HANDLERS.startT = time.time()
            GUI.MouseClick(pos)
            print(f"ACT.MouseClick({pos})")

    @staticmethod
    def on_right_click(pressed):
        if pressed:
            HANDLERS.prev = GUI.MousePosition()
            return
        curr = GUI.MousePosition()
        if abs(HANDLERS.prev[0] - curr[0]) + abs(HANDLERS.prev[1] - curr[1]) < 0.004:
            if HANDLERS.alt_pressed:
                HANDLERS.startT = time.time()
            return
        area = UTILS.OrientateArea((*HANDLERS.prev, *curr))
        area = UTILS.EvenOutArea(area)
        area = (area[0] + 0.002, area[1] + 0.002, area[2] - 0.002, area[3] - 0.002)
        GUI.SaveRegion(area)
        dT = round(time.time() - HANDLERS.startT, 3)
        area_str = "(" + ", ".join(f"{x:.3f}" for x in area) + ")"
        if not HANDLERS.alt_pressed:
            print(f'ACT.ClickIf("../{folder_dir}/#{area_str}.png", timeout={2 * dT})')
            GUI.MouseClick(UTILS.MidPt(area))
            time.sleep(0.05)
            if platform.system() == "Windows":  # What did this do again?
                from Macro.api_lib import _WIN_API

                _WIN_API._api.PostMessage(_WIN_API._GetHWND(), 31, 0, 0)
        else:
            print(f'ACT.AwaitImg("../{folder_dir}/#{area_str}.png", timeout={2 * dT})')
        HANDLERS.startT = time.time()

    @staticmethod
    def on_click(_x, _y, button, pressed):
        """
        |ACTION\\MODS|     NONE      |     SHIFT     |      ALT      |     CTRL      |
        |:---------:|:-------------:|:-------------:|:-------------:|:-------------:|
        |   Left    |  Sleep&Click  |               |ClickBattleClick|               |
        |   Right   |               |               |Reset Sleep Cnt|               |
        |   RDrag   | ClickIf Image |    AwaitImg   |               |               |
        |   Middle  | Capture Game  |               |               |               |
        """
        # |  ADVANCE  |   CTRL-SHFT   |   ALT-SHIFT   |    CTRL-ALT   | CTRL-ALT-SHFT |
        # |:---------:|:-------------:|:-------------:|:-------------:|:-------------:|
        # |   Left    |               |               |               |               |
        # |   Right   |               |               |               |               |
        # |   RDrag   |               |               |               |               |
        # |   Middle  |               |               |               |               |
        if button == mouse.Button.left:
            HANDLERS.on_left_click(pressed)
        elif button == mouse.Button.right:
            HANDLERS.on_right_click(pressed)
        elif button == mouse.Button.middle and pressed:
            print("Screen Captured")
            GUI.SaveRegion((0, 0, 1, 1), time.strftime("%H-%M-%S"))

    @staticmethod
    def on_move(x, y):
        if x < 10 and y < 10:
            HANDLERS.keyboard_listener.stop()
            HANDLERS.mouse_listener.stop()

    @staticmethod
    def on_press(key):
        # Add support for quitting with ctrl-c
        ascii_map = {
            "!": "1",
            "@": "2",
            "#": "3",
            "$": "4",
            "%": "5",
            "^": "6",
            "&": "7",
            "*": "8",
            "(": "9",
            ")": "0",
        }
        if key in {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r}:
            HANDLERS.alt_pressed = True
        elif key in {keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r}:
            HANDLERS.shift_pressed = True
        elif key in {keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r}:
            HANDLERS.ctrl_pressed = True
        elif isinstance(key, keyboard.KeyCode):
            if key.char == "q" or key.char == "\x03":
                HANDLERS.keyboard_listener.stop()
                HANDLERS.mouse_listener.stop()
            elif key.char in ascii_map:
                print(f'ACT.Battle({"ChaosWeaver"}, {ascii_map[key.char]})')
                ACT.Battle("ChaosWeaver", ascii_map[key.char])
            else:
                print(f"ACT.TypeKeys({key.char})")

    @staticmethod
    def on_release(key):
        if key in {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r}:
            HANDLERS.alt_pressed = False
        elif key in {keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r}:
            HANDLERS.shift_pressed = False
        elif key in {keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r}:
            HANDLERS.ctrl_pressed = False


if __name__ == "__main__":
    HANDLERS.keyboard_listener = keyboard.Listener(
        on_press=HANDLERS.on_press, on_release=HANDLERS.on_release
    )
    # import quests

    # quests.DarkTower()
    # print("Dark Tower Quest Done")
    GUI.MouseClick((0.9, 0.9))
    print("Mouse Clicked at (0.9, 0.9)", flush=True)
    HANDLERS.mouse_listener = mouse.Listener(on_click=HANDLERS.on_click, on_move=HANDLERS.on_move)
    HANDLERS.keyboard_listener.start()
    HANDLERS.keyboard_listener.deamon = True
    HANDLERS.mouse_listener.start()
    GUI.DrawDebugGrid()
    HANDLERS.mouse_listener.join()
    time.sleep(0.1)
