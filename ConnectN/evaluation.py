import board


class Evaluation(object):
    def __init__(self, board, agent):
        self.board = board
        self.width = board.w
        self.height = board.h
        self.agent = agent
        if self.agent.player == 1:
            self.enemy = 2
        else:
            self.enemy = 1



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

        return weight



