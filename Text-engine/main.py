# Важные компоненты
import math
from termcolor import colored, cprint
import time
import os
import random
import pygame
import mypy

pygame.init()
pygame.mixer.init()

# Текст выбора
class Choices:
    def __init__(self, choices: list[str] = []):
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

    def options(self):
        if self.cheats == False:
            cprint("Читы отключены.", "cyan")
        else:
            cprint("Читы включены.", "cyan")

        choices = Choices([
            f"Лимит слов в строке: {self.wrdLimit}(По умолчанию)",
            "Вернуться",
        ])

        print(choices.displayChoices())

        choice = input("Выбор: ")

        if choice == '1':
            new_wrdLimit = input("Введите новое число: ")
            if new_wrdLimit != "":
                self.wrdLimit = int(new_wrdLimit)
                return self.options()
        elif choice == '2':
            return self.mainMenuScreen()

        return self.mainMenuScreen()

    def mainMenuScreen(self):
        choices = Choices(
            [
                "Играть",
                "Настройки",
            ]
        )

        print(choices.displayChoices())

        choice = int(input("Ваш выбор: "))

        if choice == 1:
            return True
        else:
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
def splitText(text: str, limit = mainMenu.wrdLimit):
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
def warning(text: str):
    text = splitText(text)
    return print(f"{colored(text, 'red')}")
def header(text: str):
    text = splitText(text)
    print(f"{colored(text, 'yellow')}")
def success(text: str):
    text = splitText(text)
    return print(colored(f'Успех! {text}!', "green"))

# Очистка консоли
def clear():
    return os.system('cls' if os.name=='nt' else 'clear')

# Локации
class Location:
    def __init__(self, name: str, displayName: str, monsterChance: int, lootChance: int, peopleChance: int, available: bool = True, entities: list[object] = [], description: str = "", availFrom: list[str] = []):
        self.name = name
        self.displayName = displayName
        self.monsterChance = monsterChance
        self.lootChance = lootChance
        self.peopleChance = peopleChance
        self.description = description

        self.availFrom = availFrom

        self.entities = entities

        self.available = available

        self.tpSound = pygame.mixer.Sound('Sounds/Player/Teleport.wav')
        self.confirmSound = pygame.mixer.Sound('Sounds/Menus/Confirm.wav')
        self.denySound = pygame.mixer.Sound('Sounds/Menus/Denied.wav')

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

    def goto(self, name: str, locations: list[object]):
        header("Ждите...")
        time.sleep(0.5)
        return goto(name, locations)

    def getLocs(self, locations: list[object]):
        availableLocs = []

        for i in locations:
            if i.name != self.name:
                availableLocs.append(i)

        return availableLocs

    def getLoc(self, num: int):
        initLocs = self.getLocs()
        return initLocs[num - 1].name

    def getPerson(self):
        maxChance = self.peopleChance * 10
        chance = random.randint(0, maxChance)

        citizens = []

        if len(self.entities) > 0:
            for i in self.entities:
                if type(i) == NPC:
                    citizens.append(i)
        else:
            header("Тут никаго.")
            input("Нажмите Enter.")
            return False

        person = random.choice(citizens)

        if chance > maxChance / 2:
            header("Начало встречи.")
            input("Нажмите Enter.")
            return person
        else:
            header("Пока нескем общаться.")
            input("Нажмите Enter.")
            return False

    def showMap(self, locations: list[object]):
        text = ""
        num = 0

        for i in locations:
            num += 1
            text += f"{num} - {i.displayName}"

    def start(self, locs: list[object], player: object, choice: str = '0', confSnd: bool = False, denSnd: bool = False):
        clear()
        if choice == '0' or choice == '':
            header(f"Вы находитесь в {self.displayName}")

            if confSnd == True:
                self.confirmSound.play()

            if confSnd == False and denSnd == False:
                self.tpSound.play()

            if denSnd == True:
                self.denySound.play()

            selection = Choices([
                "Идти",
                "О местности",
                "Игрок",
                "Поговорить",
            ])

            print(selection.displayChoices())
            choice = str(input())
        if choice == '0' or choice == "":
            return self.start(locs, player, '0', False, True)
        elif choice == '1':
            self.confirmSound.play()
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
            self.confirmSound.play()
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
            persone = self.getPerson()
            if persone == False:
                return self.start(locs, player, '0', False, True)
            else:
                persone.meet(player, self.name)

# Предмет
class Item:
    def __init__(self, name: str, count: int, use: str, description: str = ""):
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
    def __init__(self, name: str, dispName: str, heal: int, count: int, description: str):
        self.name = name
        self.dispName = dispName
        self.heal = heal
        self.count = count
        self.description = description

        self.useSound = pygame.mixer.Sound('Sounds/Player/Heal.wav')
        self.statsSound = pygame.mixer.Sound('Sounds/Menus/Confirm.wav')

    def use(self, target: object):
        self.useSound.play()
        return target.health + self.heal

    def stats(self):
        self.statsSound.play()
        print(f"{colored('|Имя', 'cyan')}: {self.dispName}")
        print(f"{colored('|Описание', 'cyan')}: {self.description}")
        print(f"{colored('|Количество', 'cyan')}: {self.count}")
        return print(f"{colored('|__________________', 'cyan')}")

# Еда
class Food:
    def __init__(self, name: str, hunger: int, description: str):
        self.name = name
        self.hunger = hunger
        self.description = description

    def use(self, target: object):
        header(f"Вы использовали {self.name} на {target.name}.")
        return target.stamina + self.hunger

# Игрок
class Player:
    def __init__(self, name: str, gender: str, race: str):
        # Get a name for character
        if name == "":
            self.name = os.getlogin()
        else:
            self.name = name

        self.maxHealth = 100
        self.married = False
        self.armor = False

        # For better text
        if gender == "female" or gender == "Female" or gender == 'f' or gender == 'F' or gender == 'ж' or gender == 'Ж':
            self.textColor = "magenta"
            self.gender = "f"
            self.displayGender = "Женский"
        elif gender == "male" or gender == "Male" or gender == 'm' or gender == 'M' or gender == 'м' or gender == 'М':
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

        self.confirmSound = pygame.mixer.Sound('Sounds/Menus/Confirm.wav')

    def stats(self):
        self.confirmSound.play()
        cprint(f"Уровень: {self.lvl}", self.textColor)
        cprint(f"Имя: {self.name}", self.textColor)
        cprint(f"Пол: {self.displayGender}", self.textColor)
        cprint(f"Расса: {self.race}", self.textColor)
        cprint(f"Здоровье: {self.health}")

    def showInv(self):
        if len(self.inventory) > 0:
            self.confirmSound.play()
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
    
    def choose(self, data: list):
        self.say("Что же мне выбрать?")
        data[1]

    def say(self, text: str):
        text = splitText(text)
        cprint(f'{self.name}: {text}', self.textColor)

    def addToInv(self, item: object):
        for i in self.inventory:
            if i.name == item.name:
                return self.plusToInv(i)
        header(f"К вам добавилось {item.name} {item.count} шт.")
        return self.inventory.append(item)

    def plusToInv(self, item: object):
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
    
    def minusFromInv(self, item: object):
        header(f"С вас отняли {item.name} {item.count} шт.")
        for i in self.inventory:
            if i.name == item.name:
                i.count -= item.count
                if i.count == 0:
                    self.inventory.remove(i)
                    break
                else:
                    break

    def takeDMG(self, amount: int):
        return self.health - amount

    def heal(self, amount: int):
        return self.health + amount

# Не игровой персонаж
class NPC:
    def __init__(self, name: str, race: str, gender: str, type: str, gay: bool, married: list[str, str] = ["", ""]):
        self.name = name
        self.race = race
        self.gender = gender
        self.type = type
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

    def addRelationship(self, target: object, relType: str):
        self.relationList.append([target.name, target.gender, relType])

    def stats(self, player: object):
        if self.health > 0:
            cprint(f"Уровень: {self.lvl}", self.textColor)
            cprint(f"Здоровье: {self.health}")
            cprint(f"Имя: {self.name}", self.textColor)
            cprint(f"Пол: {self.displayGender}", self.textColor)
            cprint(f"Расса: {self.race}", self.textColor)
            cprint(f"Класс: {self.type}", self.textColor)
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
        cprint(f'{self.name}: {text}', self.textColor)

    def showInv(self):
        if len(self.inventory) > 0:
            header("Инвентарь")
            for i in self.inventory:
                i.stats()
        else:
            self.say("У меня ничего нет...")

    def addToInv(self, item: object, alert: bool = True):
        for i in self.inventory:
            if i.name == item.name:
                return self.plusToInv(i, alert)
        if alert == True:
            header(f"К '{self.name}' добавилось {item.name} {item.count} шт.")
        return self.inventory.append(item)

    def plusToInv(self, item: object, alert: bool = True):
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

    def clearInv(self, alert: bool = True):
        self.inventory = []
        if alert == True:
            header(f"Инвентарь {self.name} очищен")
        return self.inventory

    def minusFromInv(self, item: object, alert: bool = True):
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

    def endConversation(self, placeName: str):
            return goto(placeName)

    def conversationWithStranger(self, player: object, placeName: str):
        self.say(f"Очень приятно познакомиться, {player.name}, я {self.name}, как ты себя чувствуешь?")
        self.relationList.append([player.name, 'Знакомая' if player.gender == 'f' else 'Знакомый'])
        answ = input('Хорошо[д], Плохо[н]: ')
        answ = detectChoice(answ)
        if answ == 'yes':
            self.say("Чтож, хих, я " + "рада." if self.gender == 'f' else "рад.")
            input("Нажмите Enter.")
            self.say("Ладно, встретимся позже.")
            input("Нажмите Enter.")
            return self.endConversation(placeName)
        elif answ == 'no':
            self.say(f"Оу, мне жаль {player.name}")
            input("Нажмите Enter.")
            self.say("Ладно, встретимся позже.")
            input("Нажмите Enter.")
            return self.endConversation(placeName)
        else:
            return self.conversationWithStranger(player, placeName)

    def startMeet(self, player, placeName):
        yes = 0
        for i in self.relationList:
            if player.name == i[0]:
                yes += 1

        if yes == 0:
            return self.conversationWithStranger(player, placeName)

    def meet(self, player, placeName, err = False):
        if err == True:
            warning("Такого выбора нет!")
        else:
            self.say(f"Привет, я {self.name}, хочешь говорить?")

        choice = input('[д/н]: ')
        choice = detectChoice(choice)
        if choice == 'yes':
            self.startMeet(player, placeName)
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
    def __init__(self, race: str, gender: str, dmgPoint: int, maxHealth: int, place: str):
        self.race = race
        self.gender = gender
        self.place = place
        self.dmgPoint = dmgPoint
        self.maxHealth = maxHealth

        self.defeat = False
        self.health = 100

        self.hitSound = pygame.mixer.Sound('Sounds/Player/Hit.wav')

    def takeDMG(self, amount: int):
        self.health -= amount
        return self.checkHealth()

    def doDMG(self, target: object):
        warning(f"{self.race} атакует {target.name}!")
        self.hitSound.play()
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

    def say(self, text: str):
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
def goto(locName: str, locations: list[object] = []):
    if locations == []:
        locations = locs

    for i in locations:
        if i.name == locName:
            newLoc = i
            return newLoc.start(locations, player, '0', False, False)

# Не играбельное божество
goddess = [
    NPC("Люцифер", "Дьявол", "f", "дьявол", True),
    NPC("Габриелла", "Ангел", "f", "ангел", True),
]

# Локации
locs = [
    Location("Plane", "Равнина", 0, 0, 0, True, [], "Просто равнина.", ['Plane2']),
    Location("Plane2", "Не равнина", 0, 0, 0, True, [], "Это не равнина.", ['City']),
    Location("City", "Город", 20, 10, 10, True, [NPC("Линда", "кошка", "f", "житель", True),], "Жилой Город.", ['Plane', 'Plane2']),
]

# Другие персонажи
devil = goddess[0]
angel = goddess[1]

player = []

def start(checkRace: bool = False, checkGender: bool = False, err: bool = False, data: list = [], dialogue: bool = False, done: bool = False):
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
        devil.say(f"Чтож, {data[0]}, пришло время идти в ад за то, что ты " + "сделала" if data[2] == 'f' else "сделал")
        input("Нажмите Enter.")
        clear()
        angel.say("Постой!")
        input("Нажмите Enter.")
        clear()
        devil.say("Как ты тут оказалась? Ты же ангел.")
        input("Нажмите Enter.")
        clear()
        angel.say("Знаю, и я решила что тебе стоит дать " + "ей шанс на новую жизнь" if data[2] == 'f' else "ему шанс на новую жизнь.")
        input("Нажмите Enter.")
        clear()
        devil.say("...Ты сейчас серьёзна?")
        input("Нажмите Enter.")
        clear()
        angel.say("Да, " + "ей ждут очень важные дела на земле." if data[2] == 'f' else "ему ждут очень важные дела на земле.")
        input("Нажмите Enter.")
        clear()
        devil.say("А почему сама не займёшся этим?")
        input("Нажмите Enter.")
        clear()
        angel.say("Мне не положено ничего делать, зато " + "ей можно" if data[2] == 'f' else "ему можно")
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
        header("Вам предстоит начать новую жизнь, ведь вы теперь не " + "та, кем были." if data[2] == 'f' else "тот, кем были.")
        input("Нажмите Enter.")

        return data

clear()

# Начало
mainMenu.mainMenuScreen()

player = start()


player = Player(player[0], player[2], player[1])

# Переход
goto("Plane", locs)
