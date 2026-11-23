
import pandas as pd

# 1. Load datasets
df = pd.read_csv("outputs/cleaned_chart_data.csv")
events = pd.read_csv("outputs/song_entry_exit_events.csv")

df["date"] = pd.to_datetime(df["date"])
events["date"] = pd.to_datetime(events["date"])

# 2. Select confirmed re-entry events
reentries = events[
    events["event"] == "Confirmed Re-entry"
].copy()

# 3. Get song and artist information
song_details = (
    df.groupby("song_artist_key")
    .agg(
        song=("song", "first"),
        artist=("artist", "first")
    )
    .reset_index()
)

# 4. Calculate re-entry frequency
frequency = (
    reentries.groupby("song_artist_key")
    .agg(
        reentry_count=("event", "count"),
        first_comeback=("date", "min"),
        last_comeback=("date", "max"),
        average_rank_change=("rank_change", "mean")
    )
    .reset_index()
)

# 5. Merge song details
frequency = frequency.merge(
    song_details,
    on="song_artist_key",
    how="left"
)

# 6. Calculate rank improvement percentage
frequency["average_rank_change"] = (
    frequency["average_rank_change"].round(2)
)

# 7. Sort by re-entry frequency
frequency = frequency.sort_values(
    ["reentry_count", "average_rank_change"],
    ascending=[False, False]
)

# 8. Save results
frequency.to_csv(
    "outputs/song_comeback_frequency.csv",
    index=False
)

# 9. Artist-wise comeback frequency
artist_frequency = (
    frequency.groupby("artist")
    .agg(
        unique_comeback_songs=("song_artist_key", "nunique"),
        total_reentries=("reentry_count", "sum")
    )
    .reset_index()
    .sort_values(
        "total_reentries",
        ascending=False
    )
)

artist_frequency.to_csv(
    "outputs/artist_comeback_frequency.csv",
    index=False
)

# 10. Display results
print("\n========== SONG COMEBACK FREQUENCY ==========")

print("\nTotal songs with confirmed re-entries:")
print(len(frequency))

print("\nTop 15 Comeback Songs:")
print(
    frequency[
        [
            "song",
            "artist",
            "reentry_count",
            "average_rank_change"
        ]
    ].head(15).to_string(index=False)
)

print("\nTop 10 Artists by Total Re-entries:")
print(
    artist_frequency.head(10).to_string(index=False)
)

print("\nTotal confirmed re-entry events:")
print(frequency["reentry_count"].sum())

print("\nFiles saved:")
print("1. outputs/song_comeback_frequency.csv")
print("2. outputs/artist_comeback_frequency.csv")

print("\n========== ANALYSIS COMPLETED ==========")
