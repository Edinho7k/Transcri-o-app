import os
import whisper
from flask import Flask, request, render_template, send_file

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Carrega o modelo Whisper
model = whisper.load_model("base")

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files: #receb o arquivo enviado
            return "Nenhum arquivo enviado"

        file = request.files["file"]
        if file.filename == "":
            return "Nenhum arquivo selecionado"

        # Salva o arquivo no servidor
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Transcreve o áudio
        result = model.transcribe(file_path)
        transcription_text = result["text"]

        # Salva a transcrição no mesmo diretório do arquivo
        transcription_path = file_path + "_transcription.txt"
        with open(transcription_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(transcription_text)

        return render_template("index.html", transcription=transcription_text, transcription_path=transcription_path)

    return render_template("index.html", transcription=None)

@app.route("/download/<path:filename>")
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
