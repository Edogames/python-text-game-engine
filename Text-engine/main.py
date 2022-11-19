# Важные компоненты
from termcolor import colored, cprint
import time
import os
import random
import json

class SaveSystem:
    def __init__(self, player = [], location: str = "", npc = []):
        if len(player) > 0:
            self.player = player[0]
        self.npc = npc
        self.location = location
        self.save_data = []
        self.data = None

    def save(self):
        self.save_data = [
            {
                'name': self.player.name,
                'gender': self.player.gender,
                'race': self.player.race,
                'inventory': self.player.inventory,
            },
            {
                'name': self.location,
            },
        ]

        if len(self.npc) > 0:
            newNpcArr = []
            for i in self.npc:
                newArr = {
                    'name': i['name'],
                    'married': i['married'],
                    'relationList': i['relationList'],
                    'inventory': i['inventory'],
                }
                newNpcArr.append(newArr)
            self.save_data.append(newNpcArr)

        with open('save.json', 'w', encoding='utf-8') as jsonFile:
            json.dump(self.save_data, jsonFile, ensure_ascii=False, indent=4, default = lambda x: x.__dict__)

        return jsonFile.close()

    def load(self):
        if os.path.exists('save.json'):
            if os.stat('save.json').st_size > 0:
                with open('save.json', 'r') as f:
                    objs = json.loads(f.read())
                    return objs
            else:
                warning("Файл сохранений - пустой!")
                warning("Начните новую игру, что бы эта функция сработала.")
                return False
        else:
            warning("Нет сохранений!")
            warning("Начните новую игру, что бы эта функция сработала.")
            return False

# Текст выбора
class Choices:
    def __init__(self, choices = []):
        self.choices = choices

    def displayChoices(self):
        num = 0
        text = ""
        for i in self.choices:
            num += 1
            text += f"{colored(f'{num} -', 'cyan')} {i} "

        return text

# Меню
class MainMenu:
    def __init__(self, wrdLimit = 10, cheats: bool = False):
        self.cheats = cheats
        self.wrdLimit = wrdLimit
        self.saveSystem = SaveSystem()
        self.data = True
        self.language = 'ru'

    def options(self):
        clear()
        if self.cheats == False:
            cprint("Читы отключены.", "cyan")
        else:
            cprint("Читы включены.", "cyan")

        choices = Choices([
            f"Лимит слов в строке: {self.wrdLimit}(По умолчанию)",
            "Вернуться",
        ])

        print(choices.displayChoices())

        choice = str(input("Выбор: "))

        if choice == '':
            return self.options()
        elif choice == '1':
            new_wrdLimit = input("Введите новое число: ")
            if new_wrdLimit != "":
                self.wrdLimit = int(new_wrdLimit)
                return self.options()
        elif choice == '2':
            return self.mainMenuScreen()

        return self.mainMenuScreen()

    def playBtn(self, choice = '0'):
        clear()
        choices = Choices([
            "Начать новую игру",
            "Загрузить сохранение",
            "Назад",
        ])

        print(choices.displayChoices())
        choice = str(input("Ваш выбор: "))

        if choice == '':
            return self.playBtn()
        elif choice == '3':
            return self.mainMenuScreen()
        elif choice == '1':
            warning("Эта опция может удалить ваши сохранения!")
            warning("Вы уверены?")
            choices = Choices([
                "Да",
                "Нет",
            ])
            print(choices.displayChoices())
            choice = input("Ваш выбор: ")
            if choice == '':
                return self.playBtn('1')
            elif choice == '1':
                return self.data
            elif choice == '2':
                return self.mainMenuScreen()
        elif choice == '2':
            self.data = self.saveSystem.load()
            if self.data != False:
                return self.data
            else:
                input("Нажмите Enter.")
                return self.playBtn()

    def mainMenuScreen(self):
        clear()
        choices = Choices(
            [
                "Играть",
                "Настройки",
            ]
        )

        print(choices.displayChoices())

        choice = str(input("Ваш выбор: "))

        if choice == '':
            return self.mainMenuScreen()
        elif choice == '1':
            return self.playBtn()
        elif choice == '2':
            return self.options()

mainMenu = MainMenu(10, False)

# Всякие детекторы
def detectGender(val):
    female = ['f', 'F', 'ж', "Ж"]
    male = ["м", "М", 'm', 'M']

    if val in female:
        return 'f'
    elif val in male:
        return 'm'
    else:
        return False
def detectChoice(val):
    yes = ['д', 'Д', 'y', 'Y']
    no = ['н',  'Н',  'n',  'N']

    if val in yes:
        return 'yes'
    elif val in no:
        return 'no'
    else:
        return False

# Разделитель текста по лимиту
def splitText(text: str):
    limit = mainMenu.wrdLimit
    words = text.split()
    newText = ""
    wrdCount = 0
    for i in words:
        newText += i + " "
        wrdCount += 1
        if wrdCount == limit or "." in i:
            newText += '\n'
            wrdCount = 0

    return newText

# Типы уведомлений
def warning(text: str, anim: bool = True):
    text = splitText(text)
    if anim == True:
        for i in text:
            time.sleep(0.025)
            cprint(i, 'red', end='', flush=True)
        print()
        time.sleep(0.15)
        return
    else:
        return cprint(text, 'red')
def header(text: str, anim: bool = True):
    text = splitText(text)
    if anim == True:
        for i in text:
            time.sleep(0.01)
            cprint(i, 'yellow', end='', flush=True)
        print()
        time.sleep(0.15)
        return
    else:
        return cprint(text, 'yellow')
def success(text: str, anim: bool = True):
    text = splitText(text)
    if anim == True:
        for i in text:
            time.sleep(0.025)
            cprint(i, 'green', end='', flush=True)
        time.sleep(0.15)
        return
    else:
        return cprint(text, 'green')

# Очистка консоли
def clear():
    return os.system('cls' if os.name=='nt' else 'clear')

# Локации
class Location:
    def __init__(self, name, displayName, monsterChance, lootChance, peopleChance, available = True, entities = [], description = "", availFrom = []):
        self.name = name
        self.displayName = displayName
        self.monsterChance = monsterChance
        self.lootChance = lootChance
        self.peopleChance = peopleChance
        self.description = description

        self.availFrom = availFrom

        self.entities = entities

        self.available = available

    def stats(self):
        print(f"Имя местности: {self.displayName}")
        if self.description != "":
            print(f"Описание местности: {self.description}")
        else:
            print("Неизвестно.")
        if self.monsterChance >= 5:
            monColor = "red"
        else:
            monColor = "green"

        if self.lootChance >= 5:
            lootColor = "green"
        else:
            lootColor = "red"
        cprint(f"Шанс нападение монстров: {self.monsterChance}", monColor)
        cprint(f"Шанс выпадение предметов: {self.monsterChance}", lootColor)

    def getLocs(self, locations):
        availableLocs = []

        for i in locations:
            if i.name != self.name:
                availableLocs.append(i)

        return availableLocs

    def getLoc(self, num):
        initLocs = self.getLocs()
        return initLocs[num - 1].name

    def getPerson(self):
        maxChance = self.peopleChance * 10
        chance = random.randint(0, maxChance)

        if len(self.entities) == 0:
            header("Тут никаго.")
            input("Нажмите Enter.")
            return False

        person = random.choice(self.entities)
        person = random.choice(person)

        if chance > maxChance / 2:
            header("Начало встречи.")
            input("Нажмите Enter.")
            return person
        else:
            header("Пока нескем общаться.")
            input("Нажмите Enter.")
            return False

    def showMap(self, locations):
        text = ""
        num = 0

        for i in locations:
            num += 1
            text += f"{num} - {i.displayName}"

    def start(self, locs, player, choice = '0', confSnd = False, denSnd = False):
        if len(self.entities) > 0:
            newArr = []
            for i in self.entities[0]:
                newDict = {
                    'name': i.name,
                    'married': i.married,
                    'relationList': i.relationList,
                    'inventory': i.inventory,
                }
                newArr.append(newDict)
            saveSystem = SaveSystem([player], self.name, newArr)
            saveSystem.save()
        else:
            saveSystem = SaveSystem([player], self.name)
            saveSystem.save()

        clear()
        if choice == '0' or choice == '':
            if confSnd == True:
                header(f"Вы находитесь в {self.displayName}", False)

            if confSnd == False and denSnd == False:
                header(f"Вы находитесь в {self.displayName}")

            if denSnd == True:
                header(f"Вы находитесь в {self.displayName}", False)


            selection = Choices([
                "Идти",
                "О местности",
                "Игрок",
                "Инвентарь",
                "Поговорить",
            ])

            print(selection.displayChoices())
            choice = str(input())
        if choice == '0' or choice == "":
            return self.start(locs, player, '0', False, True)
        elif choice == '1':
            clear()
            player.say("Куда же мне идти?")
            text = ""
            number = 0
            availLocs = []
            for i in locs:
                if i.name != self.name and i.available == True:
                    for j in i.availFrom:
                        if j == self.name:
                            number += 1
                            availLocs.append(i)
                            text += f"{colored(f'{number} -', 'cyan')} {i.displayName} "

            print(text, f"{colored('0 -', 'cyan')} Отмена")
            num = input()

            if num == '0':
                return self.start(locs, player, '0', False, True)
            elif num == "":
                return self.start(locs, player, '1', False, True)
            return goto(availLocs[int(num) - 1].name, locs)
        elif choice == '2':
            clear()
            self.stats()
            input("Нажмите Enter что бы продолжить...")
            return self.start(locs, player, '0', True)
        elif choice == '3':
            clear()
            selection = Choices([
                "О себе",
            ])
            text = selection.displayChoices()
            text += f"{colored('0 -', 'cyan')} Вернуться"
            print(text)
            choice = int(input())
            if choice == 1:
                player.stats()
                input("Нажмите Enter что бы продолжить...")
                return self.start(locs, player, '3', True, False)
            elif choice == 0:
                return self.start(locs, player, '0', False, True)
        elif choice == '4':
            player.showInv()
            input("Нажмите Enter что бы продолжить...")
            return self.start(locs, player, '0', True, False)
        elif choice == '5':
            person = self.getPerson()
            if person == False:
                return self.start(locs, player, '0', False, True)
            else:
                person.meet(player, self.name)

# Предмет
class Item:
    def __init__(self, name, count, use, description = ""):
        self.name = name
        self.count = count
        self.use = use
        self.description = description

    def stats(self):
        print(f"{colored('|Имя', 'cyan')} -> {colored(self.name, 'cyan')}")
        print(f"{colored('|Количество', 'cyan')} -> {colored(self.count, 'cyan')}")
        return print(f"{colored('|__________________', 'cyan')}")

# Лечилка
class Heal:
    def __init__(self, name, dispName, heal, count, description):
        self.name = name
        self.dispName = dispName
        self.heal = heal
        self.count = count
        self.description = description

    def use(self, target):
        return target.health + self.heal

    def stats(self):
        print(f"{colored('|Имя', 'cyan')}: {self.dispName}")
        print(f"{colored('|Описание', 'cyan')}: {self.description}")
        print(f"{colored('|Количество', 'cyan')}: {self.count}")
        return print(f"{colored('|__________________', 'cyan')}")

# Еда
class Food:
    def __init__(self, name, hunger, description):
        self.name = name
        self.hunger = hunger
        self.description = description

    def use(self, target):
        header(f"Вы использовали {self.name} на {target.name}.")
        return target.stamina + self.hunger

# Игрок
class Player:
    def __init__(self, name, gender, race):
        # Get a name for character
        if name == "":
            self.name = os.getlogin()
        else:
            self.name = name

        self.maxHealth = 100
        self.married = False
        self.armor = False

        gender = detectGender(gender)

        # For better text
        if gender == "f":
            self.textColor = "magenta"
            self.gender = "f"
            self.displayGender = "Женский"
        elif gender == "m":
            self.textColor = "green"
            self.gender = "m"
            self.displayGender = "Мужской"

        # Have own start value
        self.strength = 10
        self.lvl = 1
        self.health = 100
        self.stamina = 100
        self.lives = 3

        self.race = race

        self.inventory = []

    def stats(self):
        cprint(f"Уровень: {self.lvl}", self.textColor)
        cprint(f"Имя: {self.name}", self.textColor)
        cprint(f"Пол: {self.displayGender}", self.textColor)
        cprint(f"Расса: {self.race}", self.textColor)
        cprint(f"Здоровье: {self.health}")

    def showInv(self):
        if len(self.inventory) > 0:
            header("Инвентарь")
            for i in self.inventory:
                i.stats()
        else:
            self.say("У меня ничего нет...")

    def healList(self):
        newList = []
        title = ""
        num = 0
        data = []
        for i in self.inventory:
            if type(i) == Heal:
                num += 1
                newList.append(i)
                title += f"{colored(num, 'cyan')} - {i.dispName}"
        data.append(newList)
        return self.choose(data)
    
    def choose(self, data):
        self.say("Что же мне выбрать?")
        data[1]

    def say(self, text):
        text = splitText(text)
        cprint(f'{self.name}: {text}', self.textColor)

    def addToInv(self, item):
        for i in self.inventory:
            if i.name == item.name:
                return self.plusToInv(i)
        header(f"К вам добавилось {item.name} {item.count} шт.")
        return self.inventory.append(item)

    def plusToInv(self, item):
        for i in self.inventory:
            if i.name == item.name:
                i.count += item.count
                return i
        header(f"Вы получили {item.name} {item.count} шт.")
        return self.addToInv(item)

    def clearInv(self):
        header("Ваш инвентарь был очищен.")
        self.inventory = []
        return self.inventory
    
    def minusFromInv(self, item):
        header(f"С вас отняли {item.name} {item.count} шт.")
        for i in self.inventory:
            if i.name == item.name:
                i.count -= item.count
                if i.count == 0:
                    self.inventory.remove(i)
                    break
                else:
                    break

    def takeDMG(self, amount):
        return self.health - amount

    def heal(self, amount):
        return self.health + amount

# Не игровой персонаж
class NPC:
    def __init__(self, name, race, gender, charType, gay, married = []):
        self.name = name
        self.race = race
        self.gender = gender
        self.charType = charType
        self.gay = gay

        self.lvl = 1
        self.health = 100
        self.stamina = 100

        self.married = married

        self.inventory = []
        self.relationList = []

        if self.gender == "f":
            self.textColor = "magenta"
            self.displayGender = "Женский"
        else:
            self.textColor = "green"
            self.displayGender = "Мужской"

    def addRelationship(self, target, relType):
        self.relationList.append([target.name, relType])

    def stats(self, player):
        if self.health > 0:
            cprint(f"Уровень: {self.lvl}", self.textColor)
            cprint(f"Здоровье: {self.health}")
            cprint(f"Имя: {self.name}", self.textColor)
            cprint(f"Пол: {self.displayGender}", self.textColor)
            cprint(f"Расса: {self.race}", self.textColor)
            cprint(f"Класс: {self.charType}", self.textColor)
            if len(self.married) > 0:
                if self.married[0] == True:
                    print(f"Замужем с {self.married[1]}.")
                else:
                    print("Нет пары.")
            for i in self.relationList:
                if i[0] == player.name and i[1] == player.gender:
                    return print(f"Вы для {self.name} как {i[2]}.")
            return print(f"Вы для {self.name} по сути ни кто.")
        else:
            if self.gender == "m":
                return warning(f"{self.name} Мёртв.")
            else:
                return warning(f"{self.name} Мертва.")

    def say(self, text: str):
        text = splitText(text)
        return cprint(f'{self.name}: {text}', self.textColor)

    def showInv(self):
        if len(self.inventory) > 0:
            header("Инвентарь")
            for i in self.inventory:
                i.stats()
        else:
            self.say("У меня ничего нет...")

    def addToInv(self, item, alert = True):
        for i in self.inventory:
            if i.name == item.name:
                return self.plusToInv(i, alert)
        if alert == True:
            header(f"К '{self.name}' добавилось {item.name} {item.count} шт.")
        return self.inventory.append(item)

    def plusToInv(self, item, alert = True):
        if alert == True:
            if self.gender == "f":
                header(f"{self.name} получила {item.name} {item.count} шт.")
            else:
                header(f"{self.name} получил {item.name} {item.count} шт.")

        for i in self.inventory:
            if i.name == item.name:
                i.count += item.count
                return i
        return self.addToInv(item)

    def clearInv(self, alert = True):
        self.inventory = []
        if alert == True:
            header(f"Инвентарь {self.name} очищен")
        return self.inventory

    def minusFromInv(self, item, alert = True):
        if alert == True:
            header(f"С {self.name} отняли {item.name} {item.count} шт.")
        for i in self.inventory:
            if i.name == item.name:
                i.count -= item.count
                if i.count == 0:
                    self.inventory.remove(i)
                    break
                else:
                    break

    def smolTalk(self, player, placeName, choice = '0'):
        clear()
        if choice == '4':
            self.say(f"Очень приятно познакомиться, {player.name}, я {self.name}, как ты себя чувствуешь?")
            answ = input('Хорошо[д], Плохо[н]: ')
            answ = detectChoice(answ)
            if answ == 'yes':
                self.say(f"Чтож, хих, я {'рада.' if self.gender == 'f' else 'рад.'}")
                input("Нажмите Enter.")
                return self.smolTalk(player, placeName)
            elif answ == 'no':
                self.say(f"Оу, мне жаль {player.name}")
                input("Нажмите Enter.")
                return self.smolTalk(player, placeName)
            else:
                return self.smolTalk(player, placeName, '4')
        else:
            self.say(f'О чём хочешь говорить?')
            choices = Choices([
                "О тебе",
                "О чём угодно",
                "Прекратить разговор",
            ])

            print(choices.displayChoices())
            choice = input("Ваш выбор: ")

            if choice == '':
                clear()
                return self.smolTalk(player, placeName)
            elif choice == '1':
                self.stats(player)
                input("Нажмите Enter.")
                return self.smolTalk(player, placeName)
            elif choice == '2':
                clear()
                return self.smolTalk(player, placeName, '4')
            elif choice == '3':
                clear()
                self.say(f"Хорошо, {player.name}, потом, тогда поговорим.")
                input("Нажмите Enter.")
                header(f"{self.name} {'улыбнулась и ушла' if self.gender == 'f' else 'улыбнулся и ушёл'}.")
                input("Нажмите Enter.")
                return self.endConversation(placeName)

    def endConversation(self, placeName):
            return goto(placeName)

    def conversationWithStranger(self, player, placeName):
        self.addRelationship(player, 'знакомая' if player.gender == 'f' else 'знакомый')
        return self.smolTalk(player, placeName, '0')

    def checkRelationship(self, player, placeName):
        yes = 0
        for i in self.relationList:
            if player.name == i[0]:
                yes += 1

        if yes == 0:
            return self.conversationWithStranger(player, placeName)
        else:
            return self.smolTalk(player, placeName)

    def meet(self, player, placeName, err = False):
        if err == True:
            warning("Такого выбора нет!")
        else:
            self.say(f"Привет, я {self.name}, хочешь говорить?")

        choice = input('[д/н]: ')
        choice = detectChoice(choice)
        if choice == 'yes':
            self.checkRelationship(player, placeName)
            input("Нажмите Enter")
            return goto(placeName, [])
        elif choice == 'no':
            self.say('Ну, видимо у тебя много дел, чтож, не буду мешать.')
            input("Нажмите Enter")
            return goto(placeName, [])
        else:
            return self.meet(player, placeName, True)

# Враг/монстр
class Monster:
    def __init__(self, race, gender, dmgPoint, maxHealth, place):
        self.race = race
        self.gender = gender
        self.place = place
        self.dmgPoint = dmgPoint
        self.maxHealth = maxHealth

        self.defeat = False
        self.health = 100

    def takeDMG(self, amount):
        self.health -= amount
        return self.checkHealth()

    def doDMG(self, target):
        warning(f"{self.race} атакует {target.name}!")
        target.health -= self.dmgPoint

    def death(self):
        self.defeat = True

    def checkHealth(self):
        if self.health < 0:
            self.health = 0
            return self.death()
        elif self.health > self.maxHealth:
            self.health = self.maxHealth
            return self.health

    def say(self, text):
        text = splitText(text)
        cprint(f"{self.race}: {text}", 'red')

# Получение данных
def getName():
    print("(Не вводя имя, вы дадите имя персонажу то же что и системе)")
    value = input("Введите ваше имя: ")
    if value == "":
        value = os.getlogin()
    return value

def getRace():
    value = input("Введите ваш рассу: ")
    return value

# Идти в
def goto(locName, locations = []):
    if locations == []:
        locations = locs

    for i in locations:
        if i.name == locName:
            newLoc = i
            header("Ждите...")
            time.sleep(0.5)
            return newLoc.start(locations, player, '0', False, False)

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

# Локации
locs = [
    Location("Plane", "Равнина", 0, 0, 0, True, [], "Просто равнина.", ['City']),
    Location("Plane2", "Не равнина", 0, 0, 0, True, [], "Это не равнина.", ['City']),
    Location("City", "Город", 20, 10, 10, True, [cityNpc], "Жилой Город.", ['Plane', 'Plane2']),
]

# Другие персонажи
devil = goddess[0]
angel = goddess[1]

player = []

# Начало
mainMenu.mainMenuScreen()

data = mainMenu.data

if type(data) not in (tuple, list):
    def start(checkRace = False, checkGender = False, err = False, data = [], dialogue = False, done = False):
        clear()

        if checkRace == False and checkGender == False and dialogue == False:
            header("Вы просыпаетесь в аду, и перед вами стоит дьяволица, раскошная женщина, и смотрит на вас не совсем довольная.")
            input("Нажмите Enter.")
            clear()
            devil.say("Как звать?")
            name = getName()
            data.append(name)

            return start(True, False, False, data)

        if checkRace == True:
            devil.say("Таак... какой же ты рассы у нас?")
            if err == True:
                warning("Расса не может быть пустым!")
            race = getRace()

            if race != "":
                data.append(race)
                return start(False, True, False, data)
            else:
                return start(True, False, True, data)

        if checkGender == True:
            devil.say("Что-то не понятно, какого ты пола.")
            if err == True:
                warning("Такого пола нет!")

            gender = input('[м/ж]: ')
            gender = detectGender(gender)

            if gender == 'm' or gender == 'f':
                data.append(gender)
                return start(False, False, False, data, True)
            else:
                return start(False, True, True, data, False)

        if dialogue == True:
            clear()
            devil.say(f"Чтож, {data[0]}, пришло время идти в ад за то, что ты {'сделала' if data[2] == 'f' else 'сделал'}")
            input("Нажмите Enter.")
            clear()
            angel.say("Постой!")
            input("Нажмите Enter.")
            clear()
            devil.say("Как ты тут оказалась? Ты же ангел.")
            input("Нажмите Enter.")
            clear()
            angel.say(f"Знаю, и я решила что тебе стоит дать {'ей' if data[2] == 'f' else 'ему'} шанс на новую жизнь.")
            input("Нажмите Enter.")
            clear()
            devil.say("...Ты сейчас серьёзна?")
            input("Нажмите Enter.")
            clear()
            angel.say(f"Да, {'ей' if data[2] == 'f' else 'ему'} ждут очень важные дела на земле.")
            input("Нажмите Enter.")
            clear()
            devil.say("А почему сама не займёшся этим?")
            input("Нажмите Enter.")
            clear()
            angel.say(f"Мне не положено ничего делать, зато {'ей можно' if data[2] == 'f' else 'ему можно'}")
            input("Нажмите Enter.")
            clear()
            devil.say(f"Эх...чтож, так и быть, тебе повезло, {data[0]}...")
            input("Нажмите Enter.")
            clear()
            devil.say(f"Ты не идёшь в ад, но учти, если не справишся, то твой путь тебе, думаю, понятен.")
            input("Нажмите Enter.")
            clear()

            print("Произашла вспышка, и вы потеряли сознание...")
            input("Нажмите Enter.")
            header("Вы проснулись через час после всего, что случилось в том мире.")
            input("Нажмите Enter.")
            header(f"Вам предстоит начать новую жизнь, ведь вы теперь {'не та' if data[2] == 'f' else 'не тот'}, кем были.")
            input("Нажмите Enter.")

            return data


    clear()

    player = start()
    player = Player(player[0], player[2], player[1])

    saveSystem = SaveSystem([player], cityNpc)
    saveSystem.save()

    # Переход
    goto("Plane", locs)
else:
    player = Player(data[0]['name'], data[0]['gender'], data[0]['race'])
    if len(data) > 2:
        for i in cityNpc:
            for a in data[2]:
                if i.name == a['name']:
                    for j in cityNpc:
                        j.inventory = a['inventory']
                        j.relationList = a['relationList']
                        j.married = a['married']
    goto(data[1]['name'])
