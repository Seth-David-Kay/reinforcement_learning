import lib # Importing my library file
import time

def guiish_simulate_run(moves):
    # See what the trained player does with a somewhat working gui
    clean_board = lib.board()
    clean_board.add_platforms()
    new_player = lib.player(clean_board)
    clean_board.print_board_with_players()
    for i in range(len(moves)):
        time.sleep(0.35)
        print(moves[i])
        new_player.make_one_move(moves[i], False, clean_board)
        clean_board.print_board_with_players()

def cli_input_simulate_run():
    moves = input("Enter the moves you want to simulate, taken from the moves_taken file (or the same format): ")
    # Example input: | ur | ur | ur | d | r | d | u | l | u |
    moves = moves.split("|")
    moves = [move.strip() for move in moves if move != ""]
    clean_board = lib.board()
    clean_board.add_platforms()
    new_player = lib.player(clean_board)
    clean_board.print_board_with_players()
    for i in range(len(moves)):
        time.sleep(0.35)
        print(moves[i])
        new_player.make_one_move(moves[i], False, clean_board)
        clean_board.print_board_with_players()
