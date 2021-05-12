import time

from Material.Board import Board
from Material.Move import Move
from Material.Player import Player, Color



def simulate_game(game):
    stellungen_white = 0
    stellungen_black = 0
    board = Board()
    Board.make_start_position(board)
    time_white = 0
    time_black = 0

    move_nr = 0

    is_okay = True
    while is_okay:
        print("Game:", game+1, "Move:", move_nr+1)
        if board.turn == Color.White:
            start = time.time()
            print(board.turn.name.upper(), "IS MOVING:")
            is_okay, score, ammount = Board.make_engine_move_alphabetha(board, depth=4, validate=3)
            stellungen_white += ammount
            print(board)
            print(board.turn.name.upper(), "Engine:", score)
            Board.next_player(board)
            end = time.time()
            time_white += end-start
            print("Time:", str(end-start))

        else:
            start = time.time()
            print(board.turn.name.upper(), "IS MOVING:")
            is_okay, score, ammount = Board.make_engine_move_alphabetha(board, depth=4, validate=3)
            stellungen_black += ammount
            print(board)
            print(board.turn.name.upper(), "Engine:", score)
            Board.next_player(board)
            end = time.time()
            time_black += end-start
            print("Time:", str(end-start))
        move_nr += 1
        #print(board)
    print("W:", stellungen_white, "Stellungen Analysiert")
    print("B:", stellungen_black, "Stellungen Analysiert")
    print("Time:", "W:", time_white, "B:", time_black)
    if stellungen_white != 0 and stellungen_black != 0:
        print("Time/Stellung:", "W:", time_white/stellungen_white, "B:", time_black/stellungen_black)

    return Board.end_game(board), stellungen_white, stellungen_black, time_white, time_black

def play(ammound=100):
    print("play", ammound, "games")
    print("lets go :)")
    stellungen_white_gesammt = 0
    stellungen_black_gesammt = 0
    time_white_gesammt = 0
    time_black_gesammt = 0
    if ammound > 0:
        black = 0.0
        white = 0.0
        draw = 0.0
        for i in range(ammound):
            print("------------------ RUN:", str(i+1), "------------------")
            result, stellungen_white, stellungen_black, time_white, time_black = simulate_game(i)
            stellungen_white_gesammt += stellungen_white
            stellungen_black_gesammt += stellungen_black
            time_black_gesammt += time_black
            time_white_gesammt += time_white

            if result["winner"] == "B":
                black += 1.0
            elif result["winner"] == "W":
                white += 1.0
            elif result["winner"] == "D":
                draw += 1.0
            print("W:", white, "B:", black, "D", draw)
        print("W:", white, "B:", black, "D", draw)
        print()
        white_rate = white/ammound
        print("White Rate:", white_rate)

        black_rate = black/ammound
        print("Black Rate:", black_rate)

        draw_rate = draw/ammound
        print("DRAW  Rate:", draw_rate)
        print()
        print("es wurden", ammound, "Spiele Gespielt")
        print("W hat insgesammt", stellungen_white_gesammt, "Stellungen Analysiert")
        print("W hat im schnitt", time_white_gesammt/stellungen_white_gesammt, "Sekunden für eine Stellung gebraucht")
        print("W hat im schnitt wurden pro Spiel", float(stellungen_white_gesammt)/ammound, "Stellungen Analysiert")
        print("B hat insgesammt", stellungen_black_gesammt, "Stellungen Analysiert")
        print("B hat im schnitt", time_black_gesammt/stellungen_black_gesammt, "Sekunden für eine Stellung gebraucht")
        print("B hat im schnitt wurden pro Spiel", float(stellungen_black_gesammt)/ammound, "Stellungen Analysiert")
        print()
        print("Stellungen_gesammt:", "W:", stellungen_white_gesammt, "B:", stellungen_black_gesammt, "("+ str(stellungen_white_gesammt+stellungen_black_gesammt)+")")
        print("Time_gesammt:", "W:", time_white_gesammt, "B:", time_black_gesammt, "("+ str(time_white_gesammt+time_black_gesammt)+")")

play(ammound=100)
