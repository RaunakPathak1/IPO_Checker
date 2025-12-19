##query_vector_database_tool (RAG)
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)


open_router_key = os.getenv("OPENROUTER_API_KEY", "")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-3-flash-preview"
openrouter = OpenAI(api_key=open_router_key, base_url=BASE_URL)

def call_llm(MODEL, system_message, user_message):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    response = openrouter.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content



## vector DB utilities for DHRP documents
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
DB_PATH = r"C:\Users\rauna\projects\My Projects\IPO_Checker\ChromaDB"
chroma_client = chromadb.PersistentClient(path=DB_PATH)
COLLECTION_NAME = 'dhrp_embeddings_collection'
EMBEDDING_MODEL = 'multi-qa-mpnet-base-dot-v1'
embedding_model = SentenceTransformer(EMBEDDING_MODEL)
dhrp_doc_collection = chroma_client.get_collection(COLLECTION_NAME)


