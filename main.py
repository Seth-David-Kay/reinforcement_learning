import lib # Importing my library file
import random

if __name__=="__main__":
    # Init
    nn_file_name = "neural_net.txt"
    board = lib.board()
    board.add_platforms()

    # Players
    player_dict = {}
    for i in range(10000):
        player = lib.player(board)
        moves = player.get_rand_move_list(10)
        highest_point, final_height, time_of_highest_point, move_coords = player.move_on_list(moves, False, board)
        player_dict[player] = {"highest_point": highest_point, "time_of_highest_point": time_of_highest_point, "final_height": final_height, "moves": moves, "move_coords": move_coords}

    # Neural net math
    nn = lib.neural_net(nn_file_name)
    nn.rank_players(player_dict)
    new_player = lib.player(board)
    for _ in player_dict: print(player_dict[_].get("final_score"))
    for player in player_dict:
        nn.weigh_values(player_dict[player]["moves"], player_dict[player]["move_coords"], player_dict[player]["final_score"], nn_file_name)

    print(nn.get_best_move(new_player))
