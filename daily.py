from actions import ACT
from Macro.api_lib import _WIN_API  # TODO: Make Generic Quit Method....

_WIN_API.GetGameSize()
if _WIN_API.hwnd:
    quit()

ACT.Startup()
ACT.LoreBook.Quest(False)
ACT.AwaitImg(ACT.noOverlay, timeout=5)
if not ACT.LoreBook:
    ACT.MoveInDirection("west")
    ACT.Battle("ChaoseWeaver", ("4v", "7"))
    ACT.FinishQuest()
    ACT.LoreBook.Await().Pot()

_WIN_API._gui.PostMessage(_WIN_API.hwnd, 16, 0, 0)  # WM_CLOSE
