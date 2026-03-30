import streamlit as st
import requests

st.set_page_config(page_title="RAG Explorer", page_icon="🔍")
st.title("Streamlit RAG UI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Enter your query..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        url = "http://127.0.0.1:8000/api/v1/query/"
        payload = {"query": prompt}
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  
            data = response.json()
            full_response = data.get("result", "No 'result' key found in API response.")
            
            st.markdown(full_response)
            
        except requests.exceptions.RequestException as e:
            full_response = f"⚠️ Error connecting to API: {str(e)}"
            st.error(full_response)

    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})