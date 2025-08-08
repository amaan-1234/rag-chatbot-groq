# 🚀 Streamlit Cloud Deployment Guide

This guide will help you deploy your RAG Chatbot to Streamlit Cloud successfully.

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be pushed to GitHub
2. **Groq AI API Key**: Get your API key from [Groq Console](https://console.groq.com/)

## 🔧 Step-by-Step Deployment

### Step 1: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app"
   - Select your repository: `rag-chatbot-groq`
   - Set the main file path to: `streamlit_app_deploy.py`
   - Click "Deploy!"

### Step 2: Configure Environment Variables

**IMPORTANT**: You must add your Groq API key to the Streamlit Cloud secrets.

1. **Access App Settings**
   - Go to your deployed app URL
   - Click the ⚙️ (Settings) icon in the top right
   - Click on "Secrets"

2. **Add Your API Key**
   - In the secrets editor, add:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key_here"
   ```
   - Replace `your_actual_groq_api_key_here` with your real Groq API key
   - Click "Save"

3. **Optional: Add other environment variables**
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key_here"
   EMBEDDING_MODEL = "text-embedding-3-small"
   LLM_MODEL = "llama3-8b-8192"
   CHUNK_SIZE = "500"
   CHUNK_OVERLAP = "50"
   ```

### Step 3: Verify Deployment

After saving the secrets, your app will automatically redeploy. You should see:

- ✅ "System Ready" message in the sidebar
- ✅ No error messages about missing API keys
- ✅ Ability to upload documents and chat

## 🛠️ Troubleshooting

### Common Issues

1. **"GROQ_API_KEY environment variable is not set"**
   - **Solution**: Add your API key to Streamlit Cloud secrets
   - Go to Settings → Secrets → Add your key

2. **"GROQ_API_KEY is still set to placeholder value"**
   - **Solution**: Replace the placeholder with your actual API key
   - Make sure you're using your real Groq API key, not the example text

3. **"Failed to initialize components"**
   - **Solution**: Check that your API key is valid
   - Verify your Groq account has credits
   - Test your API key locally first

4. **Import errors**
   - **Solution**: Make sure all files are pushed to GitHub
   - Check that `requirements.txt` is in the repository

### Debug Steps

1. **Test locally first**
   ```bash
   python test_config.py
   ```

2. **Check GitHub repository**
   - Ensure all files are committed and pushed
   - Verify `streamlit_app_deploy.py` is the main file

3. **Verify API key**
   - Get a fresh API key from [Groq Console](https://console.groq.com/)
   - Make sure you have credits in your Groq account

## 📁 Required Files

Make sure these files are in your GitHub repository:

- ✅ `streamlit_app_deploy.py` (main app file)
- ✅ `config.py`
- ✅ `document_processor.py`
- ✅ `vector_store_deploy.py`
- ✅ `rag_chatbot.py`
- ✅ `requirements.txt`
- ✅ `README.md`
- ✅ `.gitignore`

## 🎉 Success!

Once deployed successfully, your RAG Chatbot will be:
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
   git push origin master
   ```
3. **Streamlit Cloud** will automatically redeploy

---

**Your RAG Chatbot is now live on the internet! 🚀**
