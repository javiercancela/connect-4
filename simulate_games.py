from simulator import Simulator
import pickle
import pandas as pd


simulator = Simulator()
simulator.run(4)
df = pd.DataFrame(simulator.get_all_states(), columns=['state', 'move', 'result'])
df.to_parquet("connet4.parquet", index=False)
