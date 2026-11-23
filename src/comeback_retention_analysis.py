
import pandas as pd

# 1. Load datasets
df = pd.read_csv("outputs/cleaned_chart_data.csv")
events = pd.read_csv("outputs/song_entry_exit_events.csv")

# 2. Convert dates
df["date"] = pd.to_datetime(df["date"])
events["date"] = pd.to_datetime(events["date"])

# 3. Sort chart data
df = df.sort_values(["song_artist_key", "date"])

# 4. Select confirmed re-entry events
reentries = events[
    events["event"] == "Confirmed Re-entry"
].copy()

# 5. Calculate retention for every comeback
retention_results = []

for _, event in reentries.iterrows():

    song_key = event["song_artist_key"]
    comeback_date = event["date"]

    # Find this song's chart records from comeback date onward
    song_data = df[
        (df["song_artist_key"] == song_key) &
        (df["date"] >= comeback_date)
    ].sort_values("date")

    # Count consecutive calendar days
    retention_days = 0
    expected_date = comeback_date

    for chart_date in song_data["date"].drop_duplicates():

        if chart_date == expected_date:
            retention_days += 1
            expected_date += pd.Timedelta(days=1)
        else:
            break

    # Store the result INSIDE the main loop
    retention_results.append({
        "song_artist_key": song_key,
        "comeback_date": comeback_date,
        "previous_rank": event["previous_rank"],
        "comeback_rank": event["current_rank"],
        "retention_days": retention_days
    })

# 6. Create retention DataFrame
retention = pd.DataFrame(retention_results)

# 7. Add song and artist details
song_details = (
    df.groupby("song_artist_key")
    .agg(
        song=("song", "first"),
        artist=("artist", "first")
    )
    .reset_index()
)

retention = retention.merge(
    song_details,
    on="song_artist_key",
    how="left"
)

# 8. Save event-wise retention
retention.to_csv(
    "outputs/comeback_retention_events.csv",
    index=False
)

# 9. Calculate song-wise retention
song_retention = (
    retention.groupby(["song_artist_key", "song", "artist"])
    .agg(
        total_comebacks=("retention_days", "count"),
        average_retention_days=("retention_days", "mean"),
        maximum_retention_days=("retention_days", "max")
    )
    .reset_index()
)

song_retention["average_retention_days"] = (
    song_retention["average_retention_days"].round(2)
)

song_retention = song_retention.sort_values(
    ["average_retention_days", "total_comebacks"],
    ascending=[False, False]
)

# 10. Save song-wise retention
song_retention.to_csv(
    "outputs/song_comeback_retention.csv",
    index=False
)

# 11. Display results
print("\n========== COMEBACK RETENTION ANALYSIS ==========")

print("\nTotal comeback events available:")
print(len(reentries))

print("\nTotal comeback events analysed:")
print(len(retention))

print("\nAverage retention across all comeback events:")
print(round(retention["retention_days"].mean(), 2), "days")

print("\nTop 15 songs by average comeback retention:")
print(
    song_retention[
        [
            "song",
            "artist",
            "total_comebacks",
            "average_retention_days",
            "maximum_retention_days"
        ]
    ].head(15).to_string(index=False)
)

print("\nLongest individual comeback retention:")
print(
    retention.sort_values(
        "retention_days",
        ascending=False
    )[
        [
            "song",
            "artist",
            "comeback_date",
            "retention_days"
        ]
    ].head(10).to_string(index=False)
)

print("\nFiles saved:")
print("1. outputs/comeback_retention_events.csv")
print("2. outputs/song_comeback_retention.csv")

print("\n========== ANALYSIS COMPLETED ==========")
