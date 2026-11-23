
import pandas as pd

# Load datasets
df = pd.read_csv("outputs/cleaned_chart_data.csv")
events = pd.read_csv("outputs/song_entry_exit_events.csv")

# Convert dates
df["date"] = pd.to_datetime(df["date"])
events["date"] = pd.to_datetime(events["date"])

# Select confirmed re-entries
reentries = events[
    events["event"] == "Confirmed Re-entry"
].copy()

print("\n========== RETENTION DATA DIAGNOSTIC ==========")

print("\nTotal chart records:")
print(len(df))

print("\nTotal confirmed re-entry events:")
print(len(reentries))

print("\nEvent file columns:")
print(events.columns.tolist())

print("\nFirst 10 re-entry events:")
print(
    reentries[
        ["song_artist_key", "date", "previous_rank"]
    ].head(10).to_string(index=False)
)

print("\nNumber of unique songs in re-entry events:")
print(reentries["song_artist_key"].nunique())

print("\nFirst 10 chart dates:")
print(sorted(df["date"].drop_duplicates())[:10])

print("\nLast 10 chart dates:")
print(sorted(df["date"].drop_duplicates())[-10:])

print("\n========== DIAGNOSTIC COMPLETED ==========")
