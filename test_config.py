#!/usr/bin/env python3
"""
Test script to verify configuration and components work properly.
"""

import os
from config import Config

def test_config():
    """Test the configuration."""
    print("Testing configuration...")
    
    # Check if GROQ_API_KEY is set
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment variables")
        return False
    
    if api_key == "your_groq_api_key_here":
        print("❌ GROQ_API_KEY is still set to placeholder value")
        return False
    
    print("✅ GROQ_API_KEY is set")
    
    # Test Config validation
    try:
        Config.validate()
        print("✅ Configuration validation passed")
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        from document_processor import DocumentProcessor
        print("✅ DocumentProcessor imported successfully")
    except Exception as e:
        print(f"❌ Failed to import DocumentProcessor: {e}")
        return False
    
    try:
        from vector_store_deploy import VectorStore
        print("✅ VectorStore imported successfully")
    except Exception as e:
        print(f"❌ Failed to import VectorStore: {e}")
        return False
    
    try:
        from rag_chatbot import RAGChatbot
        print("✅ RAGChatbot imported successfully")
    except Exception as e:
        print(f"❌ Failed to import RAGChatbot: {e}")
        return False
    
    return True

def test_components():
    """Test that components can be initialized."""
    print("Testing component initialization...")
    
    try:
        from document_processor import DocumentProcessor
        from vector_store_deploy import VectorStore
        from rag_chatbot import RAGChatbot
        
        # Initialize components
        doc_processor = DocumentProcessor()
        vector_store = VectorStore()
        chatbot = RAGChatbot(vector_store, doc_processor)
        
        print("✅ All components initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Component initialization failed: {e}")
        return False

def main():
    """Main test function."""
    print("🤖 RAG Chatbot Configuration Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        return False
    
    # Test configuration
    if not test_config():
        return False
    
    # Test components
    if not test_components():
        return False
    
    print("\n🎉 All tests passed! Your configuration is ready for deployment.")
    return True

if __name__ == "__main__":
    main()
