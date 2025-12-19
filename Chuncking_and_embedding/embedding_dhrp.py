from c_e_utils import PDF_FILE_PATH,embedding_model,chroma_client,COLLECTION_NAME
from chunking_dhrp import extract_and_chunk_pdf


#Creating chuncks from PDH
created_chunks = extract_and_chunk_pdf(PDF_FILE_PATH)

chunks = [chunk['text'] for chunk in created_chunks]
print('Chunks extracted')

metadatas = [{'source' : chunk['file_name'], 'page': chunk['page']} for chunk in created_chunks]
print('Metadata extracted')

ids = [str(i) for i in range(len(created_chunks))]
print('IDs created')


sentence_embeddings = embedding_model.encode(chunks)
print('Embeddings created')


dhrp_collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"description": "Embeddings of DHRP documents"}
)
print('Collection created or retrieved')


dhrp_collection.add(
    embeddings=sentence_embeddings,
    documents=chunks,
    metadatas=metadatas,
    ids=ids
)

print('Chunks added to ChromaDB collection')
print(f"Total documents in the collection: {dhrp_collection.count()}")
print('Process completed successfully.')