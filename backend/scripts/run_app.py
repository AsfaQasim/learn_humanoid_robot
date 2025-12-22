#!/usr/bin/env python3
"""
Run Script for RAG Chatbot Backend with uv

This script starts the FastAPI application using uv if available,
otherwise falls back to regular Python execution.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_with_uv():
    """Run the application with uv."""
    print("Starting application with uv...")
    try:
        subprocess.run(['uv', 'run', 'uvicorn', 'src.main:app', '--reload'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running with uv: {e}")
        return False
    except FileNotFoundError:
        print("❌ uv not found. Install it with 'pip install uv' or try the standard run method.")
        return False
    return True


def run_standard():
    """Run the application with standard Python."""
    print("Starting application with standard Python...")
    try:
        subprocess.run([sys.executable, '-m', 'uvicorn', 'src.main:app', '--reload'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running with standard Python: {e}")
        return False
    return True


def main():
    print("🚀 RAG Chatbot Backend - Application Runner")
    print("=" * 50)

    # Change to backend directory
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)
    print(f"Working in directory: {os.getcwd()}")

    print("\nChoose run method:")
    print("1. Uv (faster execution)")
    print("2. Standard Python")

    choice = input("Enter your choice (1 or 2, default 1): ").strip() or "1"

    success = False
    if choice == "1":
        success = run_with_uv()
        if not success:
            print("\n⚠️  uv failed, trying standard Python...")
            success = run_standard()
    elif choice == "2":
        success = run_standard()
    else:
        print("Invalid choice. Trying uv first...")
        success = run_with_uv()
        if not success:
            success = run_standard()

    if success:
        print("\n🎉 Application running successfully!")
        print("✨ The API should be available at http://localhost:8000")
    else:
        print("\n❌ Failed to start the application. Please check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()