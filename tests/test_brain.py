# Smoke tests for the answer-extraction logic.
# These run WITHOUT Ollama, microphone, or speakers -
# that's the whole point of pulling pick_answer out of think().

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from brain import pick_answer


def test_picks_the_longest_string():
    # Normal case: a REAL answer is a full sentence,
    # which is always longer than the model name "llama3.2:1b".
    fake = {
        "model": "llama3.2:1b",
        "done": "true",
        "response": "The capital of Indonesia is Jakarta."
    }
    assert pick_answer(fake) == "The capital of Indonesia is Jakarta."


def test_survives_a_renamed_field():
    # Ollama renamed its answer field in 2026.
    # This test proves we do not depend on ANY field name.
    fake = {"model": "llama3.2:1b", "some_future_field": "Jakarta is the capital of Indonesia."}
    assert pick_answer(fake) == "Jakarta is the capital of Indonesia."


def test_ignores_non_string_values():
    # Numbers and booleans in the response must not crash the extractor
    fake = {
        "model": "llama3.2:1b",
        "total_duration": 4123456789,
        "reply": "I have finished processing your request.",
    }
    assert pick_answer(fake) == "I have finished processing your request."