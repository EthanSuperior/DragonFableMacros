from BattleSim import Drakath, DeathKnight, Dragon, Stats, Resistances, Simulator

if __name__ == "__main__":
    player_res = Resistances(
        {
            "all": 1,
            "health": -17,
            "good": 27,
            "evil": 27,
            "light": 75,
            "immobility": 80,
            "darkness": 75,
        }
    )
    player_stats = Stats(
        STR=84,
        DEX=284,
        INT=84,
        CHA=50,
        LUK=23,
        END=277,
        WIS=83,
        CRIT=86,
        BONUS=87,
        BOOST=0,
        MPM=52,
        BDP=33,
        Resist=player_res,
        MaxHP=3265,
        MaxMP=960,
        plus_dmg=1.071,
        plus_dot_dmg=1.71,
        plus_noncrit_dmg=1.126,
        plus_crit_dmg=1.834,
        damage=(123 + 128) // 2,
    )
    pet_drag = Dragon(
        element="light",
        training={"protection": 200, "magic": 0, "fighting": 200, "assistance": 199, "mischief": 1},
    )
    Simulator([DeathKnight(player_stats), pet_drag], [Drakath()]).start()
