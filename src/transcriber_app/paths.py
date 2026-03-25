from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Common directories
EX_CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_DIR = PROJECT_ROOT / "src" / "transcriber_app" / "config"
LOG_DIR = PROJECT_ROOT / "logs"
OUTPUT_DIR = PROJECT_ROOT / "output"