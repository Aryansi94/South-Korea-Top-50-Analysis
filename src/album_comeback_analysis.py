
import pandas as pd

# 1. Load datasets
df = pd.read_csv("outputs/cleaned_chart_data.csv")
momentum = pd.read_csv("outputs/comeback_momentum_scores.csv")

# 2. Prepare song details
song_details = (
    df.groupby("song_artist_key")
    .agg(
        song=("song", "first"),
        artist=("artist", "first"),
        album_type=("album_type", "first")
    )
    .reset_index()
)

# 3. Merge album information with comeback data
analysis = momentum.merge(
    song_details[
        ["song_artist_key", "album_type"]
    ],
    on="song_artist_key",
    how="left"
)

# 4. Clean album type labels
analysis["album_type"] = (
    analysis["album_type"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# 5. Calculate album-type-wise comeback performance
album_summary = (
    analysis.groupby("album_type")
    .agg(
        total_comeback_events=(
            "momentum_spike_score", "count"
        ),
        unique_comeback_songs=(
            "song_artist_key", "nunique"
        ),
        average_retention_days=(
            "retention_days", "mean"
        ),
        average_rank_improvement=(
            "rank_improvement", "mean"
        ),
        average_momentum_score=(
            "momentum_spike_score", "mean"
        )
    )
    .reset_index()
)

# 6. Round numerical values
numeric_columns = [
    "average_retention_days",
    "average_rank_improvement",
    "average_momentum_score"
]

album_summary[numeric_columns] = (
    album_summary[numeric_columns].round(2)
)

# 7. Sort by average momentum score
album_summary = album_summary.sort_values(
    "average_momentum_score",
    ascending=False
)

# 8. Save results
album_summary.to_csv(
    "outputs/album_comeback_advantage.csv",
    index=False
)

analysis.to_csv(
    "outputs/comeback_album_type_details.csv",
    index=False
)

# 9. Display results
print("\n========== ALBUM VS SINGLE COMEBACK ANALYSIS ==========")

print("\nAlbum Type Distribution:")
print(df["album_type"].value_counts())

print("\nComeback Performance by Album Type:")
print(album_summary.to_string(index=False))

print("\nTotal comeback events analysed:")
print(len(analysis))

print("\nFiles saved:")
print("1. outputs/album_comeback_advantage.csv")
print("2. outputs/comeback_album_type_details.csv")

print("\n========== ANALYSIS COMPLETED ==========")
