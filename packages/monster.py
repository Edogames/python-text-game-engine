from packages.utilities import warning, splitText
from termcolor import cprint

# Враг/монстр
class Monster:
    def __init__(self, race, gender, dmgPoint, maxHealth, place):
        self.race = race
        self.gender = gender
        self.place = place
        self.dmgPoint = dmgPoint
        self.maxHealth = maxHealth

        self.defeat = False
        self.health = 100

    def takeDMG(self, amount):
        self.health -= amount
        return self.checkHealth()

    def doDMG(self, target):
        warning(f"{self.race} атакует {target.name}!")
        target.health -= self.dmgPoint

    def death(self):
        self.defeat = True

    def checkHealth(self):
        if self.health < 0:
            self.health = 0
            return self.death()
        elif self.health > self.maxHealth:
            self.health = self.maxHealth
            return self.health

    def say(self, text):
        text = splitText(text)
        cprint(f"{self.race}: {text}", 'red')
