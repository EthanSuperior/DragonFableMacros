from dataclasses import dataclass, replace
import numpy as np
import abc


class Resistances:
    def __init__(self, vals={}):
        self.values = vals
        self.bth = vals.get("bth", 0.0)
        self.health = vals.get("health", 0.0)
        self.immobility = vals.get("immobility", 0.0)

    def __add__(self, other):
        new_vals = self.values.copy()
        other_dict = other.values if isinstance(other, Resistances) else other
        for k, v in other_dict.items():
            new_vals[k] = new_vals.get(k.lower(), 0.0) + v

        new_resist = Resistances(new_vals)
        new_resist.bth += other.bth if isinstance(other, Resistances) else other.get("bth", 0.0)
        new_resist.health += (
            other.health if isinstance(other, Resistances) else other.get("health", 0.0)
        )
        new_resist.immobility += (
            other.immobility if isinstance(other, Resistances) else other.get("immobility", 0.0)
        )
        return new_resist

    def __getitem__(self, key):
        return min(
            self.values.get(key.lower(), 0.0) + self.values.get("all", 0.0),
            self.values.get("max", 4000),
        )


@dataclass
class Stats:  # skip main 6 stats, these are all the secondary stats....
    MaxHP: int = 0
    MinHP: int = 0  # used for boss stages
    MinHPDirect: int = 0  # used for deathproof and boss stages
    MaxMP: int = 0
    CRIT: float = 0.0
    BONUS: float = 0.0
    BOOST: float = 0.0
    MPM: float = 0.0
    BPD: float = 0.0
    RESIST: Resistances = Resistances({})
    WPN_DMG: float = 0.0
    target: int = 0
    dmg_type: int = 0
    _hit_damage: float = 0.0
    _crit_damage: float = 0.0

    def clone(self):
        return replace(self)


# TODO: Make helper to calculate actual damage somewhere.....


class Unit(abc.ABC):
    def __init__(self, abilities, effects, stats):
        super().__init__()
        self.abilities = abilities
        self.effects = effects
        self.stats = stats


class Effect(abc.ABC):
    def set_id(self, id):
        self.id = id
        return id

    def apply(self, char: Stats):
        return char


class Ability(abc.ABC):
    hits = 1
    hit_dmg = 1
    cd = 0

    def set_id(self, id):
        self.id = id
        if self.free_action:
            self.cd = max(self.cd, 1)
        return id

    def pre_atk(self, node, idx, target_idx):  # used for instant things like change precense
        return [node]

    def on_hit(self, node, idx, target_idx):
        return node

    def post_atk(self, node, idx, target_idx):
        return [node]
