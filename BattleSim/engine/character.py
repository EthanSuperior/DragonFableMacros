from engine.stats import Stats
from engine.effects import Effect
from engine.abilities import Ability
from engine.simulator import SimulationNode
import copy


class Character:
    def __init__(self, name: str, abilities: list[Ability], base_stats: Stats, effects=None):
        self.name = name
        self.element = "fear"
        self.abilities = abilities
        self.base_stats = base_stats
        self.effects = effects if effects is not None else []
        self.hp = base_stats.MaxHP
        self.mp = base_stats.CurrMP
        self.ability_cooldowns = {ability.name: 0 for ability in self.abilities}

    def copy(self):
        new_char = Character(
            self.name,
            [a.copy() for a in self.abilities],
            self.base_stats,
            [e.copy() for e in self.effects],
        )
        new_char.hp = self.hp
        new_char.mp = self.mp
        new_char.ability_cooldowns = self.ability_cooldowns.copy()
        return new_char

    def get_stats(self) -> Stats:
        current = copy.deepcopy(self.base_stats)
        for eff in self.effects:
            if eff.remaining > 0:
                current = eff.apply(current)
        return current

    def add_effect(self, effect: Effect):
        self.effects.append(effect.copy())

    def tick(self):
        """Run `update()` on all active effects and remove expired ones."""
        alive_effects = []
        for effect in self.effects:
            effect.update(self)
            if effect.remaining > 0:
                alive_effects.append(effect)
        self.effects = alive_effects

        for ability_name, cooldown in self.ability_cooldowns.items():
            if cooldown > 0:
                self.ability_cooldowns[ability_name] -= 1

    def is_dead(self) -> bool:
        return self.hp <= 0

    def heal(self, amount: float):
        new = self.copy()
        new.hp = min(self.hp + amount, self.base_stats.MaxHP)
        return new

    def damage(self, amount: float):
        new = self.copy()
        new.hp = max(self.hp - amount, 0)
        return new

    def __str__(self):
        return f"{self.name}: HP: {self.hp:.1f} | MP: {self.mp}"
