import board


class Evaluation(object):
    def __init__(self, board, agent):
        self.board = board
        self.width = board.w
        self.height = board.h
        self.agent = agent
        self.n = board.n
        if self.agent.player == 1:
            self.enemy = 2
        else:
            self.enemy = 1

    def find_connect_3(self):
        currPlayerPoints = 0
        enemy_player_points = 0
        for x in range(self.width):
            for y in range(self.height):
                for dx, dy in [(1, 0), (1, 1), (0, 1), (1, -1)]:  # Check each direction at each spot
                    if ((x + (self.n - 1) * dx >= self.width) or  # Not out of bounds
                        (y + (self.n - 1) * dy < 0) or (y + (self.n - 1) * dy >= self.height)): break
                    xpos = 0
                    ypos = 0
                    startToken = self.board.board[x][y]
                    if startToken == 0: break  # Not a player
                    for i in range(0, 2):  # Check in direction (dy, dx)
                        xpos = xpos + dx
                        ypos = ypos + dy
                        if xpos >= self.height or ypos >= self.width: break  # Out of bounds
                        currentToken = self.board.board[xpos][ypos]
                        if currentToken != startToken:
                            break
                    if startToken == self.agent.player:
                        currPlayerPoints += 1;
                    else:
                        enemy_player_points += 1;
        return currPlayerPoints, enemy_player_points



    # def find_open_winning_spots(self):
    #     currPlayerPoints = 0
    #     enemy_player_points = 0
    #     for x in range(self.width):
    #         for y in range(self.height):
    #             for dx, dy in [(1, 0), (1, 1), (0, 1), (1, -1)]:  # Check each direction at each spot
    #                 seq_count = 0
    #                 if ((x + (self.n - 1) * dx >= self.width) or  # Not out of bounds
    #                         (y + (self.n - 1) * dy < 0) or (y + (self.n - 1) * dy >= self.height)):
    #                     break
    #                 curr_player = self.board.board[y][x]  # Whose tokens are we looking at?
    #                 if curr_player == 0: break
    #                 # Go through elements
    #                 for i in range(1, self.n):
    #                     if self.board.board[y + i * dy][x + i * dx] == curr_player:
    #                         seq_count += 1
    #                     #if self.board[y + i * dy][x + i * dx] == 0:
    #                         #Append this as a "winSpot" = (x, y)
    #                     else:
    #                         break
    #                 print("seq ++ count player " + str(curr_player) + " connected " + str(seq_count))
    #                 if seq_count >= 2: #
    #                     print(curr_player)
    #                     if curr_player == self.agent.player:
    #                         currPlayerPoints = currPlayerPoints + 2
    #                     elif curr_player == self.enemy:
    #                         enemy_player_points = enemy_player_points + 1
    #     return currPlayerPoints #, enemy_player_points

    def empty_spaces_below(self, x, y):
        """Return 0 if there is an even number of empty spaces at and below (x,y)
            and 1 if there is an odd number"""
        empty_spaces = 1
        # while(x < self.h - 1):
        #    x = x + 1
        while (x > 0):
            x = x - 1
            if (self.board[x][y] == 0):
                empty_spaces = empty_spaces + 1
            else:
                break
        print(empty_spaces)
        if (empty_spaces % 2 == 0): return 0
        return 1

    def calc_center_value(self):
        weight = 0
        middlex = 1
        #dif = abs(middlex - self.action)
        #base_weight = self.width - dif
        base_weight = 0
        if self.board.board[0][3] == self.agent.player:
            base_weight += 5000
        #if self.action == 0 or self.action == 1 or self.action == 2 or self.action == 4 or self.action == 5 or self.action == 6:
        #    base_weight = -100000

        print("Weight: " + str(base_weight))


        #max_moves = self.width * self.height
        #moves_remaining = max_moves - self.moves
        #this next line should probably be modified to make sure it does not interfere with other parts of the heuristic
        #balanced_moves_remaining = moves_remaining / middlex
        #weight = balanced_moves_remaining + base_weight

        weight = base_weight


        return weight

    #def calc_block(self):


    def evaluate(self):
        weight = 0
        #if self.board.get_outcome() == self.agent.player:
        #    weight += 1000
        #if self.board.get_outcome() == self.enemy:
        #    weight += -1000
        weight += self.calc_center_value()
        print(self.find_connect_3())
        weight += 1000 * self.find_connect_3()[0]
        weight += -1000 * self.find_connect_3()[1]
        return weight



