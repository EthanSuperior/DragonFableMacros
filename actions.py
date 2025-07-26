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
    def CutsceneEnd(path):
        while not GUI.CheckImage(path):
            ACT.MouseClick((0.964, 0.792))
            ACT.Sleep(0.1)

    @staticmethod
    def ClickIf(path, timeout=3, interval=0.01):
        return GUI.ClickIf(path, timeout=timeout, interval=interval)

    @staticmethod
    def MouseClick(pos, times=1):
        return GUI.MouseClick(pos, times=times)

    @staticmethod
    def TypeKeys(keys, interval=0.01):
        if keys[0] == "e":
            GUI.MouseClick((0.5, 0.66))
        elif callable(keys[0]):
            keys[0]()
        else:
            return GUI.TypeKeys(keys, interval=interval)
        ACT.Sleep(interval)
        return ACT.TypeKeys(keys[1:], interval=interval)  # Preformed special op

    @staticmethod
    def Sleep(secs):
        time.sleep(secs)

    @staticmethod
    def _Battle(player_moves, pet_moves, endConditions=[], cyclical=False):
        player_moves = list(player_moves)
        pet_moves = list(pet_moves)
        while True:
            GUI.AwaitImg(
                ACT.atkBtn, ACT.deadmask, ACT.ctnBtn, *endConditions, ACT.stkBtn, timeout=-1
            )
            if any(GUI.CheckImage(i) for i in endConditions):
                return list(filter(GUI.CheckImage, endConditions))[0]
            elif GUI.CheckImage(ACT.atkBtn):
                moveset = pet_moves if GUI.CheckImage(ACT.petBtn) else player_moves
                if cyclical:
                    moveset.append(move := moveset.pop(0))
                else:
                    move = moveset.pop(0) if moveset else " "
                ACT.TypeKeys(move)
                GUI.AwaitNotImg(ACT.atkBtn)
            elif GUI.CheckImage(ACT.deadmask):
                print("dead", flush=True)
                ACT.ClickIf(ACT.deadCtn)
                return ACT.dead
            elif GUI.CheckImage(ACT.ctnBtn):
                GUI.TypeKeys(" ")
                GUI.AwaitImg(ACT.noOverlay, timeout=1)
                return ACT.ctnBtn
            else:
                GUI.ClickIf(ACT.stkBtn, timeout=0)

    @staticmethod
    def ForfitBattle():
        ACT.AwaitImg(ACT.atkBtn)  # Can only flee on your turn in battle...
        ACT.Sleep(0.2)
        ACT.Options.Flee()

    @staticmethod
    def Battle(className, moveSet=1):
        if isinstance(moveSet, tuple) or isinstance(moveSet, list):
            return ACT._Battle(*moveSet)
        if className == "ChaosWeaver":
            if moveSet == 1:
                return ACT._Battle("3v", "78")
            elif moveSet == -1:
                return ACT._Battle("4v3z", "78")
            elif moveSet == -3:
                return ACT._Battle("43 v", "78")
            elif moveSet == "BOSS":
                return ACT._Battle(
                    ["e4", "e1", *"9v3", "e4", "ec", *"8z2", "e4", "e3", "6"],
                    "67384513 4  3 4  3 4",
                    cyclical=True,
                )
            elif moveSet == -2:
                return ACT._Battle("4xv", "71")
            elif moveSet == "VERLYRUS?":
                return ACT._Battle("49v0cz3", "097v4")
            elif moveSet == "AARGH":
                return ACT._Battle("549tv641c0z4x32", "4907v4")
            return ACT._Battle("478", "78")
        return ACT._Battle("vc487", "78")

    @staticmethod
    def BattleWar(waves: list, counts: list, className="ChaosWeaver", rareWaves="skip"):
        if "num" not in ACT.__dict__:
            ACT.num = int(s[1]) if len((s := __import__("sys").argv)) > 1 and s[1].isdigit() else 0
        # wave = waves[1]
        wave = GUI.AwaitImg(*waves, timeout=20)
        if wave is None:
            return False
        idx = waves.index(wave)
        cnts = counts[idx][:]
        ACT.num += 1
        print(f"\rStarting wave #{ACT.num}/1000", end="", flush=True)
        while True:
            ACT.MoveInDirection(wave.split("/")[-1])
            # TODO: Make this a little more graceful....
            GUI.AwaitImg(ACT.atkBtn, ACT.QuestComplete["in"])  # ACT.questFail,
            if GUI.CheckImage(ACT.atkBtn):
                ACT.Battle(className, cnts.pop() if len(cnts) > 1 else cnts[0])
            elif ACT.QuestComplete:
                ACT.QuestComplete.Close()
                GUI.MouseClick((0.5, 0.5))  # Click anywhere to move mouse
                ACT.NewItem.Keep()
                break
            # elif GUI.CheckImage(ACT.questFail):
            #     pass
            # else:
            #     pass
        return True

    @staticmethod
    def MoveInDirection(direction):
        if direction.lower()[0] == "n":
            GUI.MouseClick((0.5, 0.03))
        elif direction.lower()[0] == "s":
            GUI.MouseClick((0.5, 0.81))
        elif direction.lower()[0] == "e":
            GUI.MouseClick((0.98, 0.578))
        elif direction.lower()[0] == "w":
            GUI.MouseClick((0.01, 0.69))
        else:
            print(direction.lower()[0])

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

        # TODO: ADD Aliases to Global
        for entry in os.listdir("./Global"):
            full_path = os.path.abspath(os.path.join("./Global", entry)).replace("\\", "/")
            if os.path.isdir(full_path):
                ACT[entry] = Dialog(full_path)
            elif os.path.isfile(full_path) and entry.endswith(".png"):
                ACT[entry.split("/")[-1].split("#")[0]] = full_path

        def debug_mouse(_, y, b, p):
            if y >= 2050 and b == mouse.Button.middle and p:
                __import__("traceback").print_stack(
                    list(__import__("sys")._current_frames().values())[-1]
                )
                GUI.SaveRegion((0, 0, 1, 1), "trace")

        # if not __file__.endswith("creator.py"):
        debug = mouse.Listener(on_click=debug_mouse)
        debug.daemon = True
        debug.start()

    @staticmethod
    def ToggleWeaponType():
        # THIS SHOULD BE A HIGHER-ORDER FUNCTION like toggle(4) or maybe toggle([(0.511, 0.474),(0.511, 0.474)])
        # NOTE ALWAYS FOLLOWS A CERTAIN ORDER WHEN YOU OPEN THE DIALOG REGARDLESS OF CURRENT ELEMENT
        ACT.WeaponToggle.Open()
        ACT.Sleep(0.1)
        ACT.MouseClick((0.511, 0.474))
        ACT.WeaponToggle.Close()

    @staticmethod
    def FinishQuestAndItems(keepMode="All"):
        ACT.FinishQuest()
        ACT.KeepItem(keepMode=keepMode)

    @staticmethod
    def KeepItem(keepMode="All"):
        ACT.NewItem.Await()
        if keepMode.lower() == "all":
            keepItem = True
        elif keepMode.lower() == "none":
            keepItem = False
        elif keepMode.lower() == "unique":
            keepItem = not ACT.Items.Any()
        else:
            keepItem = GUI.CheckImage(str(ACT.Items[keepMode]))

        if keepItem and keepMode.lower() == "unique":
            ACT.Items.Add((0.302, 0.243, 0.714, 0.315), time.strftime("%H-%M-%S"))
        ACT.NewItem.Keep() if keepItem else ACT.NewItem.Pass()

    @staticmethod
    def FinishQuest():
        ACT.QuestComplete.Await().Close()
        ACT.MouseClick((0.5, 0.5))

    @staticmethod
    def SummonPetDragon():
        def summon_drag():
            ACT.DragonAmulet.Open()
            ACT.Sleep(0.1)
            ACT.DragonAmulet.Summon.Open()
            ACT.Sleep(0.1)
            ACT.DragonAmulet.Summon.Pet()
            ACT.Sleep(0.1)

        return summon_drag

    @staticmethod
    def Equip(*items, slot=None):
        def battleEquip():
            ACT.Inventory.Open()
            for name in items:
                GUI.MouseClick((0.294, 0.765))
                ACT.Sleep(0.1)
                GUI.TypeKeys("a", modifiers=True)
                GUI.SetClipboard(name)
                GUI.TypeKeys("v", modifiers=True)
                ACT.Sleep(0.1)
                GUI.MouseClick((0.294, 0.239))
                ACT.Inventory.Equip(False)
            (ACT.Slot(slot) if slot else ACT.Inventory.Close)()

        return battleEquip

    @staticmethod
    def Slot(name):
        def battleSlot():
            ACT.Inventory.Open()
            GUI.MouseClick((0.294, 0.765))
            ACT.Sleep(0.1)
            GUI.TypeKeys("a", modifiers=True)
            GUI.SetClipboard(name)
            GUI.TypeKeys("v", modifiers=True)
            ACT.Sleep(0.1)
            GUI.MouseClick((0.294, 0.239))
            ACT.Inventory.Slot()

        return battleSlot


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
    # ACT.LoreBook[1].Close(False)
    # ACT.Battle("ChaosWeaver", ("43vz", "90"))
    # ACT.Equip(["uragiri", "drop bear hat"], slot="hammer")
    while True:
        GUI.AwaitImg(ACT.deadmask, timeout=-1)
        print("Found it....", GUI.CheckImage(ACT.deadmask))
    quit()
