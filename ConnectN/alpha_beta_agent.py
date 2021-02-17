import math
import agent
import evaluation

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        v = 0
        a = 0
        self.enemy = 0
        if self.player == 1:
            self.enemy = 2
            v, a = self.maxvalue(brd, -math.inf, math.inf, 0)
        else:
            self.enemy = 1
            v, a = self.maxvalue(brd, -math.inf, math.inf, 0)

        print(v)
        return a


    def maxvalue(self, board, alpha, beta, d):
        alp = alpha
        bet = beta
        if board.get_outcome() == self.player:
            #print("Outcome found (max)")
            return 1000, -1
        elif board.get_outcome() == self.enemy:
            #print("Outcome found (max)")
            return -1000, -1
        if d == self.max_depth:
            print("do we get to depth?")
            return evaluation.Evaluation(board, self).evaluate(), -1
        v = -math.inf
        act = 0
        for a in self.get_successors(board):
            print("Exploring max: ", a[1])
            val = self.minvalue(a[0], alp, bet, d+1)
            print("Value after min: " + str(val))
            print("Beta: " + str(bet))
            if val >= v:
                v = val
                act = a[1]
            alp = max(alp, v)
            if v >= bet:
                print("Max val 1:" + str(v))
                return v, a[1]
        print("Max val 2:" + str(v))
        return v, act



    def minvalue(self, board, alpha, beta, d):
        alp = alpha
        bet = beta
        if board.get_outcome() == self.player:
            # print("Outcome found (max)")
            return 1000
        if board.get_outcome() == self.enemy:
            # print("Outcome found (max)")
            return -1000
        if d == self.max_depth:
            print("do we get to depth?")
            return evaluation.Evaluation(board, self).evaluate()
        v = math.inf
        for a in self.get_successors(board):
            print("Exploring min: ", a[1])
            val, act = self.maxvalue(a[0], alp, bet, d+1)
            print("Value after max: " + str(val))
            print("Alpha: " + str(alp))
            v = min(v, val)
            bet = min(bet, v)
            if v <= alp:
                print("Min val 1:" + str(v))
                return v
        print("Min val 2:" + str(v))
        return v

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ
