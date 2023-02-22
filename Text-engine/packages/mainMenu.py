from termcolor import cprint
from packages.saveSystem import SaveSystem
from packages.choices import Choices
from packages.utilities import clear, pressEnter
from packages.gameInstructions import InformationBoard, BasicInstructions

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
            from packages.utilities import warning
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
                "Инструкции",
            ]
        )

        print(choices.displayChoices())

        choice = str(input("Ваш выбор: "))

        if choice == '':
            # Возвращаемся в главное меню
            return self.mainMenuScreen()
        elif choice == '1':
            # Вот тут кнопка начало игры
            return self.playBtn()
        elif choice == '2':
            # Вот тут меню настроек
            return self.options()
        elif choice == '3':
            # Вот тут инструкция показываеться
            BasicInstructions.Gameplay()
            return self.mainMenuScreen()

