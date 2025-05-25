from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import torch
import soundfile as sf
from pydub import AudioSegment
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

app = Flask(__name__)
CORS(app)

processor = Wav2Vec2Processor.from_pretrained("./local_model")
model = Wav2Vec2ForCTC.from_pretrained("./local_model")

UPLOAD_FOLDER = "./recordings"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        file = request.files["file"]
        file_path = os.path.join(UPLOAD_FOLDER, "temp.webm")
        file.save(file_path)

        # Convert WebM to WAV
        wav_path = os.path.join(UPLOAD_FOLDER, "temp.wav")
        audio = AudioSegment.from_file(file_path, format="webm")
        audio = audio.set_frame_rate(16000).set_channels(1)  # Match model requirements
        audio.export(wav_path, format="wav")

        # Load the WAV file
        speech, sample_rate = sf.read(wav_path)

        # Transcription
        inputs = processor(speech, sampling_rate=sample_rate, return_tensors="pt", padding=True)
        logits = model(**inputs).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]

        return jsonify({"transcription": transcription})
    except Exception as e:
        print("Error processing file:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

