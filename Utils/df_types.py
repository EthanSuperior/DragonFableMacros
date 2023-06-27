from enum import Enum
class Classes(Enum):
    Warrior = 'Warrior^metal'
    Mage = 'Atealan CC Base^ice'
    BDL = 'DragonLord#Bulwark^metal'
    WDL = 'DragonLord#Wrath^metal'
    Necro = 'Necromancer^darkness'
    DragSlay = 'DragonSlayer^metal'
    Drag = 'Dragon Rider'
    Chaosweaver = 'Chaosweaver^metal'
    Pirate = 'Dread Pirate^darkness'
    Techno = 'Technomancer^light'
    KidDrag = 'KidDrag^bacon'

class Elements(Enum):
    Bacon = 'bacon'
    Darkness = 'darkness'
    Disease = 'disease'
    Ebil = 'ebil'
    Energy = 'energy'
    Evil = 'evil'
    Fear = 'fear'
    Fire = 'fire'
    Good = 'good'
    Ice = 'ice'
    Light = 'light'
    Metal = 'metal'
    Nature = 'nature'
    Poison = 'poison'
    Silver = 'silver'
    Stone = 'stone'
    Water = 'water'
    Wind = 'wind'
    Unknown = '???'

class GearType(Enum):
    Any = 0
    Weapon = 1
    Pet = 2
    Helm = 3
    Wing = 4
    Cape = 4
    Necklace = 5
    Belt = 6
    Ring = 7
    Trinket = 8
    Bracer = 9
    Armor = 10
    Junk = 11
    Misc = 11

class PlayerInfo:
    classID = Classes.Mage
    wep = Elements.Wind

QuestLocations = {
    'NorthWest':  (75, 63),  'North':  (638, 63),  'NorthEast':   (1198, 63),
    'West':       (75, 513), 'Center': (638, 513), 'East':        (1198, 513),
    'SouthWest':  (75, 710), 'South':  (638, 710), 'SouthEast':   (1198, 710)}

default_class = PlayerInfo()