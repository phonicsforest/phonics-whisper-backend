from flask import Flask, request, jsonify
import whisper
import tempfile

app = Flask(__name__)

model = whisper.load_model("tiny")

@app.route("/transcribe_sentence", methods=["POST"])
def transcribe():
    audio_file = request.files["audio"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        audio_file.save(tmp.name)
        result = model.transcribe(tmp.name)

    return jsonify({
        "transcript": result["text"]
    })