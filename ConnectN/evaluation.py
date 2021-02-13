import board


class Evaluation(object):
    def __init__(self, board, agent):
        self.board = board
        self.width = board.w
        self.height = board.h
        self.agent = agent


    def calc_center_value(self):
        middlex = self.width / 2
        dif = abs(middlex - self.xpos)
        base_weight = self.width - dif

        max_moves = self.width * self.height
        moves_remaining = max_moves - self.moves
        #this next line should probably be modified to make sure it does not interfere with other parts of the heuristic
        balanced_moves_remaining = moves_remaining / middlex
        weight = balanced_moves_remaining + base_weight

        return weight

    def evaluate(self):
        if self.board.get_outcome() == self.agent.player:
            return 1000
        else:
            return 1



