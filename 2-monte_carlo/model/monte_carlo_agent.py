import numpy as np
from collections import defaultdict
from game_engine.game import Game


class MonteCarloAgent:
    """
    Monte Carlo agent that learns to play Connect-4 through experience.
    Uses Monte Carlo methods to estimate state values and epsilon-greedy exploration.
    """
    def __init__(self, player_id, epsilon=0.1):
        self.player_id = player_id
        # Epsilon determines the exploration rate: higher epsilon = more random moves
        self.epsilon = epsilon
        # Maps states to their estimated values based on observed returns
        self.value_function = defaultdict(float)
        # Stores all returns observed for each state for averaging
        self.returns = defaultdict(list)
        # Tracks states visited in current game episode
        self.state_history = []

    def get_state_key(self, board_state):
        """Convert board state to a hashable tuple for dictionary storage"""
        return tuple(board_state)

    def choose_action(self, game):
        """
        Select action using epsilon-greedy strategy:
        - With probability epsilon: choose random action (exploration)
        - With probability 1-epsilon: choose best known action (exploitation)
        """
        valid_moves = game.get_valid_moves()

        # Exploration: Random move
        if np.random.random() < self.epsilon:
            return np.random.choice(valid_moves)

        # Exploitation: Initializing values for trying to find the best move
        best_value = float("-inf")
        best_moves = []

        # Evaluate each possible next state
        for move in valid_moves:
            # Simulate move to see resulting state
            game_copy = self._copy_game(game)
            game_copy.make_move(move)
            next_state = self.get_state_key(game_copy.board.get_board_state())
            state_value = self.value_function[next_state]

            # Track moves that lead to best states
            if state_value > best_value:
                best_value = state_value
                best_moves = [move]
            elif state_value == best_value:
                best_moves.append(move)

        # Randomly choose among best moves to break ties
        return np.random.choice(best_moves)

    def record_state(self, game):
        """Store current state in episode history for later learning"""
        state = self.get_state_key(game.board.get_board_state())
        self.state_history.append(state)

    def update_value_function(self, reward):
        """
        Monte Carlo update of value function:
        - Uses observed final reward to update all state values
        - Each state's value becomes average of all returns seen from that state
        """
        G = reward  # The final reward/return

        # Update each state's value based on the final reward
        for state in reversed(self.state_history):
            # Store the return for this state
            self.returns[state].append(G)
            # Update state value to be average of all returns
            self.value_function[state] = np.mean(self.returns[state])

        # Clear episode history for next game
        self.state_history = []

