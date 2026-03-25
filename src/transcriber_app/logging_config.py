import os
import logging
import yaml
from pathlib import Path
from transcriber_app.paths import LOG_DIR, CONFIG_DIR, EX_CONFIG_DIR

def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logger = logging.getLogger("audio_pipeline")
    logger.setLevel(log_level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s ",
        "%Y-%m-%d %H:%M:%S"
    )

    # File loading
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(LOG_DIR / "pipeline.log")
    file_handler.setFormatter(formatter)

    #Console logging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger

# -------------------------------------------------------------
# configure parameter loading
# -------------------------------------------------------------
def load_config(config_path: str = None):
    logger = logging.getLogger("audio_pipeline")
    EX_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        if config_path and Path(config_path).exists():
            path = Path(config_path)
            logger.info(f"Loding config from {path}")
        elif config_path:
            ex_path = EX_CONFIG_DIR / config_path
            if ex_path.exists():
                path = ex_path
                logger.info(f"Loding config from {path}")
            else:
                logger.error(f"NO config file found in {EX_CONFIG_DIR}")
        else:
            path = CONFIG_DIR / "config_default.yaml"
            logger.info(f"Loading default config: {path}")

        with open(path, "r") as f:
            config = yaml.safe_load(f)

        if config is None:
            raise ValueError("Config file is empty")
            
        return config
    
    except FileNotFoundError:
        logger.error(f"Config file not found: {path}")
        raise
    
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        raise