from gui_lib import GUI
from dialog import Dialog
import time


class _ACTMETA(type):

    def __getitem__(cls, key):
        if str(key).lower() in cls.Dialogs:
            return cls.Dialogs[str(key).lower()]
        return cls.Images[str(key).lower()]

    def __setitem__(cls, key, value):
        if isinstance(value, str):
            cls.Images[str(key).lower()] = value
        elif isinstance(value, Dialog):
            cls.Dialogs[str(key).lower()] = value

    def __delitem__(cls, key):
        if str(key).lower() in cls.Dialogs:
            del cls.Dialogs[str(key).lower()]
        else:
            del cls.Images[str(key).lower()]

    def __getattr__(cls, key):
        return cls[key]

    def __str__(cls):
        print(cls.Images, cls.Dialogs)


class ACT(metaclass=_ACTMETA):
    @staticmethod
    def AwaitImg(*paths, timeout=3, interval=0.01):
        return GUI.AwaitImg(*paths, timeout=timeout, interval=interval)

    @staticmethod
    def AwaitNotImg(*paths, timeout=3, interval=0.01):
        return GUI.AwaitNotImg(*paths, timeout=timeout, interval=interval)

    @staticmethod
    def ClickIf(path, timeout=3, interval=0.01):
        return GUI.ClickIf(path, timeout=timeout, interval=interval)

    @staticmethod
    def MouseClick(pos):
        return GUI.MouseClick(pos)

    @staticmethod
    def TypeKeys(keys, interval=0.01):
        if keys[0] == "e":
            GUI.MouseClick((0.5, 0.66))
            keys = keys[1:]
        return GUI.TypeKeys(keys, interval=interval)

    @staticmethod
    def Sleep(secs):
        time.sleep(secs)

    @staticmethod
    def _Battle(player_moves, pet_moves, endConditions=[], cyclical=False):
        player_moves = list(player_moves)
        pet_moves = list(pet_moves)
        while True:
            GUI.AwaitImg(ACT.atkBtn, ACT.ctnBtn, *endConditions, ACT.stkBtn, ACT.dead, timeout=-1)
            if any(GUI.CheckImage(i) for i in endConditions):
                return filter(GUI.CheckImage, endConditions)[0]
            elif GUI.CheckImage(ACT.atkBtn):
                if GUI.CheckImage(ACT.petBtn):
                    move = pet_moves.pop(0) if pet_moves else " "
                else:
                    move = player_moves.pop(0) if player_moves else " "
                ACT.TypeKeys(move)
                GUI.AwaitNotImg(ACT.atkBtn)
            elif GUI.CheckImage(ACT.ctnBtn):
                GUI.TypeKeys(" ")
                GUI.AwaitImg(ACT.noOverlay, timeout=1)
                return ACT.ctnBtn
            elif GUI.CheckImage(ACT.dead):
                ACT.ClickIf("ScreenCaps/#(0.451, 0.587, 0.577, 0.619).png")
                return ACT.dead
            else:
                GUI.ClickIf(ACT.stkBtn, timeout=0)

    @staticmethod
    def Battle(className, count=1):
        if className == "ChaosWeaver":
            if count == 1:
                return ACT._Battle("3v", "78")
            elif count == -2:
                return ACT._Battle("4xv", "71")
            elif count == "VERLYRUS?":
                return ACT._Battle("49v0cz", "097v4")
            return ACT._Battle("487", "78")
        return ACT._Battle("487", "78")

    @staticmethod
    def BattleWar(startBtn: str, waves: list, counts: list, className="ChaosWeaver"):
        print(f"Starting Waves of {startBtn.split('/')[1].split('#')[0]} war")
        num = 0
        while GUI.ClickIf(startBtn, timeout=20):  # True
            # wave = waves[1]
            wave = GUI.AwaitImg(*waves, timeout=20)
            if wave is None:
                return
            idx = waves.index(wave)
            cnts = counts[idx][:]
            print(f"\rStarting wave #{(num := num + 1)} ({num+2464})", end="", flush=True)
            print(ACT.QuestComplete["in"])
            while True:
                ACT.MoveInDirection(wave.split("/")[-1])
                GUI.AwaitImg(ACT.atkBtn, ACT.QuestComplete["in"])  # ACT.questFail,
                if GUI.CheckImage(ACT.atkBtn):
                    ACT.Battle(className, cnts.pop() if len(cnts) > 1 else cnts[0])
                elif ACT.QuestComplete:
                    ACT.QuestComplete.Close()
                    ACT.NewItem.Await().Keep()
                    break
            # elif GUI.CheckImage(ACT.questFail):
            #     pass
            # else:
            #     pass

    @staticmethod
    def MoveInDirection(direction):
        if direction.lower()[0] == "n":
            GUI.MouseClick((0.5, 0.003))
        elif direction.lower()[0] == "s":
            GUI.MouseClick((0.5, 0.81))
        elif direction.lower()[0] == "e":
            GUI.MouseClick((0.98, 0.578))
        elif direction.lower()[0] == "w":
            GUI.MouseClick((0.01, 0.69))

    @staticmethod
    def MakeDialog(folder):
        return Dialog(folder)

    @staticmethod
    def Setup():
        import os
        from pynput import mouse

        print("Running Setup...")
        os.chdir("./Images")
        ACT.Images = {}
        ACT.Dialogs = {}

        for entry in os.listdir("./General"):
            full_path = os.path.join("./General", entry)
            if os.path.isdir(full_path):
                ACT[entry] = Dialog(f"./General/{entry}")
            elif os.path.isfile(full_path) and entry.endswith(".png"):
                ACT[entry.split("\\")[-1].split("/")[-1].split("#")[0]] = f"./General/{entry}"
        # ACT.atkBtn = FetchImg("atkBtn")
        # ACT.ctnBtn = FetchImg("ctnBtn")
        # ACT.stkBtn = FetchImg("stkBtn")
        # ACT.petBtn = FetchImg("petBtn")
        # ACT.dead = FetchImg("dead")

        # ACT.noOverlay = FetchImg("noOverlay")

        def debug_mouse(_, y, b, p):
            if y >= 2050 and b == mouse.Button.middle and p:
                __import__("traceback").print_stack(
                    list(__import__("sys")._current_frames().values())[-1]
                )
                GUI.SaveRegion((0, 0, 1, 1), "trace")

        debug = mouse.Listener(on_click=debug_mouse)
        debug.daemon = True
        debug.start()


ACT.Setup()

if __name__ == "__main__":
    # ACT.LoreBook() => ACT.LoreBook(True) => ACT.LoreBook.Yes() => ACT.LoreBook.Action('yes', autoClose=True)
    # ACT.LoreBook(False) => ACT.LoreBook.No() => ACT.LoreBook.No(True) => ACT.LoreBook.Action('no', autoClose=True)
    # ACT.LoreBook.Pot() => ACT.LoreBook.Pot(True) => ACT.LoreBook.Action('pot', autoClose=True)
    # ACT.LoreBook.Open() Open() and Close() will open and close the book manually
    # if ACT.LoreBook: => is Act.LoreBook open?
    # if ACT.LoreBook.Pot: => is Act.LoreBook.Pot visible?
    # print(ACT)
    # For Example!!
    print(bool(ACT.QuestComplete))
    quit()
