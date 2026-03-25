import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from dotenv import load_dotenv
load_dotenv()

import argparse
from transcriber_app.logging_config import setup_logging
from transcriber_app.transcription import run_transcription

logger = setup_logging()

def main():
    parser = argparse.ArgumentParser(description="Audio to subtitles pipeline")

    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path or filename of config file"
    )

    parser.add_argument(
        "--audio",
        type=str,
        default="sample.wav",
        help="Path to audio file"
    )

    args = parser.parse_args()

    try:
        result = run_transcription(
            audio_path=args.audio,
            config_path=args.config
        )

        logger.info("\n"
            "--------------------------------------------------\n"
            "Transcription complete. Files generated:\n"
            f"{result['json']}\n"
            f"{result['srt']}\n"
            f"{result['txt']}\n"
            "--------------------------------------------------"
        )
    except Exception as e:
        logger.error(f"[FATAL] Pipeline failed: {e}")

if __name__ == "__main__":
    main()