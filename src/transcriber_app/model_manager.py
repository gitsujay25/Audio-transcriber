import torch
import whisperx
from whisperx.diarize import DiarizationPipeline
import logging
logger = logging.getLogger("audio_pipeline.model_manager")

class LoadModels:
    _instance = None

    def __init__(self, model_config=None, pyannote_token=None):
        if LoadModels._instance is not None:
            raise Exception("LoadModels is a singleton. Use get_instance().")
        logger.info("Loading models (this may take a while)...")

        self.model_config = model_config or {}

        # Device detection
        if torch.backends.mps.is_available():
            self.device = "mps"
            temp_device="cpu"
        elif torch.cuda.is_available():
            self.device = "cuda"
            temp_device="cuda"
        else:
            self.device = "cpu"
            temp_device="cpu"
        logger.info(f"Using device: {self.device}")

        # Model parameters
        my_asr_options = {
            "temperatures": [self.model_config.get("temperatures", 0.3)],
            "initial_prompt": self.model_config.get("initial_prompt", None)
        }
        
        # Load models
        self.transcribe_model = whisperx.load_model(
            self.model_config.get("name", "medium"),
            device=temp_device,
            compute_type=self.model_config.get("compute_type", "float32"),
            language=self.model_config.get("language", None),
            asr_options = my_asr_options
        )
        # self.align_model, self.metadata = whisperx.load_align_model(
        #     language_code = self.model_config.get("language", None),
        #     device = self.device
        # )
        self.diarize_model = DiarizationPipeline(
            token=pyannote_token,
            device=self.device
        )

        LoadModels._instance = self

    @classmethod
    def get_instance(cls, model_config=None, pyannote_token=None):
        if cls._instance is None:
            if not all([model_config, pyannote_token]):
                raise ValueError("Models not initialized yet. Provide all parameters.")
            cls(model_config, pyannote_token)
        
        return cls._instance