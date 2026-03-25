import logging
logger = logging.getLogger("audio_pipeline.utils")

import textwrap
from pydub import AudioSegment
import os
from pathlib import Path

# -------------------------------------------------------------
# Audio pre-processing
# -------------------------------------------------------------
def preprocess_audio(input_path: Path, output_dir:Path):
    try:
        if not input_path.exists():
            raise FileNotFoundError(f"File not found in {input_path}")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{input_path.stem}.wav"
        audio = AudioSegment.from_file(str(input_path))

        # Convert to mono + 16kHz always
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(output_path, format="wav")

        logger.info(f"Preprocessed audio saved at: {output_path}")
        return output_path
            
    except Exception as e:
        logger.error(f"Audio processing failed {e}")
        raise
# -------------------------------------------------------------
# Subtitle and Transcript formating and exporting
# -------------------------------------------------------------
def format_time_sec(time_sec:float) -> str:
    hours = int(time_sec//3600)
    minutes = int((time_sec % 3600)//60)
    seconds = int((time_sec % 60))
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def format_time(time_sec:float) -> str:
    ms = time_sec*1000
    hours = int(ms//3600000)
    minutes = int((ms%3600000)//60000)
    secs = int((ms%60000)//1000)
    millis = int(ms%1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def split_text(text: str, max_char=42):
    lines = textwrap.wrap(text, max_char)
    subtitles = []
    for i in range(0, len(lines), 2):
        subtitles.append("\n".join(lines[i:i+2]))
    return subtitles

def export_srt(segments:list, filename="subtitles.srt"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for entry in segments:
                f.write(f"{entry['index']}\n")
                f.write(f"{format_time(entry['start'])} --> {format_time(entry['end'])}\n")
                f.write(f"{entry['text']}\n\n")
    except Exception as e:
        logger.error(f"[ERROR] Failed to write {filename}: {e}")

def export_transcript(segments:list, filename="transcript.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for speaker, time_stamp, text in segments:
                f.write(f"{speaker}: ({time_stamp})\n  {text}\n\n")
    except Exception as e:
        logger.error(f"[ERROR] Failed to write {filename}: {e}")

# -------------------------------------------------------------
# Subtitle and Transcript Processing
# -------------------------------------------------------------
def pre_process_merging(pieces, start, end, text):
    merge_indices=[]
    for ii, piece in enumerate(pieces):
        duration = (end - start)*len(piece.split())/len(text.split())
        if duration < 1:
            merge_indices.append(ii)

    if merge_indices:
        for merge_index in reversed(merge_indices):
            if merge_index > 0:
                pieces[merge_index-1] = pieces[merge_index-1] + " " + pieces[merge_index]
                del pieces[merge_index]

    return pieces

def generate_subtitles(segments, max_char):
    srt_entries = []
    index = 1
    for seg in segments:
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()

        pieces = split_text(text, max_char)
        pieces = pre_process_merging(pieces, start, end, text)
        for piece in pieces:
            duration = (end - start)*len(piece.split())/len(text.split())
            srt_entries.append({
                "index": index,
                "start": start,
                "end": min(start + duration, end),
                "text": piece
            })
            start += duration
            index += 1

    return srt_entries

def generate_transcript(segments):
    merged = []
    prev_speaker = None
    buffer = []
    time_stamp = None

    for seg in segments:
        speaker = seg.get("speaker", "UNKNOWN")
        text = seg["text"].strip()
        start = format_time_sec(seg.get("start", 0))

        if speaker == prev_speaker:
            buffer.append(text)
        else:
            if buffer:
                merged.append((prev_speaker, time_stamp, " ".join(buffer)))
            buffer = [text]
            time_stamp = start
            prev_speaker = speaker

    if buffer:
        merged.append((prev_speaker, time_stamp, " ".join(buffer)))

    return merged