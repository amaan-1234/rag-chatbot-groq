import os
import pickle
import tempfile
from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from config import Config

class VectorStore:
    """Vector store for document embeddings using FAISS (deployment-friendly)."""
    
    def __init__(self):
        """Initialize the vector store."""
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.vectorstore = None
        self.documents = []
        self._load_existing_data()
    
    def _load_existing_data(self):
        """Load existing data from temporary storage."""
        try:
            # Use a simple file-based storage for deployment
            storage_file = os.path.join(tempfile.gettempdir(), "rag_chatbot_data.pkl")
            if os.path.exists(storage_file):
                with open(storage_file, 'rb') as f:
                    data = pickle.load(f)
                    self.documents = data.get('documents', [])
                    if self.documents:
                        # Recreate FAISS index
                        texts = [doc.page_content for doc in self.documents]
                        metadatas = [doc.metadata for doc in self.documents]
                        self.vectorstore = FAISS.from_texts(
                            texts, 
                            self.embeddings, 
                            metadatas=metadatas
                        )
        except Exception as e:
            print(f"Warning: Could not load existing data: {e}")
            self.documents = []
    
    def _save_data(self):
        """Save data to temporary storage."""
        try:
            storage_file = os.path.join(tempfile.gettempdir(), "rag_chatbot_data.pkl")
            data = {
                'documents': self.documents
            }
            with open(storage_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Warning: Could not save data: {e}")
    
    def add_documents(self, documents: List[Document]) -> Dict[str, Any]:
        """Add documents to the vector store."""
        try:
            if not documents:
                return {"success": False, "message": "No documents to add"}
            
            # Add to documents list
            self.documents.extend(documents)
            
            # Create or update FAISS index
            texts = [doc.page_content for doc in self.documents]
            metadatas = [doc.metadata for doc in self.documents]
            
            if self.vectorstore is None:
                self.vectorstore = FAISS.from_texts(
                    texts, 
                    self.embeddings, 
                    metadatas=metadatas
                )
            else:
                # Add new documents to existing index
                new_texts = [doc.page_content for doc in documents]
                new_metadatas = [doc.metadata for doc in documents]
                self.vectorstore.add_texts(new_texts, metadatas=new_metadatas)
            
            # Save data
            self._save_data()
            
            return {
                "success": True,
                "message": f"Successfully added {len(documents)} documents",
                "chunks_created": len(documents)
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error adding documents: {str(e)}"}
    
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Search for similar documents."""
        try:
            if self.vectorstore is None:
                return []
            
            return self.vectorstore.similarity_search(query, k=k)
        except Exception as e:
            print(f"Error in similarity search: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        try:
            total_documents = len(self.documents)
            total_chunks = len(self.documents)
            
            # Get unique source files
            source_files = set()
            for doc in self.documents:
                if 'source' in doc.metadata:
                    source_files.add(doc.metadata['source'])
            
            return {
                "total_documents": len(source_files),
                "total_chunks": total_chunks,
                "source_files": list(source_files)
            }
        except Exception as e:
            return {
                "total_documents": 0,
                "total_chunks": 0,
                "source_files": [],
                "error": str(e)
            }
    
    def clear_all(self) -> Dict[str, Any]:
        """Clear all documents from the vector store."""
        try:
            self.documents = []
            self.vectorstore = None
            
            # Remove storage file
            storage_file = os.path.join(tempfile.gettempdir(), "rag_chatbot_data.pkl")
            if os.path.exists(storage_file):
                os.remove(storage_file)
            
            return {"success": True, "message": "All documents cleared"}
        except Exception as e:
            return {"success": False, "message": f"Error clearing documents: {str(e)}"}
