import sys
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).parent.parent))

DB_PATH = r"C:\Users\rauna\projects\My Projects\IPO_Checker\ChromaDB"
chroma_client = chromadb.PersistentClient(path=DB_PATH)

COLLECTION_NAME = 'dhrp_embeddings_collection'

#DHRP PDF FILE PATH
PDF_FILE_PATH = r'C:\Users\rauna\projects\My Projects\IPO_Checker\DRHP'

EMBEDDING_MODEL = 'multi-qa-mpnet-base-dot-v1'
# DB_PATH = r"C:\Users\rauna\projects\My Projects\IPO_Checker\ChromaDB"
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

