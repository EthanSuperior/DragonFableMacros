import glob
import random

import Utils.df_types as df_t
import Utils.macro_utils as m
import Utils.ui_macro_utils as m_ui
import Utils.quest_macro_utils as m_q
import DFSubscripts.navigation as nav
from Utils import battle_utils

def InnBuyFood():
    m.ImageSearch('Inn/InnChallenge.png', (866, 40, 1192, 225), 3)
    m.Click(635, 699)
    nav.BuyFood()
    nav.quest_nav('Inn')

def ChooseExaltiaOption():
    m.ImageCheck('Inn/ExaltiaOption.png', (132, 75, 566, 293), 3)
    m.Click(362, 383) # m.Click(921, 386)
    m.sleep(1)
    m.Click(580, 477)
    m.sleep(1)
    pass

def ExaltiaTower(floor):
    m_ui.ClickBtn('Inn/ExaltiaStart.png', (488, 300, 782, 364))
    m.Click(640, 60+(110*floor))
    m.sleep(2)
    def lowerFloor():
        ChooseExaltiaOption()
        m_q.move_to(df_t.QuestLocations['North'], (df_t.Classes.Chaosweaver, 'Quick'))
        m_q.move_to(df_t.QuestLocations['NorthEast'], (df_t.Classes.Chaosweaver, 'Quick'))
        m_q.move_to(df_t.QuestLocations['NorthWest'], (df_t.Classes.Chaosweaver, 'Quick'))
    def upperFloor():
        ChooseExaltiaOption()
        m_q.move_to(df_t.QuestLocations['North'], (df_t.Classes.Chaosweaver, 'Recover'))
        for _ in range(2):
            m_q.move_to(df_t.QuestLocations['North'], (df_t.Classes.Chaosweaver, 'Recover'))
    if floor == 1 or floor == 2:
        m_q.move_to(df_t.QuestLocations['North'], (df_t.Classes.Chaosweaver, 'Recover'))
        for _ in range(3):
            lowerFloor()
        m_q.move_to(df_t.QuestLocations['East'], (df_t.Classes.Chaosweaver, 'Boss'))
        ChooseExaltiaOption()
        m_q.move_to(df_t.QuestLocations['North'], (df_t.Classes.Mage, 'Boss'))
    elif floor == 3:
        m_q.move_to('North', (df_t.Classes.Chaosweaver, 'Recover'))
        for _ in range(3):
            upperFloor()
        nav.manaPot(False)
        nav.manaPot()
        m.sleep(1)
        m.Click(1180, 524)
        try:
            battle_utils.battle((df_t.Classes.Chaosweaver, 'Bound')) #49vc       #768
        except Exception as msg:
            if 'Failed' in str(msg):
                pass
                # m.Click(640, 375)
                # raise msg
            print(str(msg)+'\n\n\n')
        m.sleep(2)
        m.Click(1180, 524)
        m.sleep(2)
        ChooseExaltiaOption()
        #49bv0c43
        for _ in range(3): nav.healthPot(False)
        nav.manaPot(False)
        nav.manaPot()
        m.sleep(1)
        m_q.move_to('North', (df_t.Classes.Chaosweaver, 'Warden'))
    elif floor == 4:
        m.sleep(1)
        m_q.move_towards((637, 44), (df_t.Classes.Chaosweaver, 'ArchiveNorm'))
        m.sleep(1)
        for _ in range(3):
            ChooseExaltiaOption()
            m_q.move_to((637, 44), (df_t.Classes.Chaosweaver, 'ArchiveNorm'))
            m_q.move_to('East', (df_t.Classes.Chaosweaver, 'ArchiveNorm'))
            m_q.move_to('East', (df_t.Classes.Chaosweaver, 'ArchiveNorm'))
        m_q.move_to('North', (df_t.Classes.Chaosweaver, 'ArchiveMini'))
        ChooseExaltiaOption()
        for _ in range(3): nav.healthPot(False)
        nav.manaPot(False)
        nav.manaPot()
        m.sleep(1)
        m_q.move_to('North', (df_t.Classes.Chaosweaver, 'ArchiveBoss'))
def InnFight(classID, subCategory):
    InnChallengeLayout = [['Dragon', 'Dragon2', 'Nefarious', 'Otherworldly'],
                          ['Otherworldly2', 'Dreamscape', 'Dreamscape2', 'Unfortunate'],
                          ['Azaveyran', 'Forgotten', 'Exaltia', 'Corrupted'],
                          ['Displaced', 'Conduit', 'Inevitable', 'Lords'],
                          ['Lost', 'Lost2', 'Change', 'Doomed'],
                          ['Tenets', 'Ties', 'Eggsalted', 'Beginning'],
                          ['Crossroads']]

    def index_2d(myList, v):
        for i, x in enumerate(myList):
            for j, y in enumerate(x):
                if y in v: return i, j
        return None, None
    m.ImageSearch('Inn/InnChallenge.png', (866, 40, 1192, 225), 3)
    moveSet, useFood = 'Boss', False
    i, j = index_2d(InnChallengeLayout, subCategory)
    try:
        if i is None:
            useFood = False
            m_ui.ClickBtn('Inn/InnChallenge.png', (850, 40, 1192, 256))  # AARGH
            if 'AARGH_BURN' in subCategory:
                classID = df_t.Classes.DragSlay
                m.ImageCheck('Battle/Attack.png', (576, 630, 698, 698), 4)
                if not m.ImageCheck(glob.glob('Inn/DragonNames/*.png'),(820, 730, 1140, 773), 1):
                    nav.flee_battle()
                    m_ui.ClickBtn(glob.glob('Inn/InnFailed?.png'), (459, 321, 822, 429))
                    InnFight(classID,subCategory)
                    raise AssertionError('Quest Failed')
            else:
                classID = df_t.Classes.Chaosweaver
                m.ImageCheck('Battle/Attack.png', (576, 630, 698, 698), 4)
                m.ImageCheck('Battle/Attack.png', (576, 630, 698, 698), 4)
                if m.ImageCheck(glob.glob('Inn/CWReject/*.png'), (820, 730, 1140, 774), 1):
                    nav.flee_battle()
                    m.Click(656, 830)
                    raise AssertionError('Quest Failed')
                else:
                    if not m.ImageCheck(glob.glob('Inn/AARGHs/*.png'), (820, 730, 1140, 774)):
                        m.RegionGrab((830, 745, 1040, 769)).save(f'Inn/AARGHs/{random.random()}.png','png')
                    battle_utils.battle((classID, 'AARGH'))
        else: m.Click(238 + (174 * j), 164 + (56 * i))
        if 'Dragon' in subCategory:
            m.ClickImage('Inn/DragonChallenge.png', (517, 502, 739, 568), 3)
            battle_utils.battle((classID, moveSet))
        elif 'Nefarious' in subCategory: pass
        elif 'Otherworldly' in subCategory: pass
        elif 'Dreamscape' in subCategory: pass
        elif 'Dreamscape2' in subCategory: pass
        elif 'Unfortunate' in subCategory: pass
        elif 'Azaveyran' in subCategory:
            m.ImageSearch('Inn/AzaveyranChallenge.png', (254, 38, 1014, 168), 3)
            if 'Chicken' in subCategory: m.Click(283, 289)
            classID = df_t.Classes.Mage
            battle_utils.battle((classID, moveSet))
        elif 'Forgotten' in subCategory: pass
        elif 'Exaltia' in subCategory:
            useFood = True
            return ExaltiaTower(int(subCategory[-1]))
        elif 'Corrupted' in subCategory:
            m.ImageSearch('Inn/CorruptedChallenge.png', (502, 304, 762, 504), 3)
            if 'Pandora' in subCategory:
                m.Click(640, 394)
                m.ClickImage('Inn/Pandora.png', (98, 160, 466, 344), 3)
            battle_utils.battle((classID, moveSet), True)
        elif 'Displaced' in subCategory: pass
        elif 'Conduit' in subCategory: pass
        elif 'Inevitable' in subCategory: pass
        elif 'Lords' in subCategory: pass
        elif 'Lost' in subCategory: pass
        elif 'Change' in subCategory: pass
        elif 'Doomed' in subCategory:
            if 'Purpose' in subCategory:
                m.sleep(1)
                m.Click(633, 436)
            battle_utils.battle((classID, moveSet), False)
        elif 'Tenets' in subCategory: pass
        elif 'Ties' in subCategory: pass
        elif 'Eggsalted' in subCategory: pass
        elif 'Beginning' in subCategory: pass
        elif 'Crossroads' in subCategory: pass
        m_q.CheckQuestDialog()
    except AssertionError as msg:
        if 'Failed' in str(msg):
            m.sleep(1)
            m.Click(515, 375)
        if 'Success' in str(msg): m_ui.ClickBtn('Inn/InnSuccess.png', (459, 321, 822, 429))
        if useFood: InnBuyFood()
        raise AssertionError(msg)
