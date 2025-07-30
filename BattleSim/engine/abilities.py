from .character import Character
from .effects import Effect
import random
import copy
from .formulas import *

def apply_probabilistic_effects(outcomes, effects):
    """
    Applies a list of effects to a list of outcomes, forking the outcomes
    based on the chance of each effect.
    """
    if not effects:
        return outcomes

    new_outcomes = []
    for u, t, p in outcomes:
        # Start with the base case where no effects are applied
        effect_outcomes = [(u, t, p)]

        for effect in effects:
            next_effect_outcomes = []
            for current_u, current_t, current_p in effect_outcomes:
                # State where the effect is not applied
                next_effect_outcomes.append(
                    (current_u, current_t, current_p * (1 - effect.chance))
                )

                # State where the effect is applied
                u_with_effect = current_u.copy()
                t_with_effect = current_t.copy()
                (
                    u_with_effect if effect.target == "self" else t_with_effect
                ).add_effect(effect)
                next_effect_outcomes.append(
                    (u_with_effect, t_with_effect, current_p * effect.chance)
                )
            effect_outcomes = next_effect_outcomes
        new_outcomes.extend(effect_outcomes)
    return new_outcomes

class Ability:
    def __init__(
        self,
        name,
        cost=0,
        cooldown=0,
        hits=1,
        damage_multiplier=1.0,
        crit_bonus=0,
        pre_attack_effects=None,
        on_hit_effects=None,
        post_attack_effects=None,
    ):
        self.name = name
        self.cost = cost
        self.cooldown = cooldown
        self.hits = hits
        self.damage_multiplier = damage_multiplier
        self.crit_bonus = crit_bonus

        self.pre_attack_effects = pre_attack_effects or []
        self.pre_attack_effects: list[Effect]
        self.on_hit_effects = on_hit_effects or []
        self.on_hit_effects: list[Effect]
        self.post_attack_effects = post_attack_effects or []
        self.post_attack_effects: list[Effect]

    def copy(self):
        return copy.deepcopy(self)

    def use(self, user: Character, target: Character, chance=1.0):
        if user.mp < self.cost or user.ability_cooldowns.get(self.name, 0) > 0:
            return None

        new_user = user.copy()
        new_target = target.copy()
        new_user.mp -= self.cost
        new_user.ability_cooldowns[self.name] = self.cooldown

        outcomes = [(new_user, new_target, chance)]

        # Apply pre-attack effects
        outcomes = apply_probabilistic_effects(outcomes, self.pre_attack_effects)

        for _ in range(self.hits):
            new_outcomes = []
            for u, t, p in outcomes:
                crit_chance = calculate_crit_chance(u, t)
                dodge_chance = calculate_mpm_chance(u, t)
                glance_chance = cacluate_bdp_chance(u, t)

                # Probabilities
                miss_prob = dodge_chance
                crit_prob = crit_chance * (1 - miss_prob)
                glance_prob = glance_chance * (1 - crit_prob - miss_prob)
                normal_prob = 1 - (miss_prob + crit_prob + glance_prob)

                # Base damage
                base_dmg = u.damage * self.damage_multiplier

                # Miss outcome
                miss_outcomes = [(u, t, p * miss_prob)]

                # Glance outcome
                glance_dmg = base_dmg * 0.05 * get_dmg_multiplier(u, t)
                glance_outcomes = [(u, t.damage(glance_dmg), p * glance_prob)]

                # Normal hit outcomes
                normal_hit_outcomes = [
                    (u, t, p * normal_prob),
                ]
                normal_hit_outcomes = apply_probabilistic_effects(
                    normal_hit_outcomes, self.on_hit_effects
                )
                for i in range(len(normal_hit_outcomes)):
                    u_hit, t_hit, p_hit = normal_hit_outcomes[i]
                    hit_dmg = base_dmg * get_dmg_multiplier(u_hit, t_hit)
                    normal_hit_outcomes[i] = (u_hit, t_hit.damage(hit_dmg), p_hit)

                # Crit hit outcomes
                crit_hit_outcomes = [
                    (u, t, p * crit_prob),
                ]
                crit_hit_outcomes = apply_probabilistic_effects(
                    crit_hit_outcomes, self.on_hit_effects
                )
                for i in range(len(crit_hit_outcomes)):
                    u_crit, t_crit, p_crit = crit_hit_outcomes[i]
                    crit_dmg = base_dmg * get_dmg_multiplier(u_crit, t_crit, True)
                    crit_hit_outcomes[i] = (u_crit, t_crit.damage(crit_dmg), p_crit)

                new_outcomes.extend(miss_outcomes)
                new_outcomes.extend(glance_outcomes)
                new_outcomes.extend(normal_hit_outcomes)
                new_outcomes.extend(crit_hit_outcomes)

            outcomes = new_outcomes

        # Apply post-attack effects
        outcomes = apply_probabilistic_effects(outcomes, self.post_attack_effects)

        return outcomes

    def __str__(self):
        return f"{self.name} ({self.hits}x @ {self.damage_multiplier * 100:.1f}%)"