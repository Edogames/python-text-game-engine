# Важные компоненты
from termcolor import colored, cprint
import time
import os
import random
import pygame
pygame.init()
pygame.mixer.init()

# Типы уведомлений
def warning(text):
    return print(f"{colored(text, 'red')}")
def header(text):
    return print(f"{colored(text, 'yellow')}")
def success(text):
    return print(colored(f'Успех! {text}!', "green"))

# Очистка консоли
def clear():
    return os.system('cls' if os.name=='nt' else 'clear')

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
    def __init__(self, cheats = False):
        self.cheats = cheats

    def mainMenuScreen(self):
        print(f"{colored('1 -', 'cyan')} Играть, {colored('2 -')} Настройки")

        choice = int(input("Ваш выбор: "))

        if choice == 1:
            return start()
        else:
            return getattr(self, 'options')

    def options(self):
        if self.cheats == False:
            cprint("Читы отключены.", "cyan")
        else:
            cprint("Читы включены.", "cyan")

        input("Нажмите Enter что бы вернуться...")
        return self.mainMenuScreen()

# Локации
class Location:
    def __init__(self, name, displayName, monsterChance, lootChance, available = True, description = ""):
        self.name = name
        self.displayName = displayName
        self.monsterChance = monsterChance
        self.lootChance = lootChance
        self.description = description

        self.available = available
        self.tpSound = pygame.mixer.Sound('Sounds/Player/Teleport.wav')

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

    def goto(self, name, locations):
        header("Ждите...")
        time.sleep(0.5)
        return goto(name, locations)

    def getLocs(self, locations):
        availableLocs = []

        for i in locations:
            if i.name != self.name:
                availableLocs.append(i)
        
        return availableLocs

    def getLoc(self, num):
        initLocs = self.getLocs()
        return initLocs[num - 1].name


    def showMap(self, locations):
        text = ""
        num = 0

        for i in locations:
            num += 1
            text += f"{num} - {i.displayName}"
    
    def start(self, locs, player, choice = 0):
        clear()
        if choice == 0:
            header(f"Вы находитесь в {self.displayName}")

            self.tpSound.play()

            selection = Choices([
                "Идти",
                "О местности",
            ])

            print(selection.displayChoices())
            choice = int(input())
        if choice == "" or choice == 0:
            return self.start(locs, player)
        elif choice == 1:
            clear()
            player.say("Куда же мне идти?")
            text = ""
            number = 0
            availLocs = []
            for i in locs:
                if i.name != self.name and i.available == True:
                    number += 1
                    availLocs.append(i)
                    text += f"{colored(f'{number} -', 'cyan')} {i.displayName} "

            print(text, f"{colored(0, 'cyan')} - Отмена")
            num = input()
            
            if num == '0':
                return self.start(locs, player)
            elif num == "":
                return self.start(locs, player, 1)
            newLoc = availLocs[int(num) - 1].name
            return goto(newLoc, locs)
        elif choice == 2:
            clear()
            self.stats()
            return self.start(locs)

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

        self.useSound = pygame.mixer.sound('Sounds/Player/Heal.wav')
        self.statsSound = pygame.mixer.sound('Sounds/Menus/Confirm.wav')

    def use(self, target):
        self.useSound.play()
        return target.health + self.heal

    def stats(self):
        self.statsSound.play()
        print(f"{colored('|Имя', 'cyan')}: {self.dispName}")
        print(f"{colored('|Описание', 'cyan')}: {self.description}")
        print(f"{colored('|Количество', 'cyan')}: {self.count}")
        return print(f"{colored('|__________________', 'cyan')}")

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

        self.race = race

        self.inventory = []

        self.confirmSound = pygame.mixer.sound('Sounds/Menus/Confirm.wav')

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
    
    def choose(self, data):
        self.say("Что же мне выбрать?")
        data[1]

    def say(self, text):
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
    def __init__(self, name, race, gender, type, gay, married = [False, ""]):
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

    def addRelationship(self, target, relType):
        self.relationList.append([target.name, target.gender, relType])

    def stats(self, player):
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

    def say(self, text):
        cprint(f'{self.name}: {text}', self.textColor)

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

        self.hitSound = pygame.mixer.Sound('Sounds/Player/Hit.wav')

    def takeDMG(self, amount):
        self.health -= amount
        return self.checkHealth()

    def doDMG(self, target):
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

    def say(self, text):
        cprint(f"{self.race}: {text}", 'red')

# Начало
def start():
    clear()

    name = input("Введите ваше имя: ")
    race = input("Введите ваш рассу: ")
    gender = input("Выберите ваш пол[ж/м]: ")

    player = Player(name, gender, race)
    return player


locs = [
    Location("Plane", "Равнина", 20, 10, True, "Просто равнина."),
    Location("NotAPlane", "Не равнина", 20, 10, True, "Это не равнина."),
    Location("NotAPlane2", "Не равнина2", 20, 10, True, "Это не равнина."),
]

clear()
player = start()

def goto(locName, locations = []):
    if locations == []:
        locations = locs

    for i in locations:
        if i.name == locName:
            newLoc = i
            return newLoc.start(locations, player)

goto("Plane", locs)
