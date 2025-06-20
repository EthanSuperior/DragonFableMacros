from gui_lib import GUI
import time


class ACT:
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
                GUI.TypeKeys(move)
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
            print(f"\rStarting wave #{(num := num + 1)} ({num+1470})", end="", flush=True)
            while True:
                ACT.MoveInDirection(wave.split("/")[-1])
                GUI.AwaitImg(ACT.atkBtn, ACT.questPass)  # ACT.questFail,
                if GUI.CheckImage(ACT.atkBtn):
                    ACT.Battle(className, cnts.pop() if len(cnts) > 1 else cnts[0])
                elif GUI.CheckImage(ACT.questPass):
                    GUI.ClickIf(ACT.questClose)
                    GUI.AwaitImg(ACT.newItem)
                    GUI.ClickIf(ACT.keepItem)
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
            GUI.MouseClick((0.99, 0.578))
        elif direction.lower()[0] == "w":
            GUI.MouseClick((0.01, 0.69))

    @staticmethod
    def Setup():
        import glob
        import os
        from pynput import mouse

        print("Running Setup...")
        os.chdir("./Images")

        def FetchImg(name):
            return glob.glob(f"./{name}*.png")[0]

        ACT.atkBtn = FetchImg("atkBtn")
        ACT.ctnBtn = FetchImg("ctnBtn")
        ACT.stkBtn = FetchImg("stkBtn")
        ACT.petBtn = FetchImg("petBtn")
        ACT.questPass = FetchImg("questPass")
        ACT.questClose = FetchImg("questClose")
        ACT.newItem = FetchImg("newItem")
        ACT.noOverlay = FetchImg("noOverlay")
        ACT.keepItem = FetchImg("KeepItem")
        ACT.dead = FetchImg("dead")

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
