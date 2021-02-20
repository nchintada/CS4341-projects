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
            v, a = self.maxvalue(brd, -math.inf, math.inf, 0, 0)
        else:
            self.enemy = 1
            v, a = self.maxvalue(brd, -math.inf, math.inf, 0, 0)
        # v = self.maxvalue(brd, 1000000, -100000)
        print(v)
        #for state in self.get_successors(brd):
        #    print(state)
        #    if v == evaluation.Evaluation(state[0], self).evaluate():
        #        return state[1]
        #return -1
        return a


    def maxvalue(self, board, alpha, beta, a, d):
        # score = evaluation.Evaluation(board, self).score()
        if board.get_outcome() != 0 or d == self.max_depth: # original condition: board.get_outcome() == self.player
            return evaluation.Evaluation(board, self).score(), a
        v = -math.inf
        action = 0
        for a in self.get_successors(board):
            val = self.minvalue(a[0], alpha, beta, a[1], d+1)
            if val > v:
                v = val
                action = a[1]
            #v = max(v, val)
            if v >= beta:
                #print("Max val 1:" + str(v))
                return v, a[1]
            alpha = max(alpha, v)
        #print("Max val 2:" + str(v))
        return v, action



    def minvalue(self, board, alpha, beta, a, d):
        # score = evaluation.Evaluation(board, self).score()
        if board.get_outcome() != 0 or d == self.max_depth:
            return evaluation.Evaluation(board, self).score()
        v = math.inf
        for a in self.get_successors(board):
            val, act = self.maxvalue(a[0], alpha, beta, a[1], d+1)
            v = min(v, val)
            if v <= alpha:
                #print("Min val 1:" + str(v))
                return v
            beta = min(beta, v)
        #print("Min val 2:" + str(v))
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


THE_AGENT = AlphaBetaAgent("Group10", 4)
