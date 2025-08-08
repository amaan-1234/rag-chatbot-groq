import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the RAG chatbot."""
    
    # Groq AI Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3-8b-8192")
    
    # Vector Database Configuration
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    
    # Application Configuration - Optimized for speed
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))  # Reduced from 1000
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))  # Reduced from 200
    
    # Collection name for the vector database
    COLLECTION_NAME = "documents"
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required. Please set it in your .env file.")
        
        return True
