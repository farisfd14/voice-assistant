"""
The full voice assistant pipeline, with per-stage latency measurement.

    mic -> record -> whisper STT -> ollama LLM -> pyttsx3 TTS -> speaker
    [t1]    [t2]           [t3]         [t4]            TOTAL

Run: py src/assistant.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_vad import record_until_silence  # stage 1
from stt import transcribe          # stage 2 (whisper model Loads at import)
from brain import think             # stage 3
from mouth import speak             # stage 4

WAV_PATH = "my_question.wav"


def main() -> None:
    # --- stage 1: record -----------------------------------------------
    t0 = time.perf_counter()
    seconds = record_until_silence("my_question.wav")
    t_record = time.perf_counter() - t0

    # --- stage 2: speech -> text ---------------------------------------
    t0 = time.perf_counter()
    question = transcribe(WAV_PATH)
    t_stt = time.perf_counter() - t0
    print(f"\nYou said: {question}")

    # --- stage 3: the brain answers -------------------------------------
    t0 = time.perf_counter()
    answer = think(question)
    t_think = time.perf_counter() - t0

    # --- stage 4: speak it aloud -----------------------------------------
    t0 = time.perf_counter()
    speak(answer)
    t_speak = time.perf_counter() - t0

    # --- Latency dashboard ------------------------------------------------
    total = t_record + t_stt + t_think + t_speak
    print("\n=== Latency dashboard (seconds) ===")
    print(f"{'stage':<8}{'time':>8}")
    print(f"{'record':<8}{t_record:>8.2f}")
    print(f"{'stt':<8}{t_stt:>8.2f}")
    print(f"{'think':<8}{t_think:>8.2f}")
    print(f"{'speak':<8}{t_speak:>8.2f}")
    print(f"{'TOTAL':<8}{total:>8.2f}")


if __name__ == "__main__":
    main()