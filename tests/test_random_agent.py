from connect4 import Connect4
from agents import RandomAgent


class TestRandomAgent:
    def test_select_move_returns_valid_column(self):
        game = Connect4()
        agent = RandomAgent()

        move = agent.select_move(game)

        assert move in game.get_valid_moves()

    def test_select_move_works_with_limited_options(self):
        game = Connect4()
        agent = RandomAgent()

        for col in range(6):
            game._board._grid[:, col] = 1

        move = agent.select_move(game)

        assert move == 6

    def test_plays_full_game(self):
        game = Connect4()
        agent = RandomAgent()

        while not game.is_game_over:
            move = agent.select_move(game)
            game.play(move)

        assert game.is_game_over
