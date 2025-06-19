from actions import ACT


def BicentennialDragonLord():
    startWaveBtn = "./BicentennialDragonLord/startMatch#(0.713, 0.633, 0.893, 0.687).png"
    waves = [
        "./BicentennialDragonLord/eastWave1#(0, 0.2, 1, 1).png",
        "./BicentennialDragonLord/westWave2#(0, 0.2, 1, 1).png",
        "./BicentennialDragonLord/eastWave3#(0, 0.2, 1, 1).png",
    ]
    ACT.BattleWar(startWaveBtn, waves, [[2, 2, 2], [2, 2, 2], [2, 2, 2]])


BicentennialDragonLord()
