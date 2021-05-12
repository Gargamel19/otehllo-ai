from Material.Square import Square
from Material.Move import Move
from Material.Player import Player, Color

import random
import copy
import time


class Board(object):

    stellungen = 0

    collum_names = ["A", "B", "C", "D", "E", "F", "G", "H"]

    columns = []
    player_black = Color.Black
    player_white = Color.White

    turn = Color.Black

    def __init__(self, columns=[]):
        self.columns = columns
        if not columns:
            for i in range(8):
                row = []
                for j in range(8):
                    row.append(Square(self.collum_names[i], j+1, None))
                self.columns.append(row)

    @staticmethod
    def make_start_position(board):
        board.columns = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(Square(board.collum_names[i], j + 1, None))
            board.columns.append(row)
        converted_column, converted_row = Board.convert_indices("E", 4)
        board.columns[converted_column][converted_row].color = Color.White
        converted_column, converted_row = Board.convert_indices("D", 5)
        board.columns[converted_column][converted_row].color = Color.White
        converted_column, converted_row = Board.convert_indices("E", 5)
        board.columns[converted_column][converted_row].color = Color.Black
        converted_column, converted_row = Board.convert_indices("D", 4)
        board.columns[converted_column][converted_row].color = Color.Black

    @staticmethod
    def add_stone_of_color(board, column, row, color):
        changed_squares = []
        converted_column, converted_row = Board.convert_indices(column, row)
        if not board.columns[converted_column][converted_row].color:
            vectors = [1, 0, -1]
            for i in vectors:
                for j in vectors:
                    if i == 0 and j == 0:
                        ""
                    elif len(board.columns) > converted_column+i >= 0 and len(
                            board.columns[converted_column+i]) > converted_row+j >= 0:
                        if board.columns[converted_column+i][converted_row+j].color:
                            if board.columns[converted_column+i][converted_row+j].color is not color:
                                board.columns[converted_column][converted_row].color = color
                                temp_i = converted_column + i
                                temp_j = converted_row + j
                                squares_between = [board.columns[temp_i][temp_j]]
                                while len(board.columns) > temp_i + i >= 0 and len(
                                            board.columns[temp_i + i]) > temp_j + j >= 0:
                                    if board.columns[temp_i + i][temp_j + j].color:
                                        if board.columns[temp_i + i][temp_j + j].color is color:
                                            changed_squares += squares_between
                                            break
                                        else:
                                            squares_between.append(board.columns[temp_i + i][temp_j + j])

                                    else:
                                        break
                                    temp_i += i
                                    temp_j += j

            if not changed_squares == []:
                return Move(column=column, row=row, color=color, changed_peaces=changed_squares)
        else:
            print("ERROR: on", column + str(row), "is allready a peace from", board.columns[converted_column][converted_row].color)
        return None

    @staticmethod
    def remove_stone_add_coordinate(board, column, row):
        converted_column, converted_row = board.convert_indices(column, row)
        board.columns[converted_column][converted_row].color = None

    @staticmethod
    def convert_indices(column, row):
        return Board.collum_names.index(column), row - 1

    @staticmethod
    def to_move(column, row):
        return Board.collum_names[column], row + 1

    @staticmethod
    def is_move_in_move_list(column, row, move_list):
        for move in move_list:
            if move.column == column and move.row == row:
                return move
        return None

    @staticmethod
    def make_move_help(board, column, row, color):
        move = Board.is_move_in_move_list(column, row, Board.get_legal_moves(board, color))
        if move:
            converted_column, converted_row = Board.convert_indices(move.column, move.row)
            board.columns[converted_column][converted_row].color = color
            for square in move.changed_peaces:
                converted_square_column, converted_square_row = Board.convert_indices(square.column, square.row)
                board.columns[converted_square_column][converted_square_row].color = color

    @staticmethod
    def next_player(board):
        if board.turn == Color.White:
            board.turn = Color.Black
        else:
            board.turn = Color.White


    @staticmethod
    def make_move(board, move):
        Board.make_move_help(board, move.column, move.row, move.color)

    @staticmethod
    def make_engine_move_minmax(board, color=None, depth=2, validate=0, matrix=None):
        from Minmax import MinMax
        if not color:
            color = board.turn
        minimax = MinMax(depth, validate=validate, matrix=matrix)
        move_list, value, ammount = minimax.search_for_move(board, color)
        if move_list:
            print("moves mit der gleichen bewertung:", len(move_list))
            if len(move_list) > 0:
                rand = random.randint(0, len(move_list) - 1)
                print("zug", rand, "wurde ausgewählt")
                Board.make_move(board, move_list[rand])
                print(move_list[rand], value)
                return True, value, ammount
            return False, Board.valuate(board, color), ammount
        else:
            return False, Board.valuate(board, color), ammount

    @staticmethod
    def make_engine_move_alphabetha(board, color=None, depth=2, validate=0, matrix=None):

        from AlphaBetha import AlphaBetha
        if not color:
            color = board.turn
        alphabetha = AlphaBetha(depth, validate, matrix)
        move_list, value, ammount = alphabetha.search_for_move(board, color)
        if move_list:

            if len(move_list) > 0:
                rand = random.randint(0, len(move_list) - 1)
                print("von", len(move_list), "zuegen wurde zug", rand+1, "ausgewählt")
                Board.make_move(board, move_list[rand])
                print(move_list[rand])
                return True, value, ammount
            return False, Board.valuate(board, color), ammount
        else:
            return False, Board.valuate(board, color), ammount

    @staticmethod
    def make_random_move(board, color=None):
        if not color:
            color = board.turn
        movelist = board.get_legal_moves(board, color)

        if len(movelist) > 0:
            rand = random.randint(0, len(movelist) - 1)
            board.make_move(board, movelist[rand])
            print(movelist[rand])
            return True
        else:
            print("no move found")
            return False

    @staticmethod
    def make_best_move(board, color=None):
        if not color:
            color = board.turn
        movelist = board.get_legal_moves(board, color)
        lenth = 0
        temp_move_list = []
        for move in movelist:
            if len(move.changed_peaces) > lenth:
                temp_move_list = [move]
                lenth = len(move.changed_peaces)
            elif len(move.changed_peaces) == lenth:
                temp_move_list.append(move)
        if len(temp_move_list) == 0:
            print("no move found")
            return False
        else:
            rand = random.randint(0, len(temp_move_list) - 1)
            Board.make_move(board, temp_move_list[rand])
            print(temp_move_list[rand])
            return True

    @staticmethod
    def get_legal_moves(board, color):
        move_list = []
        for i in range(8):
            for j in range(8):
                copy_board = copy.deepcopy(board)
                if copy_board.columns[i][j].color is None:
                    move = Board.add_stone_of_color(copy_board, Board.collum_names[i], j + 1, color)
                    if move:
                        move_list.append(move)
                        Board.remove_stone_add_coordinate(copy_board, Board.collum_names[i], j + 1)
                        converted_column, converted_row = Board.convert_indices(move.column, move.row)
                        copy_board.columns[converted_column][converted_row].color = color
                        for square in move.changed_peaces:
                            square.color = color
        return move_list

    @staticmethod
    def valuate(board, color):
        #print("[VALIDATE for " + color.name + "]", board)
        score = 0
        for row in board.columns:
            for square in row:
                if square.color:
                    if square.color == color:
                        score += 1
                    else:
                        score -= 1
        return score


    @staticmethod
    def valuate_corner(board, color):
        #print("[VALIDATE for " + color.name + "]", board)
        score = 0
        for i in range(len(board.columns)):
            for j in range(len(board.columns[i])):
                if board.columns[i][j].color:
                    if board.columns[i][j].color == color:
                        min_i = 5-min(8 - i, i+1)
                        min_j = 5-min(8 - j, j+1)
                        score += (min_j+min_i)
                    else:
                        min_i = 5-min(8 - i, i+1)
                        min_j = 5-min(8 - j, j+1)
                        score -= (min_j+min_i)
        return score

    @staticmethod
    def valuate_diagonal(board, color):
        # print("[VALIDATE for " + color.name + "]", board)
        score = 0
        for i in range(len(board.columns)):
            for j in range(len(board.columns[i])):
                if board.columns[i][j].color:
                    if board.columns[i][j].color == color:
                        min_i = 5 - min(8 - i, i + 1)
                        min_j = 5 - min(8 - j, j + 1)
                        zuschlag = 0
                        if i-j==0 or i+j==7:
                            zuschlag = 2
                        score += (min_j + min_i + zuschlag)
                    else:
                        min_i = 5 - min(8 - i, i + 1)
                        min_j = 5 - min(8 - j, j + 1)
                        zuschlag = 0
                        if i-j == 0 or i+j == 7:
                            zuschlag = 2
                        score -= (min_j + min_i + zuschlag)
        return score

    @staticmethod
    def valuate_second_last(board, color):
        # print("[VALIDATE for " + color.name + "]", board)
        score = 0
        for i in range(len(board.columns)):
            for j in range(len(board.columns[i])):
                if board.columns[i][j].color:
                    if board.columns[i][j].color == color:
                        min_i = 5 - min(8 - i, i + 1)
                        min_j = 5 - min(8 - j, j + 1)
                        if min_j == 4:
                            min_j = 6
                        if min_i == 4:
                            min_i = 6
                        zuschlag = 0
                        if i - j == 0 or i + j == 7:
                            zuschlag = 2
                        score += (min_j + min_i + zuschlag)
                    else:
                        min_i = 5 - min(8 - i, i + 1)
                        min_j = 5 - min(8 - j, j + 1)
                        if min_j == 4:
                            min_j = 6
                        if min_i == 4:
                            min_i = 6
                        zuschlag = 0
                        if i - j == 0 or i + j == 7:
                            zuschlag = 2
                        score -= (min_j + min_i + zuschlag)
        return score

    @staticmethod
    def valuate_matrix(board, color, matrix):
        score = 0
        for i in range(len(board.columns)):
            for j in range(len(board.columns[i])):
                if board.columns[i][j].color:
                    if board.columns[i][j].color == color:
                        score += matrix[i][j]
                    else:
                        score -= matrix[i][j]
        return score

    @staticmethod
    def end_game(board):
        white = 0
        black = 0
        winner = None
        for row in board.columns:
            for square in row:
                if square.color:
                    if square.color == Color.White:
                        white = white + 1
                    elif square.color == Color.Black:
                        black = black + 1
        if white>black:
            print("WHITE WINS:")
            winner = "W"
        elif white==black:
            print("DRAW")
            winner = "D"
        elif white<black:
            print("BLACK WINS:")
            winner = "B"

        #print("W:", white, "| B:", black)
        return {"winner": winner, "score": {"white": white, "black": black}}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        outset = []
        for i in range(len(self.columns[0])):
            outset.append(str(len(self.columns[0])-i) + " | ")
        for i in range(len(self.columns)):
            for j in range(len(self.columns[i])):
                outset[8-j-1] += self.columns[i][j].print_color() + " "
        outset.append("--|----------------")
        legend_down = "  | "
        for i in range(len(self.columns)):
            legend_down += self.columns[i][0].column + " "
        outset.append(legend_down)

        out_string = ""
        for row in outset:
            out_string = out_string + row + "\n"

        return out_string