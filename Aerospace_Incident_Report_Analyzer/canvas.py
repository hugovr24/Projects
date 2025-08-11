import pandas as pd

narr = pd.read_csv("converted_csvs/narratives.csv")
ev = pd.read_csv("converted_csvs/events.csv")
fnd = pd.read_csv("converted_csvs/Findings.csv")

print("NARRATIVE COLUMNS:", narr.columns.tolist())
print("EVENTS COLUMNS:", ev.columns.tolist())
print("FINDINGS COLUMNS:", fnd.columns.tolist())
