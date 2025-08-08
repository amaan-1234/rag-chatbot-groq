# 🤖 RAG Chatbot with Groq AI

A powerful Retrieval-Augmented Generation (RAG) chatbot built with Streamlit, FastAPI, and Groq AI. This application allows users to upload documents and chat with an AI that can answer questions based on the uploaded content.

## ✨ Features

- **Document Upload**: Support for PDF, TXT, and MD files
- **Smart Chat Interface**: Interactive chat with context-aware responses
- **Vector Search**: Efficient document retrieval using ChromaDB
- **Fast Processing**: Optimized with Groq AI for quick responses
- **Modern UI**: Beautiful, responsive interface with dark theme
- **Real-time Processing**: Progress tracking and status updates

## 🏗️ Architecture

- **Frontend**: Streamlit web interface
- **Backend**: FastAPI REST API
- **LLM**: Groq AI (Llama3-8b-8192)
- **Embeddings**: HuggingFace Sentence Transformers
- **Vector Database**: ChromaDB
- **Document Processing**: LangChain

## 🔧 Quick Start

### Prerequisites

- Python 3.8+
- Groq AI API key
- Git

### Local Development

1. **Clone the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Run the setup script
   python setup.py
   
   # Or manually create .env file
   cp env_example.txt .env
   # Edit .env and add your GROQ_API_KEY
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access the app**
   - Web Interface: http://localhost:8501
   - API Docs: http://localhost:8000/docs

## 🛠️ Troubleshooting

### Common Issues

1. **"GROQ_API_KEY is required" error**
   - Make sure you have a `.env` file in the project root
   - Add your Groq API key: `GROQ_API_KEY=your_actual_api_key`
   - Get your API key from: https://console.groq.com/

2. **Import errors**
   - Run: `pip install -r requirements.txt`
   - Make sure you're using Python 3.8+

3. **"Module not found" errors**
   - Check that all files are in the correct directory
   - Run the setup script: `python setup.py`

4. **API connection issues**
   - Check if the FastAPI server is running on port 8000
   - Verify your internet connection
   - Check your Groq API key is valid

5. **Document upload failures**
   - Ensure file is under 10MB
   - Check file format (PDF, TXT, MD only)
   - Try with smaller files first

### Debug Steps

1. **Check environment**
   ```bash
   python setup.py
   ```

2. **Test API directly**
   ```bash
   python api.py
   ```

3. **Test Streamlit directly**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Check logs**
   - Look for error messages in the terminal
   - Check the browser console for frontend errors

## 🌐 Deployment

### Streamlit Community Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Update deployment configuration"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository: `rag-chatbot-groq`
   - Set the main file path to: `streamlit_app_deploy.py`
   - Click "Deploy!"

3. **Configure Environment Variables**
   - In your deployed app, go to "Settings" (⚙️ icon)
   - Click "Secrets"
   - Add your Groq API key:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key_here"
   ```

4. **Optional: Add other environment variables**
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key_here"
   EMBEDDING_MODEL = "text-embedding-3-small"
   LLM_MODEL = "llama3-8b-8192"
   CHUNK_SIZE = "500"
   CHUNK_OVERLAP = "50"
   ```

5. **Save and Redeploy**
   - Click "Save"
   - Your app will automatically redeploy

### Environment Variables for Deployment

Add these to your Streamlit Cloud secrets:

```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "llama3-8b-8192"
CHUNK_SIZE = "500"
CHUNK_OVERLAP = "50"
```

## 📁 Project Structure

```
rag-chatbot/
├── streamlit_app.py      # Main Streamlit interface
├── api.py               # FastAPI backend
├── rag_chatbot.py       # RAG logic
├── document_processor.py # Document processing
├── vector_store.py      # Vector database operations
├── config.py           # Configuration management
├── run.py              # Application runner
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in repo)
├── env_example.txt    # Environment template
└── README.md          # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq AI API key | Required |
| `EMBEDDING_MODEL` | Embedding model name | `text-embedding-3-small` |
| `LLM_MODEL` | LLM model name | `llama3-8b-8192` |
| `CHUNK_SIZE` | Document chunk size | `500` |
| `CHUNK_OVERLAP` | Chunk overlap size | `50` |

### API Endpoints

- `GET /health` - Health check
- `GET /stats` - Get knowledge base statistics
- `POST /upload-document` - Upload a document
- `POST /chat` - Send a chat message
- `DELETE /clear-knowledge-base` - Clear all documents

## 🎨 UI Features

- **Dark Theme**: Professional dark color scheme
- **Progress Tracking**: Real-time upload progress
- **File Validation**: Size and type checking
- **Context Display**: View source documents
- **Quick Actions**: Pre-defined questions
- **Statistics**: Document and chunk counts

## 🔒 Security

- API key stored in environment variables
- File size limits (10MB max)
- Input validation and sanitization
- Secure file handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Groq AI](https://groq.com/)
- Uses [LangChain](https://langchain.com/) for RAG
- Vector storage with [ChromaDB](https://chromadb.com/)

---

**Made with ❤️ using Streamlit, FastAPI, and Groq AI**
