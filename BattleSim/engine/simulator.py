import heapq
import threading
import copy
from engine.character import Character


class SimulationNode:
    def __init__(
        self, players: list[Character], enemies: list[Character], turn: int, history: list, chance: float
    ):
        self.players = players
        self.enemies = enemies
        self.turn = turn
        self.history = history
        self.chance = chance  # probability of reaching this state

    def __lt__(self, other):
        # Tie-breaking: prioritize lower total enemy HP, then higher total player HP
        player_hp = sum(p.hp for p in self.players)
        other_player_hp = sum(p.hp for p in other.players)
        enemy_hp = sum(e.hp for e in self.enemies)
        other_enemy_hp = sum(e.hp for e in other.enemies)

        if abs(enemy_hp - other_enemy_hp) < 1000:
            return player_hp > other_player_hp
        return enemy_hp < other_enemy_hp


class BattleSimulator:
    def __init__(self, initial_players: list[Character], initial_enemies: list[Character], thread_count: int = 4):
        self.initial_players = initial_players
        self.initial_enemies = initial_enemies
        self.queue = []
        self.lock = threading.Lock()
        self.path_stats = {}
        self.discarded_prob = 0.0
        self.best_turns = float("inf")
        self.thread_count = thread_count

    def enqueue(self, node: SimulationNode):
        with self.lock:
            heapq.heappush(self.queue, node)

    def dequeue(self):
        with self.lock:
            if self.queue:
                return heapq.heappop(self.queue)
            else:
                return None

    def run(self):
        start_node = SimulationNode(
            [copy.deepcopy(p) for p in self.initial_players],
            [copy.deepcopy(e) for e in self.initial_enemies],
            turn=0,
            history=[],
            chance=1.0,
        )
        self.enqueue(start_node)

        threads = [threading.Thread(target=self.worker_loop) for _ in range(self.thread_count)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        results = []
        for path, stats in self.path_stats.items():
            win_chance = stats.get("win", 0)
            loss_chance = stats.get("loss", 0)
            if win_chance > 0:
                results.append(
                    {
                        "path": path,
                        "win_chance": win_chance / (win_chance + loss_chance),
                        "avg_turns": stats["total_turns"] / stats["win"],
                    }
                )

        results.sort(key=lambda x: x["win_chance"], reverse=True)
        return results, self.discarded_prob

    def is_team_dead(self, team: list[Character]):
        return all(c.is_dead() for c in team)

    def worker_loop(self):
        while True:
            node = self.dequeue()
            if not node:
                break

            path_tuple = tuple(node.history)
            with self.lock:
                stats = self.path_stats.get(path_tuple, {})
                win_chance = stats.get("win", 0)
                loss_chance = stats.get("loss", 0)
                if loss_chance / (win_chance + loss_chance + 1e-9) > 0.6:
                    self.discarded_prob += node.chance
                    continue

            if self.is_team_dead(node.players):
                with self.lock:
                    stats["loss"] = stats.get("loss", 0) + node.chance
                    self.path_stats[path_tuple] = stats
                continue

            if self.is_team_dead(node.enemies):
                with self.lock:
                    stats["win"] = stats.get("win", 0) + node.chance
                    stats["total_turns"] = (
                        stats.get("total_turns", 0) + node.turn * node.chance
                    )
                    self.path_stats[path_tuple] = stats
                continue

            if node.chance < 0.01 or node.turn > self.best_turns:
                with self.lock:
                    self.discarded_prob += node.chance
                continue

            # Player's turn
            for i, player in enumerate(node.players):
                if not player.is_dead():
                    for j, enemy in enumerate(node.enemies):
                        if not enemy.is_dead():
                            for n in self.simulate_turn(node, True, i, j):
                                # Enemy's turn
                                for i_e, enemy_e in enumerate(n.enemies):
                                    if not enemy_e.is_dead():
                                        for j_p, player_p in enumerate(n.players):
                                            if not player_p.is_dead():
                                                for new_node in self.simulate_turn(n, False, i_e, j_p):
                                                    self.enqueue(new_node)

    def simulate_turn(self, node: SimulationNode, is_player_turn: bool, user_idx: int, target_idx: int):
        users = node.players if is_player_turn else node.enemies
        targets = node.enemies if is_player_turn else node.players

        user = users[user_idx]
        target = targets[target_idx]

        user.tick()
        nodes = []
        for ability in user.abilities:
            new_history = list(node.history)
            move = ("player" if is_player_turn else "enemy", user_idx, ability.name)
            new_history.append(move)

            results = ability.use(user, target, node.chance)
            if results is None:
                continue

            for new_user, new_target, new_probability in results:
                new_players = [p.copy() for p in node.players]
                new_enemies = [e.copy() for e in node.enemies]

                if is_player_turn:
                    new_players[user_idx] = new_user
                    new_enemies[target_idx] = new_target
                else:
                    new_enemies[user_idx] = new_user
                    new_players[target_idx] = new_target

                new_node = SimulationNode(
                    players=new_players,
                    enemies=new_enemies,
                    turn=node.turn + (1 if is_player_turn else 0),
                    history=new_history,
                    chance=new_probability,
                )
                nodes.append(new_node)
        return nodes