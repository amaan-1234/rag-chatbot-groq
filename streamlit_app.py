import streamlit as st
import requests
import json
import os
from typing import Dict, Any
import time

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    .user-message {
        background-color: #1565c0;
        border-left-color: #2196f3;
        color: white;
    }
    .bot-message {
        background-color: #7b1fa2;
        border-left-color: #9c27b0;
        color: white;
    }
    .context-box {
        background-color: #424242;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #616161;
        margin-top: 0.5rem;
        color: white;
    }
    .stats-box {
        background-color: #2e7d32;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #4caf50;
        color: white;
    }
    .upload-info {
        background-color: #f57c00;
        padding: 0.5rem;
        border-radius: 0.5rem;
        border: 1px solid #ff9800;
        margin-bottom: 1rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://localhost:8000"

def make_api_request(endpoint: str, method: str = "GET", data: Dict = None, files: Dict = None) -> Dict[str, Any]:
    """Make API request to the backend."""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files)
            else:
                response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

def chat_with_bot(message: str, k: int = 5) -> Dict[str, Any]:
    """Send a chat message to the bot."""
    return make_api_request("/chat", method="POST", data={"message": message, "k": k})

def upload_document(file) -> Dict[str, Any]:
    """Upload a document to the knowledge base."""
    files = {"file": file}
    return make_api_request("/upload-document", method="POST", files=files)

def get_stats() -> Dict[str, Any]:
    """Get knowledge base statistics."""
    return make_api_request("/stats")

def clear_knowledge_base() -> Dict[str, Any]:
    """Clear the knowledge base."""
    return make_api_request("/clear-knowledge-base", method="DELETE")

def check_health() -> Dict[str, Any]:
    """Check API health."""
    return make_api_request("/health")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stats" not in st.session_state:
    st.session_state.stats = {"total_documents": 0}

# Main header
st.markdown('<h1 class="main-header">🤖 RAG Chatbot (Groq AI)</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📚 Knowledge Base")
    
    # Health check
    health = check_health()
    if health.get("status") == "healthy":
        st.success("✅ API Connected")
    else:
        st.error("❌ API Connection Failed")
        st.stop()
    
    # Document upload
    st.subheader("Upload Documents")
    
    # Upload info
    st.markdown("""
    <div class="upload-info">
        <strong>📋 Upload Tips:</strong><br>
        • Supported: PDF, TXT, MD files<br>
        • Max size: 10MB<br>
        • Processing time: 30-60 seconds<br>
        • Smaller files = faster processing
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'txt', 'md'],
        help="Upload PDF, TXT, or MD files to add to the knowledge base"
    )
    
    if uploaded_file is not None:
        # Show file info
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # MB
        st.info(f"📄 File: {uploaded_file.name} ({file_size:.2f} MB)")
        
        if st.button("📤 Upload Document"):
            with st.spinner("Processing document..."):
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Update progress
                status_text.text("📖 Reading document...")
                progress_bar.progress(20)
                
                # Upload document
                result = upload_document(uploaded_file)
                
                progress_bar.progress(100)
                status_text.text("✅ Processing complete!")
                
                if result.get("success"):
                    st.success(f"✅ {result['message']}")
                    if result.get("chunks_created"):
                        st.info(f"📊 Created {result['chunks_created']} chunks")
                    if result.get("processing_time"):
                        st.info(f"⏱️ Processing time: {result['processing_time']} seconds")
                    # Refresh stats
                    st.session_state.stats = get_stats()
                else:
                    st.error(f"❌ {result.get('message', 'Upload failed')}")
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
    
    # Knowledge base stats
    st.subheader("📊 Statistics")
    stats = get_stats()
    if stats.get("total_documents") is not None:
        st.metric("Total Documents", stats["total_documents"])
        st.session_state.stats = stats
    
    # Clear knowledge base
    st.subheader("🗑️ Management")
    if st.button("Clear Knowledge Base", type="secondary"):
        if st.checkbox("I understand this will delete all documents"):
            with st.spinner("Clearing knowledge base..."):
                result = clear_knowledge_base()
                if result.get("success"):
                    st.success("✅ Knowledge base cleared")
                    st.session_state.stats = get_stats()
                else:
                    st.error(f"❌ {result.get('message', 'Failed to clear')}")
    
    # Settings
    st.subheader("⚙️ Settings")
    k_value = st.slider("Number of context chunks (k)", 1, 10, 5, help="Number of relevant document chunks to retrieve")

# Main chat area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat")
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>Bot:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
            
            # Show context if available
            if message.get("context"):
                with st.expander("🔍 View Context"):
                    st.markdown(f"""
                    <div class="context-box">
                        {message["context"]}
                    </div>
                    """, unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get bot response
        with st.spinner("🤔 Thinking..."):
            response = chat_with_bot(prompt, k_value)
            
            if response.get("success"):
                bot_message = {
                    "role": "assistant",
                    "content": response["response"],
                    "context": response.get("context", "")
                }
                st.session_state.messages.append(bot_message)
            else:
                error_message = {
                    "role": "assistant",
                    "content": f"❌ Error: {response.get('response', 'Unknown error')}"
                }
                st.session_state.messages.append(error_message)
        
        # Rerun to display new messages
        st.rerun()

with col2:
    st.subheader("📋 Quick Actions")
    
    # Quick questions
    st.write("**Try asking:**")
    quick_questions = [
        "What documents have you been trained on?",
        "Can you summarize the main topics?",
        "What are the key insights?",
        "How can I use this information?"
    ]
    
    for question in quick_questions:
        if st.button(question, key=f"quick_{question}"):
            st.session_state.messages.append({"role": "user", "content": question})
            with st.spinner("🤔 Thinking..."):
                response = chat_with_bot(question, k_value)
                if response.get("success"):
                    bot_message = {
                        "role": "assistant",
                        "content": response["response"],
                        "context": response.get("context", "")
                    }
                    st.session_state.messages.append(bot_message)
                else:
                    error_message = {
                        "role": "assistant",
                        "content": f"❌ Error: {response.get('response', 'Unknown error')}"
                    }
                    st.session_state.messages.append(error_message)
            st.rerun()
    
    # Clear chat
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using Streamlit, FastAPI, and Groq AI</p>
        <p>RAG (Retrieval-Augmented Generation) Chatbot</p>
    </div>
    """,
    unsafe_allow_html=True
)
