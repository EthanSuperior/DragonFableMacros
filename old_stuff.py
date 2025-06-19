exit()

import glob

import numpy as np
from PIL import ImageChops, ImageFilter, Image, ImageDraw
import Utils.macro_utils as m
import Utils.ui_macro_utils as m_ui
import Enums as df_t
from scipy.ndimage import label, generate_binary_structure, center_of_mass

from Utils.battle_utils import battle


# region Quest Types
def masked_quest(classID, maskLocation, events=lambda: 1 + 1, loot=()):
    masked, maskfile = masked_from_folder(m_ui.screenshot(), "Masks/" + maskLocation)
    if masked is None:
        return
    ImageDraw.Draw(masked, "1").rectangle(((0, 0), (masked.width, 98)), 0)
    coords = coords_of_mask(masked, maskfile)
    pX, pY = coords.pop(0)
    for x, y in coords:
        move_to((x, y), (classID, "Quick"), events, loot)
    move_to((pX, pY + 50), (classID, "Quick"), events, loot)


def pathfind_quest(classID, wallDict, currHeading="East", events=lambda: 1 + 1, loot=()):
    x, y, moveSetID, rm_map = [0], [0], (df_t.Classes.Warrior, "Recover"), {(-1, 0): "S"}
    # map_it(x, y, rm_map, currHeading, wallDict)
    while True:
        currHeading = new_heading(currHeading, wallDict)
        # map_it(x, y, rm_map, currHeading, wallDict)
        move_to("Center", moveSetID)
        move_towards(currHeading, moveSetID, events, loot)


# endregion
# region Battle
def CheckQuestDialog(success=lambda: 1 + 1, post=lambda: 1 + 1):
    if m.ImageCheck(["Battle/AbandonQuest.png", "Battle/ExitQuest.png"], (648, 312, 874, 404), 0.5):
        m_ui.ClickBtn("UI/CancelAbandonQuest.png", (671, 442, 810, 495))
    if m.ImageCheck("UI/QuestComplete.png", (410, 100, 820, 194)):
        m_ui.ClickBtn("UI/CloseQuest.png", (566, 645, 735, 689))
        success()
        LootQuest()
        post()
        raise AssertionError("Quest Complete")


def LootQuest():
    if m.ImageCheck("UI/ItemGet.png", (514, 126, 782, 184), 2):
        if m.ImageCheck(glob.glob("RejectedLoot/*.png"), (390, 241, 900, 296)):
            m_ui.ClickBtn(
                "UI/RejectLoot.png",
                (592, 696, 714, 733),
                "UI/Yes.png",
                (501, 443, 632, 494),
                False,
                1,
            )
            m_ui.ClickBtn("UI/Yes.png", (501, 443, 632, 494))
        else:
            m_ui.ClickBtn("UI/KeepLoot.png", (566, 644, 738, 691))


def move_to(pos, moveSetID, events=lambda: 1 + 1, loot=()):
    if type(pos) is str:
        pos = df_t.QuestLocations[pos]
    while True:
        m.Click(*pos)
        try:
            if not possibleBattle(moveSetID):
                break
            events()
            CheckQuestDialog(*loot)
        except AssertionError as msg:
            if "Failed" in msg:
                events()
                raise AssertionError("Quest Failed")
            else:
                raise msg
    events()
    CheckQuestDialog(*loot)


def move_towards(pos, moveSetID, events=lambda: 1 + 1, loot=()):
    if type(pos) is str:
        pos = df_t.QuestLocations[pos]
    m.Click(*pos)
    try:
        possibleBattle(moveSetID)
        events()
        CheckQuestDialog(*loot)
    except AssertionError as msg:
        if "Failed" in str(msg):
            events()
            raise AssertionError("Quest Failed")
        else:
            raise msg


def possibleBattle(moveSetID):
    if m.ImageCheck("Battle/Attack.png", (576, 630, 698, 698), 3):
        battle(moveSetID)
        return True
    return False


# endregion
# region Masking
def mask_image(img_in, img_mask):
    diff_img = ImageChops.difference(img_in.convert("RGB"), img_mask.convert("RGB"))
    diff_img = (
        diff_img.convert("L").filter(ImageFilter.MedianFilter(size=5)).point(lambda i: i * 255)
    )
    return diff_img.convert("1")


def masked_from_folder(img_in, mask_folder):
    for file in glob.glob(f"./{mask_folder}/*.png"):
        with Image.open(file) as img_goal:
            diff_img = mask_image(img_in, img_goal)
            area = np.bincount(np.array(diff_img).flat)[1:]
            if float(area / (diff_img.width * diff_img.height)) <= 0.2:
                # diff_img.save('_Masked.png', "png")
                return diff_img, str(file)
    return None, None


def coords_of_mask(diff_img, ordering):
    normOrder = "Right" in ordering or "Up" in ordering
    vertOrder = "Up" in ordering or "Down" in ordering
    labels, labels_nb = label(np.array(diff_img), generate_binary_structure(2, 2))
    centers = [c for c in center_of_mass(labels, labels=labels, index=range(1, labels_nb + 1))]
    centers.sort(key=lambda c: c[0 if vertOrder else 1], reverse=not normOrder)
    x_arr, y_arr = [round(c[1]) + 70 for c in centers], [round(c[0]) + 38 for c in centers]
    return list(zip(x_arr, y_arr))


def largest_in_mask(diff_img, min=0):
    labels, labels_nb = label(np.array(diff_img), generate_binary_structure(2, 2))
    areas = [*np.bincount(labels.flat)[1:]]
    if len(areas) == 0 or (m_area := max(areas)) < min:
        return None
    return center_of_mass(labels, labels=labels, index=areas.index(m_area) + 1)[::-1]


# endregion
# region Pathing
def map_it(x, y, rm_map, currHeading, wallDict):
    def str_map():
        xm_v, xma_v, ym_v, yma_v = 0, 0, 0, 0
        for k in rm_map.keys():
            xm_v = min(xm_v, k[0])
            xma_v = max(xma_v, k[0])
            ym_v = min(ym_v, k[1])
            yma_v = max(yma_v, k[1])
        map_str = [[" " for _ in range(xma_v - xm_v + 1)] for _ in range(yma_v - ym_v + 1)]
        for k, v in rm_map.items():
            map_str[k[1] - ym_v][k[0] - xm_v] = v
        with open("../dungeonRoom.txt", "wb") as file:
            file.write(("\n".join(["".join(s) for s in map_str])).encode("UTF-8"))

    if "North" in currHeading:
        y[0] -= 1
    if "South" in currHeading:
        y[0] += 1
    if "East" in currHeading:
        x[0] += 1
    if "West" in currHeading:
        x[0] -= 1
    rm_map[(x[0], y[0])] = room_symbol(wallDict)
    str_map()


def room_symbol(wallDict):
    wall_ascii = {
        (True, True, True, True): "□",
        (False, True, True, True): "╹",
        (True, False, True, True): "╺",
        (True, True, False, True): "╻",
        (True, True, True, False): "╸",
        (True, True, False, False): "╗",
        (False, True, True, False): "╝",
        (False, False, True, True): "╚",
        (True, False, False, True): "╔",
        (True, False, True, False): "═",
        (False, True, False, True): "║",
        (True, False, False, False): "╦",
        (False, True, False, False): "╣",
        (False, False, True, False): "╩",
        (False, False, False, True): "╠",
        (False, False, False, False): "╬",
    }
    img = m_ui.screenshot().convert("L").reduce(32)
    return wall_ascii[
        (
            is_wall(img, "North", wallDict),
            is_wall(img, "East", wallDict),
            is_wall(img, "South", wallDict),
            is_wall(img, "West", wallDict),
        )
    ]


def is_wall(img, direction, wallDict):
    pos, goal = wallDict[direction]
    return img.getpixel(pos) == goal


def new_heading(heading, wallDict):  # returns the new direction
    img = m_ui.screenshot().convert("L").reduce(32)

    def reverse():  # 180 degree turn
        if "North" in heading:
            return "South"
        elif "West" in heading:
            return "East"
        elif "South" in heading:
            return "North"
        else:
            return "West"

    def clockwise():  # 90 degree clockwise turn
        if "North" in heading:
            return "East"
        elif "West" in heading:
            return "North"
        elif "South" in heading:
            return "West"
        else:
            return "South"

    def wall_check():  # checks for the front and right walls
        if "North" in heading:
            return is_wall(img, "North", wallDict), is_wall(img, "East", wallDict)
        elif "West" in heading:
            return is_wall(img, "West", wallDict), is_wall(img, "North", wallDict)
        elif "South" in heading:
            return is_wall(img, "South", wallDict), is_wall(img, "West", wallDict)
        else:
            return is_wall(img, "East", wallDict), is_wall(img, "South", wallDict)

    front, right = wall_check()
    if not right:
        return clockwise()
    elif not front:
        return heading
    else:
        return new_heading(reverse(), wallDict)


# endregion


def Rooms100(classID):
    wallDict = {
        "North": ((18, 1), 37),
        "East": ((31, 11), 63),
        "South": ((15, 20), 47),
        "West": ((3, 11), 46),
    }

    def events():
        m_ui.ClickBtn("UI/CompleteQuestBtn.png", (485, 303, 780, 387))
        m_ui.ClickBtn("Farming/100RoomsMoglin.png", (553, 611, 730, 653))

    nav.loreBookHeal()
    m.sleep(1)
    nav.to_travel_map(1)
    m.Click(1108, 183)
    m_ui.ClickBtn("UI/TakeFlight_Bk1.png", (993, 638, 1168, 685))
    m.sleep(1.5)
    m_q.pathfind_quest(classID, wallDict, "East", events)


"""
def imgToText(img):
    return pyocr.image_to_string(img)

def readText(area):
    img = RegionGrab(area)
    img_rgb = np.array(img)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img = img.convert('L')
    #Try 'L' or convert('L'),
    # img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    img.save('../Blah.png', 'png')
    text = pyocr.image_to_string(img, config='-l eng --psm 8 -c tessedit_char_whitelist=0123456789')
    return text
"""


# parameter must be a PIL image
def send_to_clipboard(image):
    if not "Windows" in platform.platform():
        return
    from io import BytesIO

    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    import win32clipboard

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def reposition():
    import win32gui

    winds = []

    def enum_windows_callback(i, winds):
        if (
            win32gui.GetClassName(i) == "Chrome_WidgetWin_1"
            and win32gui.GetWindowText(i) == ""
            and win32gui.GetParent(i) == 0
        ):
            winds.append(i)

    win32gui.EnumWindows(enum_windows_callback, winds)
    sleep(0.1)
    print(winds)
    if not winds:
        return False
    global hwnd
    hwnd = winds[0]
    pos = getRelPos()
    resizeWin((min(pos[0], 654), min(pos[1], 158)), (1274, 880))
    return True


def openApp():
    import platform

    if "Windows" in platform.platform():
        import win32gui

        while not reposition():
            if win32gui.FindWindow(None, "GameLauncher on Artix Entertainment v.212") == 0:
                os.startfile("C:\\Program Files\\Artix Game Launcher\\Artix Game Launcher.exe")
                sleep(3)
            global hwnd
            hwnd = win32gui.FindWindow(None, "GameLauncher on Artix Entertainment v.212")
            Click(362, 471)
            sleep(2)
            Click(564, 800)
            sleep(7)
    login()
