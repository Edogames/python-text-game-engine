from termcolor import colored
from packages.utilities import clear, checkChoice, pressEnter
from packages.choices import Choices

class Store:
    def __init__(self, name, placeName, sellItems=[]):
        self.name = name
        self.placeName = placeName
        self.sellItems = sellItems

    def end(self):
        from packages.utilities import goto
        return goto(locName=self.placeName)

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
            from packages.utilities import header, warning
            
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
        from packages.utilities import header, warning
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
        from packages.saveSystem import SaveSystem
        from packages.utilities import header
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
                from packages.utilities import goto
                header("Удачи в вашем приключении!")
                pressEnter()
                return goto(locName=self.placeName)
