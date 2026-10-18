#!/usr/bin/env python3
"""
MedTriage AI — Unified Application Runner
Usage:
    python run.py             # Start both Backend (FastAPI) and Frontend (Vite)
    python run.py test        # Run all backend unit & safety rule tests
    python run.py backend     # Start only the FastAPI backend server
    python run.py frontend    # Start only the Vite frontend dev server
"""

import os
import sys
import time
import subprocess
import signal
from pathlib import Path

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
VENV_PYTHON = ROOT_DIR / ".venv" / "Scripts" / "python.exe"
if not VENV_PYTHON.exists():
    VENV_PYTHON = Path(sys.executable)

def run_tests():
    print("=" * 60)
    print("[*] Running MedTriage Automated Test Suite...")
    print("=" * 60)
    cmd = [str(VENV_PYTHON), "-m", "pytest", "backend/tests", "-v"]
    result = subprocess.run(cmd, cwd=str(ROOT_DIR))
    sys.exit(result.returncode)

def run_backend():
    print("=" * 60)
    print("[+] Starting FastAPI Backend at http://127.0.0.1:8000")
    print("[+] API Documentation: http://127.0.0.1:8000/docs")
    print("=" * 60)
    cmd = [
        str(VENV_PYTHON),
        "-m",
        "uvicorn",
        "backend.app.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
        "--reload"
    ]
    subprocess.run(cmd, cwd=str(ROOT_DIR))

def run_frontend():
    print("=" * 60)
    print("[+] Starting Vite Frontend at http://127.0.0.1:5173")
    print("=" * 60)
    frontend_dir = ROOT_DIR / "frontend"
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    subprocess.run([npm_cmd, "run", "dev"], cwd=str(frontend_dir))

def run_all():
    print("=" * 70)
    print("MedTriage AI -- Intelligent OPD Triage & Prioritisation System")
    print("=" * 70)
    print("Starting both Backend and Frontend services...")
    print("  -> Backend API:       http://127.0.0.1:8000")
    print("  -> Swagger Docs:      http://127.0.0.1:8000/docs")
    print("  -> Frontend UI:       http://127.0.0.1:5173")
    print("-" * 70)
    print("Press Ctrl+C to stop all services.\n")

    backend_cmd = [
        str(VENV_PYTHON),
        "-m",
        "uvicorn",
        "backend.app.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000"
    ]
    backend_proc = subprocess.Popen(backend_cmd, cwd=str(ROOT_DIR))

    # Give backend a moment to initialize
    time.sleep(1.5)

    frontend_dir = ROOT_DIR / "frontend"
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    frontend_proc = subprocess.Popen([npm_cmd, "run", "dev"], cwd=str(frontend_dir))

    def shutdown(sig, frame):
        print("\nStopping MedTriage services...")
        try:
            backend_proc.terminate()
        except Exception:
            pass
        try:
            frontend_proc.terminate()
        except Exception:
            pass
        backend_proc.wait()
        frontend_proc.wait()
        print("[OK] Services stopped safely.")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        while True:
            time.sleep(0.5)
            if backend_proc.poll() is not None:
                print(f"Backend exited with code {backend_proc.returncode}")
                frontend_proc.terminate()
                break
            if frontend_proc.poll() is not None:
                print(f"Frontend exited with code {frontend_proc.returncode}")
                backend_proc.terminate()
                break
    except KeyboardInterrupt:
        shutdown(None, None)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower().strip()
        if mode in ("test", "tests", "pytest"):
            run_tests()
        elif mode in ("backend", "api", "server"):
            run_backend()
        elif mode in ("frontend", "ui", "client"):
            run_frontend()
        else:
            print(f"Unknown mode: {mode}")
            print("Usage: python run.py [test | backend | frontend]")
            sys.exit(1)
    else:
        run_all()
