#!/usr/bin/env python3
"""
Dependency Installation Script for RAG Chatbot Backend

This script helps install all required dependencies for the backend.
It supports both pip and uv installation methods.
"""

import subprocess
import sys
import os
from pathlib import Path


def install_with_pip():
    """Install dependencies using pip."""
    print("Installing dependencies with pip...")
    print("⚠️  Note: If you encounter psycopg2-binary installation issues, see DB_INSTALLATION.md for solutions")
    requirements_path = Path('requirements.txt')
    if not requirements_path.exists():
        print(f"❌ requirements.txt not found at {requirements_path}")
        return False

    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_path)],
                      check=True)
        print("✅ Dependencies installed successfully with pip!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing with pip: {e}")
        print("💡 Tip: If psycopg2-binary failed, try installing PostgreSQL development libraries first")
        print("   See DB_INSTALLATION.md for detailed instructions")
        return False


def install_with_uv():
    """Install dependencies using uv."""
    print("Installing dependencies with uv...")
    print("⚠️  Note: If you encounter psycopg2-binary installation issues, see DB_INSTALLATION.md for solutions")
    requirements_path = Path('requirements.txt')
    if not requirements_path.exists():
        print(f"❌ requirements.txt not found at {requirements_path}")
        return False

    try:
        subprocess.run(['uv', 'pip', 'install', '-r', str(requirements_path)],
                      check=True)
        print("✅ Dependencies installed successfully with uv!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing with uv: {e}")
        print("💡 Tip: If psycopg2-binary failed, try installing PostgreSQL development libraries first")
        print("   See DB_INSTALLATION.md for detailed instructions")
        print("💡 Tip: If uv is not installed, install it first with 'pip install uv'")
        return False


def main():
    print("🔍 RAG Chatbot Backend - Dependency Installation")
    print("=" * 50)
    print("ℹ️  Note: This project now uses Google's Gemini API instead of OpenAI")
    print("   Get your free API key at: https://makersuite.google.com/app/apikey")

    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    print(f"Working in directory: {os.getcwd()}")

    print("\nChoose installation method:")
    print("1. Pip (from requirements.txt)")
    print("2. Uv (faster package installer)")

    choice = input("Enter your choice (1 or 2, default 1): ").strip() or "1"

    if choice == "1":
        success = install_with_pip()
    elif choice == "2":
        success = install_with_uv()
    else:
        print("Invalid choice. Using pip by default.")
        success = install_with_pip()

    if success:
        print("\n🎉 Installation completed successfully!")
        print("\nTo run the application:")
        print("  - With Pip: uvicorn src.main:app --reload")
        print("  - With uv: uvicorn src.main:app --reload")
        print("\n📋 Remember to set up your .env file with GEMINI_API_KEY")
    else:
        print("\n❌ Installation failed. Please check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()