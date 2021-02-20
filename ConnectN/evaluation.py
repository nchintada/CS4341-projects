import board


class Evaluation(object):
    def __init__(self, board, agent):
        self.board = board
        self.width = board.w
        self.height = board.h
        self.agent = agent


    # def calc_center_value(self):
    #     # middlex = self.width / 2
    #     # dif = abs(middlex - self.xpos)
    #     # base_weight = self.width - dif
    #     #
    #     # max_moves = self.width * self.height
    #     # moves_remaining = max_moves - self.moves
    #     # #this next line should probably be modified to make sure it does not interfere with other parts of the heuristic
    #     # balanced_moves_remaining = moves_remaining / middlex
    #     # weight = balanced_moves_remaining + base_weight
    #     weight = 0
    #     middlex = int(self.width / 2)
    #     # for y in range(0, self.height):
    #     #     if self.board.board[y][middlex] == self.agent.player:
    #     #         weight = 100 * abs(middlex - )
    #     for i in range(0, self.width):
    #         weight = 100*(self.width / 2 + (1 - 2 * (i % 2)) * (i + 1) / 2)
    #         # print("Weight: " + str(weight))
    #
    #     return weight

    def score(self):
        # Cycle through all the spaces with tokens and score them
        score = 0
        # for i in range(0, self.width):
        #     for j in range(0, self.height):
        #         midweight = 3 - abs(self.width/2 - i)
        #         if self.board.board[j][i] == self.agent.player:
        #             score += midweight
        #         if self.board.board[j][i] == self.agent.enemy:
        #             score -= midweight
        # Go for center
        for y in range(self.height):
            for x in range(self.width):
                if self.board.board[y][x] == self.agent.player:
                    score += (-(y + 1) * 2) + (((self.width / 2) - (abs((self.width / 2) - x))) + 1) * 50
        # Check vertical
        # for i in range(0, self.width - 3):
        #     for j in range(0, self.height):
        #         if self.board.board[j][i] == self.agent.player:
        #             score += 1
        # # Check horizontal
        # for i in range(0, self.width):
        #     for j in range(0, self.height - 3):
        #         if self.board.board[j][i] == self.agent.player:
        #             score += 1
        # # Check diagonal
        # for i in range(0, self.width - 3):
        #     for j in range(0, self.height - 3):
        #         if self.board.board[j][i] == self.agent.player:
        #             score += 1
        # # Check diagonal 2
        # for i in range(3, self.width):
        #     for j in range(0, self.height - 4):
        #         if self.board.board[j][i] == self.agent.player:
        #             score += 1
        # Finalize score
        # print("Score: " + str(score))
        score += 100 * self.find_three_of_four()[0]
        score += -100 * self.find_three_of_four()[1]
        if self.board.get_outcome() == self.agent.player:
            score += 10000
        if self.board.get_outcome() == self.agent.enemy:
            score -= -10000
        return score

    def find_connect_3(self):
        currPlayerPoints = 0
        enemy_player_points = 0
        for x in range(self.width):
            for y in range(self.height):
                for dx, dy in [(1, 0), (1, 1), (0, 1), (1, -1)]:  # Check each direction at each spot
                    xpos = x
                    ypos = y
                    if xpos >= self.height or ypos >= self.width: break
                    seq = 0
                    startToken = self.board.board[x][y]
                    if startToken == 0: break  # Not a player
                    for i in range(0, 2):  # Check in direction (dy, dx)
                        xpos = xpos + dx
                        ypos = ypos + dy
                        if xpos >= self.height or ypos >= self.width: break  # Out of bounds
                        currentToken = self.board.board[xpos][ypos]
                        if currentToken != startToken: break
                        seq = seq + 1
                    if seq >= 2:
                        if startToken == self.agent.player:
                            currPlayerPoints = currPlayerPoints + 1
                        else:
                            enemy_player_points = enemy_player_points + 1
        print(currPlayerPoints, enemy_player_points)
        return currPlayerPoints, enemy_player_points

    def find_three_of_four(self):
        currPlayerPoints = 0
        enemy_player_points = 0
        for x in range(self.width):
            for y in range(self.height):
                for dx, dy in [(1, 0), (1, 1), (0, 1), (1, -1)]:  # Check each direction at each spot
                    xpos = x
                    ypos = y
                    if xpos >= self.height or ypos >= self.width: break
                    seq = 0
                    startToken = self.board.board[x][y]
                    if startToken == 0: break  # Not a player
                    for i in range(0, 3):  # Check in direction (dy, dx)
                        xpos = xpos + dx
                        ypos = ypos + dy
                        if xpos >= self.height or ypos >= self.width: break  # Out of bounds
                        currentToken = self.board.board[xpos][ypos]
                        if currentToken == startToken or currentToken == 0:
                            if currentToken == startToken:
                                seq = seq + 1
                        else:
                            break
                    if seq >= 2:
                        if startToken == self.agent.player:
                            currPlayerPoints = currPlayerPoints + 1
                        else:
                            enemy_player_points = enemy_player_points + 1
        return currPlayerPoints, enemy_player_points

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

    def evaluate(self):
        weight = 0
        weight += 1000 * self.find_three_of_four()[0]
        weight += -1000 * self.find_three_of_four()[1]
        if self.board.get_outcome() == self.agent.player:
            weight += 100000
        if self.board.get_outcome() == self.agent.enemy:
            weight -= -100000
        return weight






