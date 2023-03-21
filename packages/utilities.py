import os
from termcolor import cprint, colored

# html теги
hr = "\n_____________________________\n"
br = "\n"


# получаем и заменяем html теги
def getHtmlTags(text):
    text = splitText(text)
    text = text.replace('<br>', br)
    text = text.replace('<hr>', hr)

    return text

# Дебагер переменных
def debugVar(prntVar):
    print(prntVar)
    input()
    return prntVar

# Всякие детекторы
def detectGender(val):
    val = val.lower()
    female = ['f', 'ж', 'женщина']
    male = ["м", 'm', 'мужчина']

    if val in female:
        return 'f'
    elif val in male:
        return 'm'
    else:
        return False

def detectChoice(value="", msg=""):
    value = value.lower()
    yes = ['д', "да", 'y', 'yes']
    no = ['н', 'нет', 'n', 'no']

    if msg != "":
        import PySimpleGUI as sg

        layout = [
            [sg.Text(msg)],
            [sg.Button("Да"), sg.Button("Нет")],
        ]

        window = sg.Window('Выбор', layout)

        value, event = window.read()

        if isNone(value) == True:
            return detectChoice(msg=msg)

        value = value[0].lower()

        window.close()

    if value in yes:
        return 'yes'
    elif value in no:
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
    from os import system
    return system('cls' if os.name=='nt' else 'clear')


# Детекторы
def isNone(val, repeatable=True):
    if val == None:
        if repeatable == True:
            warning("Так не выйдет! Ну-ка ещё раз!")
            pressEnter()
        return True
    else:
        return False

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
    from time import sleep
    text = splitText(text)
    if anim == True:
        for i in text:
            sleep(0.025)
            cprint(i, 'red', end='', flush=True)
        print()
        sleep(0.15)
        return
    else:
        return cprint(text, 'red')
    
def header(text: str, anim: bool = True):
    from time import sleep
    text = splitText(text)
    if anim == True:
        for i in text:
            sleep(0.01)
            cprint(i, 'yellow', end='', flush=True)
        print()
        sleep(0.15)
        return
    else:
        return cprint(text, 'yellow')
    
def success(text: str, anim: bool = True):
    from time import sleep
    text = splitText(text)
    if anim == True:
        for i in text:
            sleep(0.025)
            cprint(i, 'green', end='', flush=True)
        sleep(0.15)
        return
    else:
        return cprint(text, 'green')


# Получение данных
def getName():
    import PySimpleGUI as sg
    print("Ждём ввода имени...")

    layout = [
        [sg.Text("(Не вводя имя, вы дадите имя персонажу то же что и системе)")],
        [sg.Text('Имя игрока'), sg.InputText()],
        [sg.Submit()]
    ]

    window = sg.Window('Имя', layout)

    event, values = window.read()
    
    window.close()

    value = values[0]

    if value == "" or event == None:
        value = os.getlogin()
    return value

def getGender():
    import PySimpleGUI as sg
    print("Ждём ввода пола...")

    layout = [
        [sg.Text("Выберите пол персонажа.")],
        [sg.Button("Мужчина"), sg.Button("Женщина")]
    ]

    window = sg.Window('Пол', layout)

    value, event = window.read()

    if isNone(event) == True:
        return getGender()
    
    window.close()

    return value

def getRace():
    # ToDo: Поменять на пресеты
    import PySimpleGUI as sg
    print("Ждём ввода рассы...")

    layout = [
        [sg.Text("(Расса не может быть пустой)")],
        [sg.Text("Введите вашу рассу: "), sg.InputText()],
        [sg.Submit()]
    ]

    window = sg.Window('Расса', layout)

    event, value = window.read()

    if isNone(event) == True:
        return getRace()

    window.close()

    return value[0]


# Идти в
def goto(locName="", locDisplayName="", locations = []):
    from time import sleep
    if locations == []:
        from main import locs
        locations = locs

    for i in locations:
        if locName != "" and i.name == locName:
            from main import player
            newLoc = i
            header("Ждите...")
            sleep(0.5)
            return newLoc.start(locations, player, '0', False, False)
        if locDisplayName != "" and i.displayName == locDisplayName:
            from main import player
            newLoc = i
            header("Ждите...")
            sleep(0.5)
            return newLoc.start(locations, player, '0', False, False)
