from engine.abilities import Ability
from engine.character import Character
from engine.effects import Effect
from engine.stats import Stats


class SoulSlash(Ability):
    def __init__(self):
        super().__init__(
            name="Soul Slash",
            cost=25,
            cooldown=4,
            hits=3,
            damage_multiplier=0.3333,
            post_attack_effects=[
                Effect(
                    name="Soul Slash",
                    duration=5,
                    target="enemy",
                    percent_dmg=0.8,
                    chance=1.0,
                )
            ],
        )


class Obliterate(Ability):
    def __init__(self):
        super().__init__(
            name="Obliterate",
            cost=50,
            cooldown=6,
            hits=1,
            damage_multiplier=2.0,
        )


class Attack(Ability):
    def __init__(self):
        super().__init__(name="Attack", cost=0, cooldown=0, hits=1, damage_multiplier=1.0)


class InspireWeakness(Ability):
    def __init__(self):
        super().__init__(
            name="Inspire Weakness",
            cost=30,
            cooldown=5,
            hits=1,
            damage_multiplier=0.5,
            post_attack_effects=[
                Effect(
                    name="Inspired Weakness",
                    duration=3,
                    target="enemy",
                    stat_mods={"reduce_noncrit_dmg": 0.2, "reduce_crit_dmg": 0.2},
                    chance=1.0,
                )
            ],
        )


class DeathKnight(Character):
    def __init__(self, base_stats: Stats, effects=None):
        super().__init__(
            "DeathKnight",
            [
                SoulSlash(),
                Obliterate(),
                Attack(),
                InspireWeakness(),
            ],
            base_stats,
            effects,
        )