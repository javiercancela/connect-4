import time
from model_testing.dqn_vs_random import TestDQNRandom
from model_testing.random_vs_random import TestRandomRandom


test_dn01 = TestDQNRandom()
test_random = TestRandomRandom()
model_dqn1_won = 0
model_random_won = 0
start_time = time.time()
for i in range(100000):
    test_dn01.play_game()
    if test_dn01.get_winner() == 1:
        model_dqn1_won += 1
    test_random.play_game()
    if test_random.get_winner() == 1:
        model_random_won += 1
    if (i + 1) % 1000 == 0:
        elapsed = time.time() - start_time
        print(f"Completed {i + 1} games in {elapsed:.2f} seconds")

print(f"Model dqn01 won {model_dqn1_won} out of 100000 games.")
print(f"Model random won {model_random_won} out of 100000 games.")
