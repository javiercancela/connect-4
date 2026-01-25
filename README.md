# Connect-4 Game Engine

A pure Python game engine for Connect-4, designed for Reinforcement Learning experiments.

## Installation

```bash
pip install numpy
```

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

## Testing

```bash
pip install pytest
pytest tests/ -v
```

## Project Structure

```
connect4/
├── constants.py     # Game constants
├── board.py         # Board state management
├── win_checker.py   # Win detection
└── game.py          # Game orchestration
```
