from Utils import macro_utils as m
from Utils.quest_macro_utils import CheckQuestDialog
def Utils(classID):
    pass
def QuestLoot():
    try: CheckQuestDialog()
    except AssertionError as msg:
        if str(msg) == 'Quest Complete':
            m.Click(650, 670)
            if m.ImageCheck('UI/ItemGet.png', (514, 126, 782, 184), 2): m.Click(654, 669) # REJECT m.relClick(658, 715)
        else: raise AssertionError(msg)
