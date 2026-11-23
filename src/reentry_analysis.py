
import pandas as pd

# 1. Load cleaned dataset
df = pd.read_csv("outputs/cleaned_chart_data.csv")
df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(
    ["date", "position"]
).reset_index(drop=True)

chart_dates = sorted(df["date"].unique())

# 2. Prepare tracking variables
results = []

previous_songs = set()
seen_before = set()
previous_date = None

# Store the last rank at which each song appeared
last_seen_rank = {}

# 3. Process each chart date
for current_date in chart_dates:

    current_data = df[df["date"] == current_date]

    current_songs = set(
        current_data["song_artist_key"]
    )

    current_ranks = dict(
        zip(
            current_data["song_artist_key"],
            current_data["position"]
        )
    )

    # Check whether dates are consecutive
    consecutive_day = (
        previous_date is not None
        and (current_date - previous_date).days == 1
    )

    if previous_date is None:

        # First available chart date
        for song in current_songs:
            results.append({
                "date": current_date,
                "song_artist_key": song,
                "event": "First Observed Entry",
                "current_rank": current_ranks[song],
                "previous_rank": None,
                "rank_change": None
            })

    elif consecutive_day:

        # Songs appearing after being absent
        new_songs = current_songs - previous_songs

        for song in new_songs:

            if song in seen_before:

                old_rank = last_seen_rank.get(song)
                new_rank = current_ranks[song]

                rank_change = (
                    old_rank - new_rank
                    if old_rank is not None
                    else None
                )

                results.append({
                    "date": current_date,
                    "song_artist_key": song,
                    "event": "Confirmed Re-entry",
                    "current_rank": new_rank,
                    "previous_rank": old_rank,
                    "rank_change": rank_change
                })

            else:

                results.append({
                    "date": current_date,
                    "song_artist_key": song,
                    "event": "First Observed Entry",
                    "current_rank": current_ranks[song],
                    "previous_rank": None,
                    "rank_change": None
                })

        # Songs leaving the chart
        exited_songs = previous_songs - current_songs

        for song in exited_songs:
            results.append({
                "date": current_date,
                "song_artist_key": song,
                "event": "Confirmed Exit",
                "current_rank": None,
                "previous_rank": last_seen_rank.get(song),
                "rank_change": None
            })

    else:

        # A missing calendar date exists.
        # Do not assume an exit or confirmed re-entry.

        new_songs = current_songs - previous_songs

        for song in new_songs:

            if song in seen_before:
                event_name = "Return After Data Gap (Unconfirmed)"
            else:
                event_name = "First Observed Entry After Gap"

            results.append({
                "date": current_date,
                "song_artist_key": song,
                "event": event_name,
                "current_rank": current_ranks[song],
                "previous_rank": last_seen_rank.get(song),
                "rank_change": None
            })

    # Update song history
    seen_before.update(current_songs)

    last_seen_rank.update(current_ranks)

    previous_songs = current_songs
    previous_date = current_date


# 4. Create results DataFrame
events_df = pd.DataFrame(results)

# 5. Save events
events_df.to_csv(
    "outputs/song_entry_exit_events.csv",
    index=False
)

# 6. Display results
print("\n========== CORRECTED ENTRY AND RE-ENTRY ANALYSIS ==========")

print("\nEvent Counts:")
print(events_df["event"].value_counts())

print("\nConfirmed Re-entry Events:")
print(
    (events_df["event"] == "Confirmed Re-entry").sum()
)

print("\nConfirmed Exit Events:")
print(
    (events_df["event"] == "Confirmed Exit").sum()
)

print("\nFirst 20 Confirmed Re-entries:")
print(
    events_df[
        events_df["event"] == "Confirmed Re-entry"
    ].head(20).to_string(index=False)
)

print("\nRank Improvement Summary:")
reentries = events_df[
    events_df["event"] == "Confirmed Re-entry"
]

if not reentries.empty:
    print(reentries["rank_change"].describe())

print("\nSaved: outputs/song_entry_exit_events.csv")

print("\n========== ANALYSIS COMPLETED ==========")
