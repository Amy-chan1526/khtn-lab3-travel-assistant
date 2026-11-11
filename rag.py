import os
import json
import requests
import numpy as np
from dotenv import load_dotenv

# Load configuration from environment
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")


def get_embedding(text: str) -> np.ndarray:
    """Fetch text embedding vector using embeddinggemma model."""
    url = f"{OLLAMA_BASE_URL}/api/embeddings"
    payload = {"model": "embeddinggemma", "prompt": text}
    
    response = requests.post(url, json=payload, timeout=15)
    if response.status_code != 200:
        raise ConnectionError(f"Ollama embedding request failed (Status {response.status_code}).")
    
    vector = response.json().get("embedding")
    return np.array(vector, dtype=np.float32)


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Compute cosine similarity between two numpy vectors."""
    dot_prod = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_prod / (norm_a * norm_b))


def load_and_embed_knowledge_base(json_path: str = "knowledge_base.json") -> list:
    """Load JSON knowledge base entries and generate their embeddings once."""
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    embedded_kb = []
    for entry in data:
        # Combine title and text for rich context embedding
        text_to_embed = f"{entry['title']}: {entry['text']}"
        entry_copy = entry.copy()
        entry_copy["embedding"] = get_embedding(text_to_embed)
        embedded_kb.append(entry_copy)
    
    return embedded_kb


def retrieve_top_k(query: str, embedded_kb: list, top_k: int = 3) -> list:
    """Find top-k entries most similar to user query based on cosine similarity."""
    query_vec = get_embedding(query)
    scored_entries = []
    
    for entry in embedded_kb:
        score = cosine_similarity(query_vec, entry["embedding"])
        scored_entries.append((entry, score))
    
    # Sort entries by score descending
    scored_entries.sort(key=lambda item: item[1], reverse=True)
    return scored_entries[:top_k]


def generate_rag_answer(query: str, retrieved_items: list, threshold: float = 0.45) -> str:
    """Generate answer with qwen3:4b using retrieved entries or declare 'I don't know'."""
    # Filter entries below relevance threshold
    valid_items = [item for item, score in retrieved_items if score >= threshold]
    
    # If no retrieved entry meets confidence score, refuse to guess
    if not valid_items:
        return "I don't know."

    # Build prompt context with strict citation instructions
    context_str = "\n".join([
        f"[{item['id']}] {item['title']}: {item['text']}"
        for item in valid_items
    ])

    prompt = f"""You are a helpful travel assistant for Ho Chi Minh City. 
Answer the question ONLY based on the provided Context below.
If the Context does not contain enough information to answer, simply respond with: "I don't know."
You MUST cite the source ID (e.g. [G01], [G05]) directly after using information from that entry.

Context:
{context_str}

Question: {query}
Answer:"""

    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": "qwen3:4b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload, timeout=120)
    if response.status_code != 200:
        raise ConnectionError("Ollama text generation service unreachable.")
    
    answer_text = response.json().get("response", "").strip()
    return answer_text if answer_text else "I don't know."