import pytest
import os
from transcriber_app.audio_utils import load_audio, chunk_audio
from pydub import AudioSegment
import tempfile

def test_chunking_creates_chunks():
    # Create a 5-second silent audio for testing
    audio = AudioSegment.silent(duration=5000)
    with tempfile.TemporaryDirectory(prefix="Testing_chunks_") as temp_dir:
        chunks = chunk_audio(audio, output_dir=temp_dir, min_silence_len=100, chunk_size=2000)
        
        # Check if chunks were created
        assert(len(chunks)) > 0
        # Check if each chunk is AudioSegment
        for path in chunks:
            assert isinstance(path, str)
            assert os.path.exists(path)