# Set matplotlib backend first (MUST BE FIRST IMPORT)


import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import pickle
import PyPDF2
import docx
import io
import base64
import requests

app = FastAPI()

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
model_dir = "models"
mnb_model = pickle.load(open(f"{model_dir}/mnb_model.pkl", "rb"))
cnb_model = pickle.load(open(f"{model_dir}/cnb_model.pkl", "rb"))
svc_model = pickle.load(open(f"{model_dir}/svc_model.pkl", "rb"))

def extract_text_from_file(file: UploadFile):
    filename = file.filename.lower()
    if filename.endswith('.txt'):
        return file.file.read().decode('utf-8')
    elif filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file.file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif filename.endswith(('.docx', '.doc')):
        doc = docx.Document(file.file)
        return '\n'.join([p.text for p in doc.paragraphs])
    else:
        return "Unsupported file type"

@app.post("/api/classify")
async def classify(text: str = Form(default=None), file: UploadFile = File(default=None)):
    try:
        if file:
            extracted_text = extract_text_from_file(file)
            if extracted_text == "Unsupported file type":
                return JSONResponse(status_code=400, content={"error": "Unsupported file type"})
            text = extracted_text

        if not text:
            return JSONResponse(status_code=400, content={"error": "No text provided"})

        pred_mnb = mnb_model.predict([text])[0]
        pred_cnb = cnb_model.predict([text])[0]
        pred_svc = svc_model.predict([text])[0]

        try:
            prob_mnb = mnb_model.predict_proba([text])[0][1]
        except AttributeError:
            prob_mnb = 1.0 if pred_mnb == 1 else 0.0

        try:
            prob_cnb = cnb_model.predict_proba([text])[0][1]
        except AttributeError:
            prob_cnb = 1.0 if pred_cnb == 1 else 0.0

        prob_svc = 1.0 if pred_svc == 1 else 0.0
        ai_prob_avg = (prob_mnb + prob_cnb + prob_svc) / 3

        # Visualization
        fig, ax = plt.subplots(figsize=(8, 4))
        models = ['MultinomialNB', 'ComplementNB', 'SVC']
        probs = [prob_mnb * 100, prob_cnb * 100, prob_svc * 100]
        colors = ['#4e79a7', '#f28e2b', '#e15759']

        bars = ax.bar(models, probs, color=colors)
        ax.axhline(y=ai_prob_avg * 100, color='#76b7b2', linestyle='--')
        ax.set_ylim(0, 100)
        ax.set_ylabel('AI Probability (%)')
        ax.set_title('AI Detection Probability by Model')

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        plot_data = base64.b64encode(buf.getvalue()).decode('utf8')
        buf.close()
        plt.close(fig)

        return {
            "input_text": text[:300] + "..." if len(text) > 300 else text,
            "results": {
                "MultinomialNB": {
                    "prediction": "AI-generated" if pred_mnb == 1 else "human",
                    "probability": f"{prob_mnb * 100:.1f}%"
                },
                "ComplementNB": {
                    "prediction": "AI-generated" if pred_cnb == 1 else "human",
                    "probability": f"{prob_cnb * 100:.1f}%"
                },
                "SVC": {
                    "prediction": "AI-generated" if pred_svc == 1 else "human",
                    "probability": f"{prob_svc * 100:.1f}%"
                },
                "average_probability": f"{ai_prob_avg * 100:.1f}%"
            },
            # "plot_base64": plot_data
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# @app.route("/summarize", methods=["GET", "POST"])
# def summarize():
#     if req.method == "POST":
#         API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
#         headers = {"Authorization": "Bearer " + app.config["API_KEY"]}

#         if "file" in req.files:
#             file = req.files["file"]
#             if file and file.filename:
#                 file_text = extract_text_from_file(file)
#                 if file_text != "Unsupported file type":
#                     data = file_text
#                 else:
#                     return render_template("summarize.html", result="Unsupported file type")
#             else:
#                 data = req.form.get("data", "").strip()
#         else:
#             data = req.form.get("data", "").strip()

#         if not data:
#             return render_template("summarize.html", result="No text to summarize")

#         def query(payload):
#             try:
#                 response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
#                 response.raise_for_status()
#                 return response.json()
#             except requests.exceptions.RequestException as e:
#                 return {"error": str(e)}
#             except ValueError as e:
#                 return {"error": "Failed to decode JSON response"}

#         output = query({"inputs": data})
        
#         if isinstance(output, dict) and "error" in output:
#             return render_template("summarize.html", result=f"Error: {output['error']}")
        
#         try:
#             if isinstance(output, list) and len(output) > 0:
#                 summary = output[0].get("summary_text", "No summary found.")
#             elif isinstance(output, dict):
#                 summary = output.get("summary_text", "No summary found.")
#             else:
#                 summary = "Unexpected response format."
#         except Exception as e:
#             summary = f"Error extracting summary: {str(e)}"

#         return render_template("summarize.html", result=summary, original_text=data)
#     else:
#         return render_template("summarize.html")

if __name__ == "__main__":
       import uvicorn
       uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)