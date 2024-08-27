import lib # Importing my library file
import random


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
