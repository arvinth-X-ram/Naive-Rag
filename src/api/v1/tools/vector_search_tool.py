from src.core.db import get_vector_store
from langchain_core.tools import tool


def query_documents(query: str, k: int = 5) -> list[dict]:
   """
    Use this tool for semantic similarity search over HR documents.
    Best for natural language and concept-based HR questions.
    Use when the user wants explanations or process descriptions.
    Do not rely on exact keyword matching when using this tool.
   """
   vector_store = get_vector_store()
   docs = vector_store.similarity_search(query, k=k)
   return [
      {
         "content": doc.page_content, 
         "metadata": doc.metadata
      } 
        for doc in docs
        ]