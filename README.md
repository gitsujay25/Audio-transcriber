# 🎧 Audio Transcriber

A modular Python-based **audio-to-text transcription system** with **speaker diarization**, **word-level alignment** and **subtitle generation**.

## 📌 Overview  
This project implements an end-to-end audio processing pipeline that:

- Converts raw audio into clean, standardized format
- Transcribes speech using **Whisper (via WhisperX)**
- Aligns timestamps at the word level
- Performs **speaker diarization** (who spoke when)
- Generates:
  - Structured JSON output
  - Subtitles (`.srt`)
  - Human-readable transcripts (`.txt`)

The system is designed with **modularity, scalability, and reproducibility** in mind.

---

## 💡 Why This Project?

Most transcription tools focus only on converting speech to text.  
This project goes further by solving real-world challenges:

- **Who spoke when?** → Speaker diarization
- **Precise timing?** → Word-level alignment
- **Readable output?** → Structured transcripts + subtitles
- **Scalability?** → Modular and configurable pipeline

The goal was to design a system that is:
- Production-oriented
- Extensible to larger models
- Easy to integrate into downstream applications (e.g., medical report from conversation, meeting summarization, RAG systems)

This reflects real-world ML system design beyond just model usage.

---

## 🎬 Example Output

**Input Audio:**
- 2 speakers conversation: [Tête à tête exceptionnel avec Matthieu Ricard](https://www.youtube.com/watch?v=hxEkvQ1ILB4&t=15s)

**Generated Transcript:**

```text
SPEAKER_01: (00:00:04)
  Bonjour et bienvenue dans Faut pas croire. C'est une rencontre exceptionnelle que nous vous proposons, celle avec le moine bouddhiste français Mathieu Ricard, figure incontournable du bouddhisme depuis plus de 50 ans. Il publie enfin ses mémoires intitulées « Carnets d'un moine errant » et c'est à la Société de lecture de Genève que nous le recevons.

SPEAKER_01: (00:00:29)
  Bonjour, Mathieu Ricard.

SPEAKER_02: (00:00:31)
  Bonjour, chérie.

SPEAKER_01: (00:00:32)
  Merci beaucoup d'être avec nous ici, à Genève. Vous êtes dans cette ville dans le cadre du programme à ciel ouvert de l'Université de Genève. Et vous êtes aussi ici pour présenter vos mémoires, un pavé assez lourd de plus de 800 pages. Ces mémoires, elles s'intitulent « Mathieu Ricard, carnet d'un moine errant ». Alors on va bien sûr parler de votre vie, mais d'abord, une question. Est-ce que c'est pas un peu paradoxal pour un homme comme vous qui avez passé votre vie à laisser de côté votre ego, d'écrire et de publier ses mémoires?

SPEAKER_02: (00:01:05)
  Précisément, c'est un peu ce que je dis au début du livre. Ce ne sont pas des mémoires ordinaires pour...
  ```

---

## 🧩 System Flow

          ┌──────────────┐
          │  Input Audio │
          └──────┬───────┘
                 │
                 ▼
        ┌──────────────────┐
        │  Preprocessing   │
        │  (Mono, 16kHz)   │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │  Transcription   │
        │  (WhisperX)      │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │    Alignment     │
        │   (Word-level)   │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │   Diarization    │
        │    (Pyannote)    │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Post-processing  │
        │ (Merge + Format) │
        └────────┬─────────┘
                 │
     ┌───────────┼────────────┐
     ▼           ▼            ▼
 JSON Output   SRT File   TXT Transcript

 ---

## 🚀 Features

- 🎙️ Speech-to-text transcription using Whisper (via Whisperx)
- 🧠 Word-level alignment for precise timestamps
- 👥 Speaker diarization using Pyannote
- ⚡ GPU acceleration (CUDA / MPS / CPU support)
- 🔄 Config-driven pipeline (YAML-based)
- 🧩 Modular architecture (pipeline, models, utils separated)
- 📄 Export formats:
  - JSON (raw structured output)
  - SRT (subtitles)
  - TXT (speaker-separated transcript)

--- 

## 🏗️ Architecture

The system is divided into clear components:

- **CLI (`main.py`)**
  - Entry point for running the pipeline

- **Pipeline (`pipeline.py`)**
  - Handles transcription, alignment, and diarization

- **Model Manager (`model_manager.py`)**
  - Singleton pattern for efficient model loading
  - Loads Whisper + Pyannote models once

- **Utilities (`utils.py`)**
  - Audio preprocessing (resampling, mono conversion)
  - Subtitle formatting & export
  - Transcript generation

- **Config System (`config.yaml`)**
  - Fully configurable model and output settings

  --- 

## 📁 Project Structure
```text
project_root/
│
├── config/                   # Configuration files (YAML)
│   └── config.yaml
│
├── src/
│   └── transcriber_app/
│       ├── main.py             # CLI entry point
│       ├── pipeline.py         # Core transcription pipeline
│       ├── model_manager.py    # Model loading (singleton)
│       ├── transcription.py    # Orchestration layer
│       ├── utils.py            # Audio + formatting utilities
│       ├── logging_config.py   # Logging + config loader
│       └── paths.py            # Centralized path management
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

# Install the packages manually
pip install whisperx
pip install dotenv
pip install pydub

# Or you can use the dependencies in pyproject.toml file
# If you already installed the packages manually, still
# run the following command to build the transcriber_app 
pip install -e .
```

## 🔐 Environment Setup

Create a .env file:

```bash
PYANNOTE_TOKEN=your_huggingface_token
LOG_LEVEL=INFO
```
> You need a Hugging Face token for speaker diarization using Pyannote.

## ▶️ Usage (CLI)

**Run with default config:**
```bash
transcriber --audio path/to/audio.wav
```
**With custom config:**
```bash
transcriber --audio path/to/audio.wav --config config/config.yaml
```

## ⚙️ Configuration
Example config.yaml:
```YAML
model:
  name: medium
  language: en
  min_speaker: 2
  max_speaker: 2
  batch_size: 16
  temperatures: 0.3
  initial_promp: A conversation between doctor and patient
  compute_type: float32

subtitles:
  max_char: 42

output:
  folder: output_run
```

## 📤 Output

**The pipeline generates:**
- pre_transcript.json → Raw segments with timestamps and speakers
- subtitles.srt → Subtitle file
- transcript.txt → Clean speaker-separated transcript

## 🐳 Docker Usage

### 1. Build image
```bash
docker build -t audio-transcriber .
```

### 2. Run container
```bash
docker run --rm \
  -e PYANNOTE_TOKEN=your_token \
  -v $(pwd):/app \
  audio-transcriber \
  --audio sample.wav
```

## 📦 Tech Stack
- Whisper / WhisperX
- Pyannote Audio
- PyTorch
- Pydub
- Python 3.10

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repository, open issues, or submit pull requests.

## 📬 Contact
For questions or suggestions:
- Author: Sujay Ray
- GitHub: https://github.com/gitsujay25
- Linkdin: https://www.linkedin.com/in/sujayray92/