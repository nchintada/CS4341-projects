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
        middlex = int(self.width / 2)
        #dif = abs(middlex - self.action)
        #base_weight = self.width - dif
        base_weight = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.board.board[y][x] == self.agent.player:
                    base_weight += (-(y+1) * 2) + (((middlex - (abs(middlex - x))) + 1) * 50)
                #if self.board.board[y][x] == self.enemy:
                #    base_weight -= ((self.height - y) * 5) + ((middlex - (abs(middlex - x))) * 30)



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



