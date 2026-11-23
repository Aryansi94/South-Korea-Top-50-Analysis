
import pandas as pd

file_path = "outputs/cleaned_chart_data.csv"

df = pd.read_csv(file_path)

df["date"] = pd.to_datetime(df["date"])

print("\n========== CLEANED DATASET VERIFICATION ==========")

print("\nDataset Shape:")
print(df.shape)

print("\nDate Range:")
print("Start:", df["date"].min())
print("End:", df["date"].max())

print("\nUnique Chart Dates:")
print(df["date"].nunique())

print("\nRecords Per Date:")
print(df.groupby("date").size().value_counts().sort_index())

print("\nIs 1 March 2025 Present?")
print((df["date"] == "2025-03-01").any())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nSong-Artist Key Available?")
print("song_artist_key" in df.columns)

print("\nDuration in Minutes Available?")
print("duration_min" in df.columns)

print("\n========== VERIFICATION COMPLETED ==========")
