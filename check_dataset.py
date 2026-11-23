import pandas as pd
import os

file_path = "dataset/Atlantic_South_Korea.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)

    print("\nDATASET LOADED SUCCESSFULLY!")

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nFirst 5 Records:")
    print(df.head())

    print("\nDataset Information:")
    df.info()

else:
    print("ERROR: Dataset file not found!")