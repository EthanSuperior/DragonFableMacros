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
    STR: int = 0
    DEX: int = 0
    INT: int = 0
    CHA: int = 0
    LUK: int = 0
    END: int = 0
    WIS: int = 0
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
    dmg_type: str = "Fear"
    non_crit_mult: float = 0.0
    crit_mult: float = 0.0
    dex_mult: float = 0.0
    dot_mult: float = 0.0
    bonus_base: float = 0.0
    _hit_damage: float = 0.0
    _crit_damage: float = 0.0

    def clone(self):
        return replace(self)

    @classmethod
    def fromMain(cls, STR, DEX, INT, CHA, LUK, END, WIS, LVL: int = None):
        return cls(
            STR=STR,
            DEX=DEX,
            INT=INT,
            CHA=CHA,
            LUK=LUK,
            END=END,
            WIS=WIS,
            WPN_DMG=max(STR, DEX, INT) // 10,
            non_crit_mult=(STR * 3 / 2000) + (1 if LVL else 0),
            dex_mult=(DEX / 4000) + (1 if LVL else 0),
            dot_mult=(DEX / 400) + (1 if LVL else 0),
            crit_mult=(INT / 1000) + (1.75 if LVL else 0),
            # pet_dmg=CHA // 10,
            # pet_cdr=min(CHA // 50, 4),
            CRIT=(LUK // 10) + (5 if LVL else 0),
            MPM=(LUK // 10) + (5 if LVL else 0),
            BPD=LUK // 10,
            MaxHP=(END * 5) + (((20 * (LVL - 1)) + 100) if LVL else 0),
            RESIST=Resistances({"immobility": END // 5, "health": -(WIS // 20)}),
            MaxMP=(WIS * 5) + (((5 * (LVL - 1)) + 100) if LVL else 0),
            BONUS=WIS // 10,
        )


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
