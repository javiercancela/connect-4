import numpy as np
from collections import defaultdict
from move_selector import MoveSelector
import json
import copy


class MonteCarloAgent:
    """
    Monte Carlo agent that learns to play Connect-4 through experience.
    Uses Monte Carlo methods to estimate state values and epsilon-greedy exploration.
    """
    def __init__(self, player_id, epsilon=0.1):
        self.player_id = player_id
        self.epsilon = epsilon # Probability of choosing random move
        self.value_function = defaultdict(float) 
        self.returns = defaultdict(list) 
        self.state_history = []
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
            # Simulate the move and get store it if the value is better than the current best
            move_selector.process_move(self._simulate_move(game, move))

        # Randomly choose among best moves to break ties
        return np.random.choice(move_selector.get_best_moves())

    def record_state(self, game):
        """Store current state in episode history for later learning"""
        state = self.get_state_key(game.board.get_board_state())
        self.state_history.append(state)

    def _simulate_move(self, game, move):
        game_copy = copy.deepcopy(game)
        game_copy.make_move(move)
        next_state = self.get_state_key(game_copy.board.get_board_state())
        return self.value_function[next_state]

    def update_value_function(self, reward):

        # Update each state's value based on the final reward
        for state in reversed(self.state_history):
            # Store the return for this state
            self.returns[state].append(reward)
            # Update state value to be average of all returns
            self.value_function[state] = np.mean(self.returns[state])

        # Clear episode history for next game
        self.state_history = []

    def save_value_function(self):
        """
        Save the value function to a JSON file.
        Converts tuple keys to strings for JSON serialization.
        """
        # Convert defaultdict with tuple keys to dict with string keys
        serializable_dict = {
            ','.join(map(str, state)): value 
            for state, value in self.value_function.items()
        }
        
        # Save to file
        with open(self.file_path, 'w') as f:
            json.dump({
                'player_id': self.player_id,
                'epsilon': self.epsilon,
                'value_function': serializable_dict
            }, f)

    def load_value_function(self):
        """
        Load the value function from a JSON file.
        Converts string keys back to tuples.
        """
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            
        # Update agent parameters
        self.player_id = data['player_id']
        self.epsilon = data['epsilon']
        
        # Convert string keys back to tuples and create new defaultdict
        self.value_function = defaultdict(float)
        for state_str, value in data['value_function'].items():
            state_tuple = tuple(map(int, state_str.split(',')))
            self.value_function[state_tuple] = value
            
        # Clear any existing returns and history
        self.returns = defaultdict(list)
        self.state_history = []