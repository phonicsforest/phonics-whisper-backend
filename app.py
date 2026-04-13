from flask import Flask, request, jsonify
import whisper
import tempfile
import os

app = Flask(__name__)

# 🔥 用 tiny（free plan 必須）
model = whisper.load_model("tiny")


@app.route("/")
def home():
    return "Whisper backend is running!"


@app.route("/transcribe_sentence", methods=["POST"])
def transcribe():
    try:
        if "audio" not in request.files:
            return jsonify({"error": "No audio file"}), 400

        audio_file = request.files["audio"]

        # 儲存暫存音檔
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            audio_file.save(tmp.name)

            # 🔥 Whisper 轉文字
            result = model.transcribe(tmp.name)

        return jsonify({
            "transcript": result["text"]
        })

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({
            "error": str(e)
        }), 500


# 🔥 Render 必須：PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)