from flask import Flask, request, render_template, jsonify, send_file
import os
import qrcode
from utils.transcriber import transcribe_audio
from utils.analyzer import analyze_keywords, analyze_emotion
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check if the file is an allowed format."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_qr(url):
    """Generate a QR code for the given URL."""
    qr = qrcode.make(url)
    qr_path = os.path.join("static", "qr_code.png")
    qr.save(qr_path)
    return qr_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'audio' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['audio']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({"error": "Invalid file format"}), 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process audio
        transcribed_text = transcribe_audio(file_path)
        keywords_found = analyze_keywords(transcribed_text)
        emotion_detected = analyze_emotion(file_path)

        scam_detected = bool(keywords_found) or (emotion_detected in ['fear', 'anger'])

        result = {
            'transcription': transcribed_text,
            'keywords_found': keywords_found,
            'emotion_detected': emotion_detected,
            'scam_detected': scam_detected
        }

        os.remove(file_path)  # Clean up the uploaded file

        return render_template('index.html', result=result)

    qr_code_path = generate_qr("http://127.0.0.1:5000/")
    return render_template('index.html', qr_code=qr_code_path)

@app.route('/qr_code')
def qr_code():
    """Serve the QR code image."""
    return send_file("static/qr_code.png", mimetype='image/png')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs("static", exist_ok=True)  # Ensure static folder exists
    app.run(debug=True)
