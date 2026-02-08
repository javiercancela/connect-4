import sys
from connect4 import Connect4, PLAYER_1, PLAYER_2
from agents import RandomAgent, HeuristicAgent, MinimaxAgent


AGENTS = {
    "1": ("Random", RandomAgent),
    "2": ("Heuristic", HeuristicAgent),
    "3": ("Minimax", MinimaxAgent),
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


def clear_screen():
    print("\033[2J\033[H", end="")


def get_agent_choice():
    print("Select opponent:\n")
    for key, (name, _) in AGENTS.items():
        print(f"  {key}. {name}")
    print()

    while True:
        choice = input("Enter choice: ").strip()
        if choice in AGENTS:
            _, agent_class = AGENTS[choice]
            if agent_class is MinimaxAgent:
                depth = get_minimax_depth()
                return agent_class(depth=depth)
            return agent_class()
        print("Invalid choice. Try again.")


def get_player_choice():
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

            print(f"Column {key} is not available. Valid: {[m + 1 for m in valid_moves]}")
        except ValueError:
            print("Enter a number 1-7.")


def display_game(game: Connect4, human_player: int):
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


def play_game(agent, human_player: int):
    game = Connect4()

    while not game.is_game_over:
        display_game(game, human_player)

        if game.current_player == human_player:
            move = get_human_move(game)
        else:
            move = agent.select_move(game)

        game.play(move)

    display_game(game, human_player)


def main():
    clear_screen()
    print("Connect-4\n")

    agent = get_agent_choice()
    human_player = get_player_choice()

    play_game(agent, human_player)

    print("\nThanks for playing!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
