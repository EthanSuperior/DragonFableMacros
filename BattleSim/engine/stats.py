from dataclasses import dataclass
from typing import Dict


class Resistances:
    values: Dict[str, float]

    def __init__(self, vals={}):
        self.values = vals

    def __add__(self, other):
        new_vals = self.values.copy()
        other_dict = other.values if isinstance(other, Resistances) else other
        for k, v in other_dict.items():
            new_vals[k] = new_vals.get(k.lower(), 0.0) + v
        return Resistances(new_vals)

    def __getitem__(self, key):
        return max(
            self.values.get(key.lower(), 0.0) + self.values.get("all", 0.0),
            self.values.get("max", 4000),
        )


@dataclass
class Stats:
    STR: int = 0
    DEX: int = 0
    INT: int = 0
    CHA: int = 0
    LUK: int = 0
    END: int = 0
    WIS: int = 0
    CRIT: float = 0.0
    BONUS: float = 0.0
    BOOST: float = 0.0
    MPM: float = 0.0
    BDP: float = 0.0
    Resist: Resistances = Resistances({})
    MaxHP: int = 0
    MaxMP: int = 0
    CurrMP: int = 0
    plus_dmg: float = 0.0
    plus_dot_dmg: float = 0.0
    plus_noncrit_dmg: float = 0.0
    plus_crit_dmg: float = 0.0
    plus_base_dmg: float = 0.0
    reduce_noncrit_dmg: float = 0.0
    reduce_dot_dmg: float = 0.0
    reduce_crit_dmg: float = 0.0
    immobility_resist: float = 0.0
    bth: float = 0.0
    health_resist: float = 0.0

    def __add__(self, other):
        return Stats(
            STR=self.STR + other.STR,
            DEX=self.DEX + other.DEX,
            INT=self.INT + other.INT,
            CHA=self.CHA + other.CHA,
            LUK=self.LUK + other.LUK,
            END=self.END + other.END,
            WIS=self.WIS + other.WIS,
            CRIT=self.CRIT + other.CRIT,
            BONUS=self.BONUS + other.BONUS,
            BOOST=self.BOOST + other.BOOST,
            MPM=self.MPM + other.MPM,
            BDP=self.BDP + other.BDP,
            Resist=self.Resist + other.Resist,
            MaxHP=self.MaxHP + other.MaxHP,
            MaxMP=self.MaxMP + other.MaxMP,
            CurrMP=self.CurrMP + other.CurrMP,
            plus_dmg=self.plus_dmg + other.plus_dmg,
            plus_dot_dmg=self.plus_dot_dmg + other.plus_dot_dmg,
            plus_noncrit_dmg=self.plus_noncrit_dmg + other.plus_noncrit_dmg,
            plus_crit_dmg=self.plus_crit_dmg + other.plus_crit_dmg,
            plus_base_dmg=self.plus_base_dmg + other.plus_base_dmg,
            reduce_noncrit_dmg=self.reduce_noncrit_dmg + other.reduce_noncrit_dmg,
            reduce_dot_dmg=self.reduce_dot_dmg + other.reduce_dot_dmg,
            reduce_crit_dmg=self.reduce_crit_dmg + other.reduce_crit_dmg,
            immobility_resist=self.immobility_resist + other.immobility_resist,
            bth=self.bth + other.bth,
            health_resist=self.health_resist + other.health_resist,
        )
