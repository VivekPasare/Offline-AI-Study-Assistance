# 🎓 Offline AI Study Assistant

An intelligent, offline-first AI tutor designed for students, especially in resource-constrained environments.

## 🌟 Key Features
- **Fully Offline**: All AI processing happens locally on your machine.
- **Smart Learning Modes**:
  - **Normal**: Standard academic explanation.
  - **Simple (ELI10)**: Ultra-simplified concepts for kids or beginners.
  - **Example**: Real-life scenarios and practical analogies.
- **Study Summarizer**: Paste long notes and get bite-sized bullet points.
- **Multilingual Support**: Learn in **English** or **Hindi**.
- **Context Memory**: Remembers previous questions for consistent learning.

---

## 🛠️ Setup Instructions

### 1. Install & Setup Ollama
Download and install [Ollama](https://ollama.com). Once installed, open your terminal/command prompt and pull the lightweight model:
```bash
ollama pull gemma:2b
```

### 2. Install Dependencies
Ensure you have Python installed. Then, install the required packages:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### Step 1: Start the Backend (FastAPI)
In a new terminal, run:
```bash
python -m uvicorn backend.main:app --reload
```
This will start the engine on `http://localhost:8000`.

### Step 2: Start the Frontend (Streamlit)
In another terminal, run:
```bash
streamlit run frontend/app.py
```
The application will automatically open in your browser at `http://localhost:8501`.

---

## 🏗️ Technical Stack
- **AI Model**: Google Gemma 2b (Local Inference)
- **Engine**: Ollama
- **Backend API**: FastAPI
- **Frontend UI**: Streamlit + Custom CSS
- **Communication**: REST API (localhost)

---

## 🎯 Use Cases
- Rural schools with limited internet access.
- Students preparing for exams at home without data connectivity.
- Self-learners seeking easy-to-understand explanations.
