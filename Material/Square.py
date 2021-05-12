from Material.Player import Player, Color


class Square:
    columnnames = ["A", "B", "C", "D", "E", "F", "G", "H"]

    column = "A"
    row = 1
    color = None

    def __init__(self, c, r, color):
        self.row = r
        self.column = c
        self.color = color

    def print_color(self):
        if not self.color:
            return "."
        elif self.color is Color.White:
            return "W"
        else:
            return "B"

    def __str__(self):
        if self.color:
            return "Square: " + self.column + str(self.row) + "{" +str(self.color) + "}"
        else:
            return "Square: " + self.column + str(self.row)

    def __repr__(self):
        if self.color:
            return "Square: " + self.column + str(self.row) + "{"+str(self.color) + "}"
        else:
            return "Square: " + self.column + str(self.row)
