import time

import Utils.macro_utils
import Utils.ui_macro_utils
from Utils import ui_macro_utils as m_ui
import Utils.macro_utils as m
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
    while not m.ImageCheck('UI/CompleteNythera.png', (545, 298, 810, 364)):
        positions = []
        waitTime = time.time()
        while time.time() - waitTime < 2.5:
            diff = Utils.macro_utils.mask_image(m.RegionGrab((260, 252, 1046, 686)), glowless)
            pos = Utils.macro_utils.largest_in_mask(diff, 6000)
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
    m_ui.CheckQuestDialog()


