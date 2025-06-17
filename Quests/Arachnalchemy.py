import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../Utils")))
import ui_helpers as ui

ui.SetUp(__file__)

import time
import glob

atkbtn = "AttackBtn#(1132, 1240, 1415, 1400).png"
btlovr = "BattleOver#(1175, 1050, 1437, 1120).png"
drgtrn = "DragTurn#(2242, 1280, 2342, 1382).png"


def await_over_or_atk(k):
    ui.AwaitImg(atkbtn, btlovr)
    if ui.Check(btlovr):
        return
    ui.Press(k)
    ui.AwaitNotImg(atkbtn)


def battle_scrub():
    ui.AwaitImg(atkbtn, timeout=10)
    await_over_or_atk("3")
    await_over_or_atk("7")
    while not ui.Check(btlovr):
        await_over_or_atk(" ")
    ui.Press(" ")
    time.sleep(4)


def battle_group():
    ui.AwaitImg(atkbtn, timeout=10)
    await_over_or_atk("4")
    await_over_or_atk("8")
    await_over_or_atk("7")
    await_over_or_atk("7")
    while not ui.Check(btlovr):
        await_over_or_atk(" ")
    ui.Press(" ")
    time.sleep(4)


def battle_bass():
    def try_drag(k):
        if ui.AwaitImg(drgtrn):
            ui.Press(k)
            ui.AwaitNotImg(drgtrn)
        ui.AwaitImg(atkbtn, timeout=10)

    def try_player(k):
        ui.AwaitImg(atkbtn)
        ui.ClickIf("#(734, 197, 812, 243).png")
        if ui.Check("Subdue#(340, 210, 660, 295).png"):
            raise Exception("Finished Quest")
        ui.Press(k)
        ui.AwaitNotImg(atkbtn)

    try:
        try_player("4")
        try_player("9")
        try_drag("8")

        try_player("v")
        try_drag("3")

        try_player("z")
        try_drag("7")

        try_player("1")
        try_drag("4")

        try_player("4")
        try_player("c")
        try_drag(" ")

        try_player("0")
        try_drag("5")

        try_player("6")
        try_drag("6")
        while True:
            try_player("3")
            try_drag(" ")
            try_player("2")
            try_drag(" ")
            try_player(" ")
            try_drag(" ")
    except Exception:
        ui.ClickIf("Subdue#(340, 210, 660, 295).png")
        ui.ClickIf(btlovr)
        ui.ClickIf("#(980, 637, 1541, 785).png")
        ui.ClickIf("#(1114, 1271, 1478, 1369).png")


def quest(target="DireWolf#(1388, 149, 1800, 246).png"):
    # Heal Self
    ui.AwaitImg("QuestStart#(1519, 590, 2161, 755).png", timeout=15)
    if ui.ClickIf("QuestBook#(1372, 1501, 1511, 1642).png"):
        ui.AwaitImg("#(1210, 1558, 1339, 1674).png", timeout=10)
        ui.ClickIf("#(877, 1473, 1035, 1628).png")
        ui.ClickIf("#(1210, 1558, 1339, 1674).png")

    # Start Quest
    ui.ClickIf("QuestStart#(1519, 590, 2161, 755).png", timeout=15)
    ui.ClickIf("#(1608, 909, 2086, 1019).png")
    ui.ClickIf(target)
    for _ in range(5):
        time.sleep(0.25)
        ui.MouseClick(1213, 988)
    ui.ClickIf("#(1624, 624, 2073, 742).png")
    # Room 1
    ui.AwaitImg("PotChest#(950, 820, 1080, 950).png", timeout=24)
    ui.MouseClick(2337, 1131)
    battle_scrub()
    ui.AwaitImg(*glob.glob("Room1/*"), timeout=4)
    ui.MouseClick(2337, 1131)
    # Room 2
    for i in range(3):
        ui.AwaitImg(*glob.glob("Room2/*"), timeout=4)
        ui.MouseClick(2337, 1131)
        time.sleep(0.25)
        if i != 2:
            battle_scrub()
    # Room 3
    ui.AwaitImg(*glob.glob("Room3/*"), timeout=4)
    ui.MouseClick(2337, 1131)
    battle_group()
    ui.AwaitImg(*glob.glob("Room3/*"), timeout=4)
    ui.MouseClick(2337, 1131)
    # Room 4
    ui.AwaitImg(*glob.glob("Room4/*"), timeout=4)
    ui.MouseClick(2337, 1131)
    battle_group()
    ui.AwaitImg(*glob.glob("Room4/*"), timeout=4)
    ui.MouseClick(2337, 1131)
    # Room 5
    ui.AwaitImg(*glob.glob("Room5/*"), timeout=4)
    ui.MouseClick(2337, 1131)
    battle_bass()
    print("Quest Cleared")


for _ in range(7):
    quest("#(1864, 1137, 2274, 1227).png")
    # quest("DesertDiver#(1385, 298, 1779, 391).png")
    # quest("EOrbWeaver#(1396, 430, 1790, 523).png")
    # quest("Fluffy#(1401, 576, 1785, 659).png")
