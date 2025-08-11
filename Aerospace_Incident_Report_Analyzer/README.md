# README.md

# Aerospace Incident Report Analyzer

Final project submission for the GenAI Practicum – Data Scientist Track

## Overview
This project demonstrates a multi-agent GenAI system for analyzing aerospace incident reports. It uses LLMs and RAG (Retrieval-Augmented Generation) to:
- Summarize incident narratives
- Retrieve similar past cases from a FAISS vector store
- Classify root cause, severity, and confidence

---

## Problem Statement
Manual review of aviation incident reports is time-consuming and inconsistent. This project automates the analysis process to support aviation safety investigations.

---

## Multi-Agent System

### Agent 1: Incident Summarizer
- Input: Raw narrative text
- Output: 3–5 bullet summary (aircraft, location, key events, outcome)

### Agent 2: Root Cause Classifier
- Input: Summary + RAG context
- Output: Cause category, severity (Low/Med/High), and confidence score

---

## Retrieval-Augmented Generation (RAG)
- Vector database: FAISS
- Embedded field: `narrative`
- Metadata: aircraft make/model, location, year
- Uses LangChain and OpenAI Embeddings

---

## Project Structure
```
Hugo_GenAITrack2_FinalAssessment/
├── data/                         ← Cleaned final dataset
├── converted_csvs/              ← Extracted raw data tables (MDB export)
├── output/                      ← Output classification results
├── agents.py                    ← Summarizer and classifier agents
├── rag_utils.py                 ← FAISS vector store setup + RAG query
├── run_app.py                   ← Unified entry point (batch, CLI, streamlit)
├── requirements.txt             ← Environment dependencies
└── README.md
```

---

## How to Run It

### 1. Install requirements
```bash
pip install -r requirements.txt
```

### 2. Set your API key
Create a `.env` file:
```env
OPENAI_API_KEY=your-openai-key-here
```

### 3. Run in CLI mode (default)
```bash
python run_app.py
```

### 4. Run batch processing
```bash
python run_app.py --mode batch
```

### 5. Launch Streamlit UI
```bash
streamlit run run_app.py -- --mode streamlit
```

---

## Sample Output
```
Summary:
- Aircraft: Cessna 172
- Location: San Diego, CA
- Event: Engine failure shortly after takeoff
- Outcome: Emergency landing

Classification:
- Root Cause: Mechanical Failure
- Severity: Medium
- Confidence: 0.87
```

---

## Author
**Hugo Villafana Ramos**

---

## Submission
This is my final submission for the GenAI Practicum – Data Scientist Track.
Please evaluate the folder:
```
Hugo_GenAITrack2_FinalAssessment
```
Thank you!
