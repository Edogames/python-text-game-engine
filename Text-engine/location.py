from termcolor import colored, cprint
from utilities import clear, checkChoice, pressEnter
from choices import Choices
import random
from utilities import header, detectChoice, checkChoice
from saveSystem import SaveSystem

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
        from main import locs
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
            from utilities import goto
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