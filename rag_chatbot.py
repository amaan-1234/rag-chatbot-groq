from typing import List, Dict, Any, Optional
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from document_processor import DocumentProcessor
from vector_store import VectorStore
from config import Config

class RAGChatbot:
    """RAG-based chatbot that combines retrieval and generation."""
    
    def __init__(self):
        self.llm = ChatGroq(
            model_name=Config.LLM_MODEL,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS,
            groq_api_key=Config.GROQ_API_KEY
        )
        
        self.document_processor = DocumentProcessor()
        self.vector_store = VectorStore()
        
        # Define the system prompt for RAG
        self.system_prompt = """You are a helpful AI assistant that answers questions based on the provided context. 
        Use the following context to answer the user's question. If the context doesn't contain enough information 
        to answer the question, say so and provide a general helpful response.
        
        Context: {context}
        
        Question: {question}
        
        Answer:"""
        
        self.prompt_template = ChatPromptTemplate.from_template(self.system_prompt)
    
    def add_document(self, file_path: str) -> Dict[str, Any]:
        """Add a document to the knowledge base."""
        try:
            # Process the document
            processed_data = self.document_processor.process_document(file_path)
            
            # Add to vector store
            self.vector_store.add_documents(
                texts=processed_data['texts'],
                metadata=processed_data['metadata']
            )
            
            return {
                'success': True,
                'message': f'Successfully added document: {file_path}',
                'chunks_created': len(processed_data['texts'])
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error adding document: {str(e)}'
            }
    
    def get_relevant_context(self, query: str, k: int = 5) -> str:
        """Retrieve relevant context for a query."""
        results = self.vector_store.similarity_search(query, k=k)
        
        if not results:
            return "No relevant context found."
        
        # Combine relevant contexts
        context_parts = []
        for result in results:
            context_parts.append(result['text'])
        
        return "\n\n".join(context_parts)
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate a response using the LLM."""
        try:
            # Create messages for the chat model
            messages = [
                SystemMessage(content=self.system_prompt.format(
                    context=context,
                    question=query
                )),
                HumanMessage(content=query)
            ]
            
            # Generate response
            response = self.llm(messages)
            return response.content
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def chat(self, query: str, k: int = 5) -> Dict[str, Any]:
        """Main chat method that combines retrieval and generation."""
        try:
            # Get relevant context
            context = self.get_relevant_context(query, k=k)
            
            # Generate response
            response = self.generate_response(query, context)
            
            return {
                'success': True,
                'response': response,
                'context': context,
                'query': query
            }
        
        except Exception as e:
            return {
                'success': False,
                'response': f"Error in chat: {str(e)}",
                'context': "",
                'query': query
            }
    
    def get_knowledge_base_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        return self.vector_store.get_collection_stats()
    
    def clear_knowledge_base(self) -> Dict[str, Any]:
        """Clear all documents from the knowledge base."""
        try:
            self.vector_store.clear_collection()
            return {
                'success': True,
                'message': 'Knowledge base cleared successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error clearing knowledge base: {str(e)}'
            }
