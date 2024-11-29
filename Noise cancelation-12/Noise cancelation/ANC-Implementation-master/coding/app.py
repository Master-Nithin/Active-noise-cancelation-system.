from flask import Flask, request, jsonify, send_file, render_template
import os
import numpy as np
import scipy.io.wavfile as wav
from Simulation import Simulation  # Ensure these are in the same directory or proper path

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')  # Connects to your HTML file

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Process the audio file
    fs, x = wav.read(filepath)
    x = x / 2.0 ** 15  # Normalize input

    # If stereo, take only one channel
    if len(x.shape) > 1:
        x = x[:, 0]

    sim = Simulation(x, fs, 10)
    en, _ = sim.simulate()

    # Save the processed audio
    output_path = os.path.join(OUTPUT_FOLDER, 'out.wav')
    wav.write(output_path, fs, np.array(en * 2.0 ** 15, dtype='int16'))

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
