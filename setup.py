#!/usr/bin/env python3
"""
Setup script for RAG Chatbot
This script helps users set up their environment properly.
"""

import os
import shutil
from pathlib import Path

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path("env_example.txt")
    
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file and add your GROQ_API_KEY")
        else:
            print("❌ env_example.txt not found")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'fastapi', 'uvicorn', 'langchain', 'langchain-groq',
        'langchain-community', 'groq', 'chromadb', 'sentence-transformers',
        'python-multipart', 'pydantic', 'python-dotenv', 'streamlit',
        'pypdf', 'tiktoken', 'numpy', 'pandas', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies are installed")
        return True

def check_config():
    """Check if configuration is valid."""
    try:
        from config import Config
        Config.validate()
        print("✅ Configuration is valid")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Main setup function."""
    print("🤖 RAG Chatbot Setup")
    print("=" * 30)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Check configuration
    if not check_config():
        print("\n📝 Next steps:")
        print("1. Edit .env file and add your GROQ_API_KEY")
        print("2. Get your API key from: https://console.groq.com/")
        print("3. Run: python run.py")
        return False
    
    print("\n🎉 Setup complete! You can now run:")
    print("python run.py")
    return True

if __name__ == "__main__":
    main()
