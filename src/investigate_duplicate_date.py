
import pandas as pd

df = pd.read_csv("dataset/Atlantic_South_Korea.csv")

# Select records from 1 March 2025
day_data = df[df["date"] == "01-03-2025"].copy()

print("\nTOTAL RECORDS:", len(day_data))

# Display all 100 records in their original order
print("\nALL RECORDS FOR 1 MARCH 2025:")

print(
    day_data[
        ["position", "song", "artist", "popularity"]
    ].to_string(index=False)
)

# Check whether the two groups of 50 are identical
first_50 = day_data.iloc[:50].reset_index(drop=True)
next_50 = day_data.iloc[50:].reset_index(drop=True)

print("\nARE THE TWO LISTS IDENTICAL?")

print(first_50.equals(next_50))

print("\nPOPULARITY DIFFERENCES:")
comparison = pd.DataFrame({
    "first_list": first_50["popularity"],
    "second_list": next_50["popularity"]
})

print(comparison.describe())
