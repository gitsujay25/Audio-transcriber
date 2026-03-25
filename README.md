# 🎧 Audio Transcriber

A Python-based audio-to-text transcription pipeline with **speaker diarization**, **subtitle generation** and **transcript generation**.

## 📌 Overview  
This is a **Conversational RAG** built with completely opensource LLM models and Embedding models, which can be easily generalized to even powerful models if the
hardware resources are available. The primary focus of this RAG is to focus on the building a RAG application specifically for documents in French language. Although this model can also be used for documents in English.

---

## 🚀 Features

- 🎙️ Speech-to-text transcription using Whisper
- 🧠 Word-level alignment with WhisperX
- 👥 Speaker diarization using Pyannote
- ✂️ Intelligent audio chunking based on silence
- 📄 Clean transcript generation with speaker labels
- ⚡ GPU acceleration support (CUDA / MPS / CPU)
- 🧩 Modular and extensible architecture

--- 

## 📁 Project Structure
```text
project_root/
│
├── config/                   # Configuration files (YAML)
├── src/
│ └── transcriber_app/
│     ├── main.py             # CLI entry point
│     ├── pipeline.py         # Core transcription pipeline
│     ├── audio_utils.py      # Audio preprocessing & chunking
│     ├── subtitle_utils.py   # Subtitle & transcript formatting
│     ├── logging_config.py   # Logging setup & config loader
│     ├── paths.py            # Centralized paths
│
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/audio-transcriber.git
cd audio-transcriber
```
### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -e .
```

## 🔐 Environment Setup

Create a .env file:

```bash
PYANNOTE_TOKEN=your_huggingface_token
LOG_LEVEL=INFO
```
> You need a Hugging Face token to use Pyannote diarization.

## ▶️ Usage (CLI)

**With default config:**
```bash
transcriber --audio path/to/audio.wav
```
**With custom config:**
```bash
transcriber --audio path/to/audio.wav --config config.yaml
```

## ⚙️ Configuration
Example config.yaml:
```YAML
model:
  name: medium
  language: en

audio:
  chunk_size_ms: 50000
  silence_threshold: -40
  min_silence_len: 700

subtitles:
  max_char: 42

output:
  folder: output_run
  ```

## 📤 Output

**The pipeline generates:**
- pre_transcript.json → raw segments with timestamps
- subtitles.srt → subtitle file
- transcript.txt → speaker-separated transcript

## 🐳 Docker Usage

### 1. Build image
```bash
docker build -t audio-transcriber .
```

### 2. Run container
```bash
docker run --rm \
  -e PYANNOTE_TOKEN=your_token \
  -v $(pwd)/output:/app/output \
  audio-transcriber \
  --audio sample.wav
```

## 🧠 Architecture
This project follows a modular design:
- Pipeline → Core processing (transcription + alignment + diarization)
- Utils → Audio processing & formatting
- CLI (main.py) → Entry point & orchestration

## ⚡ Performance Notes
- Uses GPU when available (CUDA / MPS)
- Audio chunking improves handling of long files
- Diarization is performed on full audio for consistency

## 📦 Tech Stack
- Whisper / WhisperX
- Pyannote Audio
- PyTorch
- Pydub
- SoundFile
- Python 3.10

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repository, open issues, or submit pull requests.

## 📬 Contact
For questions or suggestions:
- Author: Sujay Ray
- GitHub: https://github.com/gitsujay25
- Linkdin: https://www.linkedin.com/in/sujayray92/