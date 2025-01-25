from data.connect4_dataset import Connect4Dataset
from data.simulator import Simulator
import pickle
import pandas as pd


simulator = Simulator()
simulator.run(100000)
print(simulator.get_results())
all_moves = []
for game_info in simulator.get_all_games_info():
    for state, move, score in game_info:
        all_moves.append({"state": state, "move": move, "score": score})
df = pd.DataFrame(all_moves)
df.to_parquet(Connect4Dataset.FILENAME, index=False)
