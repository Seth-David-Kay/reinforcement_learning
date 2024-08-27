import random
import math

# Class for the player
class player:
    def __init__(self, board):
        self.name = board.player_count
        self.x_coord = 0
        self.y_coord = 18

        # Init with board
        board.init_player(self)

    def get_rand_move_list(self, num_moves):
        possible_moves = ['u', 'd', 'r', 'l', 'ur', 'ul']
        random_moves = []
        for i in range(num_moves):
            random_moves.append(possible_moves[random.randint(0,5)])
        return random_moves

    def make_one_move(self, move, write_to_file, board):
        moves = [move]
        self.move_on_list(moves, write_to_file, board)

    # Takes in a list of moves to take
    def move_on_list(self, moves, write_to_file, board):
        # Return values
        highest_point = 0
        time_of_highest_point = 0
        final_height = 0
        move_count = 0
        move_coords = []
        # If we want to, write the moves to the file
        if write_to_file:
            self.write_moves_to_file(moves, "moves_taken.txt")
        for move in moves:
            if self.valid_move(move, board):
                if move == 'u':
                    self.y_coord -= 2
                elif move == 'd':
                    self.y_coord += 2
                elif move == 'r':
                    self.x_coord += 1
                elif move == 'l':
                    self.x_coord -= 1
                elif move == 'ur':
                    self.y_coord -= 2
                    self.x_coord += 1
                elif move == 'ul':
                    self.y_coord -= 2
                    self.x_coord -= 1
            # else:
                # Edge cases if not a valid move
                # TODO: Make sure I'm correct: but I think if anything fails it
                # just means no action can be taken, even in the case of moves
                # that are a combination of multiple - notably ur and ul.
                # Even if we can move up one or two blocks, to complete the
                # ur or ul we would have to move r or l, which without we would
                # just fall back to where we were, meaning we don't have any
                # intermitten steps we are leaving out.
            self.fall(board)
            # Record highest height
            if (18 - self.y_coord) > highest_point:
                highest_point = 18 - self.y_coord
                time_of_highest_point = move_count
            # Add the player's current coords to the move coords
            move_coords.append([self.x_coord, self.y_coord])
            # Increment the move count for return values
            move_count += 1
        # If write to file, write move_coords to file
        if write_to_file:
            self.write_move_coords_to_file(move_coords, "moves_taken.txt")
        # Record final height
        final_height = 18 - self.y_coord
        return highest_point, final_height, time_of_highest_point, move_coords

    def fall(self, board):
        # Fall to nearest ground block
        x = self.x_coord
        y = self.y_coord
        ground_y_coord = y + 1
        while(ground_y_coord <= 19): # Base case in while loop: ground floor
            if board.board[ground_y_coord][x] == ' - ':
                break
            else:
                ground_y_coord += 1
        self.y_coord = ground_y_coord - 1 # Minus one go go one above the ground

    # Takes in a move, returns true if valid and false if not
    def valid_move(self, move, board):
        x = self.x_coord
        y = self.y_coord
        platform = ' - ' # Hard coded string for platform
        if move == 'u':
            # Can leave the board when jumping, because the player will always fall back in
            if y - 1 < 0: # Can't be anything above, so just let the player jump and fall back down
                return True
            if y - 2 < 0:
                # If directly above is a platform, can't jump.
                # Otherwise, fine, jump, you'll just fall right back down
                if board.board[y - 1] == platform:
                    return False
                else:
                    return True
            # Now non-edge cases (literally lol)
            if board.board[y - 1][x] == platform: # Hard coded string for platform
                return False
            if board.board[y - 2][x] == platform:
                return False
        if move == 'd':
            if y + 2 > 18: # Can never go below 18
                return False
            if board.board[y + 2][x] == platform:
                return False
        if move == 'r':
            if x + 1 > 19: # Can never go out of bounds
                return False
            if board.board[y][x + 1] == platform:
                return False
        if move == 'l':
            if x - 1 < 0: # Can never go out of bounds
                return False
            if board.board[y][x - 1] == platform:
                return False
        if move == 'ur':
            if x + 1 > 19: # Out of bounds on the right - we don't care about out of bounds up
                return False
            if board.board[y - 1][x] == platform: # Hard coded string for platform
                return False
            if board.board[y - 2][x] == platform:
                return False
            if board.board[y - 2][x + 1] == platform:
                return False
        if move == 'ul':
            if x - 1 < 0: # Out of bounds on the left - we don't care about out of bounds up
                return False
            if board.board[y - 1][x] == platform: # Hard coded string for platform
                return False
            if board.board[y - 2][x] == platform:
                return False
            if board.board[y - 2][x - 1] == platform:
                return False
        # If no errors,
        return True

    def write_moves_to_file(self, moves, filename):
        with open("moves_taken.txt", "a") as file:
            file.write('%s: ' %self.name)
            for move in moves:
                file.write('| %s ' %move)
            file.write("|\n")
        file.close()

    def write_move_coords_to_file(self, move_coords, filename):
        with open("moves_taken.txt", "a") as file:
            file.write('%s: ' %self.name)
            for move_coord in move_coords:
                file.write('| %s, %s ' % (move_coord[0], move_coord[1]))
            file.write("|\n")
        file.close()

# Class for the board
class board:
    # Init
    def __init__(self):
        # Hard coded size for now
        # Short code for board = [] for 20 : add another [] for 20 in each other [], add a '[]'
        self.board = [['[ ]' for i in range(20)] for i in range(20)]
        self.players = []
        self.player_count = 0

# Board Init Section
    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            # .join is short code for iterating through the individual row to each index
            print(' '.join(row))

    def print_board_with_players(self):
        board = self.board
        for row in range(len(board)):
            row_str = ""
            for col in range(len(board[row])):
                # Check if a player exists at that tile
                has_player = False
                for player in self.players:
                    if player.x_coord == col and player.y_coord == row:
                        has_player = True
                if has_player == True:
                    row_str += ' x '
                else:
                    row_str += board[row][col]
            print(row_str)

    def add_platforms(self):
        # Just hard coded platforms for now
        board = self.board
        # Fill in ground floor
        for i in range(20): board[19][i] = ' - '
        # Add custom platforms
        board[17][5] = board[17][6] = board[17][7] = board[17][8] = ' - '
        board[16][9] = board[16][10] = board[16][11] = board[16][12] = board[16][13] = ' - '
        board[14][14] = board[14][15] = ' - '
        board[12][13] = board[12][12] = ' - '
        board[10][11] = board[10][10] = ' - '
        board[8][9] = board[8][8] = ' - '
        board[6][7] = board[6][6] = board[6][5] = board[6][4] = board[6][3] = board[6][2] = board[6][1] = board[6][0] = ' - '
        board[4][2] = ' - '
        board[3][3] = ' - '
        board[2][4] = board[2][5] = board[2][6] = board[2][7] = board[2][8] = board[2][9] = board[2][10] = ' - '
        board[1][11] = ' - '

# Player Interactions Section
    # Adds a player to the board
    def init_player(self, player):
        self.player_count += 1
        self.players.append(player)

# Class for the neural neet
# Neural net stores 6 values for each space on the board.
    # Next iteration for adaptive learning:
    # store a value for each 4 by 4 area around the player
    # that has 6 values itself, store the area and if we encounter
    # the same area find it and use those values, else create the are
    # with default values and train it from there. Also hash the area
    # so we can find it without iteration if it exists.
class neural_net:
    def __init__(self, file_name):
        self.net = []
        created_file_name = ""
        if file_name == None:
            created_file_name = self.create_net()
            self.net = self.read_net_weights_from_file(created_file_name)
        else:
            self.net = self.read_net_weights_from_file(file_name)

    def read_net_weights_from_file(self, file_name):
        # Just in case, reset self.net
        net = []
        with open(file_name, 'r') as file:
            for line in file:
                net.append([float(x) for x in line.split()])
        return net

    # TODO: Issue Documentation. Writes two newlines at the end of the new nn file.
    def create_net(self):
        file_name = "neural-net-" + str(random.randint(10000, 1000000)) + ".txt"
        weights = []
        # Init neural net with 100 random moves each with 6 options, all weights being 1
        for i in range(20 * 20): # Board size
            weights.append([])
            for j in range(6):
                weights[i].append(1/6) # Default chance it gets picked
        # Write weights to file
        with open(file_name, 'w') as file:
            for move in weights:
                for weight in move:
                    file.write('%s ' %weight)
                file.write('\n')
        file.close()
        return file_name

    def get_best_move(self, player):
        possible_moves = ['u', 'd', 'r', 'l', 'ur', 'ul']
        best_move = 'u' # Just default to 'u', should always be overwritten
        x = player.x_coord
        y = player.y_coord
        # Hash is (20 * y) + x for now
        move_percentages = self.net[(20 * y) + x]
        # Chooses a rand float between 0 and all floats added together, then
        # chooses the index at that rand float's range
        index = random.uniform(0, sum(move_percentages))
        if index > 0 and index < move_percentages[0]:
            return possible_moves[0]
        elif index > move_percentages[0] and index < move_percentages[0] + move_percentages[1]:
            return possible_moves[1]
        elif index > move_percentages[0] + move_percentages[1] and index < move_percentages[0] + move_percentages[1] + move_percentages[2]:
            return possible_moves[2]
        elif index > move_percentages[0] + move_percentages[1] + move_percentages[2] and index < move_percentages[0] + move_percentages[1] + move_percentages[2] + move_percentages[3]:
            return possible_moves[3]
        elif index > move_percentages[0] + move_percentages[1] + move_percentages[2] + move_percentages[3] and index < move_percentages[0] + move_percentages[1] + move_percentages[2] + move_percentages[3] + move_percentages[4]:
            return possible_moves[4]
        # Should always default to the next one but just to be sure puting the ranges and then a default completely random choosing
        elif index > move_percentages[0] + move_percentages[1] + move_percentages[2] + move_percentages[3] + move_percentages[4] and index < move_percentages[0] + move_percentages[1] + move_percentages[2] + move_percentages[3] + move_percentages[4] + move_percentages[5]:
            return possible_moves[5]
        # TODO: Later maybe change it to get the top move if no moves
        # were chosen
        return possible_moves[random.randint(0,5)]

    # TODO: make it have an asymptote at one and 0 : the closer a percentage gets, the slower it increases
    def weigh_values(self, moves, move_coords, finishing_place_percent, file_name, debug):
        moves_char_to_int = {"u":0, "d":1, "r":2, "l":3, "ur":4, "ul":5}
        for i in range(len(moves)):
            move_percentages = self.net[(20 * move_coords[i][1]) + move_coords[i][0]]
            # Moves at i converted to its place in moves_percentages using moves_char_to_int dict
            current_percentage = move_percentages[moves_char_to_int[moves[i]]]
            # Calculate how much to weigh the player and if it should be positive or negative given their finishing place
            # Can change to be finishing_place >= total_participants / 2 if not using finishing_place_percent
            # positive_negative = 1 if finishing_place_percent >= 100 / 2 else -1 # TODO: Making it right now that all values are positive,
            # with lower rankings having just having less of an impact. This is incorrect and not sustainable, just using it for the moment
            # to make review the outcome of my other algorithms. These values should be asymptotic and they should be able to be
            # subtracted from as well. (My thoughts on the topic as of this moment.)
            # Formula for weight adjustment to be added to taken move
            #                                                 largest percent increase : 0.05%
            # We can also make this not 0.001 hard coded and instead make it based on the total number of participatns as an equation
            # Abs just in case. At this stage in development we don't want any values to decrease.
            # TODO: Removed the -50 after finishing_place_percent below because *I THINK* that average will just be 0%, at least that
            # is what is happening in practice. And it makes sense because I use percent differences away from the average.
            # TODO: When moving to a percentile ranking system using the percentile rank equation and idea, add the -50 back in
            # so the bottom half of ranks will subtract, the average will have no impact, and the top half of ranks will add.
            # Also make sure that the algorithm can incorporate subtraction at that point.
            weight_adjustment = abs(finishing_place_percent) * 0.0001
            if debug:
                print(f"Weight Adjustment: {weight_adjustment} -> rank: {finishing_place_percent} -> move_coords: {move_coords[i]}")
            # Add adjustment to move percentage
            self.net[(20 * move_coords[i][1]) + move_coords[i][0]][moves_char_to_int[moves[i]]] += weight_adjustment
        self.write_net_to_file(file_name)

    def write_net_to_file(self, file_name):
        weights = self.net
        # Write weights to file
        with open(file_name, 'w') as file:
            for move in weights:
                for weight in move:
                    file.write('%s ' %weight)
                file.write('\n')
        file.close()
        return file_name

    # Inputs: a dict of {player object: [highest_point, time_of_highest_point, final_height]}
    # Outputs: a dict of {player object: [highest_point, time_of_highest_point, final_height, final_score]}
    def rank_players(self, player_dict):
        # Ranking system inputs: {highest_point, time_of_highest_point, final_height}
        # Get average highest_point
        total_highest_points = 0
        total_players = 0
        for player in player_dict:
            total_players += 1
            total_highest_points += player_dict[player].get("highest_point")
        # Get average highest_point
        total_time_of_highest_point = 0
        for player in player_dict:
            total_time_of_highest_point += player_dict[player].get("time_of_highest_point")
        # Get average final_height
        total_final_heights = 0
        for player in player_dict:
            total_final_heights += player_dict[player].get("final_height")
        # Get averages
        average_highest_point = total_highest_points / total_players
        average_time_of_highest_point = total_time_of_highest_point / total_players
        average_final_height = total_final_heights / total_players
        # Calculate each player's ppositional score as a percent
        for player in player_dict:
            highest_point = player_dict[player].get("highest_point")
            time_of_highest_point = player_dict[player].get("time_of_highest_point")
            final_height = player_dict[player].get("final_height")
            # TODO: Check calculation. Calulating currently by taking percent distance from average
            # NOTE: The percent difference algorithm allows for values over 100%
            highest_point_percent_difference = (self.percent_difference(highest_point, average_highest_point))
            time_of_highest_point_percent_difference = (self.percent_difference(time_of_highest_point, average_highest_point))
            final_height_percent_difference = (self.percent_difference(final_height, average_highest_point))
            # Weighted averaging for the final score
            # Encorporate difference - average below so that 50% is average and 1% is good and 100% is bad
            final_score = 0.5 * highest_point_percent_difference + 0.3 * time_of_highest_point_percent_difference + 0.2 * final_height_percent_difference
            # TODO:It's okay for the rankings to be high or low, they can't be negative which is all I care about for the moment,
            # just have to account for the large percentages later in the pipeline.
            # Add player and score to the return dict's player's dict
            player_dict[player]["final_score"] = final_score

    def percent_difference(self, v1, v2):
        if int(v1) == 0 and int(v2) == 0:
            return 0
        return (abs(v1 - v2) / ((v1 + v2) / 2)) * 100

    def print(self):
        print(self.net)
