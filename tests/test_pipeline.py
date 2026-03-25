import pytest
from unittest.mock import patch, MagicMock
from transcriber_app.pipeline import AudioTranscriptionPipeline

# Use a silent audio segment for testing
from pydub import AudioSegment
import tempfile
import os

@pytest.fixture
def silent_audio_file():
    # Create a temporary 2-second silent audio
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    audio = AudioSegment.silent(duration=2000)
    audio.export(temp_file.name, format="wav")
    yield temp_file.name
    os.remove(temp_file.name)

# Mock Whisper and Pyannote heavy models
@patch("transciber_app.pipeline.whisper.load_model")
@patch("transciber_app.pipeline.whisperx.load_align_model")
@patch("transciber_app.pipeline.Pipeline.from_pretrained")
def test_run_pipeline(mock_diarize, mock_align_model, mock_whisper_model, silent_audio_file):
    # Mock return values
    mock_whisper_instance = MagicMock()
    mock_whisper_instance.transcribe.return_value = {"segments": [{"start": 0, "end": 2, "text": "Hello"}]}
    mock_whisper_model.return_value = mock_whisper_instance

    mock_align_model.return_value = (MagicMock(), {"metadata": "dummy"})

    mock_diarize_instance = MagicMock()
    mock_diarize_instance.return_value.exclusive_speaker_diarization.itertracks.return_value = [
        (MagicMock(start=0, end=2), None, "Speaker 1")
    ]
    mock_diarize.return_value = mock_diarize_instance

    pipeline = AudioTranscriptionPipeline(
        model_name="base",
        language="en",
        pyannote_token="dummy_token",
        audio_config={"chunk_size_ms": 1000}
    )

    result = pipeline.run(silent_audio_file)

    assert "segments" in result
    assert len(result["segments"]) > 0
    for seg in result["segments"]:
        assert "start" in seg and "end" in seg and "text" in seg