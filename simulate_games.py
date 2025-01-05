from data.connect4_dataset import Connect4Dataset
from data.simulator import Simulator
import pickle
import pandas as pd


simulator = Simulator()
simulator.run(100000)
print(simulator.get_results_distribution())
df = pd.DataFrame(simulator.get_all_states(), columns=['state', 'move', 'result'])
df.to_parquet(Connect4Dataset.FILENAME, index=False)
