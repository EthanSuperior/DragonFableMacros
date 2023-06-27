from Utils import macro_utils as m
from Utils.df_types import Classes
from Utils import df_types as df_t
from Utils import ui_macro_utils as m_ui

def openLoreBook():
    if not m.ImageCheck('UI/LoreBookOpen.png', (173, 106, 551, 199), .5):
        m.ClickImage('UI/LoreBookIcon.png', (668, 744, 768, 852), 3)
        m.ImageSearch('UI/LoreBookOpen.png', (173, 106, 551, 199), 3)

def closeLoreBook():
    if m.ImageCheck('UI/LoreBookOpen.png', (173, 106, 551, 199),1) or m.ImageCheck('UI/Book1.png', (132, 195, 512, 348)):
        m.Click(633, 816)

def openBook(bkNum):
    openLoreBook()
    if str(bkNum) == '1':
        m_ui.ClickBtn('UI/Book1.png', (132, 195, 512, 348))
    elif str(bkNum) == '3':
        m_ui.ClickBtn('UI/Book3.png', (156, 550, 508, 705))

def openInventory():
    if not m.ImageCheck('UI/Inv.png',(270, 130, 588, 190)):
        m_ui.ClickBtn('UI/InvBag.png', (505, 765, 575, 835), 'UI/Inv.png', (270, 130, 593, 181), False)
    else: m_ui.ClickBtn('UI/InvTab.png', (289, 94, 400, 125), 'UI/Inv.png', (270, 130, 593, 181), False)

def closeInventory():
    if m.ImageCheck(['UI/Inv.png','UI/TempInv.png'],(270, 130, 588, 190)):
        m_ui.ClickBtn('UI/CloseBag.png', (335, 763, 501, 805))

def useItem(slotNum = 1, type='equip', finished = True):
    for _ in range(9, slotNum):
        m.Click(672, 590)
        m.sleep(.1)
    m.Click(208, 240 + (40 * min(slotNum, 9)))
    m.sleep(.1)
    if type == 'equip':
        m.Click(920, 668)
    elif type == 'slot':
        m.Click(1008, 668)
    elif type == 'show':
        m.Click(1090, 668)
    elif type == 'trash':
        m.Click(958, 716)
        m_ui.ClickBtn('UI/Yes.png', (501, 443, 632, 494))
    elif type == 'sell':
        m.Click(956, 698)
        m_ui.ClickBtn('UI/Yes.png', (501, 443, 632, 494))
    if finished: closeInventory()
def BuyFood():
    travel_to('3', 'Falconreach')
    m.Click(220, 502)
    m.ImageSearch('Locations/ChefMoglin.png', (843, 249, 1156, 700), 3)
    m.Click(758, 462)
    m.sleep(1)
    # Buy Seaweed
    m.Click(221, 586)
    m.sleep(1)
    m.Click(566, 461)
    m.sleep(1)
    # Buy Rotten Hardtack
    m.Click(225, 542)
    m.sleep(1)
    m.Click(566, 461)
    m.sleep(1)
    # Leave
    m.Click(756, 355)
    m.sleep(1)
    m.Click(775, 441)
    m.ImageSearch('Locations/Falconreach_Bk3.png', (195, 63, 523, 292), 3)

def to_travel_map(bookNum):
    if bookNum == 1:
        if not m.ImageCheck('UI/Travel_Map_Bk1.png',(731, 42, 965, 121)):
            openBook(1)
            m_ui.ClickBtn('UI/Travel_Bk1.png', (504, 594, 770, 670), 'UI/Travel_Map_Bk1.png', (731, 42, 965, 121), False)
    elif bookNum == 2: pass
    else:
        openBook(3)

def equip_class(classID):
    if m.ImageSearch('Locations/InsideHouse.png', (408, 112, 686, 360)) == [-1, -1]:
        travel_to(3, 'House')
    m.Click(571, 274)
    m.sleep(.5)
    m.Click(452, 215)
    m.sleep(2)
    name = (classID.value.split('#')[0]).split('^')[0]
    m.typeKeys(name, 0.05)
    m.Click(510, 279)
    m.sleep(1)
    df_t.default_class.classID = classID
    m.Click(567, 471)
    m.sleep(1)
    m.Click(637, 629)

def _equip_loadout(slotNum):
    xSlot = (slotNum%10) * 37
    ySlot = (slotNum//10) * 40
    m.Click(793 + xSlot, 758 + ySlot)
    m_ui.ClickBtn('UI/Load.png', (788, 822, 878, 852))
    m.ImageSearch('UI/Inv.png', (270, 130, 588, 190), 3)

def weapon_swap(element):
    openInventory()
    m.Click(245, 685)
    m.sleep(1)
    m.typeKeys('*' + element.value, 0.05)
    m.sleep(.1)
    if str(element.value) in str(df_t.default_class.classID.value):
        useItem(1, 'equip')
    else:
        useItem(0, 'equip')

def equip(classID, slotNum = 0):
    equip_class(classID)
    openInventory()
    _equip_loadout(slotNum)
    _equip_loadout(10)
    closeInventory()

def open_timeline(bookNum):
    if str(bookNum) == '1':
        openBook(1)
        m_ui.ClickBtn('UI/Timeline_Bk1.png', (502, 197, 778, 263))

def manaPot(close=True):
    openInventory()
    m.ClickImage('UI/InvManaPot.png', (216, 782, 262, 806), 3)
    if close: closeInventory()

def healthPot(close=True):
    openInventory()
    m.ClickImage('UI/InvHealthPot.png', (142, 786, 174, 808), 3)
    if close: closeInventory()

def travel_to(bookNum, location):
    openLoreBook()
    if location == 'Home' or location == "House":
        m.Click(307, 784)
        while not m.ImageCheck('Locations/InsideHouse.png', (408, 112, 686, 360)):
            m.Click(584, 406)
            m.sleep(.1)
    elif str(bookNum) == '1':
        if location == 'Falconreach':
            openBook(1)
            m_ui.ClickBtn('UI/FalconreachBtn_Bk1.png', (515, 523, 759, 584))
            while not m.ImageCheck('UI/Falconreach_Bk1.png', (295, 151, 543, 276)):
                m.Click(298, 385)
                m.sleep(.1)
        if location == 'Warlic':
            if not m.ImageCheck('Locations/WarlicPortal.png', (774, 77, 1162, 346)):
                open_timeline(1)
                m.drag((1204, 600), (72, 600))
                m.Click(298, 385)
                m_ui.ClickBtn('UI/GoToWarlic_Bk1.png',(896, 499, 1089, 551))
                m.ImageCheck('Locations/WarlicPortal.png', (774, 77, 1162, 346), 3)
    elif str(bookNum) == '3':
        if location == 'Falconreach':
            while not m.ImageCheck('Locations/Falconreach_Bk3.png', (195, 63, 523, 292)):
                m.Click(390, 786)
                m.Click(634, 612)
                m.sleep(.1)
            m.ImageSearch('Locations/Falconreach_Bk3.png', (195, 63, 523, 292), 3)
            m.sleep(.1)

def quest_nav(quest):
    if 'Inn' in quest:
        if m.ImageCheck('Inn/InnChallenge.png', (866, 40, 1192, 225)): return
        travel_to(3, 'Falconreach')
        m.Click(640, 82)
        while not m.ImageCheck('Inn/InnRoom.png', (758, 38, 1146, 144)): m.Click(638, 77)
        m.Click(921, 238)
        m.ImageSearch('Inn/InnChallenge.png', (866, 40, 1192, 225), 3)
    elif 'DM' in quest:
        if m.ImageCheck('Farming/DM/DMWarArtixBattle.png', (806, 533, 1092, 625)): return
        openLoreBook()
        m.ClickImage('Farming/DM/Mogloween.png', (268, 701, 439, 745), -1)
        m.sleep(2)
        m.Click(734, 296)
        m.sleep(2)
        m.Click(766, 360)
        m.sleep(2)
        m.Click(636, 378)
        m.sleep(1)
    elif 'PotionMastery' in quest:
        travel_to(1, 'Warlic')
    elif 'Aeris' in quest:
        closeLoreBook()
        # openInventory()
        # _equip_loadout(1)
        # _equip_loadout(10)
        # closeInventory()
        to_travel_map(1)
        m.Click(589, 170)
        m_ui.ClickBtn('UI/TakeFlight_Bk1.png', (993, 638, 1168, 685))
        m_ui.ClickBtn('Locations/EnterAeris.png', (1021, 664, 1189, 704))
        m.Click(1182, 567)
        m.sleep(2.5)
    elif "Unlucky" in quest:
        weapon_swap(df_t.Elements.Light)


def flee_battle():
    m_ui.ClickBtn('UI/Options.png', (590, 837, 685, 865))
    m_ui.ClickBtn('UI/FleeBattle.png', (888, 687, 1037, 730), 'UI/Yes.png', (499, 444, 634, 494), False, 3)
    m_ui.ClickBtn('UI/Yes.png', (499, 444, 634, 494))

def loreBookHeal():
    openLoreBook()
    m_ui.ClickBtn('UI/LoreBkHeal.png',(445, 744, 515, 818))
    closeLoreBook()

def bounty_board():
    if not m.ImageCheck('Locations/Serenitys_Bk3.png', (263, 80, 472, 258), 2):
        if not m.ImageCheck('Locations/Falconreach_Bk3.png', (195, 63, 523, 292)):
            travel_to(3, 'Falconreach')
        m.Click(344, 478)
        m.sleep(2)
    loreBookHeal()
    m.Click(997, 467)
    m.ImageSearch('Farming/Tizheruk.png', (182, 581, 360, 628), 3)

def sell_items_dragonless(slotNum = m.SLOT_TO_SELL):
    travel_to(1, 'Falconreach')
    m.Click(534, 476)
    m.ImageCheck('Locations/Ash_Bk1.png', (212, 99, 513, 363), 3)
    m_ui.ClickBtn('UI/AshStore.png', (580, 581, 752, 624))
    m_ui.ClickBtn('UI/SellTab.png',(446, 101, 563, 127),'UI/Inv.png', (270, 130, 588, 190),False)
    # (231, 578, 637, 611).png
    while not m.ImageCheck('UI/EmptySlot.png', (230, 218 + (40 * min(slotNum, 9)), 638, 251 + (40 * min(slotNum, 9)))):
        useItem(slotNum, 'sell', False)
        m.sleep(.1)
    m.Click(438, 706)
    m.sleep(.1)
    m.Click(667, 697)

if __name__ == '__main__':
    import os
    os.chdir('C:/Users/Evan Chase/Desktop/Files/ProgrammingGit/College/Fall 2023/DragonFable/Images')
    m.sleep(2)
    m_ui.reposition()
    # equip_class(Classes.DragSlay)
