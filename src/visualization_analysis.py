
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Create output folder
os.makedirs("outputs/visualizations", exist_ok=True)

# 2. Set chart style
sns.set_theme(style="whitegrid")

# 3. Load datasets
frequency = pd.read_csv(
    "outputs/song_comeback_frequency.csv"
)

retention = pd.read_csv(
    "outputs/song_comeback_retention.csv"
)

momentum = pd.read_csv(
    "outputs/song_momentum_summary.csv"
)

fandom = pd.read_csv(
    "outputs/fandom_intensity_scores.csv"
)

artist = pd.read_csv(
    "outputs/artist_comeback_performance.csv"
)

album = pd.read_csv(
    "outputs/album_comeback_advantage.csv"
)

# --------------------------------------------------
# CHART 1: Top 10 Songs by Comeback Frequency
# --------------------------------------------------

top_songs = frequency.sort_values(
    "reentry_count",
    ascending=False
).head(10)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_songs,
    x="reentry_count",
    y="song",
    hue="song",
    palette="viridis",
    legend=False
)

plt.title(
    "Top 10 Songs by Comeback Frequency",
    fontsize=16
)
plt.xlabel("Confirmed Comeback Events")
plt.ylabel("Song")

plt.tight_layout()
plt.savefig(
    "outputs/visualizations/top_10_comeback_songs.png",
    dpi=300
)
plt.close()

# --------------------------------------------------
# CHART 2: Top 10 Artists by Comeback Frequency
# --------------------------------------------------

top_artists = artist.sort_values(
    "total_comeback_events",
    ascending=False
).head(10)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_artists,
    x="total_comeback_events",
    y="artist",
    hue="artist",
    palette="magma",
    legend=False
)

plt.title(
    "Top 10 Artists by Comeback Frequency",
    fontsize=16
)
plt.xlabel("Total Comeback Events")
plt.ylabel("Artist")

plt.tight_layout()
plt.savefig(
    "outputs/visualizations/top_10_comeback_artists.png",
    dpi=300
)
plt.close()

# --------------------------------------------------
# CHART 3: Comeback Retention Distribution
# --------------------------------------------------

plt.figure(figsize=(10, 6))

sns.histplot(
    data=retention,
    x="average_retention_days",
    bins=25,
    kde=True
)

plt.title(
    "Distribution of Average Comeback Retention",
    fontsize=16
)
plt.xlabel("Average Retention (Days)")
plt.ylabel("Number of Songs")

plt.tight_layout()
plt.savefig(
    "outputs/visualizations/retention_distribution.png",
    dpi=300
)
plt.close()

# --------------------------------------------------
# CHART 4: Momentum Score Distribution
# --------------------------------------------------

plt.figure(figsize=(10, 6))

sns.histplot(
    data=momentum,
    x="average_momentum_score",
    bins=25,
    kde=True
)

plt.title(
    "Distribution of Average Comeback Momentum Scores",
    fontsize=16
)
plt.xlabel("Average Momentum Score")
plt.ylabel("Number of Songs")

plt.tight_layout()
plt.savefig(
    "outputs/visualizations/momentum_distribution.png",
    dpi=300
)
plt.close()

# --------------------------------------------------
# CHART 5: Fandom Intensity Proxy Categories
# --------------------------------------------------

fandom_counts = (
    fandom["fandom_category"]
    .value_counts()
    .reset_index()
)

fandom_counts.columns = [
    "category",
    "song_count"
]

plt.figure(figsize=(9, 6))

sns.barplot(
    data=fandom_counts,
    x="category",
    y="song_count",
    hue="category",
    palette="Set2",
    legend=False
)

plt.title(
    "Fandom Intensity Proxy Category Distribution",
    fontsize=15
)
plt.xlabel("Proxy Category")
plt.ylabel("Number of Songs")
plt.xticks(rotation=15)

plt.tight_layout()
plt.savefig(
    "outputs/visualizations/fandom_proxy_categories.png",
    dpi=300
)
plt.close()

# --------------------------------------------------
# CHART 6: Album vs Single Comeback Comparison
# --------------------------------------------------

plt.figure(figsize=(10, 6))

sns.barplot(
    data=album,
    x="album_type",
    y="average_retention_days",
    hue="album_type",
    palette="coolwarm",
    legend=False
)

plt.title(
    "Average Comeback Retention: Album vs Single",
    fontsize=15
)
plt.xlabel("Album Type")
plt.ylabel("Average Retention (Days)")

plt.tight_layout()
plt.savefig(
    "outputs/visualizations/album_vs_single_retention.png",
    dpi=300
)
plt.close()

# --------------------------------------------------
# CHART 7: Artist Comeback Events vs Average Retention
# --------------------------------------------------

plt.figure(figsize=(11, 7))

sns.scatterplot(
    data=artist,
    x="total_comeback_events",
    y="average_retention_days",
    size="unique_comeback_songs",
    hue="average_fandom_proxy_score",
    palette="viridis",
    sizes=(40, 400),
    alpha=0.8
)

plt.title(
    "Artist Comeback Frequency vs Average Retention",
    fontsize=15
)
plt.xlabel("Total Comeback Events")
plt.ylabel("Average Retention (Days)")

plt.tight_layout()
plt.savefig(
    "outputs/visualizations/artist_comeback_scatter.png",
    dpi=300
)
plt.close()

# --------------------------------------------------
# COMPLETION SUMMARY
# --------------------------------------------------

print("\n========== VISUALIZATION ANALYSIS ==========")

print("\nTotal charts generated: 7")

print("\nCharts saved inside:")
print("outputs/visualizations/")

print("\nGenerated chart files:")

for file in os.listdir("outputs/visualizations"):
    if file.endswith(".png"):
        print(file)

print("\n========== VISUALIZATION COMPLETED ==========")
