import random
import game
import agent
import alpha_beta_agent as aba

# Set random seed for reproducibility
#random.seed(11879)

#
# Random vs. Random
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.RandomAgent("random1"),       # player 1
#               agent.RandomAgent("random2"))       # player 2

#
# Human vs. Random
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               agent.RandomAgent("random"))        # player 2

#
# Random vs. AlphaBeta
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.RandomAgent("random"),  # player 1
#               aba.AlphaBetaAgent("alphabeta", 4)) # player 2


# AlphaBeta vs Random
#
# g2 = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               aba.AlphaBetaAgent("alphabeta", 4), # player 1
#               agent.RandomAgent("random"))  # player 2



#
# Human vs. AlphaBeta
#
g = game.Game(7, # width
              6, # height
              4, # tokens in a row to win
              agent.InteractiveAgent("human"),    # player 1
              aba.AlphaBetaAgent("alphabeta", 4)) # player 2

#
# Human vs. Human
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human1"),   # player 1
#               agent.InteractiveAgent("human2"))   # player 2

# Execute the game
#outcome = g.go()


def run_test_suite(ABPlayer, depth):
    seed = 1234
    random.seed(seed)



    max = 25
    AlphaBetaVictories = 0
    for i in range(0, 25):

        #
        # Random vs. AlphaBeta
        #
        goSecond = game.Game(7,  # width
                             6,  # height
                             4,  # tokens in a row to win
                             agent.RandomAgent("random"),  # player 1
                             aba.AlphaBetaAgent("alphabeta", depth))  # player 2

        # AlphaBeta vs Random
        #
        goFirst = game.Game(7,  # width
                            6,  # height
                            4,  # tokens in a row to win
                            aba.AlphaBetaAgent("alphabeta", depth),  # player 1
                            agent.RandomAgent("random"))  # player 2

        if ABPlayer == 1:
            outcome = goFirst.go()
            if outcome == 1:
                AlphaBetaVictories += 1
        else:
            outcome = goSecond.go()
            if outcome == 2:
                AlphaBetaVictories += 1
        seed += random.randint(0, 100)
        random.seed(seed)
    print("AlphaBeta won " + str(AlphaBetaVictories) + " out of " + str(max))

run_test_suite(2, 4)
