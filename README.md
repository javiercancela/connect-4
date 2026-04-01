# Connect-4 Game Engine

A pure Python game engine for Connect-4, designed for Reinforcement Learning experiments.

## Installation

```bash
uv sync
```

For local development and tests, install the dev group too:

```bash
uv sync --group dev
```

The project now ships with explicit console entry points:

- `connect4-play`
- `connect4-train-qlearning`
- `connect4-train-dqn`

## Play

```bash
uv run connect4-play
```

Select an opponent and play as Player 1 or 2. Press 1-7 to choose a column.

## Benchmark

```bash
uv run python benchmark.py
```

Run agents against each other to compare performance. Select two agents and number of games (default 1000).

## Train Q-Learning Agent

```bash
uv run connect4-train-qlearning
```

This runs tabular Q-learning training and saves a Q-table to `models/qtable.pkl.gz` by default.

Common options:

```bash
uv run connect4-train-qlearning \
  --episodes 500000 \
  --alpha 0.1 \
  --gamma 0.95 \
  --epsilon-start 1.0 \
  --epsilon-end 0.05 \
  --opponent self \
  --draw-reward 0.5
```

- `--opponent`: `self`, `random`, `heuristic`, or `minimax`
- `--load`: resume from an existing Q-table checkpoint
- `--eval-interval` and `--eval-games`: periodic greedy-policy evaluation
- `--save-interval`: periodic checkpoint writes

## Train DQN Agent

```bash
uv run connect4-train-dqn
```

This trains a Deep Q-Network with experience replay and a target network, then
saves a checkpoint to `models/dqn_model.pt` by default.

Common options:

```bash
uv run connect4-train-dqn \
  --episodes 150000 \
  --opponent self \
  --eval-interval 10000 \
  --save-interval 25000
```

- `--device`: torch device to use for training
- `--hidden-sizes`: hidden layer sizes for the MLP Q-network
- `--batch-size` and `--replay-capacity`: replay buffer and optimizer scale
- `--load`: resume from an existing DQN checkpoint

The DQN CLI chooses hardware-aware defaults at startup. On CUDA machines it
uses a larger replay batch and a deeper MLP; on CPU it falls back to a smaller
profile automatically.

### Q-Learning Algorithm

The trainer uses tabular Q-learning with epsilon-greedy exploration and
horizontal mirror canonicalization.

- **State key**: `game.get_state()` (current-player perspective) is converted to bytes.
- **Symmetry sharing**: board and horizontally mirrored board map to one canonical key.
- **Action mapping**: Q-values are stored in canonical action space and remapped when needed.
- **Defaults**: unseen `(state, action)` values are treated as `0.0`.

Per-player update flow in `training/qlearning/episode_runner.py`:

1. Select action using epsilon-greedy policy over valid canonical actions.
2. Store pending `(state, action)` for that player.
3. On that player's next turn, bootstrap with TD(0):
   `Q(s,a) <- Q(s,a) + alpha * (gamma * max_a' Q(s',a') - Q(s,a))`
4. At terminal state, apply reward-only update to pending move:
   - win `+1.0`, draw `draw_reward`, loss `-1.0`
   - `Q(s,a) <- Q(s,a) + alpha * (reward - Q(s,a))`

## Usage

```python
from connect4 import Connect4

game = Connect4()

# Play moves (columns 0-6)
game.play(3)
game.play(4)

# Check game state
print(game.current_player)  # 1 or -1
print(game.get_valid_moves())  # [0, 1, 2, 3, 4, 5, 6]
print(game.is_game_over)  # False
print(game.winner)  # None, 1, or -1

# Get board state for neural networks
state = game.get_board()  # 6x7 numpy array
flat = game.get_state_flat()  # 42-element array

# Print board
print(game)
```

## Agents

```python
from connect4 import Connect4
from agents import DQNAgent, MinimaxAgent, QLearningAgent, RandomAgent

game = Connect4()
agent = MinimaxAgent(depth=4)

while not game.is_game_over:
    move = agent.select_move(game)
    game.play(move)
```

## Testing

```bash
uv sync --group dev
uv run pytest tests/ -v
```

## Project Structure

```
pyproject.toml          # uv project metadata, dependencies, and console scripts
uv.lock                 # Locked dependency graph for reproducible installs

connect4/               # Game engine
├── cli/
│   ├── __init__.py
│   └── play.py
├── constants.py
├── board.py
├── win_checker.py
└── game.py

agents/                 # Move selection algorithms
├── random_agent.py
├── heuristic_agent.py
├── minimax_agent.py
├── dqn_agent.py
└── qlearning_agent.py

training/               # Agent training modules
├── train_qlearning.py
├── train_dqn.py
├── qlearning/
│   ├── __init__.py
│   ├── config.py
│   ├── episode_runner.py
│   ├── evaluator.py
│   ├── opponents.py
│   ├── persistence.py
│   ├── policy.py
│   ├── q_values.py
│   ├── types.py
│   └── training_loop.py
└── dqn/
    ├── __init__.py
    ├── checkpoint.py
    ├── config.py
    ├── episode_runner.py
    ├── evaluator.py
    ├── hardware.py
    ├── network.py
    ├── optimization.py
    ├── opponents.py
    ├── policy.py
    ├── replay_buffer.py
    ├── training_loop.py
    └── types.py

play.py                 # Local wrapper for the packaged game CLI
benchmark.py            # Parallelized agent-vs-agent benchmark CLI
```

## Architecture Diagrams

Mermaid diagrams for the engine, agents, and CLI scripts live in `doc/ai/README.md`.
