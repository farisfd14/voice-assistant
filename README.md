# Voice Assistant (Walkie-Talkie v1)

A hands-free voice assistant that runs 100% locally:
record mic → Whisper STT → Ollama (llama3.2:1b) → pyttsx3 TTS.

## How it works
1. **Ears** (`src/record.py`) - records 6s at 16kHz with sounddevice
2. **Transcriber** (`src/stt.py`) - Whisper tiny on CPU
3. **Brain** (`src/brain.py`) - Ollama at localhost:11434
   (requests session with trust_env=False to bypass the machine proxy)
4. **Mouth** (`src/mouth.py`) - pyttsx3 offline TTS
5. `src/assistant.py` - The pipeline, with per-stage latency dashboard

## Latency breakdown (my machine)
| Stage | Time      |
| --- |-----------|
| Recording (fixed 6s) | ~6000 ms  |
| STT (Whisper tiny, CPU) | ~880 ms   |
| LLM (Ollama, self-reported) | ~4000 ms  |
| TTS | ~17000 ms |
| **Total** | ~28000 ms |

## Latency: v1 vs v2 (VAD)

| Version | Recording stage | How it knows you're done |
|---|-----------------|---|
| v1 (walkie-talkie) | ~6.0s fixed     | it doesn't — always waits 6s |
| v2 (VAD) | ~4.2s measured  | silero-vad: stops ~1s after your last word |

## Setup
1. `py - m pip install -r requirements.txt`
2. Install Ollama, then: `ollama pull llama3.2:1b`
3. Run: `py src/assistant.py`

## Requirements
Python 3.10+, ffmpeg, Ollama, Windows (pyttsx3).

## Author
Faris - built while learning AI engineering.