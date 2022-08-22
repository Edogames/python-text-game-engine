from termcolor import colored
import os
import random

def warning(text):
    return print(f"{colored(text, 'red')}")
def header(text):
    return print(f"{colored(text, 'yellow')}")
def success(text):
    return print(colored(f'Успех! {text}!', "green"))

def clear():
    return os.system('cls' if os.name=='nt' else 'clear')

class Location:
    def __init__(self, name, displayName, monsterChance, lootChance, description):
        self.name = name
        self.displayName = displayName
        self.monsterChance = monsterChance
        self.lootChance = lootChance
        self.description = description

    def stats(self):
        print(f"Имя местности: {self.displayName}")
        print(f"Описание местности: {self.displayName}")
        if self.monsterChance >= 5:
            monColor = "red"
        else:
            monColor = "green"
        
        if self.lootChance >= 5:
            lootColor = "green"
        else:
            lootColor = "red"
        print(colored(f"Шанс нападение монстров: {self.monsterChance}", monColor))
        print(colored(f"Шанс выпадение предметов: {self.monsterChance}", lootColor))

class Item:
    def __init__(self, name, count, use, description = ""):
        self.name = name
        self.count = count
        self.use = use
        self.description = description

    def stats(self):
        print(f"{colored('|Имя', 'cyan')} -> {colored(self.name, 'cyan')}")
        print(f"{colored('|Количество', 'cyan')} -> {colored(self.count, 'cyan')}")


class Player:
    def __init__(self, name, gender, race):
        if name == "":
            self.name = os.getlogin()
        else:
            self.name = name
        
        if gender == "female" or gender == "Female" or gender == 'f' or gender == 'F':
            self.textColor = "red"
            self.gender = "f"
            self.displayGender = "Женский"
        elif gender == "male" or gender == "Male" or gender == 'm' or gender == 'M':
            self.textColor = "green"
            self.gender = "m"
            self.displayGender = "Мужской"
        
        self.strength = 10
        self.lvl = 1
        self.health = 100
        self.stamina = 100

        self.race = race

        self.inventory = []


    def stats(self):
        print(colored(f"Уровень: {self.lvl}", self.textColor))
        print(colored(f"Имя: {self.name}", self.textColor))
        print(colored(f"Пол: {self.displayGender}", self.textColor))
        print(colored(f"Расса: {self.race}", self.textColor))
        print(f"Здоровье: {self.health}")

    def showInv(self):
        if len(self.inventory) > 0:
            header("Инвентарь")
            for i in self.inventory:
                i.stats()
                print(f"{colored('|__________________', 'cyan')}")
        else:
            self.say("У меня ничего нет...")

    def say(self, text):
        print(colored(f'{self.name}: {text}', self.textColor))

    def addToInv(self, item):
        header(f"К вам добавилось {item.name} {item.count} шт.")
        return self.inventory.append(item)

    def plusToInv(self, item):
        header(f"Вы получили {item.name} {item.count} шт.")
        for i in self.inventory:
            if i.name == item.name:
                i.count += item.count
                return i
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

class NPC:
    def __init__(self, name, race, gender, type):
        self.name = name
        self.race = race
        self.gender = gender
        self.type = type
        self.lvl = 1
        self.health = 100
        self.stamina = 100

        self.inventory = []

        if self.gender == "f":
            self.textColor = "red"
            self.displayGender = "Женский"
        else:
            self.textColor = "green"
            self.displayGender = "Мужской"

    def stats(self):
        if self.health > 0:
            print(colored(f"Уровень: {self.lvl}", self.textColor))
            print(colored(f"Имя: {self.name}", self.textColor))
            print(colored(f"Пол: {self.displayGender}", self.textColor))
            print(colored(f"Расса: {self.race}", self.textColor))
            print(colored(f"Класс: {self.type}", self.textColor))
            print(f"Здоровье: {self.health}")
        else:
            if self.gender == "m":
                warning(f"{self.name} Мёртв.")
            else:
                warning(f"{self.name} Мертва.")
        
    def say(self, text):
        print(colored(f'{self.name}: {text}', self.textColor))

    def showInv(self):
        if len(self.inventory) > 0:
            header("Инвентарь")
            for i in self.inventory:
                i.stats()
                print(f"{colored('|__________________', 'cyan')}")
        else:
            self.say("У меня ничего нет...")

    def addToInv(self, item, alert = True):
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


femPlayer = Player("", "f", "человек")
malePlayer = Player("", "m", "пони")
femNPC = NPC("Джулия", "робот", 'f', 'житель')
testItem = Item("Knive", 1, "None")

clear()
femPlayer.stats()
femPlayer.showInv()
input()
clear()
femPlayer.addToInv(testItem)
femPlayer.showInv()
input()
clear()
for _ in range(10):
    femPlayer.addToInv(testItem)
femPlayer.showInv()
input()
femPlayer.clearInv()
input()
clear()
malePlayer.stats()
malePlayer.showInv()
input()
clear()
malePlayer.addToInv(testItem)
malePlayer.showInv()
input()
clear()
for _ in range(10):
    malePlayer.addToInv(testItem)
malePlayer.showInv()
input()
malePlayer.clearInv()
input()
clear()

femNPC.stats()
input()
femNPC.showInv()
input()
femNPC.addToInv(testItem)
femNPC.showInv()
input()
femNPC.plusToInv(testItem)
femNPC.plusToInv(testItem, False)
femNPC.showInv()

input()
clear()
success("Debug done")
input()
clear()
