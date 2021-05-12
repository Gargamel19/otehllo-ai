import time
import random
import copy

from Material.Board import Board
from Material.Move import Move
from Material.Player import Player, Color

best_matrixes = []
start_matrix = [
    [14, 11, 10, 9, 9, 10, 11, 14],
    [11, 8, 5, 4, 4, 5, 8, 11],
    [10, 5, 6, 3, 3, 6, 5, 10],
    [9, 4, 3, 4, 4, 3, 4, 9],
    [9, 4, 3, 4, 4, 3, 4, 9],
    [10, 5, 6, 3, 3, 6, 5, 10],
    [11, 8, 5, 4, 4, 5, 8, 11],
    [14, 11, 10, 9, 9, 10, 11, 14]
]



def simulate_game(game, matrix, tiefe_g, tiefe_s):
    stellungen_generic = 0
    stellungen_static = 0
    board = Board()
    Board.make_start_position(board)
    time_generic = 0
    time_static = 0

    move_nr = 0


    is_okay = True
    while is_okay:
        print("Game:", game+1, "Move:", move_nr+1)
        if board.turn == Color.White:
            start = time.time()
            print(board.turn.name.upper(), "IS MOVING:")
            if game % 2 == 0:
                print("GENERIC")
                is_okay, score, ammount = Board.make_engine_move_alphabetha(board, depth=tiefe_g, validate=4, matrix=matrix)
                stellungen_generic += ammount
                print(board)
                print(board.turn.name.upper(), "Engine:", score)
                Board.next_player(board)
                end = time.time()
                time_generic += end - start
            else:
                print("STATIC")
                is_okay, score, ammount = Board.make_engine_move_alphabetha(board, depth=tiefe_s, validate=3, matrix=matrix)
                stellungen_static += ammount
                print(board)
                print(board.turn.name.upper(), "Engine:", score)
                Board.next_player(board)
                end = time.time()
                time_static += end - start
            print("Time:", str(end - start))

        else:
            start = time.time()
            print(board.turn.name.upper(), "IS MOVING:")
            if game % 2 == 1:
                print("GENERIC")
                is_okay, score, ammount = Board.make_engine_move_minmax(board, depth=tiefe_g, validate=4, matrix=matrix)
                stellungen_generic += ammount
                print(board)
                print(board.turn.name.upper(), "Engine:", score)
                Board.next_player(board)
                end = time.time()
                time_generic += end - start
            else:
                print("STATIC")
                is_okay, score, ammount = Board.make_engine_move_minmax(board, depth=tiefe_s, validate=3)
                stellungen_static += ammount
                print(board)
                print(board.turn.name.upper(), "Engine:", score)
                Board.next_player(board)
                end = time.time()
                time_static += end-start
            print("Time:", str(end-start))
        move_nr += 1
        #print(board)
    print("GENERIC:", stellungen_generic, "Stellungen Analysiert")
    print("STATIC:", stellungen_static, "Stellungen Analysiert")
    print("Time:", "GENERIC:", time_generic, "STATIC:", time_static)
    if stellungen_generic != 0 and stellungen_static != 0:
        print("Time/Stellung:", "GENERIC:", time_generic/stellungen_generic, "STATIC:", time_static/stellungen_static)

    # {"winner": winner, "score": {"generic": generic, "static": static}}
    results = Board.end_game(board)
    if game % 2 == 1:
        if results["winner"] == "W":
            new_results = {"winner": "G", "score": {"G": results["score"]["white"], "S": results["score"]["black"]}}
        else:
            new_results = {"winner": "S", "score": {"G": results["score"]["white"], "S": results["score"]["black"]}}
    else:
        if results["winner"] == "B":
            new_results = {"winner": "G", "score": {"G": results["score"]["black"], "S": results["score"]["white"]}}
        else:
            new_results = {"winner": "S", "score": {"G": results["score"]["black"], "S": results["score"]["white"]}}
    return new_results, stellungen_generic, stellungen_static, time_generic, time_static

def play(matrix, ammound=100):
    print("play", ammound, "games")
    print("lets go :)")
    stellungen_generic_gesammt = 0
    stellungen_static_gesammt = 0
    if ammound > 0:
        static = 0.0
        generic = 0.0
        draw = 0.0
        for i in range(ammound):
            print("------------------ RUN:", str(i+1), "------------------")
            result, stellungen_generic, stellungen_static, stellungen_generic, stellungen_static = simulate_game(i, matrix, 2, 2)
            stellungen_generic_gesammt += stellungen_generic
            stellungen_static_gesammt += stellungen_static
            stellungen_static_gesammt += stellungen_static
            stellungen_generic_gesammt += stellungen_generic

            if result["winner"] == "G":
                static += 1.0
            elif result["winner"] == "S":
                generic += 1.0
            elif result["winner"] == "D":
                draw += 1.0
            print("G:", generic, "S:", static, "D", draw)
        print("G:", generic, "S:", static, "D", draw)
        print()
        generic_rate = generic/ammound
        print("Generic Rate:", generic_rate)

        static_rate = static/ammound
        print("Static Rate:", static_rate)

        draw_rate = draw/ammound
        print("DRAW  Rate:", draw_rate)
        print()
        print("es wurden", ammound, "Spiele Gespielt")
        print("G hat insgesammt", stellungen_generic_gesammt, "Stellungen Analysiert")
        print("G hat im schnitt", stellungen_generic_gesammt/stellungen_generic_gesammt, "Sekunden für eine Stellung gebraucht")
        print("G hat im schnitt wurden pro Spiel", float(stellungen_generic_gesammt)/ammound, "Stellungen Analysiert")
        print("S hat insgesammt", stellungen_static_gesammt, "Stellungen Analysiert")
        print("S hat im schnitt", stellungen_static_gesammt/stellungen_static_gesammt, "Sekunden für eine Stellung gebraucht")
        print("S hat im schnitt wurden pro Spiel", float(stellungen_static_gesammt)/ammound, "Stellungen Analysiert")
        print()
        print("Stellungen_gesammt:", "G:", stellungen_generic_gesammt, "S:", stellungen_static_gesammt, "("+ str(stellungen_generic_gesammt+stellungen_static_gesammt)+")")
        print("Time_gesammt:", "G:", stellungen_generic_gesammt, "S:", stellungen_static_gesammt, "("+ str(stellungen_generic_gesammt+stellungen_static_gesammt)+")")
        return generic_rate


def inset_in_best_matrix(temp_list, value, matrix):
    if len(temp_list) == 0:
        temp_list = []
        temp_dir = {"value": value, "matrix": matrix}
        temp_list.append(temp_dir)
    else:
        for i in range(len(temp_list)):
            if temp_list[i]["value"] < value:
                temp_dict = {"value": value, "matrix": matrix}
                temp_list.insert(i-1, temp_dict)
        if len(temp_list) > 20:
            temp_list.remove(len(temp_list)-1)
    return temp_list

def make_random_matrix():
    matrix = []
    for i in range(8):
        row = []
        for j in range(8):
            rand = random.randint(-20, 20)
            row.append(rand)
        matrix.append(row)
    return matrix

def crossover(better_matrix, other_matrix):
    new_matrix = copy.deepcopy(better_matrix)
    for i in range(8):
        for j in range(8):
            rand = random.randint(0, 4)
            if rand == 0:
                new_matrix[i][j] = other_matrix[i][j]
    return new_matrix

def mutate(matrix, ratio):
    for i in range(8):
        for j in range(8):
            rand = random.randint(0, ratio)
            if rand == 0:
                rand_plus = random.randint(-5, 5)
                matrix[i][j] += rand_plus
    return matrix

def print_matrix(matrix):
    strinf_mat = ""
    for row in matrix:
        string = ""
        for value in row:
            string += str(value) + " "
        strinf_mat += string + "\n"
    return strinf_mat

def write_best_moves_to_file():
    with open("ergs.txt", "w+") as file:
        string = ""
        for matrix in best_matrixes:
            print(matrix)
            string += (str(matrix["value"]) + "\n" + print_matrix(matrix["matrix"]))
        file.write(string)
    print("------------------ WROTE IN FILE ------------------")


games_in_generation = 50

generic_rate = play(start_matrix, ammound=games_in_generation)
best_matrixes = inset_in_best_matrix(best_matrixes, generic_rate, start_matrix)
write_best_moves_to_file()

generations = 100

for generation in range(generations):
    print("-- GEN", generation, "--")
    if len(best_matrixes) < 5:
        new_mat = make_random_matrix()
        morphed_matrix = crossover(best_matrixes[0]["matrix"], new_mat)
        mutated_matrix = mutate(morphed_matrix, 32)

        generic_rate = play(mutated_matrix, ammound=games_in_generation)
        best_matrixes = inset_in_best_matrix(best_matrixes, generic_rate, mutated_matrix)
        write_best_moves_to_file()
    else:
        morphed_matrix = crossover(best_matrixes[0]["matrix"], best_matrixes[1]["matrix"])
        mutated_matrix = mutate(morphed_matrix, 32)

        generic_rate = play(mutated_matrix, ammound=games_in_generation)
        best_matrixes = inset_in_best_matrix(best_matrixes, generic_rate, mutated_matrix)
        write_best_moves_to_file()




