# rag_utils.py
# PURPOSE: Utilities for building and querying a FAISS/chormaDB vetor store using LangChain

## LABRARIES
import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

# Path to processed dataset
DATA_PATH = "data/processed_incidents.csv"

# Load and embed the dataset
def init_vectorstore():
    df = pd.read_csv(DATA_PATH)
    documents = []

    for _, row in df.iterrows():
        metadata = {
            "event_id": row.get("event_id"),
            "location": row.get("location"),
            "aircraft": f"{row.get('acft_make')}{row.get('acft_model')}",
            "year": row.get("acft_year"),
            "injury_severity": row.get("injury_severity")
        }
        doc = Document(page_content=row["narrative"], metadata=metadata)
        documents.append(doc)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(documents, embeddings)
    return db

# Search for similar incidents based on a query (summary or narrative)
def get_similar_cases(query, vectorstore, k=3):
    return vectorstore.similarity_search(query, k=k)
