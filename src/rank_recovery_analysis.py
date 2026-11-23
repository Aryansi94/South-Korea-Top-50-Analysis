
import pandas as pd

# 1. Load comeback event data
events = pd.read_csv("outputs/song_entry_exit_events.csv")
df = pd.read_csv("outputs/cleaned_chart_data.csv")

# 2. Select confirmed re-entry events
reentries = events[
    events["event"] == "Confirmed Re-entry"
].copy()

# 3. Calculate rank improvement
# Positive = rank improved
# Negative = rank declined
reentries["rank_improvement"] = (
    reentries["previous_rank"] - reentries["current_rank"]
)

# 4. Classify comeback performance
def classify_comeback(value):

    if value > 0:
        return "Rank Improved"

    elif value < 0:
        return "Rank Declined"

    else:
        return "No Rank Change"


reentries["comeback_performance"] = (
    reentries["rank_improvement"].apply(classify_comeback)
)

# 5. Add song and artist details
song_details = (
    df.groupby("song_artist_key")
    .agg(
        song=("song", "first"),
        artist=("artist", "first")
    )
    .reset_index()
)

reentries = reentries.merge(
    song_details,
    on="song_artist_key",
    how="left"
)

# 6. Calculate rank recovery percentage
total_events = len(reentries)

improved = (
    reentries["comeback_performance"] == "Rank Improved"
).sum()

declined = (
    reentries["comeback_performance"] == "Rank Declined"
).sum()

unchanged = (
    reentries["comeback_performance"] == "No Rank Change"
).sum()

improvement_percentage = (
    improved / total_events * 100
)

# 7. Save individual comeback results
reentries.to_csv(
    "outputs/rank_recovery_events.csv",
    index=False
)

# 8. Song-wise rank recovery analysis
song_recovery = (
    reentries.groupby(["song_artist_key", "song", "artist"])
    .agg(
        total_comebacks=("rank_improvement", "count"),
        average_rank_improvement=("rank_improvement", "mean"),
        maximum_rank_improvement=("rank_improvement", "max"),
        minimum_rank_improvement=("rank_improvement", "min")
    )
    .reset_index()
)

song_recovery["average_rank_improvement"] = (
    song_recovery["average_rank_improvement"].round(2)
)

song_recovery = song_recovery.sort_values(
    ["average_rank_improvement", "total_comebacks"],
    ascending=[False, False]
)

# 9. Save song-wise results
song_recovery.to_csv(
    "outputs/song_rank_recovery.csv",
    index=False
)

# 10. Display results
print("\n========== RANK RECOVERY ANALYSIS ==========")

print("\nTotal confirmed comeback events:")
print(total_events)

print("\nComebacks with improved ranks:")
print(improved)

print("\nComebacks with declined ranks:")
print(declined)

print("\nComebacks with unchanged ranks:")
print(unchanged)

print("\nRank improvement percentage:")
print(round(improvement_percentage, 2), "%")

print("\nTop 15 songs by average rank improvement:")
print(
    song_recovery[
        [
            "song",
            "artist",
            "total_comebacks",
            "average_rank_improvement",
            "maximum_rank_improvement"
        ]
    ].head(15).to_string(index=False)
)

print("\nTop 10 individual comeback rank improvements:")
print(
    reentries.sort_values(
        "rank_improvement",
        ascending=False
    )[
        [
            "song",
            "artist",
            "date",
            "previous_rank",
            "current_rank",
            "rank_improvement"
        ]
    ].head(10).to_string(index=False)
)

print("\nFiles saved:")
print("1. outputs/rank_recovery_events.csv")
print("2. outputs/song_rank_recovery.csv")

print("\n========== ANALYSIS COMPLETED ==========")
