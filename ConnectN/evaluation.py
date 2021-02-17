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
        print("Score: " + str(score))
        return score


    def evaluate(self):
        if self.board.get_outcome() == self.agent.player:
            return 1000
        if self.board.get_outcome() == self.agent.enemy:
            return -1000




