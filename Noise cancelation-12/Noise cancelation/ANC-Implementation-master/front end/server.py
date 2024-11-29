from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)  # Corrected "__main.py__" to "__name__"

UPLOAD_FOLDER = 'uploads'  # Folder to save uploaded files
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Replace this with the actual command to run your noise cancellation script
    subprocess.run(['python', 'path_to_your_script/your_noise_cancel_script.py', file_path])

    return jsonify({'message': 'File processed successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run the server on port 5000

