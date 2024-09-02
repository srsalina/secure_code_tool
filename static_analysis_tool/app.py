from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import subprocess
import os
import json
import logging

# print(os.environ)

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../uploads'))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Secure Code Review Tool API. Use the /analyze endpoint to analyze your Python files."

# Load the unified dataset at startup
def load_unified_data():
    try:
        data_path = os.path.join(os.path.dirname(__file__), '../data/unified_python_vulnerabilities.json')
        if not os.path.exists(data_path):
            logging.error(f"Data file not found: {data_path}")
            return []
        
        with open(data_path, 'r') as f:
            logging.info("Unified data loaded successfully.")
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {data_path}: {e}")
        return []
    except Exception as e:
        logging.error(f"Error loading unified data: {e}")
        return []

unified_data = load_unified_data()

@app.route("/analyze", methods=["POST"])
def upload_file():
    try:
        if 'file' not in request.files:
            logging.error("No file part in the request.")
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        if file.filename == '':
            logging.error("No selected file.")
            return jsonify({'error': 'No selected file'}), 400
        
        # Ensure file is a Python file
        if not file.filename.endswith('.py'):
            logging.error("Uploaded file is not a Python file.")
            return jsonify({'error': 'Only Python files (.py) are allowed.'}), 400
        
        # Save the file to the updated uploads directory
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        logging.info(f"File saved to {file_path}")

        # Isolate Bandit Run
        scan_results = run_bandit(file_path)
        logging.info(f"Bandit Results: {scan_results}")
        
        # Isolate AI Analysis
        ai_suggestions = analyze_with_ai(file_path)
        logging.info(f"AI Suggestions: {ai_suggestions}")

        # Isolate Vulnerability Check
        vulnerabilities = check_vulnerabilities(file_path)
        logging.info(f"Vulnerabilities Found: {vulnerabilities}")

        combined_results = {
            'bandit_results': scan_results,
            'ai_suggestions': ai_suggestions,
            'vulnerabilities': vulnerabilities
        }
        logging.info("Analysis completed successfully.")
        return jsonify(combined_results)

    except Exception as e:
        logging.error(f"Error during file analysis: {e}")
        return jsonify({'error': f"Error processing file: {str(e)}"}), 500







def run_bandit(file_path):
    try:
        # Ensure that 'file_path' always points to the correct file in 'uploads'
        uploads_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../uploads'))
        abs_path = os.path.join(uploads_dir, os.path.basename(file_path))

        # Debug: Print paths for verification
        print(f"Uploads Directory: {uploads_dir}")  # Print the uploads directory path
        print(f"Absolute File Path: {abs_path}")    # Print the absolute path of the file

        # Check if the file exists at the expected location
        if not os.path.isfile(abs_path):
            logging.error(f"File not found: {abs_path}")
            return {"error": f"File not found: {abs_path}"}

        # Use absolute path for the Bandit command
        command = ["bandit", "-f", "json", "-r", abs_path]  # Pass as a list
        print(f"Running command: {' '.join(command)}")  # Debugging line
        
        # Run the command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Capture output and errors
        stdout_output = result.stdout.decode('utf-8')
        stderr_output = result.stderr.decode('utf-8')

        # Handle non-zero exit codes more gracefully
        if result.returncode not in [0, 1]:  # 0 is success, 1 means issues found (not necessarily an error)
            logging.error(f"Bandit command failed with error: {stderr_output}")
            return {"error": f"Error running Bandit: {stderr_output}"}

        # Log command output
        print(f"Command output (stdout): {stdout_output}")
        print(f"Command error (stderr): {stderr_output}")
        print(f"Command exit status: {result.returncode}")

        # Read and parse JSON results
        bandit_json = json.loads(stdout_output)

        # Format output for readability
        formatted_results = [
            {
                "issue": issue.get("issue_text"),
                "severity": issue.get("issue_severity"),
                "confidence": issue.get("issue_confidence"),
                "file": issue.get("filename"),
                "line": issue.get("line_number"),
                "more_info": issue.get("more_info")
            }
            for issue in bandit_json.get('results', [])
        ]

        logging.info("Bandit scan completed and formatted.")
        return formatted_results
    except Exception as e:
        logging.error(f"Error running Bandit: {e}")
        return {"error": f"Error running Bandit: {str(e)}"}

















def analyze_with_ai(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()
        nlp = pipeline("fill-mask", model="distilbert-base-uncased")
        suggestions = nlp(f"{code[:512]} [MASK]")  # Only process the first 512 characters
        logging.info("AI analysis completed.")
        return suggestions
    except Exception as e:
        logging.error(f"Error in AI analysis: {e}")
        return f"Error in AI analysis: {str(e)}"

def check_vulnerabilities(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read().lower()
        
        if not code:
            logging.warning(f"The file {file_path} is empty.")
            return "Error: The uploaded file is empty."
        
        found_vulnerabilities = []

        for entry in unified_data:
            try:
                if entry.get('source') == 'SafetyDB' and entry.get('package', '').lower() in code:
                    found_vulnerabilities.append(entry)
                elif entry.get('source') == 'NVD-CVE' and entry.get('cve_id', '').lower() in code:
                    found_vulnerabilities.append(entry)
                elif entry.get('source') == 'PSF' and any(affected_pkg.get('package', '').lower() in code for affected_pkg in entry.get('affected', [])):
                    found_vulnerabilities.append(entry)
            except KeyError as e:
                logging.error(f"Error checking vulnerabilities in entry: {e}")
                continue

        logging.info("Vulnerability check completed.")
        return found_vulnerabilities
    except Exception as e:
        logging.error(f"Error checking vulnerabilities: {e}")
        return f"Error checking vulnerabilities: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)  # Only run the app, no extra os.makedirs call
