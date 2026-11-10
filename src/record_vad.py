"""
Milestone 1 - VAD recording: stop guessing, start listening.

v1 (record.py) recorded a FIXED 6 seconds, whether you spoke for
2 seconds or 10. This file replaces that guess with VAD:

    silero-vad is a tiny neural network. Feed it a 32 ms slice of
    audio, and it returns a probability: "someone is speaking" (high)
    or "silence" (low).

The recording rule (this is the whole trick):
  1. Listen in a live stream of 32 ms slices.
  2. Slice says SPEECH  -> mark that speech started, keep the slice.
  3. Slice says SILENCE -> if speech already started, count it;
    after ~1 second of consecutive silence, the user is done
    talking -> STOP recording.
  4. Never record longer than max_seconds (safety_net)

At 16 kHz, a 512-samole slice IS 32 ms: 512 / 16000 = 0.032 s.
"""

import numpy as np
import sounddevice as sd
import soundfile as sf
import torch
from silero_vad import load_silero_vad

SAMPLE_RATE = 16000         # whisper's rate, and silero-vad expects this
SLICE = 512                 # samples per VAD slice = 32 ms

# ~1 second od silence = how many consecutive silent slices
SILENCE_SLICES_TO_STOP = 31

# Load the VAD model ONCE at import (like we load whisper in stt.py)
vad_model = load_silero_vad(onnx=True)


def record_until_silence(path="my_question.wav", max_seconds=15):
    """Record only while the user speaks (+1s trailing silence).

    Returns the recording length in seconds so the caller can
    measure how much time VAD saved compared to a fixed recording.
    """
    print("Listening... speak now.")

    kept_slices = []            # audio slices we decide to keep
    speech_started = False
    silent_in_a_row = 0
    max_slices = int(max_seconds * SAMPLE_RATE / SLICE)

    # InputStream reads the microphone LIVE, slice by slice,
    # instead of sd.rec() which blocks for a fixed duration.
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1,
                        dtype="float32", blocksize=SLICE) as stream:
        for _ in range(max_slices):
            data, _ = stream.read(SLICE)                    # one 32 ms slice
            tensor = torch.from_numpy(data.flatten())

            # The network's verdict for this slice (0.0 .. 1.0)
            speech_prob = vad_model(tensor, SAMPLE_RATE).item()

            if speech_prob > 0.5:
                speech_started = True
                silent_in_a_row = 0
            elif speech_started:
                silent_in_a_row += 1

            if speech_started:
                kept_slices.append(data)    # only keep speech + trailing silence

            # STOP condition: speech happened, then ~1s of silence
            if speech_started and silent_in_a_row > SILENCE_SLICES_TO_STOP:
                break

    audio = np.concatenate(kept_slices)
    seconds = len(audio) / SAMPLE_RATE
    sf.write(path, audio, SAMPLE_RATE)
    print(f"Recorded {seconds:.2f}s -> saved to {path}")
    return seconds


if __name__ == "__main__":
    # Standalone test: speak a shor question, stay silent, watch it stop by itself
    record_until_silence("vad_test.wav")