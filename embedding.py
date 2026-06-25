import os
from google import genai
from dotenv import load_dotenv
from google.genai import types


load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
embedding_model = os.environ["EMBEDDING_MODEL"]



def embed_text(text:list[str]) -> list[list[float]]:
    """
    Takes a list of strings, returns a list of embedding vectors (same order).
    """

    results = client.models.embed_content(
        model = embedding_model,
        contents=text
    )

    return [embedding.values for embedding in results.embeddings]


def embed_texts_batched(texts: list[str], batch_size: int = 100) -> list[list[float]]:
    all_vectors = []
    for text in texts:
        result = client.models.embed_content(
            model=embedding_model,
            contents=text,   
        )
        all_vectors.append(result.embeddings[0].values)
    return all_vectors

def embed_query(text:str) ->list[float]:
    result = client.models.embed_content(
        model=embedding_model,
        contents=text,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
    )
    return result.embeddings[0].values


