from ..engine.character import Character
from ..engine.stats import Stats
from ..engine.abilities import Ability
from ..engine.effects import Effect


class DeathKnight(Character):
    def __init__(self, player_stats: Stats):
        """
        Creates a DeathKnight character with its unique abilities and stats.

        Returns:
            A Character object representing the DeathKnight.
        """

        # Base stats for a level 90 DeathKnight
        base_stats = Stats(
            MaxHP=2000,  # Placeholder, adjust as needed
            CurrMP=1500,  # Placeholder, adjust as needed
            STR=0,
            DEX=0,
            INT=200,
            END=200,
            CHA=0,
            LUK=0,
        )

        abilities = [
            Ability(name="Toggle Presence", hotkey="e", cost=0, cooldown=0),
            Ability(
                name="Shift", hotkey="z", cost=40, cooldown=4, custom_logic=self.deathknight_shift
            ),
            Ability(name="Blood Tap", hotkey="x", cost=25, cooldown=3),
            Ability(name="Soul Slash", hotkey="1", cost=30, cooldown=2),
            Ability(name="Unholy Shadow", hotkey="2", cost=50, cooldown=5),
            Ability(name="Obliterate", hotkey="3", cost=80, cooldown=8),
            Ability(name="Instill Fear", hotkey="4", cost=35, cooldown=3),
            Ability(name="Garb of Undeath", hotkey="5", cost=70, cooldown=10),
            Ability(name="Attack", hotkey=" ", cost=0, cooldown=0),
            Ability(name="Inspire Weakness", hotkey="6", cost=35, cooldown=3),
            Ability(name="Unholy Will", hotkey="7", cost=55, cooldown=7),
            Ability(name="Dark Rite", hotkey="8", cost=50, cooldown=5),
            Ability(name="Strength Reap", hotkey="9", cost=60, cooldown=6),
            Ability(name="Edge of Death", hotkey="0", cost=90, cooldown=12),
            Ability(name="Cursed Strike", hotkey="c", cost=30, cooldown=2),
            Ability(name="Call of Dead", hotkey="v", cost=100, cooldown=15),
            Ability(name="Use Health Potion", hotkey="h", cost=0, cooldown=0, uses=2, heal=1045),
            Ability(name="Use Mana Potion", hotkey="m", cost=0, cooldown=0, uses=2, mana_gain=425),
        ]

        super().__init__(
            name="DeathKnight",
            abilities=abilities,
            base_stats=base_stats + player_stats,
        )

        # Add Consuming and Healing Presence effects
        self.add_effect(
            Effect(
                name="Consuming Presence",
                duration=-1,
                stat_mods={"plus_base_dmg": 1.0, "BONUS": 50, "CRIT": 50},
            )
        )
        self.add_effect(Effect(name="Healing Presence", duration=-1, percent_heal=0.03))

    def deathknight_shift(self, user, target, chance):
        if any(e.name == "Consuming Presence" for e in user.effects):
            # Damage logic
            ability = Ability(name="Shift", damage_multiplier=1.5)  # Placeholder damage
            return ability.use(user, target, chance)
        elif any(e.name == "Healing Presence" for e in user.effects):
            # Healing logic
            user.heal(500)  # Placeholder heal amount
            return [(user, target, chance)]
