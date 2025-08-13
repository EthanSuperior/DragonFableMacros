from BattleSim.simulator import Simulator

player = DeathKnight([200, 200, 200, 0, 0, 0], trinket)
pet = KidDragon([200, 200, 200, 0, 0])
Simulator(player, pet, Drakath()).run()
