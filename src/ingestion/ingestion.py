# # 1.Load the pdf
# # 2.Extract the text from the PDF
# # 3.Split the text into chunks
# #   3.1. We can use a simple split method like splitting
# #   3.2. Follow proper chunking stradegy
# #   3.3. Chunk size = x tokens
# #   3.4. chunk overlap = y tokens   
# # 4.Create embeddings for the chunks
# #   4.1. choose the embedding model(gemini-embedding-2-preview or gemini-embedding-001)
# #   4.2. choose the dimension of the embeddings 
# #   4.3. create the embeddings for each chunk
# # 5.Store thw embeddings in a vector database
# #   5.1. our preferred vector db is pgvector
# #   5.2. we have to activate  pgvector extension in our postgres database
# #   5.3. we have to create a table to store the embeddings
# #   5.4. we have the embeddings into the table


import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredPDFLoader,TextLoader,UnstructuredWordDocumentLoader,PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from src.core.db import get_vector_store


load_dotenv(override=True)
PG_CONNECTION = os.getenv("SQLALCHEMY_DATABASE_URL")

def load_document(file_path):
    # Get the file extension
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    elif ext == ".docx" or ext == ".doc":
        loader = UnstructuredWordDocumentLoader(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    # Load the document into a list of LangChain 'Document' objects
    return loader.load(),ext

def ingest_pdf(file_path):
    # loader = UnstructuredPDFLoader(file_path)
    # docs = loader.load()
    docs,ext = load_document(file_path)
    print("Pages: " +  str(len(docs)))

    for doc in docs:
        doc.metadata.update({
            "source": file_path,
            "document_extension": ext,
            "page": doc.metadata.get("page",None),
            "category": "hr_support_desk",
            "last_updated":os.path.getmtime(file_path)
        })
    print("Sample Document: "+str(docs[0]))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100
    )

    chunks = splitter.split_documents(docs)
    print("Chunks: "+str(len(chunks)))

    embeddings = GoogleGenerativeAIEmbeddings(
        model = os.getenv("GOOGLE_EMBEDDINGS_MODEL"),
        api_key = os.getenv("GOOGLE_API_KEY")
    )

    # vector_store = PGVector(
    #     collection_name = "hr_support_desk",
    #     connection = PG_CONNECTION,
    #     embeddings =embeddings
    # )
    vector_store = get_vector_store("hr_support_desk")
    vector_store.add_documents(chunks)

    # vector_store.add_documents(chunks)
    print("Ingestion completed")

# if __name__ == "__main__":
#     ingest_pdf(r"data\HR_Support_Desk_KnowledgeBase.pdf")
