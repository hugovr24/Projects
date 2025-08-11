# run_app.py
# Unified runner for batch, CLI, and Streamlit modes

import os
import sys
import argparse
import pandas as pd
from dotenv import load_dotenv
from agents import summarize_incident, classify_root_cause
from rag_utils import init_vectorstore, get_similar_cases

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


def run_batch():
    ## LOAD INCIDENT DATASET
    data = pd.read_csv("data/processed_incidents.csv")

    ##  INITIALIZE VECTOR STORE FROM DATASET
    vectorstore = init_vectorstore()

    ## CREATE OUTPUT
    os.makedirs("output", exist_ok=True)
    with open("output/classification_results.csv", "w", encoding="utf-8") as f:
        f.write("event_id,summary,classification\n")

        for index, row in data.iterrows():
            print(f"\n--- Incident #{index + 1} ({row['event_id']}) ---")
            narrative = row["narrative"]

            # Agent 1: Summarize
            summary = summarize_incident(narrative)
            print("\nSummary:\n", summary)

            # Agent 2: Get similar past cases using RAG
            similar_docs = get_similar_cases(summary, vectorstore)
            
            # Agent 2: Classify root cause
            classification = classify_root_cause(summary, similar_docs)
            print("\nClassification Result:\n", classification)

            f.write(f"{row['event_id']},\"{summary}\",\"{classification}\"\n")

    print("\n✅ Batch processing complete.")


def run_cli():
    vectorstore = init_vectorstore()
    print("\n🚀 Aerospace Incident Analyzer CLI")
    print("Type or paste an incident narrative. Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter incident narrative: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\n👋 Goodbye!")
            break

        summary = summarize_incident(user_input)
        print("\n📝 Summary:\n", summary)

        similar_docs = get_similar_cases(summary, vectorstore)
        classification = classify_root_cause(summary, similar_docs)
        print("\n📊 Classification:\n", classification)
        print("\n" + "-" * 40)


def run_streamlit():
    import streamlit as st

    st.set_page_config(page_title="Aerospace Incident Analyzer", layout="wide")
    st.title("🛩️ Aerospace Incident Analyzer")

    st.markdown("""
    Enter an incident narrative below. The system will:
    1. Summarize the incident
    2. Retrieve similar past incidents (RAG)
    3. Classify the root cause, severity, and confidence level
    """)

    @st.cache_resource
    def load_vectorstore():
        return init_vectorstore()

    vectorstore = load_vectorstore()
    user_input = st.text_area("✍️ Paste an aerospace incident narrative:", height=250)

    if user_input:
        with st.spinner("Analyzing incident..."):
            summary = summarize_incident(user_input)
            st.subheader("📝 Summary")
            st.markdown(summary)

            similar_docs = get_similar_cases(summary, vectorstore)
            st.subheader("📚 Similar Incidents")
            for doc in similar_docs:
                st.markdown(f"**Location:** {doc.metadata.get('location')}  ")
                st.markdown(f"**Aircraft:** {doc.metadata.get('aircraft')}  ")
                st.markdown(f"**Narrative:** {doc.page_content[:400]}...\n")
                st.markdown("---")

            classification = classify_root_cause(summary, similar_docs)
            st.subheader("📊 Classification")
            st.markdown(classification)
            st.success("✅ Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Aerospace Incident Analyzer")
    parser.add_argument("--mode", type=str, choices=["batch", "cli", "streamlit"], default="cli")
    args = parser.parse_args()

    if args.mode == "batch":
        run_batch()
    elif args.mode == "cli":
        run_cli()
    elif args.mode == "streamlit":
        run_streamlit()
