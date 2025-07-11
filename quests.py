from actions import ACT


def BicentennialDragonLord():
    startWaveBtn = "./BicentennialDragonLord/start#(0.713, 0.633, 0.893, 0.687).png"
    waves = [
        "./BicentennialDragonLord/eastWave1#(0.25, 0.2, 1, 1).png",
        "./BicentennialDragonLord/westWave2#(0, 0.2, 0.75, 1).png",
        "./BicentennialDragonLord/eastWave3#(0.25, 0.2, 1, 1).png",
    ]
    if ACT.ClickIf(startWaveBtn, timeout=20):  # True
        if not ACT.BattleWar(waves, [[2, 2, 2], [2, 2, 2], [2, 2, 2]]):
            ACT.MouseClick((0.01, 0.573))
            ACT.AbandonQuest()
            return BicentennialDragonLord()
        return True
    return False


def ChallengerBelt():
    if ACT.ClickIf("ChallengerBelt/start#(0.095, 0.407, 0.289, 0.463).png", timeout=30):
        for op in [*([-2] * 7), "VERLYRUS?"]:
            if ACT.Battle("ChaosWeaver", op) == ACT.dead:
                ACT.ForfitBattle()
                ACT.ClickIf("ChallengerBelt/challengeLost#(0.353, 0.371, 0.633, 0.451).png")
                continue
        ACT.QuestComplete.Await().Close()
        ACT.NewItem.Await().Keep()
        return True
    return False


def DarkTower():
    ACT.ClickIf("DarkTower/#(0.359, 0.504, 0.451, 0.618).png", timeout=5.302)
    ACT.ClickIf("DarkTower/#(0.246, 0.464, 0.386, 0.512).png", timeout=18.622)
    ACT.ClickIf("DarkTower/#(0.238, 0.406, 0.394, 0.45).png", timeout=7.318)
    ACT.ClickIf("DarkTower/#(0.244, 0.346, 0.386, 0.388).png", timeout=7.684)
    ACT.ClickIf("DarkTower/#(0.66, 0.41, 0.81, 0.448).png", timeout=11.98)
    ACT.ClickIf("DarkTower/#(0.772, 0.348, 0.916, 0.388).png", timeout=17.378)
    ACT.ClickIf("DarkTower/#(0.647, 0.353, 0.807, 0.397).png", timeout=11.004)
    ACT.CutsceneEnd("DarkTower/inQuest#(0.472, 0.019, 0.626, 0.277).png")
    ACT.Sleep(0.1)
    ACT.MouseClick((0.985, 0.481))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.985, 0.481))
    ACT.Sleep(3)
    ACT.MouseClick((0.985, 0.481))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.985, 0.481))
    ACT.Sleep(3)
    ACT.MouseClick((0.985, 0.481))
    ACT.Battle("ChaosWeaver", 2)
    ACT.MouseClick((0.985, 0.481))
    ACT.Sleep(3)
    ACT.MouseClick((0.524, 0.027))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.524, 0.027))
    ACT.Sleep(3)
    ACT.MouseClick((0.755, 0.425))
    ACT.MouseClick((0.755, 0.425))
    ACT.ClickIf("DarkTower/#(0.021, 0.44, 0.127, 0.744).png", timeout=10)
    ACT.Sleep(3)
    ACT.MouseClick((0.027, 0.688))
    ACT.Sleep(2.608)
    ACT.MouseClick((0.61, 0.249))
    ACT.Sleep(2.437)
    ACT.MouseClick((0.756, 0.611))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.756, 0.611))
    ACT.Sleep(1.921)
    ACT.MouseClick((0.793, 0.155))
    ACT.Sleep(2.236)
    ACT.MouseClick((0.528, 0.487))
    ACT.Battle("ChaosWeaver", 2)
    ACT.MouseClick((0.528, 0.487))
    ACT.AwaitImg("DarkTower/txt1#(0.365, 0.004, 0.627, 0.028).png", timeout=30)
    ACT.CutsceneEnd("DarkTower/#(0.402, 0.377, 0.614, 0.445).png")
    ACT.ClickIf("DarkTower/#(0.402, 0.377, 0.614, 0.445).png")
    ACT.QuestComplete.Await().Close()
    ACT.MouseClick((0.5, 0.5))
    ACT.NewItem.Await().Keep()
    return False


def Trithril():
    ACT.LoreBook.Pot()
    ACT.MouseClick((0.827, 0.8))
    ACT.AwaitImg("Trithril/#(0.255, 0.089, 0.509, 0.361).png", timeout=13)
    ACT.ClickIf("Trithril/#(0.689, 0.34, 0.829, 0.386).png", timeout=10.914)
    ACT.ClickIf("Trithril/#(0.674, 0.128, 0.838, 0.174).png")
    ACT.Sleep(0.3)
    ACT.MouseClick((0.969, 0.799))
    ACT.ClickIf("Trithril/#(0.706, 0.382, 0.862, 0.432).png", timeout=12)
    while not ACT.QuestComplete:
        ACT.Battle("ChaosWeaver", 1)
        ACT.Sleep(1)
    ACT.QuestComplete.Close()
    ACT.MouseClick((0.5, 0.5))
    ACT.Sleep(1)
    ACT.NewItem.Keep()
    return True


def ThroughTheTangle():
    ACT.LoreBook.Pot()
    ACT.ClickIf("ThroughTheTangle/#(0.84, 0.043, 0.974, 0.083).png", timeout=15.9)
    ACT.ClickIf("ThroughTheTangle/#(0.837, 0.267, 0.979, 0.301).png", timeout=8.498)
    ACT.CutsceneEnd("ThroughTheTangle/#(0.385, 0.108, 0.619, 0.386).png")
    ACT.MouseClick((0.675, 0.758))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.675, 0.758))
    ACT.Sleep(3.807)
    ACT.MouseClick((0.302, 0.658))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.228, 0.696))
    ACT.Sleep(3.52)
    ACT.MouseClick((0.017, 0.627))
    ACT.Sleep(3.822)
    ACT.MouseClick((0.221, 0.773))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.221, 0.773))
    ACT.Sleep(3.822)
    ACT.MouseClick((0.428, 0.629))
    ACT.Battle("ChaosWeaver", 2)
    ACT.MouseClick((0.428, 0.629))
    ACT.Sleep(2.827)
    ACT.MouseClick((0.016, 0.651))
    ACT.Sleep(3.446)
    ACT.MouseClick((0.428, 0.541))
    ACT.Battle("ChaosWeaver", 1)
    ACT.Sleep(2.288)
    ACT.MouseClick((0.692, 0.718))
    ACT.Sleep(2.288)
    ACT.MouseClick((0.967, 0.772))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.967, 0.772))
    ACT.Sleep(3.863)
    ACT.MouseClick((0.96, 0.756))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.96, 0.756))
    ACT.Sleep(3.045)
    ACT.MouseClick((0.713, 0.753))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.713, 0.753))
    ACT.Sleep(2.324)
    ACT.MouseClick((0.577, 0.804))
    ACT.Sleep(2.244)
    ACT.Inventory.Heal(False)
    ACT.Inventory.Heal(False)
    ACT.Inventory.Mana(False)
    ACT.Inventory.Mana()
    ACT.MouseClick((0.974, 0.725))
    ACT.Sleep(3.421)
    ACT.MouseClick((0.969, 0.648))
    ACT.Battle("ChaosWeaver", "BOSS")
    ACT.CutsceneEnd("ThroughTheTangle/#(0.378, 0.335, 0.614, 0.405).png")
    ACT.ClickIf("ThroughTheTangle/#(0.378, 0.335, 0.614, 0.405).png", timeout=12.686)
    ACT.MouseClick((0.969, 0.648))
    ACT.QuestComplete()
    ACT.MouseClick((0.5, 0.5))
    ACT.NewItem.Keep()
    return True


def Mushrooms():
    ACT.LoreBook.Pot()
    ACT.MouseClick((0.13, 0.576))
    ACT.ClickIf("Mushrooms/#(0.525, 0.421, 0.669, 0.459).png", timeout=19.442)
    ACT.ClickIf("Mushrooms/#(0.527, 0.364, 0.669, 0.406).png", timeout=7.452)
    ACT.CutsceneEnd("Mushrooms/#(0.323, 0.326, 0.419, 0.412).png")
    ACT.MouseClick((0.97, 0.624))
    ACT.Sleep(3.562)
    ACT.MouseClick((0.965, 0.609))
    ACT.Battle("ChaosWeaver", 2)
    ACT.MouseClick((0.965, 0.609))
    ACT.Sleep(5.011)
    ACT.MouseClick((0.974, 0.55))
    ACT.Battle("ChaosWeaver", 2)
    ACT.MouseClick((0.974, 0.55))
    ACT.Sleep(3.081)
    ACT.MouseClick((0.974, 0.55))
    ACT.Battle("ChaosWeaver", 2)
    ACT.Sleep(3.081)
    ACT.MouseClick((0.025, 0.597))
    ACT.Sleep(2.605)
    ACT.MouseClick((0.025, 0.597))
    ACT.Sleep(2.226)
    ACT.MouseClick((0.555, 0.617))
    ACT.Sleep(3.052)
    ACT.MouseClick((0.647, 0.325))
    ACT.Sleep(2.783)
    ACT.MouseClick((0.012, 0.613))
    ACT.Battle("ChaosWeaver", 2)
    ACT.MouseClick((0.012, 0.613))
    ACT.Sleep(3.538)
    ACT.MouseClick((0.016, 0.58))
    ACT.Battle("ChaosWeaver", 2)
    ACT.MouseClick((0.016, 0.58))
    ACT.Sleep(3.755)
    ACT.MouseClick((0.124, 0.509))
    ACT.Sleep(3.684)
    ACT.MouseClick((0.49, 0.743))
    ACT.Battle("ChaosWeaver", 2)
    ACT.MouseClick((0.49, 0.743))
    ACT.Sleep(3.861)
    ACT.MouseClick((0.807, 0.563))
    ACT.Sleep(1.701)
    ACT.MouseClick((0.197, 0.291))
    ACT.Battle("ChaosWeaver", 2)
    ACT.MouseClick((0.197, 0.291))
    ACT.Sleep(3.788)
    ACT.MouseClick((0.043, 0.067))
    ACT.Sleep(3.387)
    ACT.MouseClick((0.29, 0.548))
    ACT.Battle("ChaosWeaver", ("487vc073", "67834"))
    ACT.CutsceneEnd("Mushrooms/#(0.376, 0.321, 0.612, 0.403).png")
    ACT.ClickIf("Mushrooms/#(0.376, 0.321, 0.612, 0.403).png")
    ACT.QuestComplete()
    ACT.MouseClick((0.5, 0.5))
    ACT.NewItem.Keep()
    return True


def ProclamationMedal_SH():
    ACT.ClickIf("ScreenCaps/#(0.834, 0.03, 0.974, 0.09).png", timeout=9.644)
    ACT.ClickIf("ScreenCaps/#(0.828, 0.07100000000000001, 0.986, 0.127).png", timeout=18.792)
    ACT.Sleep(2.157)
    ACT.MouseClick((0.58, -0.014))
    ACT.Sleep(3)
    ACT.MouseClick((0.694, 0.629))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.694, 0.629))
    ACT.Sleep(1.191)
    ACT.MouseClick((0.376, 0.639))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.376, 0.639))
    ACT.Sleep(0.874)
    ACT.MouseClick((0.158, 0.597))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.158, 0.597))
    ACT.Sleep(0.999)
    ACT.MouseClick((0.38, 0.373))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.38, 0.373))
    ACT.Sleep(1.061)
    ACT.MouseClick((0.508, 0.422))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.508, 0.422))


def AARGH():
    # DRAG IS: MAG MISC ASSIST
    ACT.Sleep(1)
    ACT.ClickIf("ScreenCaps/#(0.757, 0.09, 0.931, 0.168).png")
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
        return ACT.AwaitImg("ScreenCaps/#(0.757, 0.09, 0.931, 0.168).png") is not None


def InevitableEquilibrium():  # https://www.youtube.com/watch?v=Zf1pzXccsuc #9:24
    # DRAG IS: 200 0 200 200 0
    def summon_miniphage():
        ACT.Inventory.Build8(False)
        ACT.Inventory.Load()
        ACT.Inventory.Await().Close()
        ACT.Sleep(0.1)

    summon_miniphage()

    def summon_dragon():
        ACT.DragonAmulet.Open()
        ACT.Sleep(0.1)
        ACT.DragonAmulet.Summon.Open()
        ACT.Sleep(0.1)
        ACT.DragonAmulet.Summon.Pet()
        ACT.Sleep(0.1)

    ACT.ClickIf("Inn/start_ie#(0.393, 0.293, 0.595, 0.351).png")
    ACT.AwaitImg(ACT.atkBtn)
    drag = summon_dragon
    mini = summon_miniphage
    # fmt: off
    player_moveset = [*"\tt\t9", [drag, *"e6"], *"c3v", "ez", *"x1796", "ec", *"13", 
                        'ex','n','ec',*'96v','ez',*'1x5n9','e6',*'c3', [mini, *'em']]
    pet_moveset = " \t 3z653   v3z  3  z53   63 "
    if (ACT.Battle("DeathKnight",
            (player_moveset, pet_moveset, ["Inn/lost_ie#(0.351, 0.364, 0.641, 0.448).png"]))
        != ACT.ctnBtn):
        # fmt: on
        ACT.Sleep(0.1)
        ACT.TypeKeys(" ")
        ACT.ClickIf("Inn/lost_ie#(0.351, 0.364, 0.641, 0.448).png")
    InevitableEquilibrium()


def BraughlmurkCrypt():
    ACT.AwaitImg("ScreenCaps/#(0.098, 0.037, 0.336, 0.261).png", timeout=12.574)
    ACT.LoreBook.Pot()
    ACT.Sleep(2.96)
    ACT.MouseClick((0.438, 0.12))
    ACT.Sleep(2.83)
    ACT.MouseClick((0.984, 0.648))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.984, 0.648))
    ACT.Sleep(3.128)
    ACT.MouseClick((0.984, 0.646))
    ACT.Sleep(2.94)
    ACT.MouseClick((0.516, 0.463))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.516, 0.463))
    ACT.Sleep(1.652)
    ACT.MouseClick((0.516, 0.463))
    ACT.Sleep(2.179)
    ACT.MouseClick((0.08, 0.571))
    ACT.Battle("ChaosWeaver", 3)
    ACT.MouseClick((0.08, 0.571))
    ACT.Sleep(2.042)
    ACT.MouseClick((0.029, 0.589))
    ACT.Battle("ChaosWeaver", 2)
    ACT.MouseClick((0.029, 0.589))
    ACT.Sleep(3.929)
    ACT.MouseClick((0.04, 0.609))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.04, 0.609))
    ACT.Sleep(3.197)
    ACT.MouseClick((0.04, 0.609))
    ACT.Battle("ChaosWeaver", 2)
    ACT.MouseClick((0.04, 0.609))
    ACT.Sleep(2.829)
    ACT.MouseClick((0.219, 0.338))
    ACT.Sleep(2.515)
    ACT.MouseClick((0.498, 0.384))
    ACT.Battle("ChaosWeaver", 3)
    ACT.MouseClick((0.498, 0.384))
    ACT.QuestComplete.Await().Close()
    ACT.MouseClick((0.5, 0.5))
    ACT.NewItem.Await().Keep()


def BraughlmurkTower():
    ACT.AwaitImg("ScreenCaps/#(0.078, 0.015, 0.158, 0.421).png", timeout=8.828)
    ACT.LoreBook.Pot()
    ACT.Sleep(2.49)
    ACT.MouseClick((0.617, 0.261))
    ACT.Sleep(4.011)
    ACT.MouseClick((0.059, 0.432))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.059, 0.432))
    ACT.Sleep(2.009)
    ACT.MouseClick((0.194, 0.212))
    ACT.Sleep(1.818)
    ACT.MouseClick((0.097, 0.55))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.097, 0.55))
    ACT.Sleep(2.229)
    ACT.MouseClick((0.153, 0.284))
    ACT.Sleep(1.677)
    ACT.MouseClick((0.165, 0.529))
    ACT.Battle("ChaosWeaver", 3)
    ACT.MouseClick((0.165, 0.529))
    ACT.Sleep(2.489)
    ACT.MouseClick((0.13, 0.251))
    ACT.Sleep(1.45)
    ACT.MouseClick((0.089, 0.548))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.089, 0.548))
    ACT.Sleep(1.767)
    ACT.MouseClick((0.168, 0.215))
    ACT.Sleep(1.377)
    ACT.MouseClick((0.113, 0.583))
    ACT.Battle("ChaosWeaver", 2)
    ACT.MouseClick((0.113, 0.583))
    ACT.Sleep(2.626)
    ACT.MouseClick((0.167, 0.207))
    ACT.Sleep(1.721)
    ACT.MouseClick((0.091, 0.561))
    ACT.Battle("ChaosWeaver", 1)
    ACT.MouseClick((0.091, 0.561))
    ACT.Sleep(2.122)
    ACT.MouseClick((0.157, 0.243))
    ACT.Sleep(2.355)
    ACT.MouseClick((0.457, 0.487))
    ACT.Battle("ChaosWeaver", 2)
    ACT.MouseClick((0.457, 0.487))
    ACT.Sleep(2.059)
    ACT.MouseClick((0.501, 0.249))
    ACT.Sleep(1.634)
    ACT.MouseClick((0.906, 0.651))
    ACT.Battle("ChaosWeaver", 3)
    ACT.MouseClick((0.906, 0.651))
    ACT.QuestComplete.Await().Close()
    ACT.MouseClick((0.5, 0.5))
    ACT.NewItem.Await().Keep()


if __name__ == "__main__":
    pass
    # exit()
    # while not ACT.QuestComplete:
    #     ACT.Battle("ChaosWeaver", -3)
    #     ACT.Sleep(1)
    # InevitableEquilibrium()
    # [BraughlmurkTower() for _ in range(6)]
    # all(iter(AARGH, False))
    all(iter(BicentennialDragonLord, False))
    # globals()['func_name']()
