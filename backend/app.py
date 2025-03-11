import os
import torch
import whisperx
import re
from flask import Flask, request, jsonify
from transformers import BartForConditionalGeneration, BartTokenizer
from flask_cors import CORS
import subprocess

subprocess.run(["ffmpeg", "-version"])

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
CORS(app, origins="http://localhost:5173")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
whisper_model = whisperx.load_model("medium", device=device, compute_type="float32")

model_name = "sumit7488/meet_brief"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

FILLER_WORDS = [
    "uh", "um", "you know", "like", "actually", "basically", "literally",
    "seriously", "right", "so", "I mean", "well", "kind of", "sort of", "okay"
]
filler_pattern = r'\b(?:' + '|'.join(map(re.escape, FILLER_WORDS)) + r')\b'

def clean_transcript(text):
    text = re.sub(filler_pattern, "", text, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', text).strip()

def chunk_text(text, max_tokens=1024):
    sentences = text.split(". ")  # Splitting by sentence
    chunks = []
    current_chunk = []
    current_chunk_length = 0

    for sentence in sentences:
        # Tokenize sentence
        tokenized_sentence = tokenizer.encode(sentence, add_special_tokens=False)
        tokenized_sentence_length = len(tokenized_sentence)

        # If adding this sentence exceeds max tokens, store the current chunk and start a new one
        if current_chunk_length + tokenized_sentence_length <= max_tokens:
            current_chunk.append(sentence)
            current_chunk_length += tokenized_sentence_length
        else:
            # Store the chunk and reset for new chunk
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_chunk_length = tokenized_sentence_length

    if current_chunk:  # Add the last chunk
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize_long_text(text, min_length):
    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(**inputs, max_length=300, min_length=min_length, length_penalty=2.0)
        summaries.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))

    return " ".join(summaries)


def convert_video_to_audio(video_path, audio_path):
    try:
        subprocess.run([
            "ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path
        ], check=True)
        return audio_path
    except subprocess.CalledProcessError as e:
        print(f"Error during video to audio conversion: {str(e)}")
        return None

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        uploaded_file = request.files["file"]
        file_ext = os.path.splitext(uploaded_file.filename)[1].lower()

        if file_ext not in [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".mp4", ".mkv", ".avi"]:
            return jsonify({"error": "Unsupported format"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        if file_ext in [".mp4", ".mkv", ".avi"]:
            audio_path = file_path.rsplit(".", 1)[0] + ".wav"
            if not convert_video_to_audio(file_path, audio_path):
                return jsonify({"error": "Video to audio conversion failed"}), 500
            os.remove(file_path)
            file_path = audio_path

        try:
            print("Starting transcription...")
            transcript_result = whisper_model.transcribe(file_path)
            combined_text = " ".join(segment["text"] for segment in transcript_result["segments"])
            
        except Exception as e:
            print(f"Transcription failed: {str(e)}")
            return jsonify({"error": f"Transcription failed: {str(e)}"}), 500

        cleaned_transcript = clean_transcript(combined_text)
        print("Transcription completed.", cleaned_transcript)
        try:
            print("Starting summarization...")
            first_summary = summarize_long_text(cleaned_transcript, 50)
            final_summary = summarize_long_text(first_summary, 100)
            print("Summarization completed.", final_summary)
        except Exception as e:
            print(f"Summarization failed: {str(e)}")
            return jsonify({"error": f"Summarization failed: {str(e)}"}), 500

        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({"transcript": cleaned_transcript, "summary": final_summary})

    except Exception as e:
        print(f"Unexpected server error: {str(e)}")
        return jsonify({"error": f"Unexpected server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)