import random
from .character import Character


def get_dmg_multiplier(user: Character, target: Character, is_crit=False):
    u_stats = user.get_stats()
    t_stats = target.get_stats()

    # Non-crit and crit multipliers
    non_crit_mult = (u_stats.STR * 3 / 20) / 100
    crit_mult = (u_stats.INT / 10) / 100

    # Resistances
    resist = t_stats.Resist[user.element] / 100

    # Damage reduction
    if is_crit:
        dr = (u_stats.plus_crit_dmg + crit_mult) * (1 - t_stats.reduce_crit_dmg)
    else:
        dr = (u_stats.plus_noncrit_dmg + non_crit_mult) * (1 - t_stats.reduce_noncrit_dmg)

    return (
        (1 + u_stats.plus_base_dmg / 100)
        * (1 + u_stats.BOOST / 100)
        * (1 - (resist / 100))
        * dr
    )


def calculate_mpm_chance(user: Character, target: Character):
    u_stats = user.get_stats()
    return u_stats.MPM / 100


def cacluate_bdp_chance(user: Character, target: Character):
    u_stats = user.get_stats()
    return u_stats.BDP / 100


def calculate_crit_chance(user: Character, target: Character):
    u_stats = user.get_stats()
    return u_stats.CRIT / 100

