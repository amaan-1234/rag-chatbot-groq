#!/usr/bin/env python3
"""
RAG Chatbot Runner Script

This script provides an easy way to start the RAG chatbot system.
It can run either the API server, the Streamlit app, or both.
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fastapi
        import streamlit
        import langchain
        import groq
        import chromadb
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has Groq API key."""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("Please create a .env file with your Groq API key:")
        print("GROQ_API_KEY=your_groq_api_key_here")
        return False
    
    # Check if Groq API key is set
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            print("⚠️  Groq API key not configured")
            print("Please set your Groq API key in the .env file")
            return False
        print("✅ Groq API key configured")
        return True
    except Exception as e:
        print(f"❌ Error checking environment: {e}")
        return False

def start_api_server():
    """Start the FastAPI server."""
    print("🚀 Starting FastAPI server...")
    try:
        process = subprocess.Popen([
            sys.executable, "api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ FastAPI server started at http://localhost:8000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Failed to start API server: {stderr.decode()}")
            return None
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        return None

def start_streamlit_app():
    """Start the Streamlit app."""
    print("🚀 Starting Streamlit app...")
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the app to start
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Streamlit app started at http://localhost:8501")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Failed to start Streamlit app: {stderr.decode()}")
            return None
    except Exception as e:
        print(f"❌ Error starting Streamlit app: {e}")
        return None

def signal_handler(signum, frame):
    """Handle shutdown signals."""
    print("\n🛑 Shutting down...")
    sys.exit(0)

def main():
    """Main function to run the chatbot."""
    print("🤖 RAG Chatbot Runner (Groq AI)")
    print("=" * 50)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        print("\nTo set up your environment:")
        print("1. Copy env_example.txt to .env")
        print("2. Add your Groq API key to .env")
        print("3. Run this script again")
        sys.exit(1)
    
    print("\nChoose an option:")
    print("1. Start API server only")
    print("2. Start Streamlit app only")
    print("3. Start both (recommended)")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                # Start API only
                api_process = start_api_server()
                if api_process:
                    print("\n📖 API Documentation available at: http://localhost:8000/docs")
                    print("Press Ctrl+C to stop the server")
                    api_process.wait()
                break
                
            elif choice == "2":
                # Start Streamlit only
                print("⚠️  Note: You need to start the API server separately")
                print("Run: python api.py")
                streamlit_process = start_streamlit_app()
                if streamlit_process:
                    print("Press Ctrl+C to stop the app")
                    streamlit_process.wait()
                break
                
            elif choice == "3":
                # Start both
                api_process = start_api_server()
                if not api_process:
                    print("❌ Failed to start API server. Exiting.")
                    sys.exit(1)
                
                # Wait a bit for API to fully start
                time.sleep(2)
                
                streamlit_process = start_streamlit_app()
                if not streamlit_process:
                    print("❌ Failed to start Streamlit app. Stopping API server.")
                    api_process.terminate()
                    sys.exit(1)
                
                print("\n🎉 Both services are running!")
                print("📖 API Documentation: http://localhost:8000/docs")
                print("🌐 Web Interface: http://localhost:8501")
                print("Press Ctrl+C to stop both services")
                
                # Wait for either process to finish
                try:
                    while True:
                        if api_process.poll() is not None:
                            print("❌ API server stopped unexpectedly")
                            streamlit_process.terminate()
                            break
                        if streamlit_process.poll() is not None:
                            print("❌ Streamlit app stopped unexpectedly")
                            api_process.terminate()
                            break
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n🛑 Stopping services...")
                    api_process.terminate()
                    streamlit_process.terminate()
                    print("✅ Services stopped")
                break
                
            elif choice == "4":
                print("👋 Goodbye!")
                sys.exit(0)
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
