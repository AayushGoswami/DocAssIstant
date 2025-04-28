# Doc Assistant

An AI-powered platform to assist healthcare professionals by providing quick and accurate analysis of medical reports, X-rays, and ECGs. Built with Flask, TensorFlow Lite, and Groq API.

---

## Features
- **Medical Report Analyzer:** Upload PDF or image files of medical reports for instant AI-generated summaries and parameter extraction.
- **X-ray Analyzer:** Upload chest X-ray images to detect signs of pneumonia using a quantized TFLite model.
- **ECG Analyzer:** Upload ECG images to classify and summarize heart conditions using a quantized TFLite model.
- **User-friendly Web Interface:** Simple upload forms and clear summaries for each tool.

---

## Demo
- Clone the repository and run locally, or deploy using [Render](https://render.com/) with the provided `render.yaml`.

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AayushGoswami/DocAssIstant.git
   cd DocAssIstant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file in the root directory:
     ```env
     GROQ_API_KEY=your_actual_groq_api_key
     ```
   - Replace `your_actual_groq_api_key` with your Groq API key.

4. **Model files:**
   - Ensure the following model files are present in `utils/models/`:
     - `chest_xray_model_quantized.tflite`
     - `ecg_model_quantized.tflite`

5. **Run the application:**
   ```bash
   python app.py
   ```
   - The app will be available at `http://localhost:8080` (or as specified in your environment).

---

## Usage
- Go to the home page and select a tool from the sidebar:
  - **Medical Report Analyzer:** Upload a PDF or image of a medical report.
  - **X-ray Analyzer:** Upload a chest X-ray image (JPG/PNG).
  - **ECG Analyzer:** Upload an ECG image (JPG/PNG).
- The AI will process the file and display a summary and key findings.

---

## Deployment
- For production, use the provided `render.yaml` for Render.com deployment.
- The app uses Gunicorn as the WSGI server in production.

---

## Requirements
- Python 3.8+
- Flask
- TensorFlow (Lite)
- Groq API access
- Pillow, numpy, PyPDF2, python-dotenv, gunicorn

---

## Credits
- Developed by [Aayush Goswami](https://github.com/AayushGoswami) and [Om Modi](https://github.com/Ommodi07).
- Powered by Groq API and TensorFlow Lite models.

---

## License
This project is licensed under the MIT License.

---

## Repository
[GitHub - DocAssIstant](https://github.com/AayushGoswami/DocAssIstant)
