
import pandas as pd

# Load datasets
df = pd.read_csv("outputs/cleaned_chart_data.csv")
events = pd.read_csv("outputs/song_entry_exit_events.csv")

df["date"] = pd.to_datetime(df["date"])
events["date"] = pd.to_datetime(events["date"])

# Get confirmed re-entry records
reentries = events[
    events["event"] == "Confirmed Re-entry"
]

# Store songs present on each date
daily_songs = {
    date: set(group["song_artist_key"])
    for date, group in df.groupby("date")
}

# Store all songs appearing before each date
all_songs = set()
chart_dates = sorted(daily_songs.keys())

valid_reentries = 0
invalid_reentries = 0

for _, row in reentries.iterrows():

    current_date = row["date"]
    song = row["song_artist_key"]

    previous_date = current_date - pd.Timedelta(days=1)

    # Check whether previous calendar date exists
    if previous_date not in daily_songs:
        invalid_reentries += 1
        continue

    # Check whether song appeared before
    appeared_before = False

    for date in chart_dates:
        if date >= current_date:
            break

        if song in daily_songs[date]:
            appeared_before = True
            break

    # Check absence on previous calendar day
    absent_previous_day = (
        song not in daily_songs[previous_date]
    )

    if appeared_before and absent_previous_day:
        valid_reentries += 1
    else:
        invalid_reentries += 1

print("\n========== RE-ENTRY VALIDATION ==========")

print("Total confirmed re-entries:", len(reentries))
print("Valid re-entries:", valid_reentries)
print("Invalid re-entries:", invalid_reentries)

if invalid_reentries == 0:
    print("\nALL RE-ENTRY EVENTS PASSED VALIDATION!")

else:
    print("\nSome events need further investigation.")

print("\n========== VALIDATION COMPLETED ==========")
