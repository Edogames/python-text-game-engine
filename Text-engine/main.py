# Важные компоненты
from termcolor import colored, cprint
import time
import os
import random
from choices import Choices
from saveSystem import SaveSystem

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
            "Удалить прогресс",
            "Назад",
        ])

        print(choices.displayChoices())
        choice = str(input("Ваш выбор: "))

        if choice == '':
            return self.playBtn()
        elif choice == '4':
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
                pressEnter()
                return self.playBtn()
        elif choice == '3':
            result = self.saveSystem.deleteSaves()
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
def checkChoice(val):
    if val == '0' or val == '':
        return None
    else:
        return val

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

# Пустой инпут
def pressEnter():
    return input("Нажмите Enter что бы продолжить...")

class Store:
    def __init__(self, name, placeName, sellItems=[]):
        self.name = name
        self.placeName = placeName
        self.sellItems = sellItems

    def end(self):
        return goto(self.placeName)

    def showSellItems(self):
        for i in self.sellItems:
            if 'heal' in i:
                print(f"{colored('|Имя', 'cyan')}: {colored(i['dispName'], 'green')}")
                print(f"{colored('|Здоровие', 'cyan')}: {colored(i['heal'], 'green')}")
                print(f"{colored('|Описание', 'cyan')}: {i['description']}")
                print(f"{colored('|Цена', 'cyan')}: {colored(i['price'], 'blue')}")
                print(f"{colored('|__________________', 'cyan')}")
            elif 'use' in i:
                print(f"{colored('|Имя', 'cyan')}: {colored(i['dispName'], 'yellow')}")
                if i['use'] == None:
                    print(f"{colored('|Нельзя нигде использовать.', 'cyan')}")
                else:
                    print(f"{colored('|Имя', 'cyan')}: {colored(i['use'], 'yellow')}")
                print(f"{colored('|Описание', 'cyan')}: {i['description']}")
                print(f"{colored('|Цена', 'cyan')}: {colored(i['price'], 'blue')}")
                print(f"{colored('|__________________', 'cyan')}")
            elif 'hunger' in i:
                print(f"{colored('|Имя', 'cyan')}: {colored(i['dispName'], 'blue')}")
                print(f"{colored('|Голод', 'cyan')}: {colored(i['hunger'], 'blue')}")
                print(f"{colored('|Описание', 'cyan')}: {i['description']}")
                print(f"{colored('|Цена', 'cyan')}: {colored(i['price'], 'blue')}")
                print(f"{colored('|__________________', 'cyan')}")

    def getItem(self, itemName):
        for i in self.sellItems:
            if i['name'] == itemName:
                return i

    def buy(self, player, itemName):
        if player.money > 0:
            
            targetItem = self.getItem(itemName)
            
            header(f"Сколько вы хотите купить {targetItem['dispName']}?")
            amount = str(input())

            if checkChoice(amount) != None and amount.isnumeric() != False:
                amount = int(amount)

                moneyToPay = targetItem['price'] * amount

                if player.money < moneyToPay:
                    warning("Не достаточно денег")
                    return self.start(player)
                else:
                    player.addToInv(targetItem, amount)
                    player.money -= moneyToPay
                    header(f"Вы купили {targetItem['dispName']}!")
                    return self.start(player)

            else:
                warning(f"{amount} Не являеться цифрой!")
                pressEnter()
                return self.start(player)
        else:
            warning("У вас нет денег! Вы можете кое что продать тут.")
            pressEnter()
            return self.start(player)

    def sell(self, player, index):
        header(f"Сколько вы хотите продать? Макс: {player.inventory[index]['count']}")
        amount = str(input())
        if checkChoice(amount) != None and amount.isnumeric() != False:
            amount = int(amount)
            if player.inventory[index]['count'] >= amount:
                header(f"Вы продали {amount} шт {player.inventory[index]['dispName']}")
                money = player.inventory[index]['price'] * amount
                player.minusFromInv(player.inventory[index], amount)
                player.money += money
                pressEnter()
                return self.start(player)
            else:
                warning(f"У вас не достаточно {player.inventory[index]['name']} в инвентаре!")
                pressEnter()
                return self.start()
        else:
            warning(f"{amount} Не являеться цифрой!")
            pressEnter()
            return self.start()

    def start(self, player, error=False):
        saveSystem = SaveSystem([player], self.placeName)
        saveSystem.save()
        clear()
        selection = Choices([
            'Покупать',
            'Продать',
            'Выйти',
        ])
        if error == False:
            header(f"Вы вошли в магазин: {self.name}")
            pressEnter()
            header(f"Что вы хотите сделать?")
        else:
            header(f"Что вы хотите сделать?")
        
        print(selection.displayChoices())
        choice = str(input())
        if checkChoice(choice) == None:
            return self.start(player, True)
        else:
            if choice == '1':
                print("Что вы хотите купить?")
                self.showSellItems()
                choice = str(input())
                if checkChoice(choice) != None and choice.isnumeric() != False:
                    choice = int(choice) - 1
                    return self.buy(player, self.sellItems[choice]['name'])
                else:
                    return self.start(player, True)
            elif choice == '2':
                print("Что вы хотите продавать?")
                player.showInv()
                choice = str(input())
                if checkChoice(choice) != None and choice.isnumeric() != False:
                    return self.sell(player, int(choice)-1)
                else:
                    return self.start(player, True)
            else:
                header("Удачи в вашем приключении!")
                pressEnter()
                return goto(self.placeName)

# Локации
class Location:
    def __init__(self, name, displayName, monsterChance, lootChance, peopleChance, available = True, entities = [], description = "", availFrom = [], items = [], store=None):
        self.name = name
        self.items = items
        self.store = store
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

    def getItem(self, target):
        maxChance = self.lootChance * 10
        chance = random.randint(0, maxChance)
        if len(self.items) > 0 and chance > maxChance / 2:
            item = random.choice(self.items)
            header(f"Вы нашли: {item['dispName']}!")
            header(f"Хотите забрать?")
            choice = str(input())
            if(detectChoice(choice) == 'yes'):
                target.addToInv(item)
                pressEnter()
                return self.start(locs, target, '0', True, False)
            else:
                return self.start(locs, target, '0', False, True)
        else:
            header("Ничего не нашлось...")
            pressEnter()
            return self.start(locs, target, '0', False, True)

    def getLoc(self, num):
        initLocs = self.getLocs()
        return initLocs[num - 1].name

    def getPerson(self):
        maxChance = self.peopleChance * 10
        chance = random.randint(0, maxChance)

        if len(self.entities) == 0:
            header("Тут никаго.")
            pressEnter()
            return False

        person = random.choice(self.entities)
        person = random.choice(person)

        if chance > maxChance / 2:
            header("Начало встречи.")
            pressEnter()
            return person
        else:
            header("Пока нескем общаться.")
            pressEnter()
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
        if checkChoice(choice) == None:
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
                "Осмотрется",
                "Идти в магазин",
            ])

            print(selection.displayChoices())
            choice = str(input())
        if checkChoice(choice) == None:
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
            pressEnter()
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
                pressEnter()
                return self.start(locs, player, '3', True, False)
            elif choice == 0:
                return self.start(locs, player, '0', False, True)
        elif choice == '4':
            player.showInv()
            pressEnter()
            return self.start(locs, player, '0', True, False)
        elif choice == '5':
            person = self.getPerson()
            if person == False:
                return self.start(locs, player, '0', False, True)
            else:
                person.meet(player, self.name)
        elif choice == '6':
            return self.getItem(player)
        elif choice == '7':
            if self.store != None:
                return self.store.start(player)
            else:
                header("Здесь нет магазинов")
                pressEnter()
                return self.start(locs, player, '0', True, False)

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
            if detectChoice(answ) == 'yes':
                self.say(f"Чтож, хих, я {'рада.' if self.gender == 'f' else 'рад.'}")
                pressEnter()
                return self.smolTalk(player, placeName)
            elif detectChoice(answ) == 'no':
                self.say(f"Оу, мне жаль {player.name}")
                pressEnter()
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
                pressEnter()
                return self.smolTalk(player, placeName)
            elif choice == '2':
                clear()
                return self.smolTalk(player, placeName, '4')
            elif choice == '3':
                clear()
                self.say(f"Хорошо, {player.name}, потом, тогда поговорим.")
                pressEnter()
                header(f"{self.name} {'улыбнулась и ушла' if self.gender == 'f' else 'улыбнулся и ушёл'}.")
                pressEnter()
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
        
        if detectChoice(choice) == 'yes':
            self.checkRelationship(player, placeName)
            pressEnter()
            return goto(placeName, [])
        elif detectChoice(choice) == 'no':
            self.say('Ну, видимо у тебя много дел, чтож, не буду мешать.')
            pressEnter()
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

def start(checkRace = False, checkGender = False, err = False, data = [], dialogue = False, done = False):
    clear()

    if checkRace == False and checkGender == False and dialogue == False:
        header("Вы просыпаетесь в аду, и перед вами стоит дьяволица, раскошная женщина, и смотрит на вас не совсем довольная.")
        pressEnter()
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
        pressEnter()
        clear()
        angel.say("Постой!")
        pressEnter()
        clear()
        devil.say("Как ты тут оказалась? Ты же ангел.")
        pressEnter()
        clear()
        angel.say(f"Знаю, и я решила что тебе стоит дать {'ей' if data[2] == 'f' else 'ему'} шанс на новую жизнь.")
        pressEnter()
        clear()
        devil.say("...Ты сейчас серьёзна?")
        pressEnter()
        clear()
        angel.say(f"Да, {'ей' if data[2] == 'f' else 'ему'} ждут очень важные дела на земле.")
        pressEnter()
        clear()
        devil.say("А почему сама не займёшся этим?")
        pressEnter()
        clear()
        angel.say(f"Мне не положено ничего делать, зато {'ей можно' if data[2] == 'f' else 'ему можно'}")
        pressEnter()
        clear()
        devil.say(f"Эх...чтож, так и быть, тебе повезло, {data[0]}...")
        pressEnter()
        clear()
        devil.say(f"Ты не идёшь в ад, но учти, если не справишся, то твой путь тебе, думаю, понятен.")
        pressEnter()
        clear()

        print("Произашла вспышка, и вы потеряли сознание...")
        pressEnter()
        header("Вы проснулись через час после всего, что случилось в том мире.")
        pressEnter()
        header(f"Вам предстоит начать новую жизнь, ведь вы теперь {'не та' if data[2] == 'f' else 'не тот'}, кем были.")
        pressEnter()

        return data

if type(data) not in (tuple, list):
    clear()

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
