from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv
from src.api.v1.services.tools import vector_search_tool
from langchain_classic.memory import ConversationBufferMemory

load_dotenv(override = True)

@tool
def search_pdf_rag(query:str):
    """A simple tool that does vector search for HR policy in a pdf"""
    docs = vector_search_tool(query)

    return docs

# @tool
# def fts_search_pdf_rag(query:str):
#     """A simple tool that does Full-Text search for HR policy in a pdf"""
#     # docs = fts_search_tool(query)

#     # return docs
#     pass

# @tool
# def hybrid_search_pdf_rag(query:str):
#     """A tool that does both vector and Full-Text search for HR policy in a pdf"""
#     # docs = fts_search_tool(query)

#     # return docs
#     pass


my_agent = create_agent(
    model = "google_genai:gemini-3.1-pro-preview",
    tools = [search_pdf_rag],
    system_prompt = "You are a RAG Bot who answers HR policy realted query . Please use the HR policy PDF using the given 'search_pdf_rag'.",
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def agents(query):

    existing_history = memory.load_memory_variables({})["chat_history"]

    messages = existing_history + [{"role": "user", "content": query}]

    response = my_agent.invoke({"messages": messages})

    response_text = response["messages"][-1].content

    memory.save_context({"input": query}, {"output": response_text})

    print(response["messages"][-1].text)
    return response