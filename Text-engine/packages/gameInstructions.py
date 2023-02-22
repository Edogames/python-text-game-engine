from termcolor import cprint, colored
from packages.utilities import pressEnter, clear, getHtmlTags

class BasicInstructions:
    def Gameplay():
        clear()
        instr = getHtmlTags(colored(open('instructions/instructions.txt', 'r').read(), 'yellow'))

        print(instr)
        
        pressEnter()
        pass

class InformationBoard:
    def __init__(self, targetName: str, genders: list, description: str, maxHealPoint: int):
        self.targetName = targetName
        self.genders = genders
        self.description = description
        self.maxHealPoint = maxHealPoint

    def showDescription(self):
        print(f"Информация об: {self.targetName}")
        print()
        if len(self.genders) > 1:
            genderlist = ""
            for i in range(self.genders):
                genderlist += f"{self.genders[i]}, " if i != len(self.genders) else f"и так же {self.genders[i]}"
            cprint(f"Бывают {genderlist}")
            pressEnter()
            return 0
