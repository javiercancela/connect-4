import time
from model_testing.random_vs_random import TestRandomRandom

TOTAL_GAMES = 100000

test_random = TestRandomRandom()
model_player1_won = 0
model_player2_won = 0
start_time = time.time()
for i in range(TOTAL_GAMES):
    test_random.play_game()
    if test_random.get_winner() == 1:
        model_player1_won += 1
    elif test_random.get_winner() == 2:
        model_player2_won += 1
    if (i + 1) % 1000 == 0:
        elapsed = time.time() - start_time
        print(f"Completed {i + 1} games in {elapsed:.2f} seconds")

print(f"Model dqn01 won {model_player1_won} out of {TOTAL_GAMES} games.")
print(f"Model random won {model_player2_won} out of {TOTAL_GAMES} games.")
