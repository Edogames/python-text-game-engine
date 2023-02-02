# Важные компоненты
from termcolor import colored, cprint
from npc import NPC
from player import Player
from monster import Monster
from saveSystem import SaveSystem
from mainMenu import MainMenu
from utilities import detectChoice, detectGender, goto, clear, pressEnter, splitText, header, warning, success
from store import Store
from location import Location

mainMenu = MainMenu(10, False)

# Не играбельное божество
goddess = [
    NPC("Люцифер", "Дьявол", "f", "дьявол", True),
    NPC("Габриелла", "Ангел", "f", "ангел", True),
]

# Не игровые персонажи
cityNpc = [
    NPC("Линда", "кошка", "f", "житель", True),
    NPC("Лара", "ящерица", "f", "воительница", True),
]


# Обычный предмет
stick = {'name': 'Stick', 'dispName': 'Палка', 'use': None, 'count': 3, 'price': 0, 'description': 'Обычная палка'}
# Личилка
miniHeal = {'name': 'SmolHeal', 'dispName': 'Маленькая аптечка', 'heal': 5, 'count': 2, 'price': 10, 'description': 'Маленькая аптечка'}
# Еда
steak = {'name': 'Stake', 'dispName': 'Стейк', 'hunger': 10, 'count': 3, 'price': 12, 'description': 'Вкусный жаренный стейк, приготовленный с любовью'}

cityItems = [
    stick,
    miniHeal,
    steak,
]

# Магазины
cityStore = Store('Продуктовая', 'City', [miniHeal, steak])

# Локации
locs = [
    Location("Plane", "Равнина", 0, 0, 0, True, [], "Просто равнина.", ['City']),
    Location("Plane2", "Не равнина", 0, 0, 0, True, [], "Это не равнина.", ['City']),
    Location("City", "Город", 20, 10, 10, True, [cityNpc], "Жилой Город.", ['Plane', 'Plane2'], cityItems, cityStore),
]

# Другие персонажи
devil = goddess[0]
angel = goddess[1]

player = []

# Начало
mainMenu.mainMenuScreen()

data = mainMenu.data

if type(data) not in (tuple, list):
    clear()
    from startFunction import start

    player = start()
    player = Player(player[0], player[2], player[1])

    saveSystem = SaveSystem([player], cityNpc)
    saveSystem.save()

    # Переход
    goto("Plane", locs)
else:
    player = Player(data[0][0]['name'], data[0][0]['gender'], data[0][0]['race'], data[0][0]['inventory'], data[0][0]['money'])
    if len(data) > 2:
        for i in cityNpc:
            for a in data[1]:
                if i.name == a['name']:
                    for j in cityNpc:
                        j.inventory = a['inventory']
                        j.relationList = a['relationList']
                        j.married = a['married']
    goto(data[0][1]['name'])
