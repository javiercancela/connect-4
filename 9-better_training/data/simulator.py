import random
import time
from game_engine.game import Game


class Simulator:
    def __init__(self):
        self.results = {1: 0, 2: 0, 0: 0}
        self.all_games_info = []

    def run(self, total_games):
        for i in range(total_games):
            if i % 1000 == 0:
                print(
                    f"{time.strftime('%H:%M:%S')}: Playing {i} games of {total_games}"
                )
            self.play_game()

    def play_game(self):
        game = Game()
        while game.get_winner() is None:
            threats = game.get_threats()
            player = game.get_turn()
            other_player = 1 if player == 2 else 2
            if len(threats[player]["checks"]) > 0:
                move = threats[player]["checks"][0][1]
            elif len(threats[other_player]["checks"]) > 0:
                move = threats[other_player]["checks"][0][1]
            else:
                valid_moves = game.get_valid_moves()
                move = random.choice(valid_moves)
            game.make_move(move)

        self.results[game.get_winner()] += 1
        self.all_games_info.append(game.get_game_info())

    def play_random_game(self):
        game = Game()
        while game.get_winner() is None:
            valid_moves = game.get_valid_moves()
            move = random.choice(valid_moves)
            game.make_move(move)

        self.results[game.get_winner()] += 1
        self.all_games_info.append(game.get_game_info())

    def get_all_games_info(self):
        return self.all_games_info

    def get_results(self):
        return self.results
