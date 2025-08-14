import threading
import numpy as np
from .data import *
import heapq

UNITS: list[Unit] = []
ABILITIES = []
EFFECTS = []
ABILITY_TO_ID = {}
EFFECT_TO_ID = {}
N_EFFECTS = 0
N_ABILITIES = 0
ENEMY_START = 2


class NodeInfo:
    __slots__ = ("effect_durations", "ability_cooldowns", "hp", "mp")

    def __init__(self, hp, mp, effects, cooldowns):
        global N_EFFECTS, N_ABILITIES
        self.hp = hp
        self.mp = mp
        self.effect_durations = (
            np.zeros(N_EFFECTS, dtype=np.int8) if effects is None else np.array(effects, np.int8)
        )
        self.ability_cooldowns = (
            np.zeros(N_ABILITIES, dtype=np.int8)
            if cooldowns is None
            else np.array(cooldowns, np.int8)
        )

    def clone(self):
        return NodeInfo(
            self.hp, self.mp, self.effect_durations.copy(), self.ability_cooldowns.copy()
        )

    def apply_effects(self, char: Stats):
        active = np.where(self.effect_durations > 0)[0]
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


class SimulatorNode:
    __slots__ = ("probability", "data", "stats")

    def __init__(self, data: tuple[NodeInfo, ...], stats: list[Stats], probability=1.0):
        self.data = data
        self.stats = stats
        self.probability = probability

    def clone(self):
        return SimulatorNode(tuple(d.clone() for d in self.data), self.stats, self.probability)

    def fork(self, idx, hp_delta, p, lbl):
        next = self.clone()
        # print(lbl, next.data[idx].hp, -hp_delta, "with", f"{p*100:02.0f}%")
        next.probability *= p
        next.data[idx].hp = max(next.data[idx].hp - hp_delta, next.stats[idx].MinHP)
        return [next]

    def act(self, idx, ability: Ability):
        if not ability.free_action:
            self.data[idx].step()
        self.data[idx].ability_cooldowns[ability.id] = ability.cd
        outcomes: list[SimulatorNode] = ability.pre_atk(self, idx, self.stats[idx].target)
        # if type(ability).__name__ == "BuffCrit":
        #     print(outcomes[0].stats[0].CRIT)
        for _ in range(ability.hits):
            outcomes = tuple(r for o in outcomes for r in o.hit(idx, ability))
        return merged(r for o in outcomes for r in ability.post_atk(o, idx, self.stats[idx].target))

    def get_stats(self, idx):
        return self.data[idx].apply_effects(self.stats[idx])

    def hit(self, idx, ability: Ability):
        stats: Stats = self.get_stats(idx)
        enemy_stats = self.get_stats(stats.target)

        def rolls(val):
            return max(0, min((val - stats.BONUS) / 150, 1))

        miss_prob = rolls(enemy_stats.MPM)
        crit_prob = max(0, min(stats.CRIT / 200, 1)) * (1 - miss_prob)
        glance_prob = rolls(enemy_stats.BPD) * (1 - crit_prob - miss_prob)
        # TODO: Seperate out the chance that was a crit and turned to normal hit due to
        # glancing into glance_crit_prob, then do hit_prob + glance_crit_prob for hit_outcomes
        hit_prob = 1 - (miss_prob + crit_prob + glance_prob)
        miss_outcomes = self.fork(stats.target, 0, miss_prob, "miss")
        # TODO: Most resistances are static and N/A, so precalculating resit to dmg_type
        # and updating only when changed dmg_type and resistances
        multiplier = ability.hit_dmg + (min(1, ability.hit_dmg) * stats.bonus_base)
        resist = 1 - (enemy_stats.RESIST[stats.dmg_type] / 100)
        hit_dmg = stats._hit_damage * multiplier * resist * stats.BOOST
        crit_dmg = stats._crit_damage * multiplier * resist * stats.BOOST

        # TODO: Validate its still 10% and not 5% damage
        glance_outcomes = self.fork(stats.target, hit_dmg * 0.1, glance_prob, "glance")

        with_on_hit = ability.on_hit(self, idx, stats.target)

        # TODO: Update hit_dmg only if needed by on_hit effects
        hit_outcomes = with_on_hit.fork(stats.target, hit_dmg, hit_prob, "hit")
        crit_dmg = stats._crit_damage * ability.hit_dmg * resist
        crit_outcomes = with_on_hit.fork(stats.target, crit_dmg, crit_prob, "crit")
        return merged(miss_outcomes + glance_outcomes + hit_outcomes + crit_outcomes)


class SimulatorBranch:
    def __init__(
        self,
        nodes: list[SimulatorNode],
        turn_num=0,
        move_history=[],
        base_win: float = 0.0,
        base_loss: float = 0.0,
        idx=0,
    ):
        self.turn_num = turn_num
        self.idx = idx
        self.move_history: list = move_history

        # Probabilities & average HP calculation
        self.win_probability, self.loss_probability, self.active_probability = (
            base_win,
            base_loss,
            0,
        )
        self.avg_hp = 0
        self.me_avg = 0
        global ENEMY_START
        pruned_nodes = []
        for n in nodes:
            total_hp = max(sum(u.hp for u in n.data[ENEMY_START:]), 0)
            # print(f"{n.probability*100:3.3f}%", n.data[0].hp, "vs", n.data[ENEMY_START].hp)
            if total_hp == 0:
                self.win_probability += n.probability
            elif n.data[0].hp <= 0:
                self.loss_probability += n.probability
            else:
                self.avg_hp += total_hp * n.probability
                self.me_avg += n.data[0].hp * n.probability
                self.active_probability += n.probability
                pruned_nodes.append(n)
        self.nodes: list[SimulatorNode] = pruned_nodes

        self.weighted_win = (self.win_probability * (65 - self.turn_num)) / 64
        # AKA What would we be at if we always won next turn?
        self.max_weight = self.weighted_win + (
            (self.active_probability * (64 - self.turn_num)) / 64
        )

    def turn(self):
        if self.idx == len(UNITS) or self.active_probability == 0:
            self.idx = 0
            return [self]
        next_outcomes = []
        # TODO: If ability availability differs between nodes in a branch,
        # split into separate branches, then run turn on both do this in the ability itself
        # print(
        #     self.idx,
        #     self.nodes[0].data[0].ability_cooldowns.__str__(),
        #     self.nodes[0].data[1].ability_cooldowns.__str__(),
        #     flush=True,
        # )
        for ability in self.nodes[0].data[self.idx].available_abilities():
            next_outcomes += [o for tree in self.fork(ability) for o in tree.turn()]
        return next_outcomes

    def fork(self, ability):
        new_history = self.move_history + [(self.idx, type(ability).__name__, "")]
        cutoff = max(1e-8 * (0.95**self.turn_num), 1e-8)  # Probability cutoff scaling
        outcomes = []
        for n in self.nodes:
            if n.probability < cutoff:
                continue
            outcomes += n.clone().act(self.idx, ability)
            new_history[-1] = (
                new_history[-1][0],
                new_history[-1][1],
                self.nodes[0].data[self.idx].effect_durations.__str__(),
            )
        return [
            SimulatorBranch(
                merged(outcomes),
                turn_num=self.turn_num + 1,
                move_history=new_history,
                base_win=self.win_probability,
                base_loss=self.loss_probability,
                idx=self.idx if (ability.extra_turn or ability.free_action) else (self.idx + 1),
            )
        ]

    def __lt__(self, other):
        # Use current score so finishing states are prioritized,
        # if they have never won then weighted_win is 0
        if self.weighted_win == other.weighted_win:
            return self.avg_hp < other.avg_hp
        return self.weighted_win > other.weighted_win


def merged(outcomes: list[SimulatorNode]):
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
        if pet:
            UNITS = [player, pet, *enemies]
        else:
            global ENEMY_START
            ENEMY_START = 1
            UNITS = [player, *enemies]
        EFFECTS = []
        ABILITIES = []
        for u in UNITS:
            EFFECTS.extend(u.effects)
            ABILITIES.extend(u.abilities)
        N_EFFECTS = len(EFFECTS)
        N_ABILITIES = len(ABILITIES)
        ABILITY_TO_ID = {type(obj).__name__: obj.set_id(i) for i, obj in enumerate(ABILITIES)}
        EFFECT_TO_ID = {type(obj).__name__: obj.set_id(i) for i, obj in enumerate(EFFECTS)}
        self.lock = threading.Lock()

        def getNodeInfo(u: Unit):
            cooldowns = np.full(N_ABILITIES, 99)
            cooldowns[[a.id for a in u.abilities]] = 0
            return NodeInfo(u.stats.MaxHP, u.stats.MaxMP, np.full(N_EFFECTS, 0), cooldowns)

        unit_data = [getNodeInfo(u) for u in UNITS]
        unit_stats = [u.stats for u in UNITS]
        root_node = SimulatorNode(unit_data, unit_stats)
        self.queue = [SimulatorBranch([root_node])]

    # TODO: Speed up somehow with threading, either the for-loop or something else...
    # Branch and Bound; Internal is Greedy Search by weighted_wins, then by boss % missing hp
    def run(self):
        best_score = 0
        best_path = None
        print("Running")
        n = 0
        while self.queue:
            tree = self.dequeue()
            n += 1
            if tree.max_weight < best_score:
                # print("pruned")
                continue
            if tree.loss_probability > 0.4:
                # print("trashed cus died too much..")
                continue
            if tree.weighted_win != tree.max_weight:
                self.enqueue(tree.turn())
            elif tree.weighted_win > best_score:
                print(
                    "Step",
                    n,
                    tree.weighted_win,
                    f"{tree.win_probability * 100:2.0f}",
                    f"{tree.loss_probability * 100:2.0f}",
                    (tree.me_avg, tree.avg_hp),
                    # [(x.weighted_win, x.avg_hp) for x in self.queue],
                    [x[1] for x in tree.move_history if x[0] == 0],
                )
                # print("Step", n, tree.max_weight, tree.weighted_win, tree.win_probability)
                # print("Updated best", tree.win_probability, tree.weighted_win)
                best_score = tree.weighted_win
                best_path = {"move_history": tree.move_history, "win": tree.win_probability}
        return best_path

    def enqueue(self, trees: list[SimulatorBranch]):
        # with self.lock:
        for tree in trees:
            heapq.heappush(self.queue, tree)

    def dequeue(self):
        # with self.lock:
        if self.queue:
            return heapq.heappop(self.queue)
        else:
            return None
