from BattleSim.data import Effect, Resistances, Stats, Ability, Unit
from BattleSim.simulator import Simulator, SimulatorNode, NodeInfo


class Player(Unit):
    def __init__(self, stat_screen: Stats, abilities: list[Ability], effects: list[Effect]):
        new_stats = stat_screen.clone()
        new_stats.WPN_DMG = sum(new_stats.WPN_DMG) / (
            len(new_stats.WPN_DMG) if isinstance(new_stats.WPN_DMG, int) else 1
        )
        new_stats._hit_damage = new_stats.WPN_DMG * new_stats.non_crit_mult * new_stats.dex_mult
        new_stats._crit_damage = new_stats.WPN_DMG * new_stats.crit_mult * new_stats.dex_mult
        new_stats.target = 1
        super().__init__(abilities, effects, new_stats)
