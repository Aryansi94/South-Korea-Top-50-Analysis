
import pandas as pd
import os
import re

# ---------------------------------------
# 1. LOAD ORIGINAL DATASET
# ---------------------------------------

input_file = "dataset/Atlantic_South_Korea.csv"

df = pd.read_csv(input_file)

print("Original dataset loaded:", df.shape)

# Required columns
required_columns = [
    "date", "position", "song", "artist",
    "popularity", "duration_ms", "album_type",
    "total_tracks", "is_explicit", "album_cover_url"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

# ---------------------------------------
# 2. CONVERT DATE FORMAT
# ---------------------------------------

df["date"] = pd.to_datetime(
    df["date"],
    format="%d-%m-%Y",
    errors="coerce"
)

invalid_dates = int(df["date"].isna().sum())

if invalid_dates > 0:
    raise ValueError(
        f"Found {invalid_dates} invalid dates. "
        "Please investigate before cleaning."
    )

# ---------------------------------------
# 3. RECORD ORIGINAL DATA QUALITY
# ---------------------------------------

original_rows = len(df)
exact_duplicates = int(df.duplicated().sum())

# ---------------------------------------
# 4. SEPARATE ANOMALOUS DATE
# ---------------------------------------

excluded_date = pd.Timestamp("2025-03-01")

excluded_records = df[
    df["date"] == excluded_date
].copy()

analysis_df = df[
    df["date"] != excluded_date
].copy()

# Preserve excluded records separately
os.makedirs("outputs", exist_ok=True)

excluded_records.to_csv(
    "outputs/excluded_2025_03_01.csv",
    index=False
)

# ---------------------------------------
# 5. NORMALIZE SONG AND ARTIST
# ---------------------------------------

def normalize_text(value):
    value = str(value).strip().casefold()
    value = re.sub(r"\s+", " ", value)
    return value

analysis_df["song_artist_key"] = (
    analysis_df["song"].apply(normalize_text)
    + " | "
    + analysis_df["artist"].apply(normalize_text)
)

# ---------------------------------------
# 6. CONVERT DURATION INTO MINUTES
# ---------------------------------------

analysis_df["duration_min"] = (
    analysis_df["duration_ms"] / 60000
).round(2)

# ---------------------------------------
# 7. CHECK CLEANED DATA
# ---------------------------------------

cleaned_rows = len(analysis_df)

daily_counts = analysis_df.groupby("date").size()

dates_with_50 = int((daily_counts == 50).sum())

unusual_dates = int((daily_counts != 50).sum())

duplicate_positions = int(
    analysis_df.duplicated(
        subset=["date", "position"]
    ).sum()
)

# ---------------------------------------
# 8. SAVE CLEANED DATASET
# ---------------------------------------

analysis_df.to_csv(
    "outputs/cleaned_chart_data.csv",
    index=False
)

# Save daily record counts
daily_counts.rename("record_count").to_csv(
    "outputs/daily_record_counts.csv"
)

# ---------------------------------------
# 9. CREATE DATA QUALITY REPORT
# ---------------------------------------

report = pd.DataFrame({
    "Metric": [
        "Original rows",
        "Original columns",
        "Invalid dates",
        "Exact duplicate rows in original",
        "Records excluded from 2025-03-01",
        "Cleaned analysis rows",
        "Dates with exactly 50 records",
        "Dates with unusual record counts",
        "Duplicate date-position records after exclusion"
    ],

    "Value": [
        original_rows,
        len(required_columns),
        invalid_dates,
        exact_duplicates,
        len(excluded_records),
        cleaned_rows,
        dates_with_50,
        unusual_dates,
        duplicate_positions
    ]
})

report.to_csv(
    "outputs/data_quality_report.csv",
    index=False
)

# ---------------------------------------
# 10. DISPLAY FINAL RESULTS
# ---------------------------------------

print("\n========== CLEANING COMPLETED ==========")

print("Original rows:", original_rows)
print("Excluded records:", len(excluded_records))
print("Cleaned rows:", cleaned_rows)
print("Dates with 50 records:", dates_with_50)
print("Unusual dates:", unusual_dates)
print("Duplicate date-position records:", duplicate_positions)

print("\nFiles saved successfully:")
print("1. outputs/cleaned_chart_data.csv")
print("2. outputs/excluded_2025_03_01.csv")
print("3. outputs/daily_record_counts.csv")
print("4. outputs/data_quality_report.csv")

print("\nOriginal dataset has NOT been modified.")
