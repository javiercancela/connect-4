# Agent Guidelines

## Project Overview

Connect-4 game engine for Reinforcement Learning. Pure game logic only - no graphics, no AI move selection.

## Architecture

```
connect4/
├── __init__.py      # Exports: Connect4, Board, WinChecker, constants
├── constants.py     # ROWS=6, COLS=7, WIN_LENGTH=4, PLAYER_1=1, PLAYER_2=-1, EMPTY=0
├── board.py         # Board class - grid state and piece placement
├── win_checker.py   # WinChecker class - static win detection
└── game.py          # Connect4 class - game orchestration

tests/
├── test_game.py
└── test_win_checker.py
```

## Key Classes

### Connect4 (game.py)
Main game interface. Manages turns, game state, and delegates to Board/WinChecker.

```python
game = Connect4()
game.play(column)        # Returns (success, winner)
game.get_valid_moves()   # List[int]
game.current_player      # 1 or -1
game.is_game_over        # bool
game.winner              # 1, -1, or None
game.get_board()         # np.ndarray (6x7)
game.get_state()         # Board from current player's perspective
game.copy()              # Deep copy for simulations
game.reset()             # Reset to initial state
```

### Board (board.py)
Grid state management. Row 0 is bottom (where pieces land).

```python
board = Board()
board.drop_piece(col, player)    # Returns row where piece landed
board.is_column_available(col)   # bool
board.get_available_columns()    # List[int]
board.get_cell(row, col)         # int (1, -1, or 0)
board.get_grid()                 # np.ndarray copy
board.copy()                     # Deep copy
```

### WinChecker (win_checker.py)
Static win detection. Checks horizontal, vertical, and both diagonals.

```python
WinChecker.check_win(board, row, col)  # bool - checks from last move position
```

## Design Decisions

- Players are 1 and -1 (not 1 and 2) for easier neural network output
- Board uses numpy int8 for memory efficiency
- Row 0 is bottom of board (gravity simulation)
- `get_state()` returns board multiplied by current player (perspective transform)
- All state methods return copies to prevent external mutation

## Testing

```bash
pytest tests/ -v
```

## Code Style

- Small, focused classes with single responsibilities
- Self-documenting method names, minimal comments
- Type hints on all public methods
- No docstrings unless logic is non-obvious

## Future Extensions

This engine is designed for RL training. Expected additions:
- RL agents (random, Monte Carlo, DQN, etc.)
- Training scripts
- Model evaluation utilities
