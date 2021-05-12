from enum import Enum


class Color(Enum):
    Black = "B"
    White = "W"

    def __str__(self):
        return "Color: " + self.name
    def __repr__(self):
        return "Color: " + self.name


class Player:

    isAi = False
    name = ""
    color = Color.White

    def __init__(self, isAi, name, color):
        self.isAi = isAi
        self.name = name
        self.color = color