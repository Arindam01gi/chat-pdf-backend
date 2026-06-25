import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
CHAT_MODEL = os.environ["CHAT_MODEL"]

def build_prompt(question:str ,context_chunks:list[str] )->str:
    context = "\n\n---\n\n".join(context_chunks)
    return f"""You are answering questions based ONLY on the context below, taken from a PDF document.
If the answer isn't in the context, say "I couldn't find that in the document" — do not guess.

Context:{context}
Question: {question}
Answer:"""


def generate_answer(question:str,context_chunks:list[str]) ->str:
    prompt = build_prompt(question=question,context_chunks=context_chunks)
    print("----- PROMPT SENT TO GEMINI -----")
    print(prompt)
    print("----------------------------------")
    response = client.models.generate_content(
        model=CHAT_MODEL,
        contents=prompt,
    )

    return response.text