@echo off
echo 🎓 Setting up Offline AI Study Assistant...
echo 📥 Checking for Ollama...

ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama is not installed!
    echo Please download and install Ollama from https://ollama.com first.
    pause
    exit /b
)

echo ✅ Ollama found!
echo 📥 Pulling Gemma:2b model (lightweight, student-friendly)...
ollama pull gemma:2b

echo ✅ Model pulled successfully!
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

echo ✨ Setup Complete! 
echo 🚀 To start the app, run: python launch.py
pause
