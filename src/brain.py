"""
Milestone 3 - the brain: send the question to the local LLM (Ollama).

Ollama runs as a service at localhost:11434. We POST a question,
it thinks, it returns JSON where the answer text lives in ["result"].
"""

import time
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"

# A proxy is configured on my machine (127.0.0.1:3213). For LOCAL
# servers like Ollama we must bypass it, so trust_env=False tells
# requests: "ignore system proxy settings, connect directly."
_session = requests.Session()
_session.trust_env = False

def think(question: str) -> str:
    """Ask the local LLM a question; return its answer text."""
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": f"Answer in one or two short sentences: {question}",
            "stream": False,        # wait for the WHOLE answer, one JSON object
        },
        timeout=120,
    )
    data = resp.json()
    # The response's only LONG string is the answer itself.
    # Everything else is metadata: model name, timestamps (short strings),
    # numbers, and the 'context' token-id list.
    # So: pick the Longest string value. Works on any Ollama version.
    strings = [v for v in data.values() if isinstance(v, str)]
    return max(strings, key=len).strip()



if __name__ == "__main__":
    q = "Why is the sky blue?"
    start = time.perf_counter()
    print("Q:", q)
    print("A:", think(q))
    print(f"({time.perf_counter() - start:.1f}s)")

