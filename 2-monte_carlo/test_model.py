import time
from model_testing.monte_carlo_vs_random import TestMCRandom

TOTAL_GAMES = 100000

test_mc = TestMCRandom()
model_mc_won = 0
model_random_won = 0
start_time = time.time()
for i in range(TOTAL_GAMES):
    test_mc.play_game()
    if test_mc.get_winner() == 1:
        model_mc_won += 1
    elif test_mc.get_winner() == 2:
        model_random_won += 1
    if (i + 1) % 1000 == 0:
        elapsed = time.time() - start_time
        print(f"Completed {i + 1} games in {elapsed:.2f} seconds")

print(f"Model Monte Carlo won {model_mc_won} out of {TOTAL_GAMES} games.")
print(f"Model random won {model_random_won} out of {TOTAL_GAMES} games.")
