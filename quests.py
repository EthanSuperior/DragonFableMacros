from actions import ACT


def BicentennialDragonLord():
    startWaveBtn = "./BicentennialDragonLord/startMatch#(0.713, 0.633, 0.893, 0.687).png"
    waves = [
        "./BicentennialDragonLord/eastWave1#(0, 0.2, 1, 1).png",
        "./BicentennialDragonLord/westWave2#(0, 0.2, 1, 1).png",
        "./BicentennialDragonLord/eastWave3#(0, 0.2, 1, 1).png",
    ]
    ACT.BattleWar(startWaveBtn, waves, [[2, 2, 2], [2, 2, 2], [2, 2, 2]])


def ChallengerBelt():
    def RestartChallenge():
        ACT.AwaitImg(ACT.atkBtn)
        ACT.Sleep(0.2)
        ACT.ClickIf("ScreenCaps/#(0.463, 0.955, 0.533, 0.977).png", timeout=17.08)
        ACT.ClickIf("ScreenCaps/#(0.442, 0.755, 0.556, 0.793).png", timeout=16.868)
        ACT.ClickIf("ScreenCaps/#(0.384, 0.494, 0.486, 0.53).png", timeout=18.162)
        ACT.ClickIf("ScreenCaps/#(0.353, 0.371, 0.633, 0.451).png", timeout=11.304)

    while True:
        ACT.ClickIf("ScreenCaps/#(0.095, 0.407, 0.289, 0.463).png", timeout=30)
        for _ in range(7):
            if ACT.Battle("ChaosWeaver", -2) == ACT.dead:
                RestartChallenge()
                continue
        if ACT.Battle("ChaosWeaver", "VERLYRUS?") == ACT.dead:
            RestartChallenge()
            continue
        ACT.AwaitImg(ACT.questPass)
        ACT.ClickIf(ACT.questClose)
        ACT.AwaitImg(ACT.newItem)
        ACT.ClickIf(ACT.keepItem)


# ACT.AwaitImg("dead#(0.055, 0.905, 0.193, 0.931).png", timeout=25.11)
# ACT.ClickIf("ScreenCaps/#(0.451, 0.587, 0.577, 0.619).png", timeout=21.184)
# ACT.Sleep(5.307)
# ACT.MouseClick((0.412, 0.84))
# ACT.ClickIf("ScreenCaps/#(0.463, 0.955, 0.533, 0.977).png", timeout=17.08)
# ACT.ClickIf("ScreenCaps/#(0.442, 0.755, 0.556, 0.793).png", timeout=16.868)
# ACT.ClickIf("ScreenCaps/#(0.384, 0.494, 0.486, 0.53).png", timeout=18.162)
# ACT.ClickIf("ScreenCaps/#(0.353, 0.371, 0.633, 0.451).png", timeout=11.304)
# ACT.Sleep(11.913)


# BicentennialDragonLord()
ChallengerBelt()
