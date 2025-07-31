from ..engine.character import Character
from ..engine.stats import Stats
from ..engine.abilities import Ability
from ..engine.effects import Effect


class Dragon(Character):
    def __init__(self, element: str, training: dict):
        """
        Creates a pet dragon character based on its element and training.

        Args:
            element: The dragon's element (e.g., 'fire', 'water').
            training: A dictionary specifying the dragon's training points in different skill trees.
                      Example: {'protection': 200, 'magic': 100, 'fighting': 150, 'assistance': 100, 'mischief': 50}
        """

        # Base stats for a level 90 Kid Dragon
        base_stats = Stats(
            MaxHP=1000,  # Placeholder, adjust as needed
            CurrMP=500,  # Placeholder, adjust as needed
            STR=0,
            DEX=0,
            INT=0,
            END=0,
            CHA=0,
            LUK=0,
        )

        abilities = []

        if training.get("protection", 0) > 0:
            abilities.append(
                Ability(
                    name="Protect",
                    hotkey="6",
                    cost=80,
                    cooldown=10,
                    on_hit_effects=[
                        Effect(name="Dragon Shield", duration=1, stat_mods={"BDP": 100})
                    ],
                )
            )  # Placeholder BDP value
        if training.get("fighting", 0) > 0:
            abilities.append(
                Ability(
                    name="Tail Lash",
                    hotkey="3",
                    cost=40,
                    cooldown=4,
                    on_hit_effects=[Effect(name="Dragon's Fire", duration=3, flat_dmg=100)],
                )
            )
        if training.get("assistance", 0) > 0:
            abilities.append(
                Ability(
                    name="Rally",
                    hotkey="9",
                    cost=50,
                    cooldown=6,
                    on_hit_effects=[
                        Effect(name="Rally", duration=3, stat_mods={"BONUS": 20, "BOOST": 20})
                    ],
                )
            )
        if training.get("mischief", 0) > 0:
            abilities.append(
                Ability(
                    name="Distract",
                    hotkey="0",
                    cost=10,
                    cooldown=2,
                )
            )

        super().__init__(
            name=f"{element.capitalize()} Dragon",
            abilities=abilities,
            base_stats=base_stats,
        )

        # Dragon effects target the player
        for ability in self.abilities:
            ability.target_self = False  # This is a simplified assumption
