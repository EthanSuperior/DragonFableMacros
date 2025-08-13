from __future__ import annotations
from .stats import Stats
from .effects import Effect
from typing import TYPE_CHECKING
import copy

if TYPE_CHECKING:
    from .abilities import Ability


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
        self.ability_uses = {
            ability.name: ability.uses for ability in self.abilities if ability.uses is not None
        }
        self.takes_turn = True

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
        new_char.ability_uses = self.ability_uses.copy()
        new_char.takes_turn = self.takes_turn
        return new_char

    def get_stats(self) -> Stats:
        current = copy.deepcopy(self.base_stats)
        for eff in self.effects:
            if eff.remaining > 0:
                current = eff.apply(current)
        return current

    def add_effect(self, effect: Effect):
        self.effects.append(effect.copy())

    def update(self):
        """Run `update()` on all active effects and remove expired ones."""
        alive_effects = []
        for effect in self.effects:
            new_effect = effect.copy()
            new_effect.update(self)
            if new_effect.remaining > 0:
                alive_effects.append(new_effect)
            elif new_effect.on_expire:
                for key, value in new_effect.on_expire.items():
                    if key == "heal":
                        self.heal(self.base_stats.MaxHP * value)

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

    def damage(self, amount: float, source: str = "ability"):
        new = self.copy()
        if source == "ability" and any(e.name == "The Edge of Death" for e in new.effects):
            new.hp = max(new.hp - amount, 1)
        else:
            new.hp = max(new.hp - amount, 0)
        return new

    def __str__(self):
        return f"{self.name}: HP: {self.hp:.1f} | MP: {self.mp}"
