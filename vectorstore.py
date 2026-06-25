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


def search_chunks(collection_name:str,query_vector:list[float],top_k:int=5):
    collection = get_or_create_collection(collection_name)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )

    return {
        "documents": results["documents"][0],
        "pages": [m["page"] for m in results["metadatas"][0]],
    }