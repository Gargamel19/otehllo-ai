class Move:
    column = "A"
    row = 1

    changed_peaces = []

    color = None

    def __init__(self, column, row, changed_peaces, color):
        self.column = column
        self.row = row
        self.changed_peaces = changed_peaces
        self.color = color

    def __str__(self):
        return "Move: " + self.column + str(self.row) + " {color: " + self.color.name + ", captures: " + str(self.changed_peaces) + "}"

    def __repr__(self):
        return "Move: " + self.column + str(self.row) + " {color: " + self.color.name + ", captures: " + str(self.changed_peaces) + "}"

