import subprocess
import time
import sys
import os

def start_backend():
    """Start the FastAPI backend server."""
    print("🚀 Starting Backend (FastAPI)...")
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--port", "8000"])

def start_frontend():
    """Start the Streamlit frontend."""
    print("🎨 Starting Frontend (Streamlit)...")
    return subprocess.Popen(["streamlit", "run", "frontend/app.py"])

if __name__ == "__main__":
    # Ensure current dir is in PYTHONPATH
    os.environ["PYTHONPATH"] = os.getcwd()
    
    backend_process = None
    frontend_process = None
    
    try:
        backend_process = start_backend()
        # Give it a moment to start
        time.sleep(3)
        
        frontend_process = start_frontend()
        
        print("\n✅ AI Study Assistant is launching!")
        print("Backend: http://localhost:8000")
        print("Frontend: http://localhost:8501")
        print("\nPress Ctrl+C to stop both servers.")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("Done.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
