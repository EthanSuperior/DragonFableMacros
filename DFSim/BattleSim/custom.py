from BattleSim.data import Effect, Resistances, Stats, Ability, Unit
from BattleSim.simulator import Simulator, SimulatorNode, NodeInfo


class Player(Unit):
    def __init__(self, stats: Stats, abilities: list[Ability], effects: list[Effect]):
        if not isinstance(stats.WPN_DMG, int):
            stats.WPN_DMG = sum(stats.WPN_DMG) / 2
        stats._hit_damage = stats.WPN_DMG * stats.non_crit_mult * stats.dex_mult
        stats._crit_damage = stats.WPN_DMG * stats.crit_mult * stats.dex_mult
        stats.target = -1
        super().__init__(abilities, effects, stats)


class DeathKnight(Player):
    def __init__(self, stats: tuple[int, ...], trinket_stats, trinket_ability, trinket_effects=[]):
        stats: Stats = Stats.fromMain(
            *[
                x + y
                for x, y in zip(stats, [69 + 15, 69 + 15, 69 + 15, 3 + 8, 15 + 8, 73 + 4, 73 + 4])
            ],
            LVL=90
        )
        stats.BPD += 26 + 5
        stats.MPM += 40 + 5
        stats.BONUS += 65 + 14
        stats.CRIT += 65 + 14
        stats.RESIST += Resistances(
            {
                "light": 70 + 10,
                "dark": 70 + 10,
                "good": 22 + 5,
                "evil": 22 + 5,
                "all": 1,
                "immobility": 25,
                "health": -14,
            }
        )
        stats.WPN_DMG = [95, 100, stats.WPN_DMG]
        trinket_ability.cd -= min(stats.LUK // 50, 4)
        abilities = [] + [trinket_ability]
        effects = [] + trinket_effects
        super().__init__(stats, abilities, effects)
        print(self.stats, self.stats.RESIST["immobility"])
