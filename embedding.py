import os
from google import genai
from dotenv import load_dotenv


load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
embedding_model = os.environ["EMBEDDING_MODEL"]


def embed_text(text:list[str]) -> list[list[float]]:
    """
    Takes a list of strings, returns a list of embedding vectors (same order).
    """

    results = client.models.embed_content(
        models = embedding_model,
        contents=text
    )

    return results

