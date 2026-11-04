"""
Milestone 3 - the mouth: speak text aloud using Windows' built-in voices.

pyttsx3 is OFFLINE text-to-speech: no internet, no API, it borrows
the speech voices already installed with Windows.
"""

import pyttsx3

# The speech engine is created ONCE at import time.
# Creating it inside speak() would add setup Lag before every sentence.
_engine = pyttsx3.init()


def speak(text: str) -> None:
    """Speak text out loud, blocking until finished."""
    _engine.say(text)       # queue the sentence
    _engine.runAndWait()    # actually say it, wait untill done


if __name__ == "__main__":
    speak("Hello! I am your local voice assistant.")