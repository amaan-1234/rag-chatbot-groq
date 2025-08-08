import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import Config

class VectorStore:
    """Handles vector database operations using ChromaDB."""
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Ensure the database directory exists
        os.makedirs(Config.CHROMA_DB_PATH, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=Config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize LangChain vector store
        self.vectorstore = Chroma(
            client=self.client,
            collection_name=Config.COLLECTION_NAME,
            embedding_function=self.embeddings
        )
    
    def add_documents(self, texts: List[str], metadata: List[Dict[str, Any]]) -> None:
        """Add documents to the vector store."""
        if len(texts) != len(metadata):
            raise ValueError("Number of texts must match number of metadata entries")
        
        # Add to ChromaDB collection
        ids = [f"doc_{i}" for i in range(len(texts))]
        self.collection.add(
            documents=texts,
            metadatas=metadata,
            ids=ids
        )
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'text': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {},
                    'distance': results['distances'][0][i] if results['distances'] and results['distances'][0] else None
                })
        
        return formatted_results
    
    def similarity_search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Perform similarity search using LangChain."""
        docs = self.vectorstore.similarity_search(query, k=k)
        
        results = []
        for doc in docs:
            results.append({
                'text': doc.page_content,
                'metadata': doc.metadata
            })
        
        return results
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        count = self.collection.count()
        return {
            'total_documents': count,
            'collection_name': Config.COLLECTION_NAME
        }
    
    def clear_collection(self) -> None:
        """Clear all documents from the collection."""
        self.client.delete_collection(Config.COLLECTION_NAME)
        self.collection = self.client.create_collection(
            name=Config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        self.vectorstore = Chroma(
            client=self.client,
            collection_name=Config.COLLECTION_NAME,
            embedding_function=self.embeddings
        )
