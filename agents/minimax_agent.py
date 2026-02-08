from connect4 import Connect4
from connect4.constants import COLS


class MinimaxAgent:
    def __init__(self, depth: int = 4):
        self.depth = max(1, depth)

    def select_move(self, game: Connect4) -> int:
        valid_moves = game.get_valid_moves()
        if len(valid_moves) == 1:
            return valid_moves[0]

        root_player = game.current_player
        best_score = float("-inf")
        best_move = valid_moves[0]

        for move in self._ordered_moves(valid_moves):
            game_copy = game.copy()
            game_copy.play(move)
            score = self._minimax(
                game_copy,
                self.depth - 1,
                float("-inf"),
                float("inf"),
                False,
                root_player,
            )

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(
        self,
        game: Connect4,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        root_player: int,
    ) -> float:
        if game.is_game_over:
            return self._terminal_score(game, depth, root_player)

        if depth == 0:
            return self._evaluate_position(game, root_player)

        valid_moves = game.get_valid_moves()

        if maximizing:
            value = float("-inf")
            for move in self._ordered_moves(valid_moves):
                child = game.copy()
                child.play(move)
                value = max(
                    value,
                    self._minimax(child, depth - 1, alpha, beta, False, root_player),
                )
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value

        value = float("inf")
        for move in self._ordered_moves(valid_moves):
            child = game.copy()
            child.play(move)
            value = min(
                value,
                self._minimax(child, depth - 1, alpha, beta, True, root_player),
            )
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

    def _terminal_score(self, game: Connect4, depth: int, root_player: int) -> float:
        if game.winner == root_player:
            return 1_000_000 + depth
        if game.winner is None:
            return 0
        return -1_000_000 - depth

    def _evaluate_position(self, game: Connect4, root_player: int) -> float:
        board = game.get_board()
        opponent = -root_player
        score = 0.0

        center_col = COLS // 2
        center_count = 0
        opponent_center_count = 0
        for row in range(board.shape[0]):
            if board[row, center_col] == root_player:
                center_count += 1
            elif board[row, center_col] == opponent:
                opponent_center_count += 1

        score += center_count * 6
        score -= opponent_center_count * 6

        for row in range(board.shape[0]):
            for col in range(board.shape[1] - 3):
                window = [board[row, col + i] for i in range(4)]
                score += self._evaluate_window(window, root_player)

        for col in range(board.shape[1]):
            for row in range(board.shape[0] - 3):
                window = [board[row + i, col] for i in range(4)]
                score += self._evaluate_window(window, root_player)

        for row in range(board.shape[0] - 3):
            for col in range(board.shape[1] - 3):
                window = [board[row + i, col + i] for i in range(4)]
                score += self._evaluate_window(window, root_player)

        for row in range(3, board.shape[0]):
            for col in range(board.shape[1] - 3):
                window = [board[row - i, col + i] for i in range(4)]
                score += self._evaluate_window(window, root_player)

        return score

    def _evaluate_window(self, window: list[int], root_player: int) -> float:
        opponent = -root_player
        root_count = window.count(root_player)
        opponent_count = window.count(opponent)
        empty_count = window.count(0)

        if root_count > 0 and opponent_count > 0:
            return 0

        if root_count == 4:
            return 100_000
        if root_count == 3 and empty_count == 1:
            return 120
        if root_count == 2 and empty_count == 2:
            return 12
        if root_count == 1 and empty_count == 3:
            return 1

        if opponent_count == 4:
            return -100_000
        if opponent_count == 3 and empty_count == 1:
            return -130
        if opponent_count == 2 and empty_count == 2:
            return -14
        if opponent_count == 1 and empty_count == 3:
            return -1

        return 0

    def _ordered_moves(self, moves: list[int]) -> list[int]:
        center = COLS // 2
        return sorted(moves, key=lambda move: (abs(move - center), move))
