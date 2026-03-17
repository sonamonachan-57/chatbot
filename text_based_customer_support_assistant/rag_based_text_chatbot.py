import os
import sys
venv_path = '/home/sona-inc5619/mp_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)


import ollama
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load manual
with open("product_manual.txt", "r", encoding="utf-8") as f:
    manual_text = f.read()

manual_sections = manual_text.split("\n\n")

# Create embeddings
embeddings = embed_model.encode(manual_sections)
embeddings = np.array(embeddings).astype('float32')

# FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Retrieval function
def retrieve_answer(query, k=3):
    query_embedding = embed_model.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, k)
    return "\n".join([manual_sections[i] for i in indices[0]])

# Chat loop
history = []
model = "llama3"

while True:
    prompt = input("You: ").strip()

    if prompt.lower() in ('exit', 'quit'):
        print("Have a nice day!")
        break

    retrieved_section = retrieve_answer(prompt)

    advanced_prompt = f"""
    You are a regional customer support assistant.

    Use ONLY the product manual info.

    If not found, say:
    "I am transferring you to a human support agent."

    Product Info:
    {retrieved_section}

    User Question:
    {prompt}
    """

    message = {"role": "user", "content": advanced_prompt}
    history.append(message)

    response = ollama.chat(model=model, messages=history)
    bot_reply = response["message"]["content"]

    print("Bot:", bot_reply)

    history.append({"role": "assistant", "content": bot_reply})