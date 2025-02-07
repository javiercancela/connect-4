from game_engine.game import Game
from model.monte_carlo_agent import MonteCarloAgent


def play_episode(agent1, agent2, game):
    """
    Simulate one complete game episode between two agents.
    Used for training agents through experience.
    """
    while game.get_winner() is None:
        # Determine current player
        current_agent = agent1 if game.get_turn() == agent1.player_id else agent2

        # Record state for learning
        current_agent.record_state(game)

        # Make move
        move = current_agent.choose_action(game)
        game.make_move(move)

    # Calculate rewards based on game outcome
    winner = game.get_winner()
    # Draw gives partial reward to both
    if winner == 0:
        reward1, reward2 = 0.5, 0.5
    else:
        # Winner gets 1.0, loser gets 0.0
        reward1 = 1.0 if winner == agent1.player_id else 0.0
        reward2 = 1.0 if winner == agent2.player_id else 0.0

    # Update both agents' value functions based on game outcome
    agent1.update_value_function(reward1)
    agent2.update_value_function(reward2)

    return winner


def train_agents(num_episodes=10000):
    """
    Train two Monte Carlo agents by playing them against each other.
    Agents learn from experience through repeated game episodes.
    """
    agent1 = MonteCarloAgent(player_id=1)
    agent2 = MonteCarloAgent(player_id=2)
    result = 0

    # Play multiple episodes and learn from each
    for episode in range(num_episodes):
        game = Game()
        winner = play_episode(agent1, agent2, game)
        if winner == 1:
            result += 1
        elif winner == 2:
            result -= 1

        # Progress monitoring
        if episode % 100 == 0:
            print(f"Episode {episode}, Winner: {winner}")

    return agent1, agent2, result


if __name__ == "__main__":
    agent1, agent2, result = train_agents()
    print(f"Result: {result}")
    if result >= 0:
        agent1.save_value_function()    
    else:
        agent2.save_value_function()

