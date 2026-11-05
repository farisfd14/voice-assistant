# ================================================================
# brain.py - the assistant's BRAIN (Milestone 3)
#
# Sends the transcribed question to a local LLM through Ollama.
# Ollama is a background service running on YOUR computer a
# Localhost:11434 - no internet needed, no API key, no cost.
#
# Two hard-won lessons are baked into this file:
#  1. trust_env=False -> bypasses the machine proxy so that
#     Localhost traffic is not routed through 127.0.0.1:3213
#     (we debugged this for an entire evening!)
#  2. pick_answer()   -> we never hardcode a JSON field name
#     like "result", because Ollama renames fields between
#     versions and hardcoding caused a KeyError crash.
# ================================================================

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"

# One session reused for every request.
# trust_env=False tells requests: "ignore the system proxy settings".
# Without this, requests tried to send even localhost traffic
# through the machine's proxy (127.0.0.1:3213) and everything broke.
_session = requests.Session()
_session.trust_env = False


def pick_answer(data: dict) -> str:
    """The answer is the longest string in Ollama's JSON response.

    We never hardcode a field name (like "result" or "response")
    because Ollama renames fields between versions.

    Assumption: the answer is a full sentence, so it is always
    longer than metadata strings like the model name.
    In practice this holds; if Ollama ever returns a one-word
    answer, this heuristic would need a smarter filter.
    """
    strings = [v for v in data.values() if isinstance(v, str)]
    return max(strings, key=len).strip()


def think(question: str) -> str:
    """Ask the local LLM a question; return its answer text."""
    resp = _session.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": f"Answer in one or two short sentences: {question}",
            "stream": False,        # wait for the WHOLE answer, one JSON object
        },
        timeout=120,
    )
    data = resp.json()
    return pick_answer(data)    # robust: no hardcoded field name


if __name__ == "__main__":
    print(think("What is the capital of Indonesia?"))