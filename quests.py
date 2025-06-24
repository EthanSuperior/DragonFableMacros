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
    ACT.AwaitImg("DarkTower/txt1#(0.365, 0.004, 0.627, 0.028).png", timeout=30)
    ACT.MouseClick((0.964, 0.777), times=7)
    ACT.Sleep(0.1)
    ACT.ClickIf("DarkTower/txt2#(0.365, 0.003, 0.627, 0.033).png", timeout=30)
    ACT.Sleep(0.1)
    ACT.ClickIf("DarkTower/txt3#(0.359, 0.008, 0.631, 0.032).png", timeout=30)
    ACT.AwaitImg("DarkTower/inQuest#(0.472, 0.019, 0.626, 0.277).png", timeout=30)
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
    ACT.ClickIf("DarkTower/#(0.359, 0.006, 0.629, 0.03).png", timeout=23.89)
    ACT.AwaitImg("DarkTower/#(0.356, 0.006, 0.63, 0.03).png", timeout=15.848)
    ACT.MouseClick((0.964, 0.777), times=44)
    ACT.Sleep(2)
    ACT.MouseClick((0.964, 0.777), times=5)
    ACT.Sleep(0.1)
    ACT.AwaitImg("DarkTower/#(0.357, 0.002, 0.631, 0.032).png", timeout=13.808)
    ACT.ClickIf("DarkTower/#(0.36, 0.006, 0.632, 0.03).png", timeout=16.274)
    ACT.ClickIf("DarkTower/#(0.361, 0.01, 0.631, 0.034).png", timeout=9.762)
    ACT.Sleep(0.1)
    ACT.ClickIf("DarkTower/#(0.361, 0.01, 0.631, 0.034).png", timeout=9.762)
    ACT.ClickIf("DarkTower/#(0.362, 0.01, 0.634, 0.032).png", timeout=14.012)
    ACT.Sleep(3)
    ACT.ClickIf("DarkTower/#(0.361, 0.76, 0.631, 0.796).png", timeout=36.896)
    ACT.MouseClick((0.964, 0.777), times=6)
    ACT.ClickIf("DarkTower/#(0.402, 0.377, 0.614, 0.445).png", timeout=6)
    ACT.QuestComplete.Close()
    ACT.MouseClick((0.5, 0.5))
    ACT.NewItem.Keep()


if __name__ == "__main__":
    # while ACT.ClickIf("ChallengerBelt/start*.png", timeout=30):
    # DarkTower()
    # exit()
    while BicentennialDragonLord(): pass
        # ChallengerBelt()
    # globals()['func_name']()
