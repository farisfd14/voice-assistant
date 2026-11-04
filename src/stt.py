"""
Milestone 2 - speech-to-text (whisper), everything reusing ever from the Latency Lab.
"""

import time
import whisper

model = whisper.load_model("tiny", device="cpu")    # Loaded ONCE at import

def transcribe(wav_path: str) -> str:
    """Turn a wav file into text. Returns the transcript."""
    start = time.perf_counter()
    result = model.transcribe(wav_path, fp16=False)
    elapsed = time.perf_counter() - start
    print(f"$TT: {elapsed:.2f}s")
    return result["text"].strip()


if __name__ == "__main__":
    print("You said:", transcribe("my_question.wav"))