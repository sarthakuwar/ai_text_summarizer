# 📝 AI Text Summarizer & Detector

A simple Flask application that summarizes text using Facebook’s BART-Large-CNN model and detects whether the text is AI-generated or human-written using SVC, MultinomialNB, and ComplementNB models. This project demonstrates how to integrate NLP models from Hugging Face with Flask for text summarization and AI detection.

!

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Model Reference](#model-reference)  
6. [Project Structure](#project-structure)  


---

## 🌟 Overview
This application offers two main functionalities:

Text Summarization: Uses BART-Large-CNN to generate concise summaries of large text blocks or uploaded files.

AI Text Detection: Classifies text as AI-generated or human-written using a combination of SVC, MultinomialNB, and ComplementNB models.

Users can:

Directly enter text or upload files (.txt, .docx, .pdf) for summarization.

Detect AI-generated text and view the prediction confidence from all three models.

Copy the summarized/detected text with one click.

Edit the summary before copying or saving

---

## ✅ Features
- **🔥 Text Summarization:** Uses [BART-Large-CNN](https://huggingface.co/facebook/bart-large-cnn) to generate concise summaries.
- **File Upload:** Upload `.txt`, `.docx`, `.pdf`, or `.doc` files for summarization.
- **Editable Summary:** Allows users to edit the summarized text directly in the output field.
- **Copy to Clipboard:** Quickly copy the summarized text with one click.
- **Clear Input:** Reset both the input text area and file input field.
- **🤖 AI Text Detection:** Detects whether the given text is AI-generated or human-written

---

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ai_text_summarizer.git
   cd ai_text_summarizer

## Usage
1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt


## Model reference
 **📝 Text Summarization**:
 
  This application uses Facebook's BART-Large-CNN model from Hugging Face's Transformers library. BART is a sequence-to-sequence model trained with denoising as 
  pretraining objective. The model is particularly effective for:

  Text summarization

  Text generation

  Text comprehension

The model can handle input text up to 1024 tokens and generates fluent, coherent summaries while preserving key information.

**🤖 AI Text Detection**:

 -**Models**:

   SVC (Support Vector Classifier) → Effective for text classification.

   (Multinomial Naive Bayes) → Good for document classification.

   ComplementNB (Complement Naive Bayes) → Effective for imbalanced datasets.

  -**Ensemble Prediction** Displays confidence scores from all three models.

## Project structure

```php
ai_text_summarizer/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── static/               # Static files (CSS, JS, images)
│   └── screenshot.png    # Application screenshot
├── templates/            # HTML templates
│   ├── summarizer.html   # Summarization interface
│   ├── classify.html     # AI text detection interface
│   └── index.html         # Base template with navigation
├── models/               # AI detection models
│   ├── svc_model.pkl     # SVC model
│   ├── mnb_model.pkl     # MultinomialNB model
│   └── cnb_model.pkl     # ComplementNB model
└── README.md             # Project documentation





