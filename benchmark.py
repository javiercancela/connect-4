import sys
from connect4 import Connect4, PLAYER_1, PLAYER_2
from agents import RandomAgent


AGENTS = {
    "1": ("Random", RandomAgent),
}


def get_agent_choice(prompt: str):
    print(f"{prompt}\n")
    for key, (name, _) in AGENTS.items():
        print(f"  {key}. {name}")
    print()

    while True:
        choice = input("Enter choice: ").strip()
        if choice in AGENTS:
            name, agent_class = AGENTS[choice]
            return name, agent_class()
        print("Invalid choice. Try again.")


def get_num_games() -> int:
    while True:
        try:
            value = input("Number of games [1000]: ").strip()
            if value == "":
                return 1000
            num = int(value)
            if num > 0:
                return num
            print("Must be positive.")
        except ValueError:
            print("Enter a valid number.")


def play_game(agent1, agent2) -> int:
    game = Connect4()
    agents = {PLAYER_1: agent1, PLAYER_2: agent2}

    while not game.is_game_over:
        agent = agents[game.current_player]
        move = agent.select_move(game)
        game.play(move)

    return game.winner


def run_benchmark(agent1, agent2, num_games: int) -> dict:
    results = {PLAYER_1: 0, PLAYER_2: 0, None: 0}

    for i in range(num_games):
        winner = play_game(agent1, agent2)
        results[winner] += 1

        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{num_games} games completed")

    return results


def print_results(name1: str, name2: str, results: dict, num_games: int):
    wins1 = results[PLAYER_1]
    wins2 = results[PLAYER_2]
    draws = results[None]

    pct1 = 100 * wins1 / num_games
    pct2 = 100 * wins2 / num_games
    pct_draw = 100 * draws / num_games

    print("\n" + "=" * 40)
    print("Results")
    print("=" * 40)
    print(f"\n{name1} (Player 1):")
    print(f"  Wins: {wins1:>6} ({pct1:>5.1f}%)")
    print(f"\n{name2} (Player 2):")
    print(f"  Wins: {wins2:>6} ({pct2:>5.1f}%)")
    print(f"\nDraws:   {draws:>6} ({pct_draw:>5.1f}%)")
    print(f"\nTotal:   {num_games:>6} games")
    print("=" * 40)


def main():
    print("Model Benchmark\n")

    name1, agent1 = get_agent_choice("Select Player 1 (X):")
    print()
    name2, agent2 = get_agent_choice("Select Player 2 (O):")
    print()
    num_games = get_num_games()

    print(f"\nRunning {num_games} games: {name1} vs {name2}\n")

    results = run_benchmark(agent1, agent2, num_games)
    print_results(name1, name2, results, num_games)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBenchmark cancelled.")
        sys.exit(0)
