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


# while ACT.ClickIf("ChallengerBelt/start*.png", timeout=30):
while True:
    # BicentennialDragonLord()
    ChallengerBelt()
# globals()['func_name']()
