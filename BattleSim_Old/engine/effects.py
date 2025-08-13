import copy


class Effect:
    def __init__(
        self,
        name,
        duration,
        target="self",  # or 'enemy'
        timing="on_hit",  # or 'pre_attack', 'post_attack'
        stat_mods=None,
        resist_mods=None,
        flat_dmg=0,
        percent_dmg=0.0,
        percent_heal=0.0,
        heal_resist=False,
        chance=1.0,
    ):
        self.name = name
        self.duration = duration
        self.remaining = duration
        self.target = target
        self.timing = timing
        self.stat_mods = stat_mods or {}
        self.resist_mods = resist_mods or {}
        self.flat_dmg = flat_dmg
        self.percent_dmg = percent_dmg
        self.percent_heal = percent_heal
        self.heal_resist = heal_resist
        self.chance = chance
        self.on_expire = None

    def copy(self):
        return copy.deepcopy(self)

    def apply(self, stats):
        """Apply stat and resistance modifications."""
        modified = stats.copy()
        for attr, val in self.stat_mods.items():
            setattr(modified, attr, getattr(modified, attr) + val)
        for r_type, val in self.resist_mods.items():
            modified.resistances[r_type] += val
        return modified

    def update(self, character):
        """Apply per-turn damage/healing if needed."""
        if self.remaining <= 0:
            return
        if self.flat_dmg != 0 or self.percent_dmg != 0 or self.percent_heal != 0:
            stats = character.get_stats()
            resist = stats.Resist.get("all", 0)
            modifier = (100 - resist) / 100.0
            base = self.flat_dmg + (self.percent_dmg * stats.MaxHP)
            dmg = base * modifier * (1 + stats.plus_dot_dmg)

            if self.heal_resist:
                character.damage(dmg, source="effect")
            else:
                character.hp += dmg

            if self.percent_heal != 0:
                character.heal(character.base_stats.MaxHP * self.percent_heal)
        self.remaining -= 1