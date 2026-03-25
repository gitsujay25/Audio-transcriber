from transcriber_app.utils import generate_subtitles, generate_transcript

def test_generate_subtitles_and_transcript():
    segments = [
        {"start": 0, "end": 2, "text": "Hello  world", "speaker": "Speaker 1"},
        {"start": 3, "end": 5, "text": "How are you", "speaker": "Speaker 2"}
    ]

    srt_entries = generate_subtitles(segments, 42)
    transcript = generate_transcript(segments)

    # Check SRT structure
    assert all("index" in e and "start" in e and "end" in e and "text" in e for e in srt_entries)

    # Check transcript sstructure
    assert all(len(t) == 3 for t in transcript)