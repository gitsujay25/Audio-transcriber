import os
import json
import logging
from pathlib import Path
import tempfile

from transcriber_app.pipeline import AudioTranscriptionPipeline
import transcriber_app.utils as utl
from transcriber_app.paths import OUTPUT_DIR
from transcriber_app.logging_config import load_config

def run_transcription(audio_path: str, config_path: str = None):
    logger = logging.getLogger("audio_pipeline.transcription")
    config = load_config(config_path)

    pyannote_token = os.getenv("PYANNOTE_TOKEN")
    if not pyannote_token:
        raise ValueError("PYANNOTE_TOKEN not found in environment variables")
    
    audio_file_path = Path(audio_path)

    # ------------------------ Output folder ------------------------
    output_name = config.get("output", {}).get("folder")
    if output_name:
        output_folder = OUTPUT_DIR / output_name
    else:
        output_folder = OUTPUT_DIR / f"output_{audio_file_path.stem}"
    output_folder.mkdir(parents=True, exist_ok=True)

    #  ------------------------ Initialize pipeline ------------------------
    pipeline = AudioTranscriptionPipeline(
        model_config=config["model"],
        pyannote_token=pyannote_token
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        preprocessed_dir = Path(temp_dir) / "preprocessed_audio"
        # ------------------------ Preprocess audio ------------------------
        logger.info("Audio processing started...")
        audio_file=utl.preprocess_audio(audio_file_path, preprocessed_dir)
        logger.info("Audio processed. Starting transcription...")

        #  ------------------------ Run transcription ------------------------
        all_segments = pipeline.transcribe_audio(str(audio_file))

        # ------------------------ Speaker allocation ------------------------
        try:
            all_segments_speaker = pipeline.speaker_allocation(
                str(audio_file),
                all_segments
            )
        except Exception as e:
            logger.warning(f"[WARNING] Speaker allocation failed: {e}")
            for seg in all_segments["segments"]:
                seg["speaker"] = "UNKNOWN"
            all_segments_speaker = {"segments": all_segments["segments"]}

    # ------------------------ Export raw JSON ------------------------
    try:
        json_path = output_folder / "pre_transcript.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(all_segments_speaker, f, indent=2)
    except Exception as e:
        logger.error(f"[ERROR] Failed to write JSON: {e}")

    # ------------------------ Generate SRT ------------------------
    try:
        srt_entries = utl.generate_subtitles(
            all_segments_speaker,
            config["subtitles"]["max_char"],
        )
        srt_path = output_folder / "subtitles.srt"
        utl.export_srt(srt_entries, filename=str(srt_path))
    except Exception as e:
        logger.error(f"[ERROR] Subtitle generation failed: {e}")

    # ------------------------ Generate ------------------------
    try:
        transcipt = utl.generate_transcript(all_segments_speaker)
        txt_path = output_folder / "transcript.txt"
        utl.export_transcript(transcipt, filename=str(txt_path))
    except Exception as e:
        logger.error(f"[ERROR] Transcript generation failed: {e}")

    return {
        "json": str(json_path),
        "srt": str(srt_path),
        "txt": str(txt_path),
    }