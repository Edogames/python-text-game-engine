import os
import time
from termcolor import cprint

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

# Очистка консоли
def clear():
    return os.system('cls' if os.name=='nt' else 'clear')

# Пустой инпут
def pressEnter():
    return input("Нажмите Enter что бы продолжить...")

# Разделитель текста по лимиту
def splitText(text: str):
    from main import mainMenu
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
        from main import locs
        locations = locs

    for i in locations:
        if i.name == locName:
            from main import player
            newLoc = i
            header("Ждите...")
            time.sleep(0.5)
            return newLoc.start(locations, player, '0', False, False)
