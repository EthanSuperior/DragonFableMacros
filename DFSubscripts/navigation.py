from Utils import macro_utils as m
from Utils import ui_macro_utils as m_ui

def openLoreBook():
    if not m.ImageCheck('UI/LoreBookOpen.png', (173, 106, 551, 199), .5):
        m.ClickImage('UI/LoreBookIcon.png', (668, 744, 768, 852), 3)
        m.ImageSearch('UI/LoreBookOpen.png', (173, 106, 551, 199), 3)

def openBook(bkNum):
    openLoreBook()
    if str(bkNum) == '1':
        m_ui.ClickBtn('UI/Book1.png', (132, 195, 512, 348))

def useItem(slotNum = 1, type='equip'):
    for _ in range(9, slotNum):
        m.Click(672, 590)
        m.sleep(.1)
    m.Click(208, 240 + (40 * min(slotNum, 9)))
    m.sleep(.1)
    if type == 'equip':
        m.Click(920, 668)
    elif type == 'sell':
        m.Click(956, 698)
        m_ui.ClickBtn('UI/Yes.png', (501, 443, 632, 494))

def travel_to(location):
    openLoreBook()
    if location == 'Falconreach':
        openBook(1)
        m_ui.ClickBtn('UI/FalconreachBtn_Bk1.png', (515, 523, 759, 584))
        while not m.ImageCheck('UI/Falconreach_Bk1.png', (295, 151, 543, 276)):
            m.Click(298, 385)
            m.sleep(.1)
    if location == 'Warlic':
        if not m.ImageCheck('Locations/WarlicPortal.png', (774, 77, 1162, 346)):
            openBook(1)
            m_ui.ClickBtn('UI/Timeline_Bk1.png', (502, 197, 778, 263))
            m.drag((1204, 600), (72, 600))
            m.Click(298, 385)
            m_ui.ClickBtn('UI/GoToWarlic_Bk1.png',(896, 499, 1089, 551))
            m.ImageCheck('Locations/WarlicPortal.png', (774, 77, 1162, 346), 3)

def sell_items_dragonless(slotNum = m.SLOT_TO_SELL):
    travel_to('Falconreach')
    m.Click(534, 476)
    m.ImageCheck('Locations/Ash_Bk1.png', (212, 99, 513, 363), 3)
    m_ui.ClickBtn('UI/AshStore.png', (580, 581, 752, 624))
    m_ui.ClickBtn('UI/SellTab.png',(446, 101, 563, 127),'UI/Inv.png', (270, 130, 588, 190),False)
    while not m.ImageCheck('UI/EmptySlot.png', (230, 218 + (40 * min(slotNum, 9)), 638, 251 + (40 * min(slotNum, 9)))):
        useItem(slotNum, 'sell')
        m.sleep(.1)
    m.Click(438, 706)
    m.sleep(.1)
    m.Click(667, 697)

