import pandas as pd

# Load the full dataset
df = pd.read_csv("data/processed_incidents.csv")

# Split size
chunk_size = 4200

# Create and save chunks
for i in range(0, len(df), chunk_size):
    chunk = df[i:i+chunk_size]
    chunk.to_csv(f"processed_incidents_part{i//chunk_size + 1}.csv", index=False)

print("✅ Split into 5 parts.")

