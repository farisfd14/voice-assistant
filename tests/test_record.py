import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

def test_constants():
    import record
    import record
    assert record.SAMPLE_RATE == 16000 # Whisper expects 16kHz audio
    assert record.SECONDS == 6         # fixed recording length for v1