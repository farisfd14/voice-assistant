# Sanity checks for the VAD recording configuration.
# (Actually recording needs a microphone, so we verify the MATH the
# recorder relies on: slice length, and that the silence counter
# really is ~1 seconds.)

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import record_vad


def test_slice_is_32ms():
    # 512 samples at 16 kHz must equal 0.032 s exactly
    assert record_vad.SLICE / record_vad.SAMPLE_RATE == 0.032


def test_silence_counter_is_about_one_second():
    # The stop rule waits ~1 second of silence after your last word
    seconds = record_vad.SILENCE_SLICES_TO_STOP * record_vad.SLICE / record_vad.SAMPLE_RATE
    assert 0.9 < seconds < 1.2