import os
from termcolor import cprint, colored
from utilities import detectGender, header, splitText
# Игрок
class Player:
    def __init__(self, name, gender, race, inventory=[], money=0):
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

        self.money = money

        self.race = race

        self.inventory = inventory

    def stats(self):
        cprint(f"Уровень: {self.lvl}", self.textColor)
        cprint(f"Имя: {self.name}", self.textColor)
        cprint(f"Пол: {self.displayGender}", self.textColor)
        cprint(f"Расса: {self.race}", self.textColor)
        cprint(f"Здоровье: {self.health}")
        cprint(f"Деньги: {self.money}")

    def showInv(self):
        if len(self.inventory) > 0:
            header("Инвентарь")
            for i in self.inventory:
                if 'heal' in i:
                    print(f"{colored('|Имя', 'cyan')}: {colored(i['dispName'], 'green')}")
                    print(f"{colored('|Здоровие', 'cyan')}: {colored(i['heal'], 'green')}")
                    print(f"{colored('|Описание', 'cyan')}: {i['description']}")
                    print(f"{colored('|Количество', 'cyan')}: {colored(i['count'], 'green')}")
                    print(f"{colored('|Цена', 'cyan')}: {colored(i['price'], 'blue')}")
                    print(f"{colored('|__________________', 'cyan')}")
                elif 'use' in i:
                    print(f"{colored('|Имя', 'cyan')}: {colored(i['dispName'], 'yellow')}")
                    if i['use'] == None:
                        print(f"{colored('|Нельзя нигде использовать.', 'cyan')}")
                    else:
                        print(f"{colored('|Имя', 'cyan')}: {colored(i['use'], 'yellow')}")
                    print(f"{colored('|Описание', 'cyan')}: {i['description']}")
                    print(f"{colored('|Количество', 'cyan')}: {colored(i['count'], 'yellow')}")
                    print(f"{colored('|Цена', 'cyan')}: {colored(i['price'], 'blue')}")
                    print(f"{colored('|__________________', 'cyan')}")
                elif 'hunger' in i:
                    print(f"{colored('|Имя', 'cyan')}: {colored(i['dispName'], 'blue')}")
                    print(f"{colored('|Голод', 'cyan')}: {colored(i['hunger'], 'blue')}")
                    print(f"{colored('|Описание', 'cyan')}: {i['description']}")
                    print(f"{colored('|Количество', 'cyan')}: {colored(i['count'], 'blue')}")
                    print(f"{colored('|Цена', 'cyan')}: {colored(i['price'], 'blue')}")
                    print(f"{colored('|__________________', 'cyan')}")
            return 0
        else:
            self.say("У меня ничего нет...")
    
    def choose(self, data):
        self.say("Что же мне выбрать?")
        data[1]

    def say(self, text):
        text = splitText(text)
        cprint(f'{self.name}: {text}', self.textColor)

    def addToInv(self, item, count=None):
        if len(self.inventory) > 0:
            for i in self.inventory:
                if i['name'] == item['name']:
                    if count != None:
                        item['count'] = count
                    self.plusToInv(i, count)
                    header(f"К Вы получили {item['dispName']} ещё {item['count']} шт.")
                else:
                    if count != None:
                        item['count'] = count
                    header(f"К Вы получили {item['dispName']} ещё {item['count']} шт.")
            return self.inventory.append(item)
        else:
            return self.inventory.append(item)

    def plusToInv(self, item, count=None):
        for i in self.inventory:
            if i['name'] == item['name']:
                if count == None:
                    i['count'] += item['count']
                else:
                    i['count'] += count
                return i
        return self.addToInv(item, count)

    def clearInv(self):
        self.inventory = []
        header("Ваш инвентарь был очищен.")
        return self.inventory
    
    def minusFromInv(self, item, amount):
        for i in self.inventory:
            if i['name'] == item['name'] and i['count'] >= amount:
                i['count'] -= amount
                if i['count'] == 0:
                    self.inventory.remove(i)
                    header(f"У вас больше нет {item['dispName']}.")
                    return True
                else:
                    header(f"С вас отняли {item['dispName']} - {amount} шт.")
                    return True
            else:
                return False

    def takeDMG(self, amount):
        return self.health - amount

    def heal(self, amount):
        return self.health + amount
