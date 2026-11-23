
import pandas as pd

df = pd.read_csv("dataset/Atlantic_South_Korea.csv")

# Find rows for 1 March 2025
indexes = df.index[df["date"] == "01-03-2025"].tolist()

first_index = min(indexes)
last_index = max(indexes)

# Display nearby records in original file order
start = max(0, first_index - 5)
end = min(len(df), last_index + 6)

print("\nRECORDS BEFORE, DURING AND AFTER 1 MARCH 2025:")

print(
    df.iloc[start:end][
        ["date", "position", "song", "artist", "popularity"]
    ].to_string(index=True)
)

print("\nFIRST ROW INDEX:", first_index)
print("LAST ROW INDEX:", last_index)
