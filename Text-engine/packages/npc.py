from termcolor import cprint
from packages.utilities import warning, header, splitText, clear, detectChoice, detectGender, pressEnter, goto
from packages.choices import Choices

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
