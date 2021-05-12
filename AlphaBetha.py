

import sys
import copy

from Material.Player import Color
from Material.Board import Board

class AlphaBetha:
    gew_tiefe = 0
    move = None

    aktuelle_tiefe = 0

    dot_counter = 0

    validate = 0
    matrix = None

    def __init__(self, gew_tiefe, validate=0, matrix=matrix):
        self.gew_tiefe = gew_tiefe
        self.validate = validate
        self.matrix = matrix

    def search_for_move(self, board, color):
        print("[ALPHABETHA GESTARTET FÜR " + color.name + "]: gewünschte Tiefe:", self.gew_tiefe, "BEWERTUNGSFUNKTION:",
              self.validate)
        bewertung = self.maxi(board, color, self.gew_tiefe, -(sys.maxsize-1), sys.maxsize)
        if not self.move:
            print("KEIN MOVE GEFUNDEN")
            return None, 0, self.dot_counter
        else:
            return self.move, bewertung, self.dot_counter

    def maxi(self, board, color, depth, alpha, beta):
        if self.aktuelle_tiefe < self.gew_tiefe-depth:
            self.aktuelle_tiefe = self.gew_tiefe-depth
        moves = Board.get_legal_moves(board, color)
        if depth == 0 or len(moves) == 0:
            self.dot_counter += 1
            if self.validate == 0:
                return Board.valuate(board, color)
            elif self.validate == 1:
                return Board.valuate_corner(board, color)
            elif self.validate == 2:
                return Board.valuate_diagonal(board, color)
            elif self.validate == 3:
                return Board.valuate_second_last(board, color)
            elif self.validate == 4:
                return Board.valuate_matrix(board, color, self.matrix)
        max_value = alpha
        for temp_move in moves:
            copy_board = copy.deepcopy(board)
            Board.make_move(copy_board, temp_move)
            if color == Color.Black:
                next_color = Color.White
            else:
                next_color = Color.Black
            wert = self.mini(copy_board, next_color, depth-1, max_value, beta)
            if wert > max_value:
                max_value = wert
                if depth == self.gew_tiefe:
                    self.move = [temp_move]
                if max_value >= beta:
                    break
            elif wert == max_value:
                if depth == self.gew_tiefe:
                    self.move.append(temp_move)
        return max_value

    def mini(self, board, color, depth, alpha, beta):
        if self.aktuelle_tiefe < self.gew_tiefe - depth:
            self.aktuelle_tiefe = self.gew_tiefe - depth
        moves = Board.get_legal_moves(board, color)
        if depth == 0 or len(moves) == 0:
            self.dot_counter += 1
            if self.validate == 0:
                return Board.valuate(board, color)
            elif self.validate == 1:
                return Board.valuate_corner(board, color)
            elif self.validate == 2:
                return Board.valuate_diagonal(board, color)
            elif self.validate == 3:
                return Board.valuate_second_last(board, color)
            elif self.validate == 4:
                return Board.valuate_matrix(board, color, self.matrix)

        min_value = beta
        for temp_move in moves:
            copy_board = copy.deepcopy(board)
            Board.make_move(copy_board, temp_move)
            if color == Color.Black:
                next_color = Color.White
            else:
                next_color = Color.Black
            wert = self.maxi(copy_board, next_color, depth-1, alpha, min_value)
            if wert < min_value:
                min_value = wert
                if min_value <= alpha:
                    break
        return min_value
