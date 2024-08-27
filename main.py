import lib # Importing my library file
import tests # Importing my tests file
import random

# Which class should this go in? None? Probably none, right?
def train_model_it():
    # TODO: add a loading bar in terminal that goes up every time 100 new players or something get trained
    nn_file_name = "neural_net.txt"
    board = lib.board()
    board.add_platforms()
    player_dict = {}
    for i in range(100000):
        player = lib.player(board)
        moves = player.get_rand_move_list(10)
        highest_point, final_height, time_of_highest_point, move_coords = player.move_on_list(moves, False, board)
        player_dict[player] = {"highest_point": highest_point, "time_of_highest_point": time_of_highest_point, "final_height": final_height, "moves": moves, "move_coords": move_coords}

    # Neural net math
    nn = lib.neural_net(nn_file_name)
    nn.rank_players(player_dict)
    for player in player_dict:
        nn.weigh_values(player_dict[player]["moves"], player_dict[player]["move_coords"], player_dict[player]["final_score"], nn_file_name, False)

if __name__=="__main__":
    # Init
    # train_model_it()
    tests.best_moves_guiish()
    print("All done")

# TODO: There is some issue with generating the next best move - test if the random get next best move function
# is working properly by measuring random outputs and seeing if they match percentage in neural net file

# When looking into the nn file itself, remember that it starts on line 1 and not 0, so the first
# move made is referencing 360 lines in, line 361

# TODO: Issue with tranining generations: right now to get the best move you have to make a move
# and then get the best move from there. Should be a way to get the best move,
# not make a move, and then get the next best move. then you can pass the list of best
# moves into the make move from list. I think can be abstracted into a function using the lib
# methods I have right now by making a move getting the best move, over and over, then stroign the best mvoes gotten
# in a list and applying them to a new player on a clean board. Is this solution too inneficient? I think
# it's not, after all essentially all make a single move method in lib is doing is making that move
# and returning the new coords, which are fed back into getting the best move. So it's efficient, just
# sub-par OOP design unless abstracted.
