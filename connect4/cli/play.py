import os
import sys

from agents import DQNAgent, HeuristicAgent, MinimaxAgent, QLearningAgent, RandomAgent
from connect4 import Connect4, PLAYER_1, PLAYER_2


AGENTS = {
    "1": ("Random", "random"),
    "2": ("Heuristic", "heuristic"),
    "3": ("Minimax", "minimax"),
    "4": ("Q-Learning", "qlearning"),
    "5": ("DQN", "dqn"),
}


def get_minimax_depth() -> int:
    while True:
        try:
            value = input("Minimax depth [4]: ").strip()
            if value == "":
                return 4
            depth = int(value)
            if depth > 0:
                return depth
            print("Depth must be positive.")
        except ValueError:
            print("Enter a valid number.")


def get_qtable_path() -> str:
    default = "models/qtable.pkl.gz"
    path = input(f"Q-table path [{default}]: ").strip()
    if path == "":
        return default
    return path


def get_dqn_checkpoint_path() -> str:
    default = "models/dqn_model.pt"
    path = input(f"DQN checkpoint path [{default}]: ").strip()
    if path == "":
        return default
    return path


def clear_screen() -> None:
    print("\033[2J\033[H", end="")


def get_agent_choice():
    print("Select opponent:\n")
    for key, (name, _) in AGENTS.items():
        print(f"  {key}. {name}")
    print()

    while True:
        choice = input("Enter choice: ").strip()
        if choice in AGENTS:
            _, agent_key = AGENTS[choice]
            if agent_key == "minimax":
                depth = get_minimax_depth()
                return MinimaxAgent(depth=depth)
            if agent_key == "qlearning":
                path = get_qtable_path()
                if not os.path.exists(path):
                    print(f"File not found: {path}")
                    print("Train a model first with: uv run connect4-train-qlearning")
                    continue
                return QLearningAgent(qtable_path=path)
            if agent_key == "dqn":
                path = get_dqn_checkpoint_path()
                if not os.path.exists(path):
                    print(f"File not found: {path}")
                    print("Train a model first with: uv run connect4-train-dqn")
                    continue
                return DQNAgent(checkpoint_path=path)
            if agent_key == "random":
                return RandomAgent()
            return HeuristicAgent()
        print("Invalid choice. Try again.")


def get_player_choice() -> int:
    print("\nPlay as:\n")
    print("  1. Player 1 (X) - plays first")
    print("  2. Player 2 (O) - plays second")
    print()

    while True:
        choice = input("Enter choice: ").strip()
        if choice == "1":
            return PLAYER_1
        if choice == "2":
            return PLAYER_2
        print("Invalid choice. Try again.")


def get_human_move(game: Connect4) -> int:
    valid_moves = game.get_valid_moves()

    while True:
        try:
            key = input("Your move (1-7): ").strip()
            column = int(key) - 1

            if column in valid_moves:
                return column

            print(f"Column {key} is not available. Valid: {[move + 1 for move in valid_moves]}")
        except ValueError:
            print("Enter a number 1-7.")


def display_game(game: Connect4, human_player: int) -> None:
    clear_screen()
    print("Connect-4\n")
    print(game)
    print()

    if game.is_game_over:
        if game.winner == human_player:
            print("You win!")
        elif game.winner is not None:
            print("You lose!")
        else:
            print("Draw!")
    elif game.current_player == human_player:
        print("Your turn")
    else:
        print("Opponent thinking...")


def play_game(agent, human_player: int) -> None:
    game = Connect4()

    while not game.is_game_over:
        display_game(game, human_player)

        if game.current_player == human_player:
            move = get_human_move(game)
        else:
            move = agent.select_move(game)

        game.play(move)

    display_game(game, human_player)


def main() -> None:
    clear_screen()
    print("Connect-4\n")

    agent = get_agent_choice()
    human_player = get_player_choice()

    play_game(agent, human_player)

    print("\nThanks for playing!")


def run() -> None:
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
