# 100%   125=>216:188=>323  ;   138=>237:207=>356
#  33%    42=>72 : 63=>108  ;    46=>79 : 69=>119         DOT(39/39;58/58)
# 120%   151=>259:213=>366  ;   166=>285:235=>403
# 100w20B151=>259:226=>388  ;   166=>285:248=>427


def r(x):
    return (
        *get_dmg(x, 1, 1),
        ";",
        *get_dmg(x, 1.1, 1),
        "!!",
        *get_dmg(x, 1, 1.2),
        "&&",
        *get_dmg(x, 1.1, 1.2),
    )


def get_dmg(
    atk_dmg_per, res, boost, dmg=116, bonus_base=0.5, str_boost=1.03, dex_boost=1.05, int_boost=1.77
):
    base_dmg = dmg * str_boost * dex_boost
    crit_dmg = dmg * int_boost * dex_boost

    def d(bns, crit):
        base = base_dmg if not crit else crit_dmg
        
        dmg = base * (atk_dmg_per + (min(1, atk_dmg_per) * bns)) * res * boost
        return round(dmg)

    return (
        f"{d(0,False)}=>{d(0,True)}",
        f"{d(bonus_base,False)}=>{d(bonus_base,True)}",
    )


while True:
    print(r(float(input(">>>"))))
