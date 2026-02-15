# Agent Guidelines

## Project Overview

Connect-4 engine and baseline agents for reinforcement learning experiments and agent-vs-agent evaluation.

## Architecture

```
connect4/
├── __init__.py      # Exports: Connect4, Board, WinChecker, constants
├── constants.py     # Board/player constants
├── board.py         # Board class (state, gravity, availability)
├── win_checker.py   # Static win detection from last move
└── game.py          # Connect4 game orchestration

agents/
├── __init__.py         # Exports: RandomAgent, HeuristicAgent, MinimaxAgent
├── random_agent.py     # Random valid move baseline
├── heuristic_agent.py  # Tactical one-ply heuristic with safety checks
└── minimax_agent.py    # Alpha-beta minimax with evaluation function

tests/
├── test_game.py
├── test_win_checker.py
├── test_random_agent.py
└── test_minimax_agent.py

play.py             # Interactive human vs agent CLI
benchmark.py        # Parallelized agent-vs-agent benchmark CLI
```

## Mermaid Diagrams

See `doc/ai/README.md` for complete diagrams:

- `doc/ai/architecture-overview.md`
- `doc/ai/class-diagram.md`
- `doc/ai/gameplay-sequence.md`
- `doc/ai/game-loop-flow.md`
- `doc/ai/heuristic-agent-flow.md`
- `doc/ai/minimax-agent-flow.md`
- `doc/ai/board-win-logic.md`

## Key Engine Classes

### Connect4 (`connect4/game.py`)

Main game API. Controls turns, validates moves, detects win/draw, and exposes board state helpers.

```python
game = Connect4()
game.play(column)        # (True, winner_or_none) or raises ValueError
game.get_valid_moves()   # list[int]
game.is_valid_move(col)  # bool
game.current_player      # 1 or -1
game.is_game_over        # bool
game.winner              # 1, -1, or None
game.is_draw             # bool
game.move_count          # int
game.get_board()         # np.ndarray shape (6, 7), copy
game.get_state()         # board from current-player perspective
game.get_state_flat()    # flattened board (42,)
game.copy()              # deep copy for simulation/search
game.reset()             # reset and return empty board copy
```

### Board (`connect4/board.py`)

Stores grid as `np.int8` with row `0` at the bottom (gravity model).

```python
board = Board()
board.drop_piece(col, player)    # returns landing row
board.is_column_available(col)   # bool
board.get_available_columns()    # list[int]
board.is_full()                  # bool
board.get_cell(row, col)         # int: 1, -1, 0
board.get_grid()                 # defensive copy
board.copy()                     # deep copy
```

### WinChecker (`connect4/win_checker.py`)

Checks four-in-a-row from last move by scanning bidirectionally in four directions.

```python
WinChecker.check_win(board, row, col)  # bool
```

## Agent Interface

All agents implement:

```python
def select_move(self, game: Connect4) -> int
```

`select_move` assumes at least one valid move is available.

## Built-in Agents

### RandomAgent (`agents/random_agent.py`)

Returns a random valid move.

### HeuristicAgent (`agents/heuristic_agent.py`)

Priority order:
1. Play immediate winning move
2. Block single immediate opponent winning move
3. Avoid moves that allow immediate opponent win
4. Prefer central columns among remaining moves

### MinimaxAgent (`agents/minimax_agent.py`)

Depth-limited minimax with alpha-beta pruning and center-first move ordering.  
Uses:
- terminal scoring (`+/-1_000_000 +/- depth`)
- non-terminal heuristic from center control and 4-cell window scoring

## CLI Scripts

### `play.py`

Human vs selected agent (`Random`, `Heuristic`, `Minimax`).  
If minimax is selected, prompts for search depth (default `4`).

### `benchmark.py`

Runs many games between two selected agents. Supports:
- minimax depth selection per side
- configurable game count (default `1000`)
- configurable worker count (default CPU count)
- process-pool execution with fallback to single worker in restricted environments

## Design Decisions

- Players are `1` and `-1` (not `1` and `2`) for model-friendly symmetric encoding
- Board uses `numpy.int8` for compact state representation
- Row index `0` is the bottom row (piece drop direction)
- `get_state()` applies perspective transform by multiplying board by `current_player`
- Public board/state getters return copies to avoid external mutation
- Agent simulations rely on `Connect4.copy()` and may access internals for speed

## Testing

```bash
pytest tests/ -v
```

Current suite covers:
- game lifecycle, win modes, draw property, move validation, copy/reset behavior
- board operations and availability
- win checking in all directions
- random agent validity
- minimax center preference, tactical win/block behavior
