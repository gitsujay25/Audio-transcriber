import logging
logger = logging.getLogger("audio_pipeline.pipeline")

from transcriber_app.model_manager import LoadModels
import torch
import whisperx

class AudioTranscriptionPipeline:
    def __init__(self, model_config=None, pyannote_token=None):
        self.model_config = model_config or {}
        self.all_models = LoadModels.get_instance(
            model_config=model_config,
            pyannote_token=pyannote_token
        )
        self.transcribe_model = self.all_models.transcribe_model
        # self.align_model = self.all_models.align_model
        # self.metadata = self.all_models.metadata
        self.diarize_model = self.all_models.diarize_model
        self.device = self.all_models.device

    def speaker_allocation(self, audio_file: str, segments):
        logger.info("Diarization in progress ...")
        with torch.no_grad():
            diarization = self.diarize_model(
                audio_file,
                min_speakers=self.model_config.get("min_speakers", None),
                max_speakers=self.model_config.get("max_speakers", None)
            )

        segment_speaker = whisperx.assign_word_speakers(
            diarization,
            segments
        )

        filtered_segments = [
            {
                "start": s["start"],
                "end": s["end"],
                "text": s["text"],
                "speaker": s.get("speaker", "UNKNOWN") # .get() prevents crashes if speaker is missing
            }
            for s in segment_speaker["segments"]
        ]

        return filtered_segments

    def transcribe_audio(self, audio_file: str):
        try:
            with torch.no_grad():
                segments = self.transcribe_model.transcribe(
                    audio_file,
                    batch_size=self.model_config.get("batch_size", 16),
                    print_progress=True
                )
        except RuntimeError as e:
            logger.error(f"[ERROR] Transcript failed for  {audio_file}: {e}")
            segments = {"segments": []} # skip this chunk

        try:
            if self.model_config["language"]==None:
                align_model_langugae = segments["language"]
            else:
                align_model_langugae=self.model_config["language"]

            align_model, metadata = whisperx.load_align_model(
                language_code = align_model_langugae,
                device = self.device
            )
            with torch.no_grad():
                segments_aligned = whisperx.align(
                    segments["segments"],
                    align_model,
                    metadata,
                    audio_file,
                    device=self.device
                )
        except RuntimeError as e:
            logger.error(f"[ERROR] Alignment failed for  {audio_file}: {e}")
            segments_aligned = {"segments": segments["segments"]}

        return segments_aligned