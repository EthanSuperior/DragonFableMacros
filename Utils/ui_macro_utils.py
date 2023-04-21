import glob
import os

from Utils import macro_utils as m

def reposition():
    m.assignWin('Chrome_WidgetWin_1', '')
    m.sleep(.1)
    pos = m.getRelPos()
    m.resizeWin((min(pos[0], 654), min(pos[1], 158)), (1274, 880))
def openApp():
    import platform
    if 'Windows' in platform.platform():
        import win32gui
        while win32gui.FindWindow('Chrome_WidgetWin_1', '') == 0:
            m.sleep(10)
            os.startfile("C:/Program Files/Artix Game Launcher/Artix Game Launcher.exe")
            m.sleep(3)
            m.Click(119, 241)
            m.sleep(2)
            m.Click(362, 471)
            m.sleep(3)
        m.assignWin('Chrome_WidgetWin_1', '')
    reposition()
    login()
def login():
    reposition()
    m.ClickImage('UI/LoginButton.png', (513, 590, 733, 664), -1)
    m.Click(618, 625)
    m.ImageSearch('UI/CharShadia.png', (748, 190, 1176, 312), -1)
    m.Click(948, 237)
    m.ImageSearch('UI/Launch.png', (154, 651, 470, 744), -1)
    m.Click(312, 695)
# region UI_Btn
def ClickBtn(pathList, area, confirmPathList=None, confirmArea=None, disappear=True, timeout=3):
    if confirmArea is None: confirmArea = area
    if confirmPathList is None: confirmPathList = pathList
    def mid(a, b): return a + ((b - a) / 2)
    if m.ImageCheck(pathList, area, timeout):
        m.Click(mid(area[0], area[2]), mid(area[1], area[3]))
        if disappear and m.ImgGoneCheck(confirmPathList, confirmArea, timeout): return True
        elif m.ImageSearch(confirmPathList, confirmArea, timeout): return True
    return False
# endregion
def CheckQuestDialog(success=lambda:1+1, post=lambda:1+1, fail=lambda:1+1):
    if m.ImageCheck(['Battle/AbandonQuest.png', 'Battle/ExitQuest.png'], (648, 312, 874, 404), .5):
        ClickBtn('UI/CancelAbandonQuest', (671, 442, 810, 495))
    if m.ImageCheck('UI/QuestComplete.png', (410, 100, 820, 194)):
        ClickBtn('UI/CloseQuest.png', (566, 645, 735, 689))
        success()
        LootQuest()
        post()
        raise AssertionError('Quest Complete')
    if m.ImageCheck('Battle/Defeat.png', (255, 748, 371, 783)):
        fail()
        raise AssertionError('Quest Failed')

def LootQuest():
    if m.ImageCheck('UI/ItemGet.png', (514, 126, 782, 184), 2):
        if m.ImageCheck(glob.glob('RejectedLoot/*.png'), (390, 241, 900, 296)):
            ClickBtn('UI/RejectLoot.png', (592, 696, 714, 733), 'UI/Yes.png', (501, 443, 632, 494), False, 1)
            ClickBtn('UI/Yes.png', (501, 443, 632, 494))
        else:ClickBtn('UI/KeepLoot.png', (566, 644, 738, 691)),
