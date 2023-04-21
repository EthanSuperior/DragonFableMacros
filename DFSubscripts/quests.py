import Utils.macro_utils as m
from Utils.battle_utils import battle
import DFSubscripts.farming as frm
from DFSubscripts.inn import InnFight
from DFSubscripts.navigation import quest_nav
from Utils.ui_macro_utils import reposition
from Utils.df_types import Classes
import DFSubscripts.navigation as nav

def Debug(classID):
    m.sleep(.5)
    # battle((Classes.Necro, 'Boss'), True)
    # while True:
    # print('HP    -'+df.getHp()+' MP:' + df.getHp())
    # print('HP    -'+df.getHp()+' MP:' + df.getHp())
    # time.sleep(.05)
"""
Long Walk
Utils
"""

def startQuest(name):
    reposition()
    quest_nav(name)
def runQuest(name):
    try:
        if name == 'DM': frm.DefenderMedals(Classes.WDL)
        elif name == '100Rooms': frm.Rooms100(Classes.Mage)
        elif name == 'Tizheruk': frm.Farming(Classes.Necro, name)
        elif name == 'Delay': m.sleep(3)
        elif name == 'Treat': frm.Candy(Classes.WDL)
        elif name == 'Battle': battle((Classes.Chaosweaver, 'AARGH'))
        elif name == 'DeathKnight': frm.DeathKnight()
        elif name == 'Unlucky': frm.UnluckyDoom()
        elif name == 'Visor': frm.Visor()
        elif 'Aeris' in name: frm.AerisBattlespire()
        elif 'Inn' in name: InnFight(Classes.Chaosweaver, name.removeprefix('Inn'))
        elif name == 'PotionMastery': frm.Nythera()
        elif 'Gold' in name: frm.NinjaGold()
        elif 'SlayBells' in name: frm.SlayBells()
        elif name == 'SellThem': nav.sell_items_dragonless()
        else: Debug(Classes.Mage)
        return True
    except AssertionError: return False



if __name__ == '__main__':
    import os
    import pyautogui
    pyautogui.FAILSAFE = True
    os.chdir('C:/Users/Evan Chase/Desktop/Files/Programming/DragonFable/Images')
    m.sleep(1)
    startQuest('Inn')
