from BattleSim.data import Effect, Stats, Ability, Unit
from BattleSim.simulator import Simulator, SimulatorNode, NodeInfo
from BattleSim.custom import DeathKnight


# --- Test Abilities ---
class GuaranteedHit(Ability):
    def __init__(self):
        self.free_action = False
        self.extra_turn = False
        self.hits = 1
        self.hit_dmg = 0.4


class BossAtk(Ability):
    def __init__(self):
        self.free_action = False
        self.extra_turn = False
        self.hits = 1
        self.hit_dmg = 1


class MultiHit(Ability):
    def __init__(self):
        self.free_action = False
        self.extra_turn = False
        self.hits = 2
        self.hit_dmg = 2
        self.cd = 2  # 2 turns inbetween


class BuffCrit(Ability):
    def __init__(self):
        self.hits = 0
        self.free_action = False
        self.extra_turn = False
        self.cd = 2

    def pre_atk(self, node, idx, target):
        # Clone stats for the node
        new_node = node.clone()
        new_node.data[idx].effect_durations[0] = 3  # 4 turns inclusive....
        new_node
        return [new_node]


class CritEffect(Effect):
    def apply(self, char):
        char.CRIT += 00
        return char


# --- Test Units ---
class TestPlayer(Unit):
    def __init__(self, hp, dmg):
        abilities = [GuaranteedHit(), MultiHit(), BuffCrit()]
        effects = [CritEffect()]
        stats = Stats(MaxHP=hp, _hit_damage=dmg, _crit_damage=2 * dmg, target=1, dmg_type="None")
        super().__init__(abilities, effects, stats)


class TestBoss(Unit):
    def __init__(self, hp, dmg):
        abilities = [BossAtk()]
        effects = []
        stats = Stats(MaxHP=hp, _hit_damage=dmg, _crit_damage=2 * dmg, target=0, dmg_type="None")
        super().__init__(abilities, effects, stats)


# Create player (10 dmg per turn) and boss (5 dmg per turn)
player = TestPlayer(hp=50, dmg=5)
boss = TestBoss(hp=50, dmg=6)

DeathKnight([0, 0, 0, 0, 0, 0, 0], Stats(), None, [])
exit()
# --- Run simulation ---
sim = Simulator(player, None, boss)  # pet=None
best_path = sim.run()

# --- Check result ---
print("Best Path:", best_path)
