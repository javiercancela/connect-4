import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from connect4 import Connect4, PLAYER_1, PLAYER_2
from agents import DQNAgent, HeuristicAgent, MinimaxAgent, QLearningAgent, RandomAgent


AGENTS = {
    "1": ("Random", "random"),
    "2": ("Heuristic", "heuristic"),
    "3": ("Minimax", "minimax"),
    "4": ("Q-Learning", "qlearning"),
    "5": ("DQN", "dqn"),
}


def get_minimax_depth(agent_label: str) -> int:
    while True:
        try:
            value = input(f"{agent_label} minimax depth [4]: ").strip()
            if value == "":
                return 4
            depth = int(value)
            if depth > 0:
                return depth
            print("Depth must be positive.")
        except ValueError:
            print("Enter a valid number.")


def get_qtable_path(agent_label: str) -> str:
    default = "models/qtable.pkl.gz"
    while True:
        path = input(f"{agent_label} Q-table path [{default}]: ").strip()
        if path == "":
            path = default
        if os.path.exists(path):
            return path
        print(f"File not found: {path}")
        print("Train a model first with: uv run connect4-train-qlearning")


def get_dqn_checkpoint_path(agent_label: str) -> str:
    default = "models/dqn_model.pt"
    while True:
        path = input(f"{agent_label} DQN checkpoint path [{default}]: ").strip()
        if path == "":
            path = default
        if os.path.exists(path):
            return path
        print(f"File not found: {path}")
        print("Train a model first with: uv run connect4-train-dqn")


def get_agent_choice(prompt: str):
    print(f"{prompt}\n")
    for key, (name, _) in AGENTS.items():
        print(f"  {key}. {name}")
    print()

    while True:
        choice = input("Enter choice: ").strip()
        if choice in AGENTS:
            name, agent_key = AGENTS[choice]
            if agent_key == "minimax":
                depth = get_minimax_depth(prompt.strip(":"))
                return f"{name}(d={depth})", (agent_key, depth)
            if agent_key == "qlearning":
                path = get_qtable_path(prompt.strip(":"))
                return name, (agent_key, path)
            if agent_key == "dqn":
                path = get_dqn_checkpoint_path(prompt.strip(":"))
                return name, (agent_key, path)
            return name, (agent_key, None)
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


def get_num_workers() -> int:
    default_workers = os.cpu_count() or 1

    while True:
        try:
            value = input(f"Workers [{default_workers}]: ").strip()
            if value == "":
                return default_workers
            workers = int(value)
            if workers > 0:
                return workers
            print("Must be positive.")
        except ValueError:
            print("Enter a valid number.")


def _build_agent(agent_config):
    agent_key, param = agent_config

    if agent_key == "random":
        return RandomAgent()
    if agent_key == "heuristic":
        return HeuristicAgent()
    if agent_key == "minimax":
        return MinimaxAgent(depth=param or 4)
    if agent_key == "qlearning":
        return QLearningAgent(qtable_path=param or "models/qtable.pkl.gz")
    if agent_key == "dqn":
        return DQNAgent(checkpoint_path=param or "models/dqn_model.pt")

    raise ValueError(f"Unknown agent key: {agent_key}")


def play_game(agent1_config, agent2_config) -> int:
    game = Connect4()
    agents = {PLAYER_1: _build_agent(agent1_config), PLAYER_2: _build_agent(agent2_config)}

    while not game.is_game_over:
        agent = agents[game.current_player]
        move = agent.select_move(game)
        game.play(move)

    return game.winner


def _play_batch(agent1_config, agent2_config, batch_size: int) -> dict:
    batch_results = {PLAYER_1: 0, PLAYER_2: 0, None: 0}

    for _ in range(batch_size):
        winner = play_game(agent1_config, agent2_config)
        batch_results[winner] += 1

    return batch_results


def _merge_results(results: dict, batch_results: dict):
    results[PLAYER_1] += batch_results[PLAYER_1]
    results[PLAYER_2] += batch_results[PLAYER_2]
    results[None] += batch_results[None]


def run_benchmark(agent1_config, agent2_config, num_games: int, num_workers: int) -> dict:
    results = {PLAYER_1: 0, PLAYER_2: 0, None: 0}
    progress_step = 100
    completed = 0

    if num_workers == 1:
        batch_results = _play_batch(agent1_config, agent2_config, num_games)
        _merge_results(results, batch_results)
        print(f"  {num_games}/{num_games} games completed")
        return results

    worker_count = min(num_workers, num_games)
    task_count = min(worker_count * 4, num_games)
    batch_sizes = [num_games // task_count] * task_count
    for i in range(num_games % task_count):
        batch_sizes[i] += 1

    try:
        with ProcessPoolExecutor(max_workers=worker_count) as executor:
            future_to_batch_size = {
                executor.submit(_play_batch, agent1_config, agent2_config, batch_size): batch_size
                for batch_size in batch_sizes
            }

            for future in as_completed(future_to_batch_size):
                batch_results = future.result()
                _merge_results(results, batch_results)
                completed += future_to_batch_size[future]

                if completed % progress_step == 0 or completed == num_games:
                    print(f"  {completed}/{num_games} games completed")
    except (PermissionError, OSError):
        # Some restricted environments disallow multiprocessing semaphores.
        print("  Process workers unavailable in this environment, falling back to single worker.")
        batch_results = _play_batch(agent1_config, agent2_config, num_games)
        _merge_results(results, batch_results)
        print(f"  {num_games}/{num_games} games completed")

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
    num_workers = get_num_workers()

    print(f"\nRunning {num_games} games on {num_workers} workers: {name1} vs {name2}\n")

    results = run_benchmark(agent1, agent2, num_games, num_workers)
    print_results(name1, name2, results, num_games)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBenchmark cancelled.")
        sys.exit(0)
