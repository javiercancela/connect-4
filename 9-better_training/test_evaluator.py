from game_engine.board import Board
from game_engine.evaluator import Evaluator


board = Board()
evaluator = Evaluator()
board.make_move(1, 0)
print(f"Player 1: {evaluator.get_score(1, board.board_positions)}")
print(board)
board.make_move(2, 4)
print(f"Player 2: {evaluator.get_score(2, board.board_positions)}")
print(board)

board.make_move(1, 3)
print(f"Player 1: {evaluator.get_score(1, board.board_positions)}")
print(board)
board.make_move(2, 0)
print(f"Player 2: {evaluator.get_score(2, board.board_positions)}")
print(board)

board.make_move(1, 0)
print(f"Player 1: {evaluator.get_score(1, board.board_positions)}")
print(board)
board.make_move(2, 0)
print(f"Player 2: {evaluator.get_score(2, board.board_positions)}")
print(board)

board.make_move(1, 3)
print(f"Player 1: {evaluator.get_score(1, board.board_positions)}")
print(board)
board.make_move(2, 4)
print(f"Player 2: {evaluator.get_score(2, board.board_positions)}")
print(board)

board.make_move(1, 6)
print(f"Player 1: {evaluator.get_score(1, board.board_positions)}")
print(board)
board.make_move(2, 4)
print(f"Player 2: {evaluator.get_score(2, board.board_positions)}")
print(board)

board.make_move(1, 6)
print(f"Player 1: {evaluator.get_score(1, board.board_positions)}")
print(board)
board.make_move(2, 3)
print(f"Player 2: {evaluator.get_score(2, board.board_positions)}")
print(board)

board.make_move(1, 6)
print(f"Player 1: {evaluator.get_score(1, board.board_positions)}")
print(board)
board.make_move(2, 3)
print(f"Player 2: {evaluator.get_score(2, board.board_positions)}")
print(board)

threads = evaluator.get_score(1, board.board_positions)
print(threads)
