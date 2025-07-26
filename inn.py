from actions import ACT

import os

os.chdir("./Inn")


def Timekillers():
    ACT.Battle(
        "ChaosWeaver",
        (
            ["\t", "e3", *"12t319", "e5", *"4v", "e0", *"62nzn231c", "e5", "4", "e9", *"30v"],
            "3v 2 6398153   236   31",
        ),
    )


def ChallengerBelt():
    if ACT.ClickIf("ChallengerBelt/start#(0.095, 0.407, 0.289, 0.463).png", timeout=30):
        for op in [*([-2] * 7), "VERLYRUS?"]:
            if ACT.Battle("ChaosWeaver", op) == ACT.dead:
                ACT.ForfitBattle()
                ACT.ClickIf("ChallengerBelt/lost#(0.353, 0.371, 0.633, 0.451).png")
                continue
        ACT.QuestComplete.Await().Close()
        ACT.NewItem.Await().Keep()
        return True
    return False


def Dragonoid():
    # Player is 0 0 200Int 0 200luk 0 45wis
    # DRAG IS: 200 0 0 200 200
    ACT.Equip("uragiri", slot="hammer")()
    ACT.ClickIf("Dragon/start#(0.704, 0.263, 0.9, 0.329).png")
    target = lambda: ACT.MouseClick((0.7, 0.3))
    # fmt: off
    player_moveset = [
        *"48", [ACT.Equip("doomed", slot="ice scythe"), target, "9"],
        [ACT.Slot("lucky hammer"), "x"], "v",
        [ACT.Equip("uragiri"),"4"], "7", [ACT.Equip("doomed"), "0"]
    ]
    # fmt: on
    if ACT.Battle("ChaosWeaver", (player_moveset, "910v ")) == ACT.dead:
        ACT.ClickIf("Dragon/lost#(0.353, 0.368, 0.637, 0.448).png")
    else:
        if ACT.AwaitImg("Dragon/lost#(0.353, 0.368, 0.637, 0.448).png", timeout=0.5):
            ACT.ClickIf("Dragon/lost#(0.353, 0.368, 0.637, 0.448).png")
            return
        ACT.FinishQuestAndItems(keepMode="Unique")


def ClassicInnFight(fight, setup, player_moveset, dragon_moveset):
    def ImgByName(path, name):
        for filename in os.listdir(path):
            if filename.startswith(name):
                return os.path.join(path, filename)
        return ""

    start = ImgByName(fight, "start")
    lost = ImgByName(fight, "lost")
    if not start or not lost:
        raise FileNotFoundError(f"Images for {fight} not found.")
    setup()
    ACT.Sleep(0.1)
    ACT.ClickIf(start)
    ACT.Sleep(0.1)
    if ACT.Battle("DeathKnight", (player_moveset(), dragon_moveset())) == ACT.dead:
        ACT.ClickIf(lost)
    else:
        ACT.FinishQuestAndItems()
        exit()


# DRAGON MOVES:
# 1: Stun 2: Scout 3: Lash 4: Blast 5: Heal 6: Shield 7: Nova 8: Outrage 9: Boost 0: Tickle z: Skip v: Primal


def FallenPurpose():
    # 200 END / 200 DEX / 39 CHA / 6 INT
    # 200 Protection / 200 Fighting / 200 Magic (200/200/200/0/0)
    # DeathKnight; DeathKnight Relics + Lucky Hammer
    # Exalted Blaster II (Doom)
    # Legion Bracer # Start in consuming
    # Sword needs to be in Lightmode.
    target_SMUDD = lambda: ACT.MouseClick((0.17, 0.4))
    target_Draco = lambda: ACT.MouseClick((0.8, 0.4))
    # fmt: off
    setup = ACT.ToggleWeaponType
    player_moveset =lambda: [[target_SMUDD, *"e5"], "e9", "8", [target_Draco, "6"], *"13v", "ez", "x",
                      [target_SMUDD, "1"], *"5986", "e1", "3", "e2", "ec", *"z98061vcx", "e5", "e1", "ez", "7", 
                      [target_SMUDD, "9"], *"861", "e3", *"vx", "e5", *"nz95", "e1", *"c3"]
    dragon_moveset =lambda: [*"34 734 ", [target_SMUDD, " "], *"34  34 z364 837v43  43  453 46384"]
    # fmt: on
    ClassicInnFight("FallenPurpose", setup, player_moveset, dragon_moveset)


def ConvergenceII():
    # Start Consuming
    # fmt: off
    player_moveset = ["9", "e8", "e6", *"z 1vx5c3", [lambda x: ACT.Sleep(20)], *'986z01v', 'e7', [exit]]
    drag_moveset = "3 89v3    563    " # Missing Phase 4 see: https://www.youtube.com/watch?v=4LkVDd-ArFs
    # fmt: on
    if ACT.Battle("DeathKnight", (player_moveset, drag_moveset)) == ACT.dead:
        pass


def Dominion():  # I FORFEIT THIS IS LIKE A 70 Turn battle....
    ACT.Equip("Relic DeathKnight Blade", slot="hammer")()
    ACT.ClickIf("Dominion/start#(0.704, 0.455, 0.904, 0.515).png")
    kathool = lambda: ACT.MouseClick((0.713, 0.308))
    archdryad = lambda: ACT.MouseClick((0.818, 0.406))
    skywatcher = lambda: ACT.MouseClick((0.833, 0.589))
    # fmt: off
    # start in consuming...
    player_moveset = [
        [kathool, "4"], [archdryad, "9"], *"863v",'e ', [skywatcher, '1'], *'zx7t ',
        'ec', '1', 'e ', *'  ', 'ec', 'e ', 'e0', *'2 ', 'e9', [kathool, '4'], [skywatcher, 'e','6'],
        *'1cv','ez','x', [ACT.Equip("dragonoid staff v"), ' '], 'e ', 'c', 'e1',*'58','e ', 'c', 'e ',[exit]
    ]
    drag_moveset = [[archdryad, "v"], *"  ", [kathool, '1'],*'6 5',*(15*' '),'5',
                    [skywatcher,' '],*'v ', [kathool, '1'], ' ',*('z'*9),'5']
    # fmt: on
    res = ACT.Battle("ChaosWeaver", (player_moveset, drag_moveset))
    if res == ACT.dead:
        ACT.ClickIf("Dragon/lost#(0.353, 0.368, 0.637, 0.448).png")
    else:
        if ACT.AwaitImg("Dragon/lost#(0.353, 0.368, 0.637, 0.448).png", timeout=0.5):
            ACT.ClickIf("Dragon/lost#(0.353, 0.368, 0.637, 0.448).png")
            return
        ACT.FinishQuestAndItems(keepMode="Unique")


def AARGH():
    # DRAG IS: MAG MISC ASSIST
    ACT.Sleep(1)
    ACT.ClickIf("AARGH/start#(0.757, 0.09, 0.931, 0.168).png")
    ACT.AwaitImg(ACT.atkBtn)
    from gui_lib import GUI
    import time

    area = (0.632, 0.85, 0.882, 0.876)
    img = GUI.CaptureRegion(area)
    if ACT.Battle("ChaosWeaver", "AARGH") != ACT.dead:
        ACT.QuestComplete.Await().Close()
        ACT.MouseClick((0.5, 0.5))
        ACT.NewItem.Await().Keep()
        img.save(f"AARGH/Victory/{time.strftime("%H-%M-%S")}#{area}.png", "png")
        return True
    else:
        ACT.Sleep(2)
        ACT.TypeKeys(" ")
        ACT.Sleep(0.1)
        ACT.MouseClick((0.496, 0.398))
        img.save(f"AARGH/Defeat/{time.strftime("%H-%M-%S")}#{area}.png", "png")
        return ACT.AwaitImg("AARGH/start#(0.757, 0.09, 0.931, 0.168).png") is not None


def WeirdDuo():
    drag = ACT.SummonPetDragon()

    def toggle():
        ACT.Sleep(0.1)
        ACT.MouseClick((0.259, 0.345))
        ACT.Sleep(0.1)

    # fmt: off
    player_moveset = ['6', [toggle, '1'], [toggle, '3'], [toggle, *'ex'], *'nz\t4\t', [toggle, '9'], [toggle, '8'], [toggle, '6'], [toggle, '1'], 
                      [toggle, *'ec'], [toggle, 'v'], [drag, 'x'], *'c3', 'ez', *'c  ', 'e8', *'946v']
    pet_moveset = '34   6187'
    # fmt: on
    ACT.ClickIf("WeirdDuo/start#(0.09, 0.458, 0.29, 0.516).png", timeout=18.43)
    if ACT.Battle("DeathKnight", (player_moveset, pet_moveset)) != ACT.ctnBtn:
        ACT.ClickIf("WeirdDuo/lost#(0.354, 0.368, 0.636, 0.446).png", timeout=12.88)
        ACT.AwaitImg("WeirdDuo/start#(0.09, 0.458, 0.29, 0.516).png", timeout=18.43)
        ACT.WeaponToggle.Open()
        ACT.Sleep(0.1)
        ACT.MouseClick((0.511, 0.474))
        ACT.Sleep(0.1)
        ACT.MouseClick((0.511, 0.474))
        ACT.WeaponToggle.Close()
        ACT.DragonAmulet.Open()
        ACT.Sleep(0.1)
        ACT.DragonAmulet.Summon.Open()
        ACT.Sleep(0.1)
        ACT.DragonAmulet.Summon.Dismiss()
        ACT.Sleep(0.1)


def InevitableEquilibrium():  # https://www.youtube.com/watch?v=Zf1pzXccsuc #9:24
    # DRAG IS: 200 0 200 200 0
    def summon_miniphage():
        ACT.Inventory.Build8(False)
        ACT.Inventory.Load()
        ACT.Inventory.Await().Close()
        ACT.Sleep(0.1)

    summon_miniphage()
    ACT.ClickIf("InevitableEquilibrium/start#(0.393, 0.293, 0.595, 0.351).png")
    ACT.AwaitImg(ACT.atkBtn)
    drag = ACT.SummonPetDragon()
    mini = summon_miniphage
    # fmt: off
    # t\t9", [drag, *"e6"], *"c3v", "ez", *"x17
    player_moveset = [*"\tt\t9", [drag, *"e6"], *"c3v", "ez", *"x1796", "ec", *"13", 
                        'ex','n','ec',*'96v','ez',*'1x5n9','e6',*'c3', [mini, *'em']]
    pet_moveset = " \t 3z653   v3z  3  z53   63 "
    if (ACT.Battle("DeathKnight",
            (player_moveset, pet_moveset, ["InevitableEquilibrium/lost#(0.351, 0.364, 0.641, 0.448).png"]))
        != ACT.ctnBtn):
        # fmt: on
        ACT.Sleep(0.1)
        ACT.TypeKeys(" ")
        ACT.ClickIf("InevitableEquilibrium/lost#(0.351, 0.364, 0.641, 0.448).png")
        InevitableEquilibrium()
    else:
        ACT.FinishQuestAndItems()


if __name__ == "__main__":
    ACT.MouseClick((0.366, 0.604))
    ACT.Sleep(0.1)
    while True:
        FallenPurpose()
    #     Dragonoid()
    #     pass
    # InevitableEquilibrium()
