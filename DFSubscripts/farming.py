import time

from Utils.battle_utils import battle
import Utils.quest_macro_utils as m_q
from Utils import ui_macro_utils as m_ui
import Utils.macro_utils as m
import DFSubscripts.navigation as nav
import Utils.df_types as df_t
def Farming(classID, subCategory):
    if '100Rooms' in subCategory: Rooms100(classID)
    elif 'Tizheruk' in subCategory: Tizheruk()
    # Ninja
    # DrVoltabolt
    # Unlucky Essence
    # Dragon Food
def Rooms100(classID):
    wallDict = {'North': ((18, 1), 37),
                'East': ((31, 11), 63),
                'South': ((15, 20), 47),
                'West': ((3, 11), 46)}
    def events():
        m_ui.ClickBtn('UI/CompleteQuestBtn.png', (485, 303, 780, 387))
        m_ui.ClickBtn('Farming/100RoomsMoglin.png',(553, 611, 730, 653))
    nav.loreBookHeal()
    m.sleep(1)
    nav.to_travel_map(1)
    m.Click(1108, 183)
    m_ui.ClickBtn('UI/TakeFlight_Bk1.png', (993, 638, 1168, 685))
    m.sleep(1.5)
    m_q.pathfind_quest(classID, wallDict, 'East', events)
def DefenderMedals(classID):
    m.ClickImage('Farming/DM/DMWarArtixBattle.png', (806, 533, 1092, 625), 3)
    try:
        while True: m_q.masked_quest(classID, 'DM')
    except AssertionError as msg:
        if str(msg) == 'Quest Complete':
            m.Click(650, 670)
            if m.ImageCheck('UI/ItemGet.png', (514, 126, 782, 184), 2): m.Click(654, 669)
        else: raise AssertionError(msg)
def Candy(classID):
    def knockHouse():
        m.Click(618, 50)
        m.ClickImage('Farming/Candy/KnockHouse.png', (986, 58, 1194, 106), 3)
        if m.ImageCheck('Farming/Candy/GetCandy.png', (250, 267, 454, 320), 3): m.Click(355, 296)
        elif m.ImageCheck('Farming/Candy/TrickMonster.png', (300, 188, 500, 238)):
            m.Click(405, 215)
            if m.ImageCheck('Farming/Candy/RareMonster.png', (300, 342, 500, 388), .5): m.Click(398, 364)
            else: m.Click(405, 215)
            battle((classID, 'Quick'))
        elif m.ImageCheck('Farming/Candy/MoglinCandy.png', (280, 280, 484, 333)): m.Click(377, 303)
        else: raise AssertionError("WHAT THE HECK!!")
        m.ClickImage('Farming/Candy/TakeCandy.png', (553, 485, 727, 529), 5)
        time.sleep(0.3)
    m.Click(379, 414)
    knockHouse()
    m.Click(684, 552)
    time.sleep(1)
    m.Click(721, 412)
    knockHouse()
    m.Click(1060, 550)
    time.sleep(1)
    m.Click(1076, 413)
    knockHouse()
    m.ClickImage('Farming/Candy/Heal.png', (930, 48, 1084, 102), 2)
    m.Click(1190, 545)
    time.sleep(0.5)

def Tizheruk():
    # nav.equip(df_t.Classes.Necro)
    # nav.weapon_swap(df_t.Elements.Light)
    nav.bounty_board()
    m_ui.ClickBtn('Farming/Tizheruk.png', (182, 581, 360, 628))
    m_ui.ClickBtn('Farming/AcceptBounty.png', (749, 541, 917, 587))
    m_q.move_to(df_t.QuestLocations['East'], (df_t.Classes.Necro, 'Quick'))
    m_q.move_to(df_t.QuestLocations['East'], (df_t.Classes.Necro, 'Quick'))
    m_q.move_to(df_t.QuestLocations['East'], (df_t.Classes.Necro, 'Quick'))
    m_q.move_to(df_t.QuestLocations['NorthEast'], (df_t.Classes.Necro, 'Quick'))
    for _ in range(3):
        m_q.move_to(df_t.QuestLocations['North'], (df_t.Classes.Necro, 'Quick'))
    for _ in range(4):
        m_q.move_to(df_t.QuestLocations['NorthEast'], (df_t.Classes.Necro, 'Quick'))
    while True:
        win = lambda: m_ui.ClickBtn('Farming/TizherukWin.png', (491, 267, 782, 351))
        m_q.move_to(df_t.QuestLocations['NorthEast'], (df_t.Classes.Necro, 'Boss'), win)

def Nythera():
    m.ImageCheck('Locations/WarlicPortal.png', (774, 77, 1162, 346), 3)
    m.Click(1198, 420)
    m.sleep(4)
    m.Click(1011, 609)
    m.sleep(3)
    m.Click(982, 320)
    m.ImageCheck('Locations/Nythera_Bk1.png', (903, 51, 1155, 293), 3)
    m_ui.ClickBtn('Farming/NytheraQuests.png', (592, 424, 757, 465))
    m_ui.ClickBtn('Farming/NytheraPotionMastery.png', (596, 428, 764, 465))
    m_ui.ClickBtn('Farming/PotionMasteryStart.png',(588, 329, 759, 370))
    m.sleep(1)
    for _ in range(5):
        m.Click(658, 340)
        m.sleep(.1)
    from PIL import Image
    m.Click(658, 340)
    glowless = Image.open('Farming/glowlessPotionMastery.png').convert('RGB')
    # num = 0
    timeoutTime = time.time()
    while not m.ImageCheck('UI/CompleteNythera.png', (545, 298, 810, 364)):
        positions = []
        waitTime = time.time()
        while time.time() - waitTime < 2.5:
            if time.time() - timeoutTime >= 3*60:
                m.Click(636, 855)
                m.sleep(1.862)
                m.Click(958, 665)
                nav.travel_to(1, 'Warlic')
                raise AssertionError('Quest Failed')
            diff = m_q.mask_image(m.RegionGrab((260, 252, 1046, 686)), glowless)
            pos = m_q.largest_in_mask(diff, 6000)
            if pos is not None:
                waitTime = time.time()
                # diff.save(f'Ny/change{num}_{len(positions)}.png', 'png')
                positions.append((260+pos[0], 252+pos[1]))
                m.sleep(.5)
                if m.ImageCheck('UI/CompleteNythera.png', (545, 298, 810, 364)): break
        for p in positions:
            m.Click(*p)
            m.sleep(.1)
        if m.ImageCheck('UI/CompleteNythera.png', (545, 298, 810, 364)): break
        m.sleep(2.5)
        # num += 1
    m_ui.ClickBtn('UI/CompleteNythera.png', (545, 298, 810, 364))
    m_q.CheckQuestDialog()

def DeathKnight():
    m_q.move_to(df_t.QuestLocations['East'], (df_t.Classes.Mage, 'Quick'))
    m_q.move_to(df_t.QuestLocations['East'], (df_t.Classes.Mage, 'Quick'))
    m_q.move_to(df_t.QuestLocations['East'], (df_t.Classes.Mage, 'Quick'))
    m_q.move_to(df_t.QuestLocations['SouthEast'], (df_t.Classes.Mage, 'Quick'))
    m_q.move_towards(df_t.QuestLocations['NorthEast'], (df_t.Classes.Mage, 'Quick'))

def Visor():
    m.sleep(0.851)
    m.Click(658, 27)
    m.sleep(2.14)
    m.Click(872, 390)
    m.sleep(1.327)
    m.Click(881, 192)
    m.sleep(0.526)
    m.Click(881, 192)
    m.sleep(0.481)
    m.Click(881, 192)
    m.sleep(0.436)
    m.Click(881, 192)
    m.sleep(0.457)
    m.Click(881, 192)
    m.sleep(0.553)
    m.Click(881, 192)
    m.sleep(0.46)
    m.Click(881, 192)
    m.sleep(1.103)
    m.Click(848, 103)
    m.sleep(2.184)
    m.Click(303, 59)
    m.sleep(1.096)
    m.Click(579, 218)
    m.sleep(3.123)
    m.Click(751, 207)
    m.sleep(3.296)
    m.Click(647, 81)
    m.sleep(2.688)
    m.Click(553, 218)
    m.sleep(2.372)
    m.Click(1039, 325)
    m.sleep(2.59)
    m.Click(1040, 510)
    m.sleep(1.556)
    m.Click(1154, 357)
    m.sleep(1.806)
    m.Click(965, 132)
    m.sleep(1.309)
    m.Click(965, 132)
    m.sleep(1.548)
    m.Click(1007, 70)
    m.sleep(1.879)
    m.Click(506, 459)
    m.sleep(2.215)
    m.Click(489, 334)
    m.sleep(1.135)
    m.Click(489, 334)
    m.sleep(2.824)
    m.Click(331, 183)
    m.sleep(1.399)
    m.Click(282, 80)
    m.sleep(1.507)
    m.Click(841, 595)
    m.sleep(0.985)
    m.Click(767, 425)
    m.sleep(1.372)
    m.Click(684, 390)
    m.sleep(2.106)
    m.Click(635, 259)
    m.sleep(1.449)
    m_q.move_towards((494, 114), (df_t.Classes.Mage, "Quick"))
    m_q.move_towards((395, 90), (df_t.Classes.Mage, "Quick"))

def HideBehind():
    # nav.equip(df_t.Classes.Necro)
    # nav.weapon_swap(df_t.Elements.Light)
    nav.bounty_board()
    # m_ui.ClickBtn('Farming/Tizheruk.png', (182, 581, 360, 628))
    m.sleep(2)
    m_ui.ClickBtn('Farming/AcceptBounty.png', (749, 541, 917, 587))
    while True:
        m_q.possibleBattle((df_t.Classes.Necro, 'Quick'))

def UnluckyDoom():
    #Start Quest
    m.ImageCheck('Locations/Necropolis.png',(498, 92, 818, 252), 3)
    m.Click(480, 475)
    m.sleep(2)
    m.Click(849, 425)
    m.Click(856, 285)
    m.sleep(.2)
    m.Click(890, 366)
    m.sleep(1)
    #Actual Quest
    quest_pos = ['North', (1157, 426), (1157, 426), (1092, 96), (209, 148), 'North', 'South', (968, 699),
                 (80, 457), (80, 457), 'North', (1157, 426), 'East', (78, 400), (625, 274), (625, 274)]
    for pos in quest_pos:
        m_q.move_to(pos, (df_t.Classes.Mage, 'Quick'))

def AerisBattlespire():
    m.ImageCheck('Farming/AerisDuel.png',(563, 56, 709, 219), 3)
    m.Click(665, 310)
    m.ImageCheck('Farming/Keelia.png',(851, 95, 1206, 442),3)
    m.Click(641, 330)
    while True:
        m.ImageCheck('Farming/AerisNextMatch.png',(92, 445, 337, 514),3)
        if m.ImageCheck('UI/QuestComplete.png', (410, 100, 820, 194)): break
        m.Click(219, 584)
        m.Click(221, 482)
        try:
            m_q.battle((df_t.Classes.Warrior, "PVP"))
        except AssertionError as msg: pass
    m_q.CheckQuestDialog()

def NinjaGold():
    m.ClickImage('Farming/NinjaHeal.png', (790, 387, 954, 426), 3)
    m_ui.ClickBtn('Farming/NinjaStart.png', (765, 330, 973, 375))
    battle((df_t.Classes.Chaosweaver, 'Multi'))
    m_q.CheckQuestDialog()

def SlayBells():
    m.sleep(2.912)
    m_q.move_towards((870, 309), (df_t.Classes.Mage, "Quick"))
    m.Click(464, 342)
    m.sleep(1.25)
    m.Click(486, 547)
    m.sleep(1)
    m.Click(537, 319)
    m.sleep(1)
    m.Click(537, 319)
    m.sleep(1.5)
    m.Click(84, 493)
    m.sleep(2.567)
    m.Click(919, 179)
    m.sleep(1.381)
    m.Click(352, 187)
    m.sleep(1.478)
    m.Click(374, 192)
    m.sleep(1.847)
    m.Click(630, 518)
    m.sleep(1.25)
    for _ in range(40):
        m.Click(630, 518)
        m.sleep(0.1)
    m.Click(634, 379)
    m.sleep(1.012)
    m.Click(646, 379)
    m.sleep(0.5)
    m.Click(633, 334)
    battle((df_t.Classes.Chaosweaver,'Quick'))
    for _ in range(30):
        m.Click(598, 514)
        m.sleep(0.1)
    m.sleep(2.495)
    m.Click(598, 514)
    m.sleep(3.781)
    m.Click(598, 514)
    m.sleep(2.437)
    m.Click(676, 367)
    m_q.CheckQuestDialog()
