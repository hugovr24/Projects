# Objective: Merge the NTSB event, narrative, and findings data into a clean CSV for LLM pipeline

## Libraries
import pandas as pd
import os

# Load all source tables
events = pd.read_csv("converted_csvs/events.csv")
narratives = pd.read_csv("converted_csvs/narratives.csv")
findings = pd.read_csv("converted_csvs/Findings.csv")
aircraft = pd.read_csv("converted_csvs/aircraft.csv")

# Join narrative with events on 'ev_id'
merged = pd.merge(narratives, events, on="ev_id", how="inner")

# Filter out empty or short narratives
merged = merged[merged['narr_accf'].notnull() & (merged['narr_accf'].str.len() > 100)]

# Merge aircraft info
merged = pd.merge(
    merged,
    aircraft[["ev_id", "Aircraft_Key", "acft_make", "acft_model", "acft_series", "acft_category",
        "num_eng", "homebuilt", "acft_year", "fuel_on_board"]],
    on=["ev_id", "Aircraft_Key"],
    how="left"
)

# Normalize cm_inPC to string for reliability
findings["cm_inPC"] = findings["cm_inPc"].astype(str).str.upper()

# Filter findings eherte cm_inPC is True or T
relevant_findings = findings[findings["cm_inPc"].isin(["TRUE", "T", "1"])]

# Group findings
finding_summary = relevant_findings.groupby("ev_id")["finding_description"]\
    .apply(lambda x: " | ".join(str(s) for s in x)).reset_index()

# Merge findings into merged table
final = pd.merge(merged, finding_summary, on="ev_id", how="left")

# Final field selection (only those present in merged)
final = final[[
     "ev_id", "ev_date", "ev_city", "ev_state", "narr_accf", "ev_highest_injury",
    "acft_make", "acft_model", "acft_series", "acft_category", "num_eng", "homebuilt",
    "acft_year", "fuel_on_board", "finding_description"
]]

# Rename for clarity
final.rename(columns={
    "ev_id": "event_id",
    "ev_city": "location",
    "narr_accf": "narrative",
    "ev_highest_injury": "injury_severity",
    "finding_description": "findings"
}, inplace=True)

# Save to CSV
os.makedirs("data", exist_ok=True)
final.to_csv("data/processed_incidents.csv", index=False)
print("Saved cleaned dataset to data/processed_incidents.csv")

