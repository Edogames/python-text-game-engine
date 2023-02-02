from termcolor import colored

# Текст выбора
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
