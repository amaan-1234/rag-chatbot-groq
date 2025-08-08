import os
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from config import Config

class DocumentProcessor:
    """Handles document processing, chunking, and embedding."""
    
    def __init__(self):
        # Use a smaller, faster embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
        )
    
    def load_document(self, file_path: str) -> List[Document]:
        """Load a document from file path."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_extension in ['.txt', '.md']:
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        return loader.load()
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks."""
        return self.text_splitter.split_documents(documents)
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        # Process in smaller batches for better performance
        batch_size = 32
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.embeddings.embed_documents(batch)
            all_embeddings.extend(batch_embeddings)
        
        return all_embeddings
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """Process a document: load, chunk, and generate embeddings."""
        # Load document
        documents = self.load_document(file_path)
        
        # Chunk documents
        chunks = self.chunk_documents(documents)
        
        # Extract text from chunks
        texts = [chunk.page_content for chunk in chunks]
        
        # Generate embeddings
        embeddings = self.get_embeddings(texts)
        
        # Prepare metadata
        metadata_list = []
        for chunk in chunks:
            metadata = chunk.metadata.copy()
            metadata['source'] = file_path
            metadata['chunk_id'] = len(metadata_list)
            metadata_list.append(metadata)
        
        return {
            'texts': texts,
            'embeddings': embeddings,
            'metadata': metadata_list,
            'chunks': chunks
        }
