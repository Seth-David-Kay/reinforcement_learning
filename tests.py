import lib # Importing my library file
import random
import time


def rank_players_test(player_dict):
    nn_file_name = "neural_net.txt"
    board = lib.board()
    board.add_platforms()

    # Players
    player_dict = {}
    for i in range(10):
        player = lib.player(board)
        moves = player.get_rand_move_list(10)
        highest_point, final_height, time_of_highest_point, move_coords = player.move_on_list(moves, False, board)
        player_dict[player] = {"highest_point": highest_point, "time_of_highest_point": time_of_highest_point, "final_height": final_height, "moves": moves, "move_coords": move_coords}

    # Neural net math
    nn = lib.neural_net(nn_file_name)
    nn.rank_players(player_dict)
    for _ in player_dict: print(f'final score: {player_dict[_].get("final_score")}, highest point: {player_dict[_].get("highest_point")}')

def best_moves_guiish():
    # See what the trained player does with a somewhat working gui
    nn_file_name = "neural_net.txt"
    nn = lib.neural_net(nn_file_name)
    clean_board = lib.board()
    clean_board.add_platforms()
    new_player = lib.player(clean_board)
    clean_board.print_board_with_players()
    for i in range(100):
        # Wait for me to give an input to move to the next move
        # Or wait for _x_ seconds for each 'frame'
        # user_input = input("")
        time.sleep(0.35)
        best_move = nn.get_best_move(new_player)
        # print(nn.net[(20 * new_player.y_coord) + new_player.x_coord])
        print(best_move)
        # print((new_player.y_coord * 20) + new_player.x_coord)
        new_player.make_one_move(best_move, True, clean_board)
        clean_board.print_board_with_players()
