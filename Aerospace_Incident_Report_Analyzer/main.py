# main.py
# PURPOSE: 

## LIBRARY

import sys
import os
from agents import summarize_incident, classify_root_cause
from rag_utils import init_vectorstore, get_similar_cases
from dotenv import load_dotenv
import pandas as pd
import csv

# Set up Azure OpenAI credentials from custom creds module or environment
sys.path.insert(1, '../../..')  # Adjust as needed if using custom Azure creds

# Optional: Use init_creds if working in Azure workspace with centralized credentials
# import init_creds as creds
# AZURE_OPENAI_API_KEY = creds.get_api_key()
# AZURE_OPENAI_ENDPOINT = creds.get_endpoint()
# os.environ["OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY
# os.environ["OPENAI_API_BASE"] = AZURE_OPENAI_ENDPOINT

# Fallback to .env or direct environment variables
load_dotenv()

# Ensure that 'OPENAI_API_KEY' is set

## LOAD INCIDENT DATASET
data = pd.read_csv("data/processed_incidents.csv")

# INITIALIZE VECTOR STORE FROM DATASET
vectorstore = init_vectorstore()

# CREATE OUTPUT CSV TO STORE RESULT
output_path = "output/classification_results.csv"
os.makedirs("output", exist_ok=True)

with open(output_path, mode='w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['event_id', 'summary', 'classification'])


    # Run summarization and classification on a few samples
    for index, row in data.head(3).iterrows():
        print(f"\n--- Incident #{index + 1} ({row['event_id']}) ---")
        narrative = row["narrative"]

        # Agent 1: Summarize
        summary = summarize_incident(narrative)
        print("\nSummary:")
        print(summary)

        # Agent 2: Get similar past cases using RAG
        similar_docs = get_similar_cases(summary, vectorstore)

        # Agent 2: Classify root cause
        classification = classify_root_cause(summary, similar_docs)
        print("\nClassification Results:")
        print(classification)

        # Save results
        writer.writerow([row["event_id"], summary, classification])

print(f"\n All incidents processed. Results saved to {output_path}")

