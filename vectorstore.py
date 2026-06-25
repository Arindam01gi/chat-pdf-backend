import chromadb

client = chromadb.PersistentClient(path='./chroma_data')

def get_or_create_collection(name:str):
    return client.get_or_create_collection(name)



def store_chunks(collection_name:str,chunks:list[dict],vectors :list[list[float]] ):
    collection = get_or_create_collection(collection_name)
    ids = [str(c["chunk_id"]) for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [{"page" : c["page"]} for c in chunks]

    collection.add(
        ids=ids,
        embeddings=vectors,
        documents=documents,
        metadatas=metadatas,
    )

    return collection.count()