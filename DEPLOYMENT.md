# 🚀 Deployment Guide for Streamlit Community Cloud

This guide will help you deploy your RAG Chatbot to Streamlit Community Cloud.

## 📋 Prerequisites

1. **GitHub Account**: You need a GitHub account
2. **Groq AI API Key**: Get your API key from [Groq Console](https://console.groq.com/)
3. **Git**: Make sure Git is installed on your computer

## 🔧 Step-by-Step Deployment

### Step 1: Create a GitHub Repository

1. **Go to GitHub** and create a new repository
   - Visit [github.com](https://github.com)
   - Click "New repository"
   - Name it something like `rag-chatbot-groq`
   - Make it **Public** (required for Streamlit Cloud)
   - Don't initialize with README (we already have one)

### Step 2: Push Your Code to GitHub

Open your terminal/command prompt and run:

```bash
# Navigate to your project directory
cd C:\Users\amaan\project

# Initialize Git repository
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit: RAG Chatbot with Groq AI"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/rag-chatbot-groq.git

# Push to GitHub
git push -u origin main
```

**Replace `YOUR_USERNAME`** with your actual GitHub username.

### Step 3: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app"
   - Select your repository: `rag-chatbot-groq`
   - Set the main file path to: `streamlit_app_deploy.py`
   - Click "Deploy!"

### Step 4: Configure Environment Variables

1. **Add Secrets**
   - In your deployed app, go to "Settings" (⚙️ icon)
   - Click "Secrets"
   - Add your Groq API key:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

2. **Optional: Add other environment variables**
```toml
GROQ_API_KEY = "your_groq_api_key_here"
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "llama3-8b-8192"
CHUNK_SIZE = "500"
CHUNK_OVERLAP = "50"
```

3. **Save and Redeploy**
   - Click "Save"
   - Your app will automatically redeploy

## 🌐 Your App is Live!

Once deployed, you'll get a URL like:
`https://your-app-name-your-username.streamlit.app`

## 🔍 Troubleshooting

### Common Issues:

1. **"Module not found" errors**
   - Make sure all files are pushed to GitHub
   - Check that `requirements.txt` is in the repository

2. **"API key not found" errors**
   - Verify your secrets are correctly configured
   - Check the secret name matches exactly: `GROQ_API_KEY`

3. **"Import errors"**
   - Make sure you're using `streamlit_app_deploy.py` (not `streamlit_app.py`)
   - The deploy version includes all backend functionality

4. **"Timeout errors"**
   - Document processing can take time
   - Try with smaller files first

### Debug Steps:

1. **Check the logs**
   - In Streamlit Cloud, go to your app
   - Click "Manage app" → "Logs"

2. **Test locally first**
   ```bash
   python streamlit_app_deploy.py
   ```

3. **Verify GitHub repository**
   - All files should be visible in your GitHub repo
   - Check that `.env` is NOT in the repository (it's in `.gitignore`)

## 📁 Required Files for Deployment

Make sure these files are in your GitHub repository:

- ✅ `streamlit_app_deploy.py` (main app file)
- ✅ `config.py`
- ✅ `document_processor.py`
- ✅ `vector_store.py`
- ✅ `rag_chatbot.py`
- ✅ `requirements.txt`
- ✅ `README.md`
- ✅ `.gitignore`
- ❌ `.env` (should NOT be in repository)

## 🎉 Success!

Once deployed, your RAG Chatbot will be:
- 🌐 **Publicly accessible** via web URL
- 🤖 **Fully functional** with Groq AI
- 📚 **Able to process documents** and answer questions
- 🎨 **Beautiful dark theme** with improved visibility

## 🔄 Updates

To update your deployed app:

1. **Make changes locally**
2. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
3. **Streamlit Cloud** will automatically redeploy

---

**Your RAG Chatbot is now live on the internet! 🚀**
