from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import tempfile
import shutil
import time

from rag_chatbot import RAGChatbot
from config import Config

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="A Retrieval-Augmented Generation chatbot API using Groq AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
try:
    Config.validate()
    chatbot = RAGChatbot()
    print("✅ RAG Chatbot initialized successfully")
except Exception as e:
    print(f"❌ Error initializing chatbot: {e}")
    print("Please check your .env file and ensure GROQ_API_KEY is set correctly")
    chatbot = None

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    k: Optional[int] = 5

class ChatResponse(BaseModel):
    success: bool
    response: str
    context: str
    query: str

class DocumentResponse(BaseModel):
    success: bool
    message: str
    chunks_created: Optional[int] = None
    processing_time: Optional[float] = None

class StatsResponse(BaseModel):
    total_documents: int
    collection_name: str

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "RAG Chatbot API is running with Groq AI!"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint for asking questions."""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")
    
    try:
        result = chatbot.chat(request.message, request.k)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-document", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document."""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")
    
    # Validate file type
    allowed_extensions = ['.pdf', '.txt', '.md']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed: {allowed_extensions}"
        )
    
    # Check file size (limit to 10MB)
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 10MB."
        )
    
    try:
        start_time = time.time()
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Process the document
        result = chatbot.add_document(temp_file_path)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        # Add processing time to result
        result['processing_time'] = round(processing_time, 2)
        
        return DocumentResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get knowledge base statistics."""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")
    
    try:
        stats = chatbot.get_knowledge_base_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear-knowledge-base")
async def clear_knowledge_base():
    """Clear all documents from the knowledge base."""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")
    
    try:
        result = chatbot.clear_knowledge_base()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "chatbot_initialized": chatbot is not None,
        "groq_key_configured": bool(Config.GROQ_API_KEY)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
