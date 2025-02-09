import numpy as np
from collections import defaultdict
from .move_selector import MoveSelector
import copy


class MonteCarloAgent:
    """
    Monte Carlo agent that learns to play Connect-4 through experience.
    Uses Monte Carlo methods to estimate state values and epsilon-greedy exploration.
    """
    def __init__(self, player_id, epsilon=0.1, simulation_count=100, discount_factor=0.9):
        self.player_id = player_id
        self.epsilon = epsilon # Probability of choosing random move
        self.value_function = defaultdict(float) 
        self.returns = defaultdict(list) 
        self.state_history = []
        self.simulation_count = simulation_count
        self.discount_factor = discount_factor
        self.file_path = str(__file__).replace("monte_carlo_agent.py", "monte_carlo_value_function.json")


    def get_state_key(self, board_state):
        # Convert array to tuple for use as dictionary key (arrays are not hashable)
        return tuple(board_state)

    def choose_action(self, game):
        valid_moves = game.get_valid_moves()

        # With probability epsilon, choose random move (exploration)
        if np.random.random() < self.epsilon:
            return np.random.choice(valid_moves)

        move_selector = MoveSelector()
        for move in valid_moves:
            simulated_results = []
            for i in range(self.simulation_count):
                simulated_move_value = self._simulate_move(game, move)
                simulated_results.append(simulated_move_value)

            average_value = np.mean(simulated_results)
            move_selector.process_move(average_value, move)

        # Randomly choose among best moves to break ties
        return np.random.choice(move_selector.get_best_moves())

    def record_state(self, game):
        """Store current state in episode history for later learning"""
        state = self.get_state_key(game.board.get_board_state())
        self.state_history.append(state)

    def _simulate_move(self, game, move):
        game_copy = copy.deepcopy(game)
        game_copy.make_move(move)

        while game_copy.get_winner() is None:
            valid_moves = game_copy.get_valid_moves()
            random_move = np.random.choice(valid_moves)
            game_copy.make_move(random_move)
        
        winner = game_copy.get_winner()
        reward = 0.5 if winner == 0 else 1.0 if winner == self.player_id else 0.0
        return reward

    def update_value_function(self, reward):
        """
        We iterate all the states starting from the last one, and we decrease the 
        reward for states further away in the state history.
        """
        discount_reward = reward
        for state in reversed(self.state_history):
            self.returns[state].append(discount_reward)
            # The value of a state is the average of all the rewards 
            # obtained in the different games that passed through that state
            self.value_function[state] = np.mean(self.returns[state])
            discount_reward *= self.discount_factor

        # Clear episode history for next game
        self.state_history = []

