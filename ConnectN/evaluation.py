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

    # Check if a line of identical tokens exists starting at (x,y) in direction (dx,dy)
    #
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # PARAM [int] dx: the step in the x direction
    # PARAM [int] dy: the step in the y direction
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise
    def is_line_at(self, x, y, dx, dy, d):
        """Return True if a line of identical tokens exists starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (d - 1) * dx >= self.width) or
                (y + (d - 1) * dy < 0) or (y + (d - 1) * dy >= self.height)):
            return False
        # Get token at (x,y)
        t = self.board.board[y][x]
        # Go through elements
        for i in range(1, d):
            if self.board.board[y + i * dy][x + i * dx] != t:
                return False
        return True

    # Check if a line of identical tokens exists starting at (x,y) in any direction
    #
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise
    def is_any_line_at(self, x, y, d):
        """Return True if a line of identical tokens exists starting at (x,y) in any direction"""
        return (self.is_line_at(x, y, 1, 0, d) or  # Horizontal
                self.is_line_at(x, y, 0, 1, d) or  # Vertical
                self.is_line_at(x, y, 1, 1, d) or  # Diagonal up
                self.is_line_at(x, y, 1, -1, d))  # Diagonal down


    #this is not blocking at all and never will the way it is set up, i need to re-evaluate this function
    def calc_block(self):
        weight = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.board.board[y][x] == self.enemy:
                    min_weight = 0

                    for d in range(2, 4):
                        test_weight = 0
                        if self.is_any_line_at(x, y, d):
                            test_weight -= 400 * d
                            min_weight = min(test_weight, min_weight)
                            print("Min Weight: " + str(min_weight))
                    weight += min_weight
        return weight





    def evaluate(self):
        weight = 0
        #if self.board.get_outcome() == self.agent.player:
        #    weight += 1000
        #if self.board.get_outcome() == self.enemy:
        #    weight += -1000
        weight += self.calc_center_value()
        #weight += self.calc_block()

        return weight



