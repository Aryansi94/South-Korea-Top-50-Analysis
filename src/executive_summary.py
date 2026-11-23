
import pandas as pd
import os

# 1. Create output folder
os.makedirs("outputs", exist_ok=True)

# 2. Load analysis datasets
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

quality = pd.read_csv(
    "outputs/data_quality_report.csv"
)

# 3. Calculate project KPIs
total_songs = len(frequency)
total_comebacks = frequency["reentry_count"].sum()
total_artists = len(artist)

average_retention = retention[
    "average_retention_days"
].mean()

average_momentum = momentum[
    "average_momentum_score"
].mean()

average_fandom = fandom[
    "fandom_intensity_score"
].mean()

# 4. Identify top songs and artists
top_song = frequency.sort_values(
    "reentry_count",
    ascending=False
).iloc[0]

top_artist = artist.sort_values(
    "total_comeback_events",
    ascending=False
).iloc[0]

top_fandom_song = fandom.sort_values(
    "fandom_intensity_score",
    ascending=False
).iloc[0]

longest_retention = retention.sort_values(
    "maximum_retention_days",
    ascending=False
).iloc[0]

# 5. Album vs Single comparison
album_result = album.set_index("album_type")

album_retention = album_result.loc[
    "album", "average_retention_days"
]

single_retention = album_result.loc[
    "single", "average_retention_days"
]

# 6. Fandom category distribution
fandom_distribution = (
    fandom["fandom_category"].value_counts()
)

# 7. Build executive summary
summary = f"""
============================================================
EXECUTIVE SUMMARY
SOUTH KOREA TOP 50 PLAYLIST ANALYSIS
============================================================

PROJECT TITLE:
Comeback Momentum, Chart Re-Entry, and Fandom Intensity
Analysis of South Korea Top 50 Playlist

1. PROJECT OVERVIEW

This project analyses chart re-entry patterns, comeback
frequency, retention, rank recovery, momentum, and
chart-based fandom intensity indicators in South Korea's
Top 50 music playlist.

The analysis identifies songs that return to the chart
after confirmed exits and examines their subsequent
chart performance.

2. DATASET OVERVIEW

Total unique songs with confirmed comebacks: {total_songs}
Total confirmed comeback events: {total_comebacks}
Total artists analysed: {total_artists}

The main analysis excludes all 100 records from
1 March 2025 because that date contained two distinct
50-song chart lists without enough information to identify
the authoritative snapshot.

3. COMEBACK FREQUENCY FINDINGS

Top song by comeback frequency:
{top_song['song']} - {top_song['artist']}

Confirmed comeback events:
{top_song['reentry_count']}

Top artist by comeback frequency:
{top_artist['artist']}

Total artist comeback events:
{top_artist['total_comeback_events']}

4. RETENTION ANALYSIS

Average retention across analysed songs:
{average_retention:.2f} days

Longest individual comeback retention:
{longest_retention['maximum_retention_days']:.0f} days

Song:
{longest_retention['song']} - {longest_retention['artist']}

Retention measures consecutive observed calendar
dates on the chart after a comeback.

5. MOMENTUM ANALYSIS

Average Momentum Spike Score:
{average_momentum:.2f}

The momentum score is a custom relative indicator
combining normalized rank improvement and retention.

It is not an industry-standard metric or a direct
measurement of streaming activity.

6. FANDOM INTENSITY PROXY ANALYSIS

Average Fandom Intensity Proxy Score:
{average_fandom:.2f}

Highest-scoring song:
{top_fandom_song['song']} - {top_fandom_song['artist']}

Proxy score:
{top_fandom_song['fandom_intensity_score']:.2f}

Category distribution:
{fandom_distribution.to_string()}

This score uses chart recurrence, retention,
rank improvement, and momentum as indirect indicators.
It does not measure actual fanbase size or fan engagement.

7. ALBUM VS SINGLE COMPARISON

Average retention of album tracks:
{album_retention:.2f} days

Average retention of singles:
{single_retention:.2f} days

The comparison is observational and does not establish
that album tracks inherently perform better than singles.

8. KEY CONCLUSIONS

- Repeated chart re-entry is an important indicator
  of recurring chart activity.

- Comeback frequency and retention represent different
  aspects of chart performance.

- Some songs achieve long retention despite having
  relatively few comeback events.

- Artist-level comeback activity varies considerably.

- The fandom intensity score is a chart-based proxy,
  not a direct measure of fandom size.

9. RESEARCH LIMITATIONS

- The dataset does not provide direct fan engagement
  or streaming-count measurements.

- Missing calendar dates limit the certainty of
  some exit and re-entry observations.

- The 1 March 2025 chart snapshot was excluded because
  two distinct lists were present.

- The momentum and fandom proxy scores are custom
  analytical indicators.

- The findings describe observed chart behaviour
  and do not establish causal relationships.

============================================================
END OF EXECUTIVE SUMMARY
============================================================
"""

# 8. Save summary
output_path = "outputs/executive_summary.txt"

with open(
    output_path,
    "w",
    encoding="utf-8"
) as file:

    file.write(summary)

# 9. Display summary
print(summary)

print("\nExecutive summary saved successfully:")
print(output_path)
