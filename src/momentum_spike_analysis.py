
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 1. Load analysis datasets
rank_data = pd.read_csv("outputs/rank_recovery_events.csv")
retention_data = pd.read_csv("outputs/comeback_retention_events.csv")

# 2. Select required columns from retention data
retention_data = retention_data[
    [
        "song_artist_key",
        "comeback_date",
        "retention_days"
    ]
]

# 3. Convert dates
rank_data["date"] = pd.to_datetime(rank_data["date"])
retention_data["comeback_date"] = pd.to_datetime(
    retention_data["comeback_date"]
)

# 4. Merge rank and retention data
momentum = rank_data.merge(
    retention_data,
    left_on=["song_artist_key", "date"],
    right_on=["song_artist_key", "comeback_date"],
    how="inner"
)

# 5. Calculate rank improvement
momentum["rank_improvement"] = (
    momentum["previous_rank"] - momentum["current_rank"]
)

# 6. Normalize rank improvement
# Negative improvements are treated as zero momentum.
momentum["positive_rank_improvement"] = (
    momentum["rank_improvement"].clip(lower=0)
)

scaler = MinMaxScaler()

momentum["rank_score"] = (
    scaler.fit_transform(
        momentum[["positive_rank_improvement"]]
    ) * 100
)

# 7. Normalize retention days
momentum["retention_score"] = (
    scaler.fit_transform(
        momentum[["retention_days"]]
    ) * 100
)

# 8. Calculate Momentum Spike Score
momentum["momentum_spike_score"] = (
    0.7 * momentum["rank_score"] +
    0.3 * momentum["retention_score"]
).round(2)

# 9. Classify momentum levels
def classify_momentum(score):

    if score >= 70:
        return "High Momentum"

    elif score >= 40:
        return "Moderate Momentum"

    else:
        return "Low Momentum"


momentum["momentum_category"] = (
    momentum["momentum_spike_score"].apply(
        classify_momentum
    )
)

# 10. Save event-wise momentum results
momentum.to_csv(
    "outputs/comeback_momentum_scores.csv",
    index=False
)

# 11. Calculate song-wise momentum
song_momentum = (
    momentum.groupby(
        ["song_artist_key", "song", "artist"]
    )
    .agg(
        total_comebacks=("momentum_spike_score", "count"),
        average_momentum_score=(
            "momentum_spike_score", "mean"
        ),
        maximum_momentum_score=(
            "momentum_spike_score", "max"
        ),
        average_retention_days=("retention_days", "mean")
    )
    .reset_index()
)

song_momentum["average_momentum_score"] = (
    song_momentum["average_momentum_score"].round(2)
)

song_momentum["maximum_momentum_score"] = (
    song_momentum["maximum_momentum_score"].round(2)
)

song_momentum["average_retention_days"] = (
    song_momentum["average_retention_days"].round(2)
)

song_momentum = song_momentum.sort_values(
    "average_momentum_score",
    ascending=False
)

# 12. Save song-wise momentum results
song_momentum.to_csv(
    "outputs/song_momentum_summary.csv",
    index=False
)

# 13. Display results
print("\n========== MOMENTUM SPIKE ANALYSIS ==========")

print("\nTotal comeback events analysed:")
print(len(momentum))

print("\nAverage Momentum Spike Score:")
print(round(momentum["momentum_spike_score"].mean(), 2))

print("\nMomentum Category Distribution:")
print(momentum["momentum_category"].value_counts())

print("\nTop 15 Songs by Average Momentum Score:")
print(
    song_momentum[
        [
            "song",
            "artist",
            "total_comebacks",
            "average_momentum_score",
            "maximum_momentum_score",
            "average_retention_days"
        ]
    ].head(15).to_string(index=False)
)

print("\nFiles saved:")
print("1. outputs/comeback_momentum_scores.csv")
print("2. outputs/song_momentum_summary.csv")

print("\n========== ANALYSIS COMPLETED ==========")
