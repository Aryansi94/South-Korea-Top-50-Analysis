
import pandas as pd

# Load the original dataset
file_path = "dataset/Atlantic_South_Korea.csv"
df = pd.read_csv(file_path)

# Convert date into proper date format
df["date"] = pd.to_datetime(
    df["date"],
    format="%d-%m-%Y",
    errors="coerce"
)

print("\n========== DATA QUALITY REPORT ==========")

# 1. Check invalid dates
print("\nInvalid Dates:")
print(df["date"].isna().sum())

# 2. Check exact duplicate records
print("\nExact Duplicate Records:")
print(df.duplicated().sum())

# 3. Check number of records per date
daily_counts = df.groupby("date").size()

print("\nRecords Per Date:")
print(daily_counts.value_counts().sort_index())

# 4. Find dates that do not have exactly 50 records
unusual_dates = daily_counts[daily_counts != 50]

print("\nDates Not Having Exactly 50 Records:")
print(unusual_dates)

# 5. Check duplicate chart positions on each date
duplicate_positions = df[
    df.duplicated(subset=["date", "position"], keep=False)
]

print("\nDuplicate Date-Position Records:")
print(duplicate_positions[
    ["date", "position", "song", "artist"]
].to_string(index=False))

print("\n========== CHECK COMPLETED ==========")
