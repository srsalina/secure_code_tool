from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import subprocess
import os


app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)
    scan_results = run_bandit(file_path)
    return jsonify({'results': scan_results})

def run_bandit(file_path):
    command = f"bandit -r {file_path}"
    result = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    bandit_results = result.stdout.decode('utf-8')

    # Use Hugging Face for Analysis
    with open(file_path, 'r') as file:
        code = file.read()

    nlp = pipeline("fill-mask", model="distilbert-base-uncased")
    suggestions = nlp(f"{code} [MASK]")

    # combine and output results
    combined_results = bandit_results + "\nAI Suggestions:\n" + str(suggestions)
    return combined_results


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)

