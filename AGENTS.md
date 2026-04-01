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
├── __init__.py         # Exports: RandomAgent, HeuristicAgent, MinimaxAgent, DQNAgent, QLearningAgent
├── dqn_agent.py        # Greedy checkpoint-backed DQN inference agent
├── random_agent.py     # Random valid move baseline
├── heuristic_agent.py  # Tactical one-ply heuristic with safety checks
├── minimax_agent.py    # Alpha-beta minimax with evaluation function
└── qlearning_agent.py  # Greedy policy agent backed by trained Q-table

training/
├── train_qlearning.py          # Q-learning training CLI entrypoint
├── train_dqn.py                # DQN training CLI entrypoint
└── qlearning/
    ├── __init__.py             # Exports: QLearningTrainingConfig, train_qlearning
    ├── config.py               # Training hyperparameters and epsilon schedule
    ├── episode_runner.py       # Single-episode TD updates
    ├── evaluator.py            # Periodic policy evaluation vs fixed opponents
    ├── opponents.py            # Training/eval opponent factories
    ├── persistence.py          # Gzip+pickle Q-table load/save helpers
    ├── policy.py               # Epsilon-greedy and greedy action selection
    ├── q_values.py             # Q-value get/set helpers with zero defaults
    ├── training_loop.py        # Multi-episode training orchestration
    └── types.py                # QTable alias (state -> action -> value)

training/dqn/
├── __init__.py             # Exports: DQNTrainingConfig, build_recommended_config, train_dqn
├── checkpoint.py           # Torch checkpoint load/save helpers
├── config.py               # DQN hyperparameters and epsilon schedule
├── console.py              # Timestamped training logs
├── episode_runner.py       # Single-episode replay generation
├── evaluator.py            # Greedy checkpoint evaluation vs fixed opponents
├── hardware.py             # Local hardware detection and recommended defaults
├── network.py              # Feed-forward Q-network
├── optimization.py         # Replay-sampled gradient updates
├── opponents.py            # Training/eval opponent factories
├── policy.py               # State flattening and action masking helpers
├── replay_buffer.py        # Fixed-size replay storage
├── training_loop.py        # Multi-episode DQN orchestration
└── types.py                # Replay batch and pending transition containers

tests/
├── test_game.py
├── test_win_checker.py
├── test_random_agent.py
├── test_minimax_agent.py
├── test_dqn_agent.py
├── test_dqn_training.py
└── test_qlearning_agent.py

play.py             # Interactive human vs agent CLI
benchmark.py        # Parallelized agent-vs-agent benchmark CLI
train_qlearning.py  # Legacy/extended Q-learning training script
train_dqn.py        # Legacy/extended DQN training script
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

### QLearningAgent (`agents/qlearning_agent.py`)

Loads a trained tabular Q-table from disk and plays greedily over valid moves.
Key details:
- board state is encoded from the current-player perspective
- horizontal mirror symmetry is canonicalized to reduce state space
- canonical actions are mapped back to board actions before play
- unseen states fall back to random valid moves

### DQNAgent (`agents/dqn_agent.py`)

Loads a trained torch checkpoint from disk and plays greedily over valid moves.
Key details:
- board state is encoded from the current-player perspective
- the network consumes the flattened `6x7` board
- invalid columns are masked before argmax selection
- inference defaults to CPU so CLI benchmarking can use process workers safely

## Q-learning Algorithm

The project uses tabular Q-learning with epsilon-greedy exploration and
perspective-encoded canonical states.

State/action representation:
- `state_key = state_to_key(game.get_state())` where `state_to_key` picks the
  lexicographically smaller of the board and its horizontal mirror
- action values are stored in canonical action space and remapped with `map_action`
- Q-table type is `dict[bytes, dict[int, float]]` with implicit `0.0` defaults

Episode update flow (`training/qlearning/episode_runner.py`):
1. On each Q-learning turn, choose action with epsilon-greedy policy:
   - explore with probability `epsilon`
   - otherwise choose argmax Q among valid actions (random tie-break)
2. Store `(state_key, action)` as pending for that player.
3. On that same player's next turn, perform TD bootstrap update:
   - `Q(s,a) <- Q(s,a) + alpha * (gamma * max_a' Q(s',a') - Q(s,a))`
4. At terminal state, apply final reward update for pending action:
   - win `+1.0`, draw `draw_reward`, loss `-1.0`
   - `Q(s,a) <- Q(s,a) + alpha * (reward - Q(s,a))`

Training loop (`training/qlearning/training_loop.py`):
- linearly anneals epsilon from `epsilon_start` to `epsilon_end`
- supports `self`, `random`, `heuristic`, or `minimax` opponents
- reports progress, periodically evaluates greedy policy, and checkpoints
- persists table as compressed pickle (`models/qtable.pkl.gz` by default)

## CLI Scripts

### `play.py`

Human vs selected agent (`Random`, `Heuristic`, `Minimax`, `Q-learning`, `DQN`).  
If minimax is selected, prompts for search depth (default `4`).

### `benchmark.py`

Runs many games between two selected agents. Supports:
- `Random`, `Heuristic`, `Minimax`, `Q-learning`, and `DQN` agents
- minimax depth selection per side
- configurable game count (default `1000`)
- configurable worker count (default CPU count)
- process-pool execution with fallback to single worker in restricted environments

### `training/train_qlearning.py`

Primary CLI for tabular Q-learning training. Supports:
- training episodes, alpha, gamma, epsilon schedule, and draw reward
- opponent selection (`self`, `random`, `heuristic`, `minimax`) and minimax depth
- optional Q-table resume (`--load`)
- periodic evaluation and checkpoint saves
- output path for compressed Q-table artifacts

### `training/train_dqn.py`

Primary CLI for Deep Q-Network training. Supports:
- training episodes, learning rate, gamma, epsilon schedule, and draw reward
- opponent selection (`self`, `random`, `heuristic`, `minimax`) and minimax depth
- hardware-aware defaults for device, hidden sizes, batch size, and replay capacity
- checkpoint resume, periodic evaluation, and periodic checkpoint saves
- output path for torch checkpoint artifacts

## Design Decisions

- Players are `1` and `-1` (not `1` and `2`) for model-friendly symmetric encoding
- Board uses `numpy.int8` for compact state representation
- Row index `0` is the bottom row (piece drop direction)
- `get_state()` applies perspective transform by multiplying board by `current_player`
- Public board/state getters return copies to avoid external mutation
- Agent simulations rely on `Connect4.copy()` and may access internals for speed
- Q-learning canonicalizes horizontal mirror states to share values across symmetric positions
- DQN trains on flattened current-player-perspective boards and masks invalid actions at inference/update time

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
