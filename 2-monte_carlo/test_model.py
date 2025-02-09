import time
from model_testing.monte_carlo_vs_random import TestMCRandom

TOTAL_GAMES = 1000

test_mc = TestMCRandom()
model_mc_won = 0
model_random_won = 0
for i in range(TOTAL_GAMES):
    start_time = time.time()
    test_mc.play_game()
    if test_mc.get_winner() == 1:
        model_mc_won += 1
    elif test_mc.get_winner() == 2:
        model_random_won += 1
    elapsed = time.time() - start_time
    if (i + 1) % 10 == 0:
        print(f"Model Monte Carlo won {model_mc_won} out of {i + 1} games.")
        print(f"Model random won {model_random_won} out of {i + 1} games.")
        print("======================================================")
