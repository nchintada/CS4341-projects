import evaluation
import board


board = board.Board([[0] * 6 for i in range(7)], 6, 7, 4)
evalu = evaluation.Evaluation(board, 3)
evalu2 = evaluation.Evaluation(board, 3)
print(evalu.calc_center_value())
print(evalu2.calc_center_value())