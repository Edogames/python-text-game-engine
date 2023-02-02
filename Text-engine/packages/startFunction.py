def start(checkRace = False, checkGender = False, err = False, data = [], dialogue = False, done = False):
    from packages.utilities import clear, header, pressEnter, warning, detectGender, getName, getRace
    from main import devil, angel

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
