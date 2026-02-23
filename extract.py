import pandas as pd

def extract():
    df = pd.read_csv("energy_consumption_dataset.csv")
    df.columns = df.columns.str.strip()
    return df
