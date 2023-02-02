from saveSystem import SaveSystem
from termcolor import cprint
from choices import Choices
from utilities import clear, pressEnter

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
            from main import warning
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
