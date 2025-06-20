from abc import ABC, abstractmethod
import numpy as np
import platform
from contextlib import contextmanager
from PIL import Image


class _API(ABC):
    def __init__(self):
        self.SetUp()

    def __del__(self):
        self.CleanUp()

    @staticmethod
    @abstractmethod
    def SetUp():
        pass

    @staticmethod
    @abstractmethod
    def CleanUp():
        pass

    @staticmethod
    @abstractmethod
    def WindowPosition():  # (left, top, right, bottom)
        pass

    @staticmethod
    @abstractmethod
    def MousePosition():
        pass

    @staticmethod
    @abstractmethod
    def MouseClick(pos):
        pass

    @staticmethod
    @abstractmethod
    def TypeKey(key):
        pass

    @staticmethod
    @abstractmethod
    def WindowCapture():
        pass

    @staticmethod
    @abstractmethod
    def GetGameSize():
        pass

    @staticmethod
    @abstractmethod
    def DrawDebug(area, color):
        pass

    @staticmethod
    @abstractmethod
    def ColorFromRGB(r, g, b):
        pass

    @staticmethod
    def ColorFromHex(hex):
        hex = hex.lstrip("#")
        if len(hex) == 3:
            return _WIN_API.ColorFromRGB(*(int(c * 2, 16) for c in hex))
        return _WIN_API.ColorFromRGB(int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16))


class _WIN_API(_API):
    hwnd = None
    _game_area = None
    _win_size = (0, 0, 0, 0)
    _overlay_hwnd = None
    _overlay_class = None

    @staticmethod
    def SetUp():
        from ctypes import windll
        import win32api
        import win32ui
        import win32gui
        import win32process

        _WIN_API._dll = windll
        _WIN_API._api = win32api
        _WIN_API._ui = win32ui
        _WIN_API._gui = win32gui
        _WIN_API._process = win32process

        try:
            windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_SYSTEM_DPI_AWARE
        except Exception:
            try:
                windll.user32.SetProcessDPIAware()  # Windows 7 fallback
            except Exception:
                pass
        _WIN_API.hwnd = _WIN_API._gui.FindWindow(
            "Chrome_WidgetWin_1", "Evolved DragonFable Launcher"
        )

    @staticmethod
    def CleanUp():
        if _WIN_API._overlay_hwnd:
            _WIN_API._gui.DestroyWindow(_WIN_API._overlay_hwnd)
            _WIN_API._overlay_hwnd = None

    @staticmethod
    def _GetHWND():
        return _WIN_API.hwnd if _WIN_API.hwnd != 0 else _WIN_API._gui.GetForegroundWindow()

    @staticmethod
    def _GetAllWindows():
        hwnd_list = []

        def enum_window_callback(hwnd, hwnd_list):
            if _WIN_API._gui.IsWindowVisible(hwnd):
                hwnd_list.append(
                    {
                        "hwnd": hwnd,
                        "class": _WIN_API._gui.GetClassName(hwnd),
                        "text": _WIN_API._gui.GetWindowText(hwnd),
                    }
                )

        _WIN_API._gui.EnumWindows(enum_window_callback, hwnd_list)
        return hwnd_list

    @staticmethod
    def WindowPosition():  # (left, top)
        return _WIN_API._gui.GetWindowRect(_WIN_API._GetHWND())[:2]

    @staticmethod
    def MousePosition():
        return _WIN_API._api.GetCursorPos()

    @staticmethod
    def MouseClick(pos):
        hwnd = _WIN_API._GetHWND()
        pos = _WIN_API._gui.ScreenToClient(hwnd, pos)
        if hwnd == 0:
            return
        l_pram = _WIN_API._api.MAKELONG(*pos)
        _WIN_API._gui.PostMessage(hwnd, 513, 1, l_pram)
        _WIN_API._gui.PostMessage(hwnd, 514, 1, l_pram)

    @staticmethod
    def TypeKey(key: str):
        hwnd = _WIN_API._GetHWND()
        if hwnd == 0:
            return
        # Window Keypress Messages are only processed by 'active' windows,
        # this allows us to 'ACTIVATE' the window so it processes our message
        # All without causing seizers..... its a hack
        _WIN_API._api.PostMessage(hwnd, 6, 1, 0)  # WM__ACTIVATE, WA_ACTIVE
        char_id = ord(key.lower())
        _WIN_API._api.PostMessage(hwnd, 256, char_id, 0)  # WM_KEYDOWN
        _WIN_API._api.PostMessage(hwnd, 257, char_id, 0)  # WM_KEYUP

    @contextmanager
    @staticmethod
    def _MakeDC(hwnd=None):
        if hwnd is None:
            hwnd = _WIN_API._GetHWND()
        hdc = _WIN_API._gui.GetWindowDC(hwnd)
        dcObj = _WIN_API._ui.CreateDCFromHandle(hdc)
        try:
            yield (hdc, dcObj)
        finally:
            dcObj.DeleteDC()
            _WIN_API._gui.ReleaseDC(hwnd, hdc)

    @staticmethod
    def WindowCapture():
        wH = _WIN_API._GetHWND()
        if wH == 0:
            return None
        l, t, r, b = _WIN_API._gui.GetWindowRect(_WIN_API._GetHWND())
        w, h = r - l, b - t
        with _WIN_API._MakeDC(wH) as (_, dcObj):
            saveDC = dcObj.CreateCompatibleDC()
            saveBitMap = _WIN_API._ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(dcObj, w, h)

            saveDC.SelectObject(saveBitMap)
            _WIN_API._dll.user32.PrintWindow(wH, saveDC.GetSafeHdc(), 2)
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            bmpsize = (bmpinfo["bmWidth"], bmpinfo["bmHeight"])
            im = Image.frombuffer("RGB", bmpsize, bmpstr, "raw", "BGRX", 0, 1)
            _WIN_API._gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            return im

    @staticmethod
    def GetGameSize():
        same_size = _WIN_API._win_size == _WIN_API._gui.GetWindowRect(_WIN_API._GetHWND())
        if _WIN_API._game_area is not None and same_size:
            return _WIN_API._game_area
        _WIN_API._win_size = _WIN_API._gui.GetWindowRect(_WIN_API._GetHWND())
        img = np.array(API.WindowCapture())
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
        _WIN_API._game_area = (left, top, right, bottom)
        return _WIN_API._game_area

    @staticmethod
    def _CreateOverlayWindow():
        if _WIN_API._overlay_hwnd:
            return  # Already created

        wndclass = _WIN_API._gui.WNDCLASS()
        hInstance = _WIN_API._api.GetModuleHandle(None)
        wndclass.lpfnWndProc = _WIN_API._gui.DefWindowProc
        wndclass.lpszClassName = "DebugOverlayWindow"
        wndclass.hInstance = hInstance

        try:
            _WIN_API._overlay_class = _WIN_API._gui.RegisterClass(wndclass)
        except _WIN_API._gui.error:
            pass  # Already registered

        hwnd = _WIN_API._GetHWND()
        rect = _WIN_API._gui.GetWindowRect(hwnd)
        x, y = rect[0], rect[1]
        w, h = rect[2] - rect[0], rect[3] - rect[1]

        # WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST | WS_EX_TOOLWINDOW
        style = 524288 | 32 | 8 | 128

        # WS+POPUP
        args = (-2147483648, x, y, w, h, None, None, hInstance, None)
        _WIN_API._overlay_hwnd = _WIN_API._gui.CreateWindowEx(
            style, wndclass.lpszClassName, None, *args
        )
        _WIN_API._gui.SetLayeredWindowAttributes(
            _WIN_API._overlay_hwnd, 0x00FFFFFF, 0, 1
        )  # LWA_COLORKEY
        _WIN_API._gui.SetLayeredWindowAttributes(
            _WIN_API._overlay_hwnd, _WIN_API._api.RGB(0, 0, 0), 0, 1
        )
        _WIN_API._gui.ShowWindow(_WIN_API._overlay_hwnd, 5)  # SW_SHOW

    @staticmethod
    def DrawDebug(area, color, thickness=3):
        if not _WIN_API._overlay_hwnd:
            # _WIN_API._CreateOverlayWindow()
            _WIN_API._overlay_hwnd = _WIN_API._GetHWND()
        x, y = _WIN_API.WindowPosition()
        # Create a brush or pen and draw a rectangle
        with _WIN_API._MakeDC(_WIN_API._overlay_hwnd) as (hdc, dcObj):
            try:
                if len(area) != 2:
                    pen = _WIN_API._ui.CreatePen(0, 3, color)
                    dcObj.SelectObject(pen)
                    _WIN_API._gui.SelectObject(hdc, _WIN_API._gui.GetStockObject(5))
                    dcObj.Rectangle((area[0] - x, area[1] - y, area[2] - x, area[3] - y))
                else:
                    o = thickness // 2
                    for dx in range(thickness):
                        for dy in range(thickness):
                            dcObj.SetPixel(area[0] - x + dx - o, area[1] - y + dy - o, color)
            except:
                pass

    @staticmethod
    def ColorFromRGB(r, g, b):
        return int(f"{b:02x}{g:02x}{r:02x}", 16)


class _MAC_API(_API):
    pass


class _LINUX_API(_API):
    pass


API: _WIN_API = (
    {
        "Windows": _WIN_API,
        "Darwin": _MAC_API,
        "Linux": _LINUX_API,
    }.get(platform.system(), _API)
)()
