import math
import os
import sys
import time
import numpy as np
import platform
from contextlib import contextmanager
from pynput import mouse, keyboard
from PIL import Image
import cv2
import glob


folder_dir = "ScreenCaps"
src_dir = "C:/Users/User/Desktop/Programing/DragonFableMacros"
exe_path = "C:/Users/User/Downloads/Evolved DragonFable Launcher/evolved-dragonfable-launcher.exe"


class DF_WIN_API:
    hwnd = None
    _game_area = None
    _win_size = (0, 0, 0, 0)

    def __init__(self):
        from ctypes import windll
        import win32api
        import win32ui
        import win32gui
        import win32process

        DF_WIN_API._dll = windll
        DF_WIN_API._api = win32api
        DF_WIN_API._ui = win32ui
        DF_WIN_API._gui = win32gui
        DF_WIN_API._process = win32process

        try:
            windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_SYSTEM_DPI_AWARE
        except Exception:
            try:
                windll.user32.SetProcessDPIAware()  # Windows 7 fallback
            except Exception:
                pass
        DF_WIN_API.hwnd = DF_WIN_API._gui.FindWindow(
            "Chrome_WidgetWin_1", "Evolved DragonFable Launcher"
        )

    def __del__(self):
        pass

    @staticmethod
    def _GetHWND():
        return DF_WIN_API.hwnd if DF_WIN_API.hwnd != 0 else DF_WIN_API._gui.GetForegroundWindow()

    @staticmethod
    def _GetAllWindows():
        hwnd_list = []

        def enum_window_callback(hwnd, hwnd_list):
            if DF_WIN_API._gui.IsWindowVisible(hwnd):
                hwnd_list.append(
                    {
                        "hwnd": hwnd,
                        "class": DF_WIN_API._gui.GetClassName(hwnd),
                        "text": DF_WIN_API._gui.GetWindowText(hwnd),
                    }
                )

        DF_WIN_API._gui.EnumWindows(enum_window_callback, hwnd_list)
        return hwnd_list

    @staticmethod
    def WindowPosition():  # (left, top, right, bottom)
        return DF_WIN_API._gui.GetWindowRect(DF_WIN_API._GetHWND())[:2]

    @staticmethod
    def MousePosition():
        return DF_WIN_API._api.GetCursorPos()

    @staticmethod
    def MouseClick(pos):
        hwnd = DF_WIN_API._GetHWND()
        pos = DF_WIN_API._gui.ScreenToClient(hwnd, pos)
        if hwnd == 0:
            return
        l_pram = DF_WIN_API._api.MAKELONG(*pos)
        DF_WIN_API._gui.PostMessage(hwnd, 513, 1, l_pram)
        DF_WIN_API._gui.PostMessage(hwnd, 514, 1, l_pram)

    @staticmethod
    def TypeKey(key: str):
        hwnd = DF_WIN_API._GetHWND()
        if hwnd == 0:
            return
        # Window Keypress Messages are only processed by 'active' windows,
        # this allows us to 'ACTIVATE' the window so it processes our message
        # All without causing seizers..... its a hack
        DF_WIN_API._api.PostMessage(hwnd, 6, 1, 0)  # WM__ACTIVATE, WA_ACTIVE
        char_id = ord(key.lower())
        DF_WIN_API._api.PostMessage(hwnd, 256, char_id, 0)  # WM_KEYDOWN
        DF_WIN_API._api.PostMessage(hwnd, 257, char_id, 0)  # WM_KEYUP

    @contextmanager
    @staticmethod
    def _MakeDC(hwnd=None):
        if hwnd is None:
            hwnd = DF_WIN_API._GetHWND()
        hdc = DF_WIN_API._gui.GetWindowDC(hwnd)
        dcObj = DF_WIN_API._ui.CreateDCFromHandle(hdc)
        try:
            yield (hdc, dcObj)
        finally:
            dcObj.DeleteDC()
            DF_WIN_API._gui.ReleaseDC(hwnd, hdc)

    @staticmethod
    def WindowCapture():
        wH = DF_WIN_API._GetHWND()
        if wH == 0:
            return None
        l, t, r, b = DF_WIN_API._gui.GetWindowRect(DF_WIN_API._GetHWND())
        w, h = r - l, b - t
        with DF_WIN_API._MakeDC(wH) as (_, dcObj):
            saveDC = dcObj.CreateCompatibleDC()
            saveBitMap = DF_WIN_API._ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(dcObj, w, h)

            saveDC.SelectObject(saveBitMap)
            DF_WIN_API._dll.user32.PrintWindow(wH, saveDC.GetSafeHdc(), 2)
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            bmpsize = (bmpinfo["bmWidth"], bmpinfo["bmHeight"])
            im = Image.frombuffer("RGB", bmpsize, bmpstr, "raw", "BGRX", 0, 1)
            DF_WIN_API._gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            return im

    @staticmethod
    def DrawDebug(area, color):
        with DF_WIN_API._MakeDC(DF_WIN_API._gui.GetActiveWindow()) as (hdc, dcObj):
            # Create a brush or pen and draw a rectangle
            if len(area) != 2:
                pen = DF_WIN_API._ui.CreatePen(0, 3, color)
                dcObj.SelectObject(pen)
                DF_WIN_API._gui.SelectObject(hdc, DF_WIN_API._gui.GetStockObject(5))
                dcObj.Rectangle(area)
            else:
                try:
                    dcObj.SetPixel(*area, color)
                except:
                    pass

    @staticmethod
    def ColorFromRGB(r, g, b):
        return int(f"{b:02x}{g:02x}{r:02x}", 16)

    @staticmethod
    def ColorFromHex(hex):
        hex = hex.lstrip("#")
        if len(hex) == 3:
            return DF_WIN_API.ColorFromRGB(*(int(c * 2, 16) for c in hex))
        return DF_WIN_API.ColorFromRGB(int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16))

    @staticmethod
    def GetGameSize():
        same_size = DF_WIN_API._win_size == DF_WIN_API._gui.GetWindowRect(DF_WIN_API._GetHWND())
        if DF_WIN_API._game_area is not None and same_size:
            return DF_WIN_API._game_area
        DF_WIN_API._win_size = DF_WIN_API._gui.GetWindowRect(DF_WIN_API._GetHWND())
        img = np.array(DF_GUI.API.WindowCapture())
        h, w, _ = img.shape
        red_mask = np.linalg.norm(img - np.array((102, 0, 0)), axis=2) < 10
        mid_x = w // 2
        mid_y = h // 2

        # Find transitions in mask: red → non-red on each edge
        def find_boundary_line(line, from_start=True):
            if not np.any(line):  # No red pixels at all
                return 0 if from_start else len(line)
            if not from_start:
                line = line[::-1]
            r_idx = np.where(line)[0][0]
            idx = (int)(np.where(~line[r_idx:])[0][0] + r_idx)
            return idx if from_start else len(line) - idx

        left = find_boundary_line(red_mask[mid_y, :], from_start=True)
        right = find_boundary_line(red_mask[mid_y, :], from_start=False)
        top = find_boundary_line(red_mask[:, mid_x], from_start=True)
        if top == 0:
            top = find_boundary_line(
                (np.linalg.norm(img - np.array((243, 243, 243)), axis=2) < 10)[:, mid_x],
                from_start=True,
            )
        bottom = find_boundary_line(red_mask[:, mid_x], from_start=False)
        DF_WIN_API._game_area = (left, top, right, bottom)
        return DF_WIN_API._game_area


class DF_NYI_API:
    def __init__(self):
        pass

    def __del__(self):
        pass

    @staticmethod
    def WindowPosition():  # (left, top, right, bottom)
        raise NotImplementedError("WindowPosition not implemented")

    @staticmethod
    def MousePosition():
        raise NotImplementedError("MousePosition not implemented")

    @staticmethod
    def MouseClick(pos):
        raise NotImplementedError("MouseClick not implemented")

    @staticmethod
    def TypeKey(key):
        raise NotImplementedError("TypeKey not implemented")

    @staticmethod
    def WindowCapture():
        raise NotImplementedError("WindowCapture not implemented")

    @staticmethod
    def AbsGameRegion():
        raise NotImplementedError("AbsGameRegion not implemented")

    @staticmethod
    def DrawDebug(area, color):
        raise NotImplementedError("DrawDebug not implemented")

    @staticmethod
    def ColorFromRGB(r, g, b):
        raise NotImplementedError("ColorFromRGB not implemented")

    @staticmethod
    def ColorFromHex(hex):
        raise NotImplementedError("ColorFromHex not implemented")

    @staticmethod
    def GetGameSize():
        raise NotImplementedError("GetGameSize not implemented")


class DF_GUI:
    API: DF_WIN_API = (
        {
            "Windows": DF_WIN_API,
            "Darwin": DF_NYI_API,
            "Linux": DF_NYI_API,
        }.get(platform.system(), DF_NYI_API)
    )()

    @staticmethod
    def MousePosition():
        return UTILS.ToRatio(DF_GUI.API.MousePosition())

    @staticmethod
    def CaptureRegion(area):
        return DF_GUI.API.WindowCapture().crop(UTILS.ToRelative(area))

    @staticmethod
    def CheckImage(path, precision=0.8):
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
        im = DF_GUI.API.WindowCapture().crop(UTILS.ToRelative(expanded_area))
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
                if DF_GUI.CheckImage(path):
                    return path
            time.sleep(interval)
        for path in paths:
            if DF_GUI.CheckImage(path):
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
                if not DF_GUI.CheckImage(path):
                    return path
            time.sleep(interval)
        for path in paths:
            if not DF_GUI.CheckImage(path):
                return path
        return None

    @staticmethod
    def ClickIf(path, timeout=3, interval=0.01):
        if DF_GUI.AwaitImg(path, timeout=timeout, interval=interval) is not None:
            DF_GUI.MouseClick(UTILS.MidPt(UTILS.AreaFromPath(path)))
            return True
        return False

    @staticmethod
    def MouseClick(pos):
        DF_GUI.API.MouseClick(UTILS.ToAbsolute(pos))

    @staticmethod
    def TypeKeys(keys, interval=0.01):
        DF_GUI.API.TypeKey(keys[0])
        for key in keys[1:]:
            time.sleep(interval)
            DF_GUI.API.TypeKey(key)

    @staticmethod
    def DrawGizmo(area, color="#94d6fe"):  # NOTE COLOR IS IN BGR SPACE
        DF_GUI.API.DrawDebug(UTILS.ToAbsolute(area), DF_GUI.API.ColorFromHex(color))

    @staticmethod
    def DrawDebugGrid():
        DF_GUI.DrawGizmo((0, 0, 1, 1))
        for y in np.linspace(0, 1, 101):
            for x in np.linspace(0, 1, 101):
                DF_GUI.DrawGizmo((x, y), "#FF0")


class UTILS:
    @staticmethod
    def ToRatio(area):
        pos = DF_GUI.API.WindowPosition()
        reg = DF_GUI.API.GetGameSize()
        convert = lambda i, val: (val - (reg[i % 2] + pos[i % 2])) / (reg[i % 2 + 2] - reg[i % 2])
        return tuple(round(convert(i, val), 3) for i, val in enumerate(area))

    @staticmethod
    def ToAbsolute(ratio):
        pos = DF_GUI.API.WindowPosition()
        reg = DF_GUI.API.GetGameSize()
        convert = lambda i, val: pos[i % 2] + reg[i % 2] + val * (reg[i % 2 + 2] - reg[i % 2])
        return tuple(round(convert(i, val)) for i, val in enumerate(ratio))

    @staticmethod
    def ToRelative(ratio):
        reg = DF_GUI.API.GetGameSize()
        convert = lambda i, val: reg[i % 2] + val * (reg[i % 2 + 2] - reg[i % 2])
        return tuple(round(convert(i, val)) for i, val in enumerate(ratio))

    @staticmethod
    def MidPt(area):
        if len(area) == 2:
            return round(area[0] + ((area[1] - area[0]) / 2), 3)
        return (
            round(area[0] + (area[2] - area[0]) / 2, 3),
            round(area[1] + (area[3] - area[1]) / 2, 3),
        )

    @staticmethod
    def OrientateArea(area):
        return (
            min(area[0], area[2]),
            min(area[1], area[3]),
            max(area[0], area[2]),
            max(area[1], area[3]),
        )

    @staticmethod
    def EvenOutArea(area):
        cX, cY = UTILS.MidPt(area)
        xDi = max(cX - area[0], area[2] - cX)
        yDi = max(cY - area[1], area[3] - cY)
        return round(cX - xDi, 3), round(cY - yDi, 3), round(cX + xDi, 3), round(cY + yDi, 3)

    @staticmethod
    def EnsureList(paths):
        return [paths] if isinstance(paths, str) else list(paths)

    @staticmethod
    def AreaFromPath(path):
        coords_str = path.split("#")[-1].split(")")[0].strip("(")
        return tuple(map(float, coords_str.split(",")))

    @staticmethod
    def AddBuffer(area, padding):
        return (
            max(0.0, area[0] - padding),
            max(0.0, area[1] - padding),
            min(1.0, area[2] + padding),
            min(1.0, area[3] + padding),
        )

    @staticmethod
    def GetSize(area):
        return (area[2] - area[0]), (area[3] - area[1])


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
            print(f"DF_ACT.Sleep({dT})")
        if not HANDLERS.alt_pressed:
            pos = DF_GUI.MousePosition()
            print(f"DF_ACT.MouseClick({pos})")
            DF_GUI.DrawGizmo(pos)

    @staticmethod
    def on_right_click(pressed):
        if pressed:
            HANDLERS.prev = DF_GUI.MousePosition()
            return
        curr = DF_GUI.MousePosition()
        if abs(HANDLERS.prev[0] - curr[0]) + abs(HANDLERS.prev[1] - curr[1]) < 0.004:
            if HANDLERS.alt_pressed:
                HANDLERS.startT = time.time()
            return
        area = UTILS.OrientateArea((*HANDLERS.prev, *curr))
        area = UTILS.EvenOutArea(area)
        area = (area[0] + 0.002, area[1] + 0.002, area[2] - 0.002, area[3] - 0.002)
        DF_GUI.CaptureRegion(area).save(f"{folder_dir}/#{area}.png", "png")
        DF_GUI.DrawGizmo(area)
        dT = round(time.time() - HANDLERS.startT, 3)
        if not HANDLERS.alt_pressed:
            print(f'DF_ACT.ClickIf("{folder_dir}/#{area}.png", timeout={2 * dT}))')
            DF_GUI.MouseClick(UTILS.MidPt(area))
            time.sleep(0.05)
            if platform.system() == "Windows":
                DF_WIN_API._api.PostMessage(DF_WIN_API._GetHWND(), 31, 0, 0)
        else:
            print(f'DF_ACT.AwaitImg("{folder_dir}/#{area}.png", timeout={2 * dT})')
        HANDLERS.startT = time.time()

    @staticmethod
    def on_click(_x, _y, button, pressed):
        """
        |ACTION\MODS|     NONE      |     SHIFT     |      ALT      |     CTRL      |
        |:---------:|:-------------:|:-------------:|:-------------:|:-------------:|
        |   Left    |  Sleep&Click  |               |     Sleep     |               |
        |   Right   |               |               |Reset Sleep Cnt|               |
        |   RDrag   | ClickIf Image |    AwaitImg   |               |               |
        |   Middle  | Capture Game  |               |               |               |
        """
        """     
        |  ADVANCE  |   CTRL-SHFT   |   ALT-SHIFT   |    CTRL-ALT   | CTRL-ALT-SHFT |
        |:---------:|:-------------:|:-------------:|:-------------:|:-------------:|
        |   Left    |               |               |               |               |
        |   Right   |               |               |               |               |
        |   RDrag   |               |               |               |               |
        |   Middle  |               |               |               |               |
        """
        if button == mouse.Button.left:
            HANDLERS.on_left_click(pressed)
        elif button == mouse.Button.right:
            HANDLERS.on_right_click(pressed)
        elif button == mouse.Button.middle and pressed:
            print("Screen Captured")
            DF_GUI.CaptureRegion((0, 0, 1, 1)).save(f"{folder_dir}/{time.time()}#{(0,0,1,1)}.png")

    @staticmethod
    def on_move(x, y):
        if x < 10 and y < 10:
            HANDLERS.keyboard_listener.stop()
            HANDLERS.mouse_listener.stop()

    @staticmethod
    def on_press(key):
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
        elif isinstance(key, keyboard.KeyCode):
            if key.char == "q":
                HANDLERS.keyboard_listener.stop()
                HANDLERS.mouse_listener.stop()
            elif key.char in ascii_map:
                print(f'DF_ACT.Battle_Mooks({"ChaosWeaver"}, {ascii_map[key.char]})')
                DF_ACT.Battle_Mooks("ChaosWeaver", ascii_map[key.char])
            else:
                print(f"DF_ACT.TypeKeys({key.char})")

    @staticmethod
    def on_release(key):
        if key in {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r}:
            HANDLERS.alt_pressed = False
        elif key in {keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r}:
            HANDLERS.shift_pressed = False


class DF_ACT:
    @staticmethod
    def AwaitImg(*paths, timeout=3, interval=0.01):
        return DF_GUI.AwaitImg(*paths, timeout=timeout, interval=interval)

    @staticmethod
    def AwaitNotImg(*paths, timeout=3, interval=0.01):
        return DF_GUI.AwaitNotImg(*paths, timeout=timeout, interval=interval)

    @staticmethod
    def ClickIf(path, timeout=3, interval=0.01):
        return DF_GUI.ClickIf(path, timeout=timeout, interval=interval)

    @staticmethod
    def MouseClick(pos):
        return DF_GUI.MouseClick(pos)

    @staticmethod
    def TypeKeys(keys, interval=0.01):
        return DF_GUI.TypeKeys(keys, interval=interval)

    @staticmethod
    def Sleep(secs):
        time.sleep(secs)

    @staticmethod
    def Battle(player_moves, pet_moves, endConditions=[], cyclical=False):
        player_moves = list(player_moves)
        pet_moves = list(pet_moves)
        while True:
            DF_GUI.AwaitImg(DF_ACT.atkBtn, DF_ACT.ctnBtn, *endConditions, DF_ACT.stkBtn, timeout=-1)
            if any(DF_GUI.CheckImage(i) for i in endConditions):
                return filter(DF_GUI.CheckImage, endConditions)[0]
            elif DF_GUI.CheckImage(DF_ACT.atkBtn):
                if DF_GUI.CheckImage(DF_ACT.petBtn):
                    move = pet_moves.pop(0) if pet_moves else " "
                else:
                    move = player_moves.pop(0) if player_moves else " "
                DF_GUI.TypeKeys(move)
                DF_GUI.AwaitNotImg(DF_ACT.atkBtn)
            elif DF_GUI.CheckImage(DF_ACT.ctnBtn):
                DF_GUI.TypeKeys(" ")
                DF_GUI.AwaitImg(DF_ACT.noOverlay, timeout=1)
                return DF_ACT.ctnBtn
            else:
                DF_GUI.ClickIf(DF_ACT.stkBtn, timeout=0)

    @staticmethod
    def Battle_Mooks(className, count=1):
        if className == "ChaosWeaver":
            return DF_ACT.Battle("487", "78")
        return DF_ACT.Battle("487", "78")

    @staticmethod
    def BattleWar(startBtn: str, waves: list, counts: list, className="ChaosWeaver"):
        print(f"Starting Waves of {os.path.basename(sys._getframe(1).f_code.co_filename)} war")
        num = 0
        while DF_GUI.ClickIf(startBtn, timeout=20):
            wave = DF_GUI.AwaitImg(*waves, timeout=20)
            if wave is None:
                return
            idx = waves.index(wave)
            cnts = counts[idx][:]
            print(f"\rStarting wave #{(num := num + 1)} ({num+1325})", end="", flush=True)
            while True:
                DF_ACT.MoveInDirection(wave.split("/")[-1])
                DF_GUI.AwaitImg(DF_ACT.atkBtn, DF_ACT.questPass)  # DF_ACT.questFail,
                if DF_GUI.CheckImage(DF_ACT.atkBtn):
                    DF_ACT.Battle_Mooks(className, cnts.pop() if len(cnts) > 1 else cnts[0])
                elif DF_GUI.CheckImage(DF_ACT.questPass):
                    DF_GUI.ClickIf(DF_ACT.questClose)
                    DF_GUI.AwaitImg(DF_ACT.newItem)
                    DF_GUI.ClickIf(DF_ACT.keepItem)
                    break
            # elif DF_GUI.CheckImage(DF_ACT.questFail):
            #     pass
            # else:
            #     pass

    @staticmethod
    def MoveInDirection(direction):
        if direction.lower()[0] == "n":
            DF_GUI.MouseClick((0.5, 0.003))
        elif direction.lower()[0] == "s":
            DF_GUI.MouseClick((0.5, 0.81))
        elif direction.lower()[0] == "e":
            DF_GUI.MouseClick((0.99, 0.578))
        elif direction.lower()[0] == "w":
            DF_GUI.MouseClick((0.01, 0.69))

    @staticmethod
    def Setup():
        print("Running Setup...")
        os.chdir(f"{src_dir}/Images")

        def FetchImg(name):
            return glob.glob(f"./{name}*.png")[0]

        DF_ACT.atkBtn = FetchImg("atkBtn")
        DF_ACT.ctnBtn = FetchImg("ctnBtn")
        DF_ACT.stkBtn = FetchImg("atkBtn")
        DF_ACT.petBtn = FetchImg("petBtn")
        DF_ACT.questPass = FetchImg("questPass")
        DF_ACT.questClose = FetchImg("questClose")
        DF_ACT.newItem = FetchImg("newItem")
        DF_ACT.noOverlay = FetchImg("noOverlay")
        DF_ACT.keepItem = FetchImg("KeepItem")

        def debug_mouse(_, y, b, p):
            if y >= 2050 and b == mouse.Button.middle and p:
                __import__("traceback").print_stack(list(sys._current_frames().values())[-1])
                DF_GUI.CaptureRegion((0, 0, 1, 1)).save(f"{folder_dir}/trace.png")

        debug = mouse.Listener(on_click=debug_mouse)
        debug.daemon = True
        debug.start()


DF_ACT.Setup()

if __name__ == "__main__":
    HANDLERS.keyboard_listener = keyboard.Listener(
        on_press=HANDLERS.on_press, on_release=HANDLERS.on_release
    )
    HANDLERS.mouse_listener = mouse.Listener(on_click=HANDLERS.on_click, on_move=HANDLERS.on_move)
    HANDLERS.keyboard_listener.start()
    HANDLERS.keyboard_listener.deamon = True
    HANDLERS.mouse_listener.start()
    # DF_GUI.DrawDebugGrid()
    HANDLERS.mouse_listener.join()
