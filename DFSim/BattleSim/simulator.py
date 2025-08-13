import threading
import numpy as np
from data import *
import heapq

UNITS = []
ABILITIES = []
EFFECTS = []
ABILITY_TO_ID = {}
EFFECT_TO_ID = {}
N_EFFECTS = 0
N_ABILITIES = 0


class NodeInfo:
    __slots__ = ("effect_durations", "ability_cooldowns", "hp", "mp")

    def __init__(self, hp, mp, effects, cooldowns):
        global N_EFFECTS, N_ABILITIES
        self.hp = hp
        self.mp = mp
        self.effect_durations = np.zeros(N_EFFECTS, dtype=np.int8) if effects is None else effects
        self.ability_cooldowns = (
            np.zeros(N_ABILITIES, dtype=np.int8) if cooldowns is None else cooldowns
        )

    def clone(self):
        return NodeInfo(
            self.hp, self.mp, self.effect_durations.copy(), self.ability_cooldowns.copy()
        )

    def apply_effects(self, char: Stats):
        active = np.where(self.effect_durations >= 0)[0]
        char = char.clone()
        for idx in active:
            char = EFFECTS[idx].apply(char)
        return char

    def step(self):
        self.effect_durations -= 1
        self.ability_cooldowns -= 1

    def available_abilities(self):
        global ABILITIES
        available = np.where(self.ability_cooldowns <= 0)[0]
        for idx in available:
            yield ABILITIES[idx]

    def __hash__(self):
        return hash(
            (
                self.hp,
                self.mp,
                self.effect_durations.tobytes(),
                self.ability_cooldowns.tobytes(),
            )
        )

    def __eq__(self, other):
        return (
            self.hp == other.hp
            and self.mp == other.mp
            and np.array_equal(self.effect_durations, other.effect_durations)
            and np.array_equal(self.ability_cooldowns, other.ability_cooldowns)
        )


class SimulatorBranch:
    def __init__(self, nodes: list[SimulatorNode], turn_num=0, move_history=None):
        self.nodes = nodes
        self.turns = turn_num
        self.move_history = move_history or []

        # Probabilities & average HP calculation
        self.win_probability, self.loss_probability, self.active_probability = 0, 0, 0
        self.avg_hp = 0
        for n in self.nodes:
            total_hp = max(sum(u.hp for u in n.data[2:]), 0)
            self.avg_hp += total_hp * n.probability
            if total_hp == 0:
                self.win_probability += n.probability
            elif n.data[0].hp <= 0:
                self.loss_probability += n.probability
            else:
                self.active_probability += n.probability

        self.weighted_win = (self.win_probability * (65 - self.turns)) / 64
        # AKA What would we be at if we always won next turn?
        self.max_win_prob = self.weighted_win + ((self.active_probability * (64 - self.turns)) / 64)

    def turns(self):
        idx = 0
        self.turns += 1
        outcomes = [self]
        while idx < len(UNITS):
            # This might be prime target for the thread ops... maybe...
            for ability in self.nodes[0].data[idx].available_abilities():
                next_outcomes = []
                for tree in outcomes:
                    next_outcomes += tree.fork(idx, ability)
                if not (ability.free_action or ability.extra_turn):
                    idx += 1
                outcomes = next_outcomes
        return outcomes

    def fork(self, idx, ability):
        new_history = self.move_history + [(idx, ability.name)]
        if ability.free_action:
            return SimulatorBranch(
                merged(ability.pre_atk(n, idx) for n in self.nodes),
                turn_num=self.turns,
                move_history=new_history,
            )
        else:
            cutoff = max(1e-4 * (0.95**self.turns), 1e-8)  # Probability cutoff scaling
            outcomes = []
            for n in self.nodes:
                if n.probability < cutoff:
                    continue
                outcomes += n.act(idx, ability)
            return SimulatorBranch(merged(outcomes), turn_num=self.turns, move_history=new_history)

    def __lt__(self, other):
        # Use current score so finishing states are prioritized,
        # if they have never won then weighted_win is 0
        if self.weighted_win == other.weighted_win:
            return self.avg_hp < other.avg_hp
        return self.weighted_win < other.weighted_win


class SimulatorNode:
    __slots__ = ("probability", "data")

    def __init__(self, data: tuple[NodeInfo, ...], stats: list[Stats], probability=1.0):
        self.data = data
        self.stats = stats
        self.probability = probability

    def fork(self, idx, hp_delta, p):
        # Do I clone stats here? ... or when i modify them.... for now we'll put it in apply_effects...
        next = SimulatorNode(tuple(d.clone() for d in self.data), self.stats, self.probability * p)
        next.data[idx].hp = max(next.data[idx].hp - hp_delta, next.stats[idx].MinHP)
        return next

    def act(self, idx, ability):
        self.data[idx].step()
        outcomes = ability.pre_atk(self, idx)
        for _ in range(ability.hits):
            outcomes = tuple(r for o in outcomes for r in o.hit(idx, ability))
        return merged(ability.post_atk(o, idx) for o in outcomes)

    def hit(self, idx, ability):
        global UNITS
        stats = self.stats[idx]
        enemy_stats = self.stats[stats.target]

        def rolls(val):
            return (max(0, min(val - stats.BONUS, 150)) + 1) / 151

        miss_prob = rolls(enemy_stats.MPM)
        crit_prob = (stats.CRIT / 200) * (1 - miss_prob)
        glance_prob = rolls(enemy_stats.BPD) * (1 - crit_prob - miss_prob)
        # TODO: Seperate out the chance that was a crit and turned to normal hit due to
        # glancing into glance_crit_prob, then do hit_prob + glance_crit_prob for hit_outcomes
        hit_prob = 1 - (miss_prob + crit_prob + glance_prob)

        miss_outcomes = self.fork(idx, 0, miss_prob)
        # TODO: Most resistances are static and N/A, so precalculating resit to dmg_type
        # and updating only when changed dmg_type and resistances
        hit_dmg = stats._hit_damage * enemy_stats.RESIST[stats.dmg_type]
        # TODO: Validate its still 10% and not 5% damage
        glance_outcomes = self.fork(idx, hit_dmg * 0.1, glance_prob)

        with_on_hit = ability.on_hit(self, idx)

        # TODO: Update hit_dmg only if needed by on_hit effects
        hit_dmg = stats._hit_damage * enemy_stats.RESIST[stats.dmg_type]
        hit_outcomes = with_on_hit.fork(idx, hit_dmg, hit_prob)
        crit_dmg = stats._crit_damage * enemy_stats.RESIST[stats.dmg_type]
        crit_outcomes = with_on_hit.fork(idx, crit_dmg, crit_prob)
        return merged(miss_outcomes + glance_outcomes + hit_outcomes + crit_outcomes)


def merged(outcomes: iter[SimulatorNode]):
    merged = {}
    for node in outcomes:
        if node.data in merged:
            merged[node.data].probability += node.probability
        else:
            merged[node.data] = node
    return tuple(merged.values())


class Simulator:
    def __init__(self, player, pet, *enemies):
        global UNITS, ABILITIES, EFFECTS, ABILITY_TO_ID, EFFECT_TO_ID, N_EFFECTS, N_ABILITIES
        UNITS = [player, pet, *enemies]
        EFFECTS = [u.effects for u in UNITS]
        N_EFFECTS = len(EFFECTS)
        ABILITIES = [u.abilities for u in UNITS]
        N_ABILITIES = len(ABILITIES)
        ABILITY_TO_ID = {type(obj).__name__: obj.set_id(i) for i, obj in ABILITIES}
        EFFECT_TO_ID = {type(obj).__name__: obj.set_id(i) for i, obj in EFFECTS}
        self.lock = threading.Lock()
        unit_data = [u.getUnitData() for u in UNITS]
        root_node = SimulatorNode(unit_data, [d.apply_effects(d) for d in unit_data])
        self.queue = [SimulatorBranch([root_node])]

    # TODO: Speed up somehow with threading, either the for-loop or something else...
    # Branch and Bound; Internal is Greedy Search by weighted_wins, then by boss % missing hp
    def run(self):
        best_score = float("inf")
        best_path = None
        while self.queue:
            tree = self.dequeue()
            if tree.max_win_prob < best_score:
                continue
            if tree.weighted_win > best_score:
                best_score = tree.weighted_win
                best_path = tree
            if tree.weighted_win != tree.max_win_prob:
                self.enqueue(tree.turns())
        return best_path

    def enqueue(self, nodes: iter[SimulatorBranch]):
        # with self.lock:
        for node in nodes:
            heapq.heappush(self.queue, node)

    def dequeue(self):
        # with self.lock:
        if self.queue:
            return heapq.heappop(self.queue)
        else:
            return None
