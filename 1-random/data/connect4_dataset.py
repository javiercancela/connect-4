from torch.utils.data import Dataset
import pandas as pd


class Connect4Dataset(Dataset):
    
    FILENAME = str(__file__).replace("connect4_dataset.py", "connect4.parquet")


    def __init__(self):
        df = pd.read_parquet(self.FILENAME)
        self.states = df["state"].values
        self.actions = df["move"].values
        self.rewards = df["score"].values

    def __len__(self):
        return len(self.states)

    def __getitem__(self, idx):
        return self.states[idx], self.actions[idx], self.rewards[idx]
