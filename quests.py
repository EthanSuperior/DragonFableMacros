from actions import ACT


def BicentennialDragonLord():
    startWaveBtn = "./BicentennialDragonLord/start#(0.713, 0.633, 0.893, 0.687).png"
    waves = [
        "./BicentennialDragonLord/eastWave1#(0, 0.2, 1, 1).png",
        "./BicentennialDragonLord/westWave2#(0, 0.2, 1, 1).png",
        "./BicentennialDragonLord/eastWave3#(0, 0.2, 1, 1).png",
    ]
    if ACT.ClickIf(startWaveBtn, timeout=20):  # True
        ACT.BattleWar(waves, [[2, 2, 2], [2, 2, 2], [2, 2, 2]])
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
    ACT.AwaitImg("ScreenCaps/#(0.255, 0.089, 0.509, 0.361).png", timeout=13)
    ACT.ClickIf("ScreenCaps/#(0.689, 0.34, 0.829, 0.386).png", timeout=10.914)
    ACT.ClickIf("ScreenCaps/#(0.674, 0.128, 0.838, 0.174).png")
    ACT.Sleep(0.3)
    ACT.MouseClick((0.969, 0.799))
    ACT.ClickIf("ScreenCaps/#(0.706, 0.382, 0.862, 0.432).png", timeout=12)
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
    ACT.ClickIf("ScreenCaps/#(0.84, 0.043, 0.974, 0.083).png", timeout=15.9)
    ACT.ClickIf("ScreenCaps/#(0.837, 0.267, 0.979, 0.301).png", timeout=8.498)
    ACT.CutsceneEnd("ScreenCaps/#(0.385, 0.108, 0.619, 0.386).png")
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
    ACT.CutsceneEnd("ScreenCaps/#(0.378, 0.335, 0.614, 0.405).png")
    ACT.ClickIf("ScreenCaps/#(0.378, 0.335, 0.614, 0.405).png", timeout=12.686)
    ACT.MouseClick((0.969, 0.648))
    ACT.QuestComplete()
    ACT.MouseClick((0.5, 0.5))
    ACT.NewItem.Keep()
    return True


if __name__ == "__main__":
    # while ACT.ClickIf("ChallengerBelt/start*.png", timeout=30):
    # DarkTower()
    # exit()
    # iterable = iter(ThroughTheTangle, False)
    (ThroughTheTangle() for _ in range(4))
    # all(iterable)
    # ChallengerBelt()
    # globals()['func_name']()
