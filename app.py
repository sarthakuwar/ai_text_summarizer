import requests
import os
import PyPDF2
import docx
from flask import Flask, render_template, request as req, jsonify

app = Flask(__name__)

# Ensure a directory for uploads exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_text_from_file(file):
    """
    Extract text from different file types
    Supports .txt, .pdf, .docx, .doc files
    """
    filename = file.filename.lower()
    
    if filename.endswith('.txt'):
        # Read text files directly
        return file.read().decode('utf-8')
    
    elif filename.endswith('.pdf'):
        # Extract text from PDF
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    elif filename.endswith(('.docx', '.doc')):
        # Extract text from Word documents
        doc = docx.Document(file)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    
    else:
        return "Unsupported file type"

@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")

@app.route("/Summarize", methods=["GET", "POST"])
def Summarize():
    if req.method == "POST":
        # API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        # headers = {"Authorization": "Bearer {API_KEY}"}

        # Check if file is uploaded
        if "file" in req.files:
            file = req.files["file"]
            if file and file.filename:
                # Extract text from the uploaded file
                file_text = extract_text_from_file(file)
                if file_text != "Unsupported file type":
                    data = file_text
                else:
                    return render_template("index.html", result="Unsupported file type")
            else:
                # Fallback to text input if file upload fails
                data = req.form.get("data", "").strip()
        else:
            # No file uploaded, use text input
            data = req.form.get("data", "").strip()

        # Ensure we have some text to summarize
        if not data:
            return render_template("index.html", result="No text to summarize")

        def query(payload):
            try:
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                
                # Print raw response for debugging
                print("Response status code:", response.status_code)
                print("Response content:", response.text)
                
                # Check if response was successful
                response.raise_for_status()
                
                # Try to parse JSON
                output = response.json()
                return output
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                return {"error": str(e)}
            except ValueError as e:
                print(f"JSON decode error: {e}")
                return {"error": "Failed to decode JSON response"}

        # Get summary
        output = query({
            "inputs": data,

        })
        
        # Check for errors in the output
        if isinstance(output, dict) and "error" in output:
            return render_template("index.html", result=f"Error: {output['error']}")
        
        # Extract summary
        try:
            if isinstance(output, list) and len(output) > 0:
                summary = output[0].get("summary_text", "No summary found.")
            elif isinstance(output, dict):
                summary = output.get("summary_text", "No summary found.")
            else:
                summary = "Unexpected response format."
        except Exception as e:
            summary = f"Error extracting summary: {str(e)}"

        return render_template("index.html", result=summary)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)