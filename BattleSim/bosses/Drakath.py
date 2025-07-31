from ..engine.character import Character
from ..engine.stats import Stats
from ..engine.abilities import Ability
from ..engine.effects import Effect


class Drakath(Character):
    def __init__(self):
        """
        Creates the boss character Drakath, Champion of Chaos.

        Returns:
            A Character object representing Drakath.
        """

        # Base stats for Drakath
        base_stats = Stats(
            MaxHP=26334, CurrMP=12605, STR=337, DEX=337, INT=337, END=21, CHA=0, LUK=0
        )

        abilities = [
            # Phase 1
            Ability(
                name="Attack 1",
                hotkey="1",
                cost=0,
                cooldown=0,
                sets_cooldowns={"Attack 2": 0},
            ),
            Ability(
                name="Attack 2",
                hotkey="2",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 2.1": 0},
            ),
            Ability(
                name="Attack 2.1",
                hotkey="2",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 2.2": 0},
            ),
            Ability(
                name="Attack 2.2",
                hotkey="2",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 3": 0},
            ),
            Ability(
                name="Attack 3",
                hotkey="3",
                cost=0,
                cooldown=999,
                damage_multiplier=1000000,
            ),
            # Phase 2
            Ability(
                name="Attack 4",
                hotkey="4",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 5": 0},
            ),
            Ability(
                name="Attack 5",
                hotkey="5",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 6": 0},
            ),
            Ability(
                name="Attack 6",
                hotkey="6",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 5.1": 0},
            ),
            Ability(
                name="Attack 5.1",
                hotkey="5",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 7": 0},
            ),
            Ability(
                name="Attack 7",
                hotkey="7",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 8": 0},
            ),
            Ability(
                name="Attack 8",
                hotkey="8",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 9": 0},
            ),
            Ability(
                name="Attack 9",
                hotkey="9",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 5": 0},
            ),
            # Phase 3
            Ability(
                name="Attack 11",
                hotkey="11",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 12": 0},
            ),
            Ability(
                name="Attack 12",
                hotkey="12",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 13": 0},
            ),
            Ability(
                name="Attack 13",
                hotkey="13",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 12.1": 0},
            ),
            Ability(
                name="Attack 12.1",
                hotkey="12",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 14": 0},
            ),
            Ability(
                name="Attack 14",
                hotkey="14",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 15": 0},
            ),
            Ability(
                name="Attack 15",
                hotkey="15",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 16": 0},
            ),
            Ability(
                name="Attack 16",
                hotkey="16",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 12": 0},
            ),
            # Phase 4
            Ability(
                name="Attack 18",
                hotkey="18",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 19": 0},
            ),
            Ability(
                name="Attack 19",
                hotkey="19",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 19.1": 0},
            ),
            Ability(
                name="Attack 19.1",
                hotkey="19",
                cost=0,
                cooldown=999,
                sets_cooldowns={"Attack 20": 0},
            ),
            Ability(
                name="Attack 20",
                hotkey="20",
                cost=0,
                cooldown=999,
                damage_multiplier=1000000,
            ),
            Ability(
                name="Chaos Blast",
                hotkey="cb",
                cost=0,
                cooldown=0,
                on_hit_effects=[
                    Effect(name="TERRIFIED", duration=5, chance=0.2, stat_mods={"BDP": -50}),
                    Effect(name="ISOLATED", duration=5, chance=0.2, stat_mods={"BONUS": -50}),
                    Effect(name="APOCALYPSE", duration=5, chance=0.2, stat_mods={"BOOST": -50}),
                    Effect(name="PARALYZED", duration=5, chance=0.2, stat_mods={"CRIT": -50}),
                    Effect(
                        name="NECROSIS", duration=5, chance=0.2, stat_mods={"plus_dot_dmg": -0.5}
                    ),
                ],
            ),
            Ability(
                name="Chaos Overload",
                hotkey="co",
                cost=0,
                cooldown=0,
                on_hit_effects=[Effect(name="Phase 1", duration=-1)],
                custom_logic=self.drakath_chaos_overload,
            ),
        ]

        super().__init__(
            name="Drakath, Champion of Chaos",
            abilities=abilities,
            base_stats=base_stats,
        )

    def drakath_chaos_overload(self, user, target, chance):
        phase = -1
        for effect in user.effects:
            if "Phase" in effect.name:
                phase = int(effect.name.split(" ")[1])
                break

        if phase == 1 and user.hp / user.base_stats.MaxHP <= 0.9:
            user.effects = [e for e in user.effects if "Phase" not in e.name]
            user.add_effect(Effect(name="Phase 2", duration=-1))
            user.hp = user.base_stats.MaxHP * 0.9
            user.ability_cooldowns = {ability.name: 999 for ability in user.abilities}
            user.ability_cooldowns["Attack 4"] = 0
        elif phase == 2 and user.hp / user.base_stats.MaxHP <= 0.5:
            user.effects = [e for e in user.effects if "Phase" not in e.name]
            user.add_effect(Effect(name="Phase 3", duration=-1))
            user.hp = user.base_stats.MaxHP * 0.5
            user.ability_cooldowns = {ability.name: 999 for ability in user.abilities}
            user.ability_cooldowns["Attack 11"] = 0
        elif phase == 3 and user.hp / user.base_stats.MaxHP <= 0.1:
            user.effects = [e for e in user.effects if "Phase" not in e.name]
            user.add_effect(Effect(name="Phase 4", duration=-1))
            user.hp = user.base_stats.MaxHP * 0.1
            user.ability_cooldowns = {ability.name: 999 for ability in user.abilities}
            user.ability_cooldowns["Attack 18"] = 0

        for i in range(8, 0, -1):
            if user.hp / user.base_stats.MaxHP <= i * 0.1 and not any(
                e.name == f"Chaos Blast {i}" for e in user.effects
            ):
                user.add_effect(Effect(name=f"Chaos Blast {i}", duration=-1))
                user.ability_cooldowns["Chaos Blast"] = 0

        return user, target, chance
