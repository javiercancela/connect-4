# Connect-4 Game Engine

A pure Python game engine for Connect-4, designed for Reinforcement Learning experiments.

## Installation

```bash
pip install numpy
```

## Play

```bash
python play.py
```

Select an opponent and play as Player 1 or 2. Press 1-7 to choose a column.

## Benchmark

```bash
python benchmark.py
```

Run agents against each other to compare performance. Select two agents and number of games (default 1000).

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
from agents import RandomAgent, MinimaxAgent

game = Connect4()
agent = MinimaxAgent(depth=4)

while not game.is_game_over:
    move = agent.select_move(game)
    game.play(move)
```

## Testing

```bash
pip install pytest
pytest tests/ -v
```

## Project Structure

```
connect4/               # Game engine
├── constants.py
├── board.py
├── win_checker.py
└── game.py

agents/                 # Move selection algorithms
├── random_agent.py
├── heuristic_agent.py
└── minimax_agent.py
```

## Architecture Diagrams

Mermaid diagrams for the engine, agents, and CLI scripts live in `doc/ai/README.md`.
