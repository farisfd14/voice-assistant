"""
Milestone 1/4 - record speech from the microphone.

Refactored from a script into a FUNCTION so assistant.py can import it
without triggering a recording at import time.
"""

import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000     # samples per second (Whisper's native rate)
SECONDS = 6             # how Long to listen

def record_question(path: str = "my_question.wav") -> None:
    """Record SECONDS of microphone audio to a wav file."""
    print(f"Recording {SECONDS}s - speak now!")
    audio = sd.rec(int(SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    sf.write(path, audio, SAMPLE_RATE)