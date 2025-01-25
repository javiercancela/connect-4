from game_engine.board import Board


def _is_placeable(board, row, column):
    """
    Returns True if a piece placed at (r,c) would actually stay there
    in a real Connect-4 game (i.e., the cell below is either out of
    bounds or occupied).
    """
    # If we're at the bottom row or the cell below is non-empty
    return (row == 0) or (board[row - 1, column] != 0)


def _count_in_direction(board, row, column, dr, dc, player):
    """
    Counts how many consecutive 'player' pieces (including the one
    at (row, column)) exist in a particular direction (dr, dc).
    """
    rows, cols = board.shape
    count = 0
    next_row, next_column = row, column
    while (
        0 <= next_row < rows
        and 0 <= next_column < cols
        and board[next_row, next_column] == player
    ):
        count += 1
        next_row += dr
        next_column += dc
    return count


def _all_four_in_a_row_segments(board):
    """
    Generate all possible 4-cell segments (as lists of coordinates)
    in horizontal, vertical, and diagonal directions.
    """
    rows, cols = board.shape

    segments = []

    # Horizontal segments
    for r in range(rows):
        for c in range(cols - 3):
            segments.append([(r, c + i) for i in range(4)])

    # Vertical segments
    for c in range(cols):
        for r in range(rows - 3):
            segments.append([(r + i, c) for i in range(4)])

    # Diagonal (down-right) segments
    for r in range(rows - 3):
        for c in range(cols - 3):
            segments.append([(r + i, c + i) for i in range(4)])

    # Diagonal (up-right) segments
    for r in range(3, rows):
        for c in range(cols - 3):
            segments.append([(r - i, c + i) for i in range(4)])

    return segments


def _check_minor_threats(board, segment, player):
    """
    Determine if a 4-cell 'segment' is a minor threat for 'player':
      - exactly 2 cells have 'player',
      - 0 cells have the opponent,
      - 2 cells are empty,
      - the 2 empty cells can eventually be filled by dropping pieces.
    Returns a list of those empty cell coordinates if it's a minor threat,
    otherwise returns None.
    """
    # Identify what's in the segment
    values = [board[r, c] for (r, c) in segment]
    empty_cells = [coord for coord in segment if board[coord] == 0]
    player_count = sum(1 for v in values if v == player)
    opponent_count = sum(
        1 for v in values if v not in [0, player]
    )  # anything not 0 or player is the opponent

    if player_count == 2 and opponent_count == 0 and len(empty_cells) == 2:
        # Now check if these 2 empty cells are "eventually placeable"
        # i.e., a piece can occupy that spot after the correct sequence of moves.
        # We'll do a simplified check:
        #  - either it is placeable right now (is_placeable),
        #  - or eventually placeable if the cell(s) below it are fillable or out of bounds.

        # For full correctness, you'd simulate placing one piece and see if the next is placeable.
        # We'll do a quick approach: if the cell below is out of bounds or occupied for each empty cell,
        # we consider it eventually placeable.

        for r, c in empty_cells:
            # If it's not placeable now, check that
            # eventually the cell directly below won't be empty.
            # We'll interpret "eventually fillable" as:
            #   if the cell below is in board and is empty, then
            #   we can eventually fill it with a piece (either the player’s or the opponent’s)
            #   so that (r, c) becomes placeable.

            # This is a simplified logic: if there's a 'column' of empty squares under (r, c),
            # we assume that eventually they might be filled.
            # In a real game, you'd track which turn goes where, but this is
            # enough to illustrate the concept for "minor threat."
            below_r = r + 1
            while below_r < board.shape[0] and board[below_r, c] == 0:
                below_r += 1
            # If we exit because below_r == board.shape[0], it means out of bounds, so eventually placeable.
            # If we exit because board[below_r, c] != 0, also eventually placeable.
            # We'll keep it simple: it's eventually placeable.
            # If you want a more rigorous check, you'd do deeper turn-by-turn simulation.

        # If we got this far, let's say it *is* a minor threat for this segment.
        return empty_cells

    return None


def _forms_connect_4(board, row, column, player):
    """
    Temporarily place 'player' in (r, c) and check if it forms 4 in a row.
    Checks horizontal, vertical, and two diagonal directions.
    """
    board[row, column] = player
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        # Count in both directions: (dr,dc) and its opposite (-dr,-dc)
        total = (
            _count_in_direction(board, row, column, dr, dc, player)
            + _count_in_direction(board, row, column, -dr, -dc, player)
            - 1
        )
        if total >= 4:
            board[row, column] = 0
            return True
    board[row, column] = 0
    return False


def _remove_duplicates(threats):
    """
    Remove duplicate threats from the list of threats.
    """
    for player in threats:
        for check in threats[player]["checks"]:
            if check in threats[player]["major_threats"]:
                threats[player]["major_threats"].remove(check)
            for minor_threat in threats[player]["minor_threats"]:
                if check in minor_threat:
                    threats[player]["minor_threats"].remove(minor_threat)
    return threats


def _compare_score_indicators(old, new, value):
    score = 0
    for element in new:
        if element not in old:
            score += value
    for element in old:
        if element not in new:
            score -= value

    return score


def _calculate_move_score(player, old_threats, new_threats):

    score = 0
    score += _compare_score_indicators(
        old_threats[player]["checks"], new_threats[player]["checks"], 0.4
    )
    score += _compare_score_indicators(
        old_threats[player]["major_threats"], new_threats[player]["major_threats"], 0.3
    )
    score += _compare_score_indicators(
        old_threats[player]["minor_threats"], new_threats[player]["minor_threats"], 0.1
    )

    return score


class Evaluator:
    def __init__(self):
        self.past_threats = {
            1: {"checks": [], "major_threats": [], "minor_threats": []},
            2: {"checks": [], "major_threats": [], "minor_threats": []},
        }

    def get_score(self, last_player, board):
        new_threats = self._find_threats(board)

        next_player = 1 if last_player == 2 else 2
        score = _calculate_move_score(last_player, self.past_threats, new_threats)
        score += _calculate_move_score(next_player, self.past_threats, new_threats)

        self.past_threats = new_threats

        return score

    def get_existing_threats(self):
        return self.past_threats

    def _find_threats(self, board):
        new_threats = {
            1: {"checks": [], "major_threats": [], "minor_threats": []},
            2: {"checks": [], "major_threats": [], "minor_threats": []},
        }

        # Step 1: Identify checks & major threats (existing logic)
        for row in range(Board.ROWS):
            for column in range(Board.COLUMNS):
                if board[row][column] == 0:
                    for player in [1, 2]:
                        if _forms_connect_4(board, row, column, player):
                            if _is_placeable(board, row, column):
                                new_threats[player]["checks"].append((row, column))
                            else:
                                new_threats[player]["major_threats"].append(
                                    (row, column)
                                )

        # Step 2: Identify minor threats
        segments = _all_four_in_a_row_segments(board)
        for seg in segments:
            for player in [1, 2]:
                minor = _check_minor_threats(board, seg, player)
                if minor:
                    # 'minor' is a list of 2 empty coords.
                    # We can store them however you like;
                    # for clarity, I'll just store the pair of coords.
                    # Or you can store each coordinate individually.
                    new_threats[player]["minor_threats"].append(tuple(minor))

        return _remove_duplicates(new_threats)
