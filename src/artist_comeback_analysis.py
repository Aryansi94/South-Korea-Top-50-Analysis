
import pandas as pd

# 1. Load song-level datasets
frequency = pd.read_csv(
    "outputs/song_comeback_frequency.csv"
)

retention = pd.read_csv(
    "outputs/song_comeback_retention.csv"
)

recovery = pd.read_csv(
    "outputs/song_rank_recovery.csv"
)

fandom = pd.read_csv(
    "outputs/fandom_intensity_scores.csv"
)

# 2. Select required columns
frequency = frequency[
    ["song_artist_key", "artist", "reentry_count"]
]

retention = retention[
    ["song_artist_key", "average_retention_days"]
]

recovery = recovery[
    ["song_artist_key", "average_rank_improvement"]
]

fandom = fandom[
    ["song_artist_key", "fandom_intensity_score"]
]

# 3. Merge all datasets
artist_data = frequency.merge(
    retention,
    on="song_artist_key",
    how="inner"
)

artist_data = artist_data.merge(
    recovery,
    on="song_artist_key",
    how="inner"
)

artist_data = artist_data.merge(
    fandom,
    on="song_artist_key",
    how="inner"
)

# 4. Group data by artist
artist_summary = artist_data.groupby("artist").agg(
    unique_comeback_songs=(
        "song_artist_key", "nunique"
    ),
    total_comeback_events=(
        "reentry_count", "sum"
    ),
    average_retention_days=(
        "average_retention_days", "mean"
    ),
    average_rank_improvement=(
        "average_rank_improvement", "mean"
    ),
    average_fandom_proxy_score=(
        "fandom_intensity_score", "mean"
    ),
    maximum_fandom_proxy_score=(
        "fandom_intensity_score", "max"
    )
).reset_index()

# 5. Round numerical values
numeric_columns = [
    "average_retention_days",
    "average_rank_improvement",
    "average_fandom_proxy_score",
    "maximum_fandom_proxy_score"
]

artist_summary[numeric_columns] = (
    artist_summary[numeric_columns].round(2)
)

# 6. Rank artists by comeback frequency
artist_summary = artist_summary.sort_values(
    "total_comeback_events",
    ascending=False
)

# 7. Save results
artist_summary.to_csv(
    "outputs/artist_comeback_performance.csv",
    index=False
)

# 8. Display results
print("\n========== ARTIST COMEBACK PERFORMANCE ANALYSIS ==========")

print("\nTotal artists analysed:")
print(len(artist_summary))

print("\nTotal comeback events:")
print(artist_summary["total_comeback_events"].sum())

print("\nTop 15 Artists by Comeback Frequency:")

print(
    artist_summary.head(15).to_string(index=False)
)

print("\nTop 10 Artists by Average Fandom Proxy Score:")

print(
    artist_summary.sort_values(
        "average_fandom_proxy_score",
        ascending=False
    ).head(10).to_string(index=False)
)

print("\nOutput saved:")
print("outputs/artist_comeback_performance.csv")

print("\n========== ANALYSIS COMPLETED ==========")
