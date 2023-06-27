from time import sleep

import Utils.df_types as df_types
import Utils.macro_utils as m
from Utils import ui_macro_utils


def getHp():
    return m.readText((260, 742, 368, 792))
def getMp():
    return m.readText((382, 750, 491, 784))
def getEHp():
    txt = m.readText((836, 799, 942, 832))
    return int('0'+"".join([c for c in txt if c.isdigit()]))
def getEMp():
    txt = m.readText((970, 799, 1076, 832))
    return int("".join([c for c in txt if c.isDigit()]))
def getMoveSet(moveSetID):
    def EmpowerBDL(k): # (EmpowerBDL, 'c')
        m.Click(745, 593)
        return k
    def Gambit(k, toggle=False):
        if toggle: m.Click(601, 596)
        m.typeKeys('4')
        m.ImgGoneCheck('Battle/Attack.png', (576, 630, 698, 698), 4)
        m.ImageCheck('Battle/Attack.png', (576, 630, 698, 698), 4)
        m.Click(601, 60)
        return k
    def Depower(k):
        m.Click(601, 596)
        m.sleep(1)
        return k
    def Quit(k): raise AssertionError('Force End Battle Rotation') # (Quit, '')
    def ClawIfUp(k): return '6' if m.ImageCheck('Battle/DLClaw.png', (715, 639, 772, 694)) else k
    def ChangeTarget(targetImg, k, toggle=False):
        if toggle:
            m.Click(601, 596)
            m.sleep(1)
        for _ in range(6):
            if m.ImageCheck(targetImg, (811, 737, 1166, 857), 0.5): break
            m.typeKeys('\t')
        # for _ in range(6):
        #     if m.ImageCheck(targetImg, (811, 737, 1166, 857), 0.5): break
        #     m.typeKeys('>')
        # for _ in range(6):
        #     if m.ImageCheck(targetImg, (811, 737, 1166, 857), 0.5): break
        #     m.typeKeys('<')
        m.sleep(1)
        return k

    classId, style = moveSetID
    if classId == df_types.Classes.Mage:
        if 'Quick' in style: return False, ['v', '8', '7']
        elif 'Recover' in style: return False, ['1', '4', 'v', '8', '7']
        elif 'Burst' in style: return True, ['3', '6', '0', '8', '7', '9', '6', '0', '8', '7', '9', '6', '0', '8', '7']
        elif 'Hatir' in style: return True, ['z', '9', '0', '1', '8', '2', '5', '6', '7', 'z', '9', '0', '3', '8', '2', '5', '6', '7']
        else: return True, ['3', '6', '0', '8', '7', '9', '5', '1', '4', '2', '6', '0', '8', '7', '9']
    elif classId == df_types.Classes.Necro:
        if 'Recover' in style: return False, ['x', '1', '8']
        else: return True, ['0', '5', '2', 'x', 'v', '0', '6', 'z', '7', '8', '0', '5', '2', 'x', 'v', '0', '4', '1', '2', 'c']
    elif classId == df_types.Classes.BDL:
        if 'Recover' in style: return False, ['3', '2', (EmpowerBDL, '4'), 'v', '6', '6', 'x']
        elif 'Pandora' in style: return True, ['0','v','6',(EmpowerBDL, '4'),'x','6','c','6',(EmpowerBDL, '3'),'2','9',(EmpowerBDL, '8'),'z','5']
        else: return True, ['0', '3', '6', 'x', '9', '1', '2', '6', (EmpowerBDL, '5'), 'v', '4', '8', (EmpowerBDL, 'c'), 'z', (Quit, '')]
    elif classId == df_types.Classes.WDL:
        if 'Quick' in style: return False, ['z', 'x', '6', '6']
    elif classId == df_types.Classes.Warrior:
        if 'PVP' in style: return True, ['3','5','6','7','v','6','7','5','z','6','7','4','6','7',' ']
        else: return False, ['v',' ','z','3','z','5','z',' ']
    elif classId == df_types.Classes.Chaosweaver:
        if 'PVP' in style: return False, [(Gambit,'8'),'v','c','9',(Gambit,'z'),(Depower,'x'),'2','0',(Gambit,'c',True),'2','9','3','z',(Gambit,'8'),'0']
        elif 'ArchiveNorm' in style: return False, [(Gambit, '3'), '2', '6']
        elif 'ArchiveMini' in style: return False, [(Gambit, '9'), 'v', 'c']
        elif 'ArchiveBoss' in style: return False, [(ChangeTarget, 'Inn/Enemies/Celestial.png','3'),(Gambit,'c'),(ChangeTarget,'Inn/Enemies/Infernal.png','z'),(Depower,'9'),(Depower, '1'),(Gambit,'x'),'v','0','c','2',(Gambit, 'z'), (Depower, '9'),'6','2',(Gambit,'0', True),'c','x','2','z',(Gambit, 'v'), (Depower, '9'),'c','0']
        elif 'Quick' in style: return False, [(Gambit,'3'),'v','c']
        elif 'Recover' in style: return False, [(Gambit,'3'),'c']
        elif 'Bound' in style: return False, ['4','9','v','5','3','z','4','0','c']
        elif 'AARGH' in style: return True, ['1','3','4','9','z','v','3','4','0','c','6',' ']
        elif 'Warden' in style: return False, ['4','9','b','v','z','5','3','4','0','c']
        elif 'Boss' in style: return True, ['e4','d1','9','v','3','e4','dc',8,'z','2','e4','d3','6']
        elif 'Multi' in style: return False, ['4','8','7','v','z']
    elif classId == df_types.Classes.DragSlay:
        if 'Boss' in style: return True, ['3', '4', '0', '4', '7', '4']
    elif classId == df_types.Classes.Drag: return True, ['5', '7', '2', '6', 'c', 'v', 'x', 'b', '6', '3', '1']
    elif classId == df_types.Classes.KidDrag: return False, (['x','x','x','x','x','x','x','x'] if 'Multi' in style else ['3'])
    else: return True, [' '] # m.click(251, 661)
def eatFood(foodLeft):
    healPerc = 23 #Each px is 1%
    pix = ui_macro_utils.screenshot(True).getpixel((192 + healPerc, 730))
    if foodLeft > 0 and pix == (14, 14, 14):
        m.Click(538, 794)
        m.ClickImage('UI/TempItems.png', (428, 82, 580, 138), 3)
        m.Click(368, 244)
        m.Click(956, 650)
        sleep(2)
        m.Click(434, 709)
        m.ImageSearch('Battle/Attack.png', (576, 630, 698, 698), -1)
        return foodLeft - 1
    return foodLeft
def battle(moveSetID, useFood = False):
    def dragPrimal(): return 'z' if m.ImageCheck('Battle/DragonsPrimal.png', (164, 634, 230, 708)) else ' '
    dragonMoveSet = ['6', '7', '3', '8', '4', '5', '1', '3', ' ', '4', '', '', '3', '', '4', '', '', '3', '', '4']
    looping, moveSet = getMoveSet(moveSetID)
    canEat = 2
    if 'Quick' in moveSetID or 'PVP' in moveSetID: dragonMoveSet.append(dragonMoveSet.pop(0))
    if 'ArchiveNorm' in moveSetID: dragonMoveSet.append(dragonMoveSet.pop(0))
    if 'Bound' in moveSetID or 'Warden' in moveSetID: dragonMoveSet = ['7','6','8','3','5']+dragonMoveSet
    if 'AARGH' in moveSetID: dragonMoveSet = ['8','6','7','','3','4']+dragonMoveSet
    if 'ArchiveBoss' in moveSetID: useFood = True
    while not m.ImageCheck('Battle/Battle_Complete.png', (548, 508, 756, 588)):
        sleep(.2)
        if m.ImageCheck('Battle/Stuck.png', (550, 670, 723, 713)): m.Click(636, 692)
        if not m.ImageCheck('Battle/Attack.png', (576, 630, 698, 698)): continue
        m.forceAwake()
        m.sleep(.01)
        if m.ImageCheck('Battle/DragonsTurn.png', (1120, 642, 1180, 700)):
            # Dragon's Turn
            if (a := dragonMoveSet.pop(0)) == '': m.typeKeys(dragPrimal())
            else: m.typeKeys(a)
            dragonMoveSet.append(a)
        else:
            # Player's Turn
            if useFood and canEat: canEat = eatFood(2)
            if type(a := moveSet.pop(0)) is tuple: m.typeKeys(a[0](*a[1:]))
            else: m.typeKeys(a)
            moveSet.append(a if looping else ' ')
        m.ImgGoneCheck('Battle/Attack.png', (576, 630, 698, 698), 1)
    if m.ImageCheck('Battle/Defeat.png', (253, 755, 371, 777)):
        m.typeKeys(' ')
        raise AssertionError('Battle Failed')
    else: m.typeKeys(' ')
