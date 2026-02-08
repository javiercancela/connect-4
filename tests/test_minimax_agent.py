from connect4 import Connect4
from agents import MinimaxAgent


class TestMinimaxAgent:
    def test_select_move_returns_valid_column(self):
        game = Connect4()
        agent = MinimaxAgent(depth=2)

        move = agent.select_move(game)

        assert move in game.get_valid_moves()

    def test_select_move_prefers_center_on_empty_board(self):
        game = Connect4()
        agent = MinimaxAgent(depth=2)

        move = agent.select_move(game)

        assert move == 3

    def test_select_move_takes_immediate_winning_move(self):
        game = Connect4()
        agent = MinimaxAgent(depth=3)

        game.play(0)
        game.play(6)
        game.play(1)
        game.play(6)
        game.play(2)
        game.play(5)

        move = agent.select_move(game)

        assert move == 3

    def test_select_move_blocks_opponent_immediate_win(self):
        game = Connect4()
        agent = MinimaxAgent(depth=3)

        game.play(0)
        game.play(6)
        game.play(1)
        game.play(5)
        game.play(2)

        move = agent.select_move(game)

        assert move == 3
