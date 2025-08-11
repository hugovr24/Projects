# agents.py
# PURPOSE: LLM agents for summarization and root cause classification

## LIBRARIES
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

## AGENT 1 1: Summarize an aerospace incident

def summarize_incident(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        message=[
            {"role": "system", "content": "You are an aerospace analyst. Summarize incident reports in 3-5 bullet points including aircraft type, location, key events, and outcomes."},
            {"role": "user", "content": f"Summarize the following incident:\n{text}"}
        ]
    )
    return response['choices'][0]['message']['content']

# AGENT 2: Classify Root Cause using RAG

def classify_root_cause(summary, similar_docs):
    similar_text = "\n\n".join([doc.page_content for doc in similar_docs])
    prompt = (
        f"You are an aerospace safety investigator.\n"
        f"Incident Summary:\n{summary}\n\n"
        "Based on this context, classify the root cause (e.g., Mechanical Failure, Human Error, Unknown), assign a severity (Low/Medium/High), and provide a confidence score (0-1)."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages = [
            {"role": "system", "content": "You are a root cause classification assitant for aerospace reports."},
            {"role":"user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']["content"]