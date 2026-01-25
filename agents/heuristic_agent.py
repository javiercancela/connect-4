import random
from connect4 import Connect4
from connect4.constants import COLS
from connect4.win_checker import WinChecker


class HeuristicAgent:
    def select_move(self, game: Connect4) -> int:
        valid_moves = game.get_valid_moves()

        if len(valid_moves) == 1:
            return valid_moves[0]

        current_player = game.current_player
        opponent = -current_player

        # Check for winning moves
        winning_moves = []
        for move in valid_moves:
            if self._is_winning_move(game, move, current_player):
                winning_moves.append(move)

        if winning_moves:
            return random.choice(winning_moves)

        # Check for opponent's winning moves (need to block)
        opponent_winning_moves = []
        for move in valid_moves:
            if self._is_winning_move(game, move, opponent):
                opponent_winning_moves.append(move)

        if len(opponent_winning_moves) == 1:
            return opponent_winning_moves[0]

        # Filter out moves that give opponent a winning move
        safe_moves = []
        for move in valid_moves:
            if not self._gives_opponent_winning_move(game, move):
                safe_moves.append(move)

        # If no safe moves, use all valid moves
        if not safe_moves:
            safe_moves = valid_moves

        # Pick the most central move(s)
        return self._pick_most_central(safe_moves)

    def _is_winning_move(self, game: Connect4, column: int, player: int) -> bool:
        game_copy = game.copy()
        # Temporarily override current player to simulate the move
        game_copy._current_player = player
        board = game_copy._board
        row = board._find_drop_row(column)
        board._grid[row, column] = player
        return WinChecker.check_win(board, row, column)

    def _gives_opponent_winning_move(self, game: Connect4, move: int) -> bool:
        # Simulate making this move
        game_copy = game.copy()
        game_copy.play(move)

        if game_copy.is_game_over:
            return False

        # Check if opponent has any winning move
        opponent_moves = game_copy.get_valid_moves()
        opponent = game_copy.current_player

        for opp_move in opponent_moves:
            if self._is_winning_move(game_copy, opp_move, opponent):
                return True

        return False

    def _pick_most_central(self, moves: list[int]) -> int:
        center = COLS // 2  # Column 3 for 7-column board

        # Calculate distance from center for each move
        min_distance = min(abs(move - center) for move in moves)

        # Get all moves with minimum distance
        best_moves = [move for move in moves if abs(move - center) == min_distance]

        return random.choice(best_moves)
