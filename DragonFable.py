import os
import sys
from time import localtime, strftime, time, sleep

from DFSubscripts.farming import Nythera
from DFSubscripts.navigation import sell_items_dragonless, travel_to
from Utils.ui_macro_utils import openApp, reposition
from Utils.macro_utils import SLOT_TO_SELL, MAX_SLOTS, SAVE_PATH

def delay():
    for i in range(3, 0, -1):
        print(', '.join([str(x) for x in range(3, i-1, -1)]) + ' ...', end = ' \r')
        sleep(0.75)
    print('3, 2, 1 GO!!', end = ' \r')
    sleep(0.75)

def get_variables():
    i = 0
    try:
        name = sys.argv[1]
        if name == 'continue':
            with open('../DFQuestLog.txt', 'r+') as of:
                lines = list(of)
                if 'END' in lines[-1].upper():
                    raise AssertionError('Quest Already Completed')
                else:
                    i, name, count = lines[0].split()
                    i = int(next((lines[i] for i in range(len(lines) -1,-1,-1) if 'Completed' in lines[i]), 'a 0').split()[1])
                    of.write('\n-RESTART-')
                    if name != 'Delay': openApp()
        else:
            try:
                count = int(sys.argv[2])
                try:
                    if sys.argv[3] == 'afk':openApp()
                except IndexError: pass
            except IndexError: count = -1
    except IndexError:
        name = input('What Quest do you want to run? ')
        count = int(input('How many times: '))
    return name, int(count), i

def update_log(i, startTime, startI):
    if (i-startI) == 0: time_str = 'N/A'
    else: time_str = ("%.2f" % ((time()-startTime) / (i-startI)))
    with open('../DFQuestLog.txt', 'a') as of:
        if i != startI:
            of.write('\nCompleted: ' + str(i) + ' Avg: ' + time_str)
        print('Completed: ' + str(i) + ' Avg: ' + time_str, end=' \r')
    return i + 1

def main():
    os.chdir(SAVE_PATH)
    name, count, i = get_variables()
    delay()
    startQuest()
    if i == 0:
        with open('../DFQuestLog.txt', 'w') as of: of.write(f'Running {name} {count}\n-BEGIN-')
    with open('../DFQuestLog.txt', 'a') as of:
        of.write('\nStart Time: ' + (strftime("%H:%M:%S", localtime())))
        print('Start Time: ' + (strftime("%H:%M:%S", localtime())))
    startTime, startI = time(), i
    if count == -1:
        while True:
            i = update_log(i, startTime, startI)
            if name == 'PotionMastery' and i % (MAX_SLOTS - SLOT_TO_SELL + 1) == 0:
                runQuest('SellThem')
                startQuest()
            runQuest(name)
    else:
        for _ in range(startI, count):
            i = update_log(i, startTime, startI)
            if name == 'PotionMastery' and i % (MAX_SLOTS - SLOT_TO_SELL + 1) == 0:
                runQuest('SellThem')
                startQuest()
            runQuest(name)
    update_log(count, startTime, startI)
    with open('../DFQuestLog.txt', 'a') as of:
        of.write('\nEnd Time: ' + (strftime("%H:%M:%S", localtime())) + '\n-END-')
        print('End Time: ' + (strftime("%H:%M:%S", localtime())))
    try:
        sleep(1)
    except IndexError: pass

def startQuest():
    reposition()
    travel_to('Warlic')

def runQuest(name):
    try:
        if name == 'PotionMastery': Nythera()
        elif name == 'SellThem': sell_items_dragonless()
    except AssertionError: return

if __name__ == '__main__':
    main()