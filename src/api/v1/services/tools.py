from src.core.db import get_vector_store


def vector_search_tool(query):

    vector_store = get_vector_store()
    
    docs = vector_store.similarity_search(query, k=5)
    return docs