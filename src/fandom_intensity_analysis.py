
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 1. Load datasets
frequency = pd.read_csv(
    "outputs/song_comeback_frequency.csv"
)

retention = pd.read_csv(
    "outputs/song_comeback_retention.csv"
)

recovery = pd.read_csv(
    "outputs/song_rank_recovery.csv"
)

momentum = pd.read_csv(
    "outputs/song_momentum_summary.csv"
)

# 2. Select required columns
frequency = frequency[
    [
        "song_artist_key",
        "song",
        "artist",
        "reentry_count"
    ]
]

retention = retention[
    [
        "song_artist_key",
        "average_retention_days"
    ]
]

recovery = recovery[
    [
        "song_artist_key",
        "average_rank_improvement"
    ]
]

momentum = momentum[
    [
        "song_artist_key",
        "average_momentum_score"
    ]
]

# 3. Merge all indicators
fandom = frequency.merge(
    retention,
    on="song_artist_key",
    how="inner"
)

fandom = fandom.merge(
    recovery,
    on="song_artist_key",
    how="inner"
)

fandom = fandom.merge(
    momentum,
    on="song_artist_key",
    how="inner"
)

# 4. Handle missing values
fandom = fandom.fillna(0)

# 5. Normalize indicators
scaler = MinMaxScaler()

columns_to_normalize = [
    "reentry_count",
    "average_retention_days",
    "average_rank_improvement",
    "average_momentum_score"
]

normalized = scaler.fit_transform(
    fandom[columns_to_normalize]
)

normalized_df = pd.DataFrame(
    normalized * 100,
    columns=[
        "frequency_score",
        "retention_score",
        "rank_recovery_score",
        "momentum_score"
    ],
    index=fandom.index
)

fandom = pd.concat(
    [fandom, normalized_df],
    axis=1
)

# 6. Calculate Fandom Intensity Proxy Score
fandom["fandom_intensity_score"] = (
    0.30 * fandom["frequency_score"] +
    0.30 * fandom["retention_score"] +
    0.20 * fandom["rank_recovery_score"] +
    0.20 * fandom["momentum_score"]
).round(2)

# 7. Classify fandom intensity
def classify_fandom(score):

    if score >= 70:
        return "High Proxy Intensity"

    elif score >= 40:
        return "Moderate Proxy Intensity"

    else:
        return "Low Proxy Intensity"


fandom["fandom_category"] = (
    fandom["fandom_intensity_score"].apply(
        classify_fandom
    )
)

# 8. Sort by final score
fandom = fandom.sort_values(
    "fandom_intensity_score",
    ascending=False
)

# 9. Save results
fandom.to_csv(
    "outputs/fandom_intensity_scores.csv",
    index=False
)

# 10. Display results
print("\n========== FANDOM INTENSITY PROXY ANALYSIS ==========")

print("\nTotal songs analysed:")
print(len(fandom))

print("\nAverage Fandom Intensity Proxy Score:")
print(round(fandom["fandom_intensity_score"].mean(), 2))

print("\nFandom Intensity Category Distribution:")
print(fandom["fandom_category"].value_counts())

print("\nTop 15 Songs by Fandom Intensity Proxy Score:")
print(
    fandom[
        [
            "song",
            "artist",
            "reentry_count",
            "average_retention_days",
            "average_rank_improvement",
            "fandom_intensity_score",
            "fandom_category"
        ]
    ].head(15).to_string(index=False)
)

print("\nFiles saved:")
print("1. outputs/fandom_intensity_scores.csv")

print("\n========== ANALYSIS COMPLETED ==========")
