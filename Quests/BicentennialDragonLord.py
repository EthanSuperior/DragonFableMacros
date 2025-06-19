import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../Utils")))
from ratio_based_ui import DF_ACT

startWaveBtn = "./BicentennialDragonLord/startMatch#(0.713, 0.633, 0.893, 0.687).png"
waves = [
    "./BicentennialDragonLord/eastWave1#(0, 0.2, 1, 1).png",
    "./BicentennialDragonLord/westWave2#(0, 0.2, 1, 1).png",
    "./BicentennialDragonLord/eastWave3#(0, 0.2, 1, 1).png",
]
DF_ACT.BattleWar(startWaveBtn, waves, [[2, 2, 2], [2, 2, 2], [2, 2, 2]])
