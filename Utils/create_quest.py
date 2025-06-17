import os
import macro_utils as m_ui
from ctypes import windll
from pynput import mouse, keyboard
import time

folder_dir = "ScreenCaps"
startT = None
_currX, _currY = 0, 0


def on_click(x, y, button, pressed):
    global startT
    if button == mouse.Button.left:
        if pressed:
            if startT is None:
                startT = time.time()
            else:
                dT = int((time.time() - startT) * 1000) / 1000
                startT = time.time()
                print(f"time.sleep({dT})\nui.MouseClick{m_ui.getRelMousePos()}")
    else:
        global _currX, _currY
        if pressed:
            # print("{} RC at {}".format("Pressed", m_ui.getRelMousePos()))
            _currX, _currY = m_ui.getRelMousePos()
        else:
            # print("{} RC at {}".format("Released", m_ui.getRelMousePos()))
            x, y = m_ui.getRelMousePos()
            if abs(_currX - x) + abs(_currY - y) >= 10:
                area = (min(_currX, x), min(_currY, y), max(_currX, x), max(_currY, y))
                area = m_ui.give_me_mid(m_ui.get_mid(area), area)
                m_ui.RegionGrab(area).save(f"{folder_dir}/#{area}.png", "png")
                global alt_pressed
                if not alt_pressed:
                    print(f'ui.ClickIf("{folder_dir}/#{area}.png")')
                    m_ui.Click(*m_ui.get_mid(area))
                    m_ui.Click(*m_ui.get_mid(area))
                else:
                    print(f'ui.AwaitImg("{folder_dir}/#{area}.png")')
                startT = time.time()


def on_move(x, y):
    if x < 10 and y < 10:
        keyboard_listener.stop()
        mouse_listener.stop()


alt_pressed = False


def on_press(key):
    global alt_pressed
    if key in {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r}:
        alt_pressed = True
    elif isinstance(key, keyboard.KeyCode):
        print(f"m_ui.typeKeys({key.char})")


def on_release(key):
    global alt_pressed
    if key in {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r}:
        alt_pressed = False


if __name__ == "__main__":
    os.chdir("C:/Users/User/Desktop/Programing/DragonFableMacros/Images")
    # m_ui.sleep(1)
    # for a in m_ui.GetAllWindows():
    #     print(a)
    m_ui.assignWin("Chrome_WidgetWin_1", "Evolved DragonFable Launcher")
    m_ui.screenshot(True)
    exit()
    # import win32gui
    # def enum_windows_callback(hwnd, windows):
    #     title = win32gui.GetWindowText(hwnd)
    #     if win32gui.GetClassName(hwnd) == "Chrome_WidgetWin_1":
    #         windows.append((hwnd, title, win32gui.GetClassName(hwnd)))

    # windows = []
    # win32gui.EnumWindows(enum_windows_callback, windows)
    # for hwnd, title, vls in windows:
    #     print(f"HWND: {hwnd}, Title: {title} Class: {vls}")
    # print(win32gui.FindWindow()
    # m_ui.openApp()
    # exit()

    ans = "Arachnalchemy"
    # pyag.prompt(text="", title="What is the name of this Quest", default="")
    import ui_helpers

    ui_helpers.useForegroundWin()
    # print(ans)
    if ans:
        folder_dir = ans
    try:
        os.makedirs(f"C:/Users/User/Desktop/Programing/DragonFableMacros/Images/{folder_dir}")
        print(
            'import sys\nimport os\nsys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../Utils")))\nimport ui_helpers as ui\n\nui.SetUp(__file__)\n\nimport time'
        )
    except Exception:
        pass

    # area = (340, 210, 660, 295)
    # m_ui.RegionGrab(area).save(f"{folder_dir}/#{area}.png", "png")
    # exit()

    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)

    keyboard_listener.start()
    mouse_listener.start()

    keyboard_listener.join()
    mouse_listener.join()
