from typing import Type, List
from engine import Character, Stats, Resistances, BattleSimulator


def RunSimulation(player_stats: Stats, player_class: Type[Character], enemy_class: Type[Character]):
    players = [player_class(player_stats)]
    enemies = [enemy_class()]
    sim = BattleSimulator(initial_players=players, initial_enemies=enemies, thread_count=8)
    results, discarded_probability = sim.run()

    if results:
        best = results[0]
        print("\n🛡️ Optimal Strategy Found")
        print("---------------------------")
        print("Win Probability: ", best["win_chance"] * 100, "%")
        print("Average Turns:   ", best["avg_turns"])
        print("Ability Sequence:")

        player_moves = [move[2] for move in best["path"] if move[0] == 'player' and move[1] == 0]
        allies_moves = [move[2] for move in best["path"] if move[0] == 'player' and move[1] != 0]
        enemy_moves = [move[2] for move in best["path"] if move[0] == 'enemy']

        print("  Player Moves:", ", ".join(player_moves))
        if allies_moves:
            print("  Allies' Moves:", ", ".join(allies_moves))
        if enemy_moves:
            print("  Enemy Moves:", ", ".join(enemy_moves))

    else:
        print("❌ No guaranteed win path found.")

    print("\nℹ️ Discarded Probabilities (<1%):", discarded_probability * 100, "%")


if __name__ == "__main__":
    player_stats = Stats(
        STR=200,
        DEX=0,
        INT=0,
        CHA=0,
        LUK=200,
        END=200,
        WIS=200,
        CRIT=36,
        BONUS=0,
        BOOST=100,
        MPM=0,
        BDP=0,
        Resist=Resistances(),
        MaxHP=3000,
        MaxMP=500,
        CurrMP=500,
        plus_dmg=0,
        plus_dot_dmg=0,
        plus_noncrit_dmg=0,
        plus_crit_dmg=0,
        plus_base_dmg=0,
        reduce_noncrit_dmg=0,
        reduce_dot_dmg=0,
        reduce_crit_dmg=0,
        immobility_resist=0,
        bth=0,
        health_resist=0,
    )
    from classes import DeathKnight
    from bosses import Drakath

    RunSimulation(player_stats, DeathKnight, Drakath)
