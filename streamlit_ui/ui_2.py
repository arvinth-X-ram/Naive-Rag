import streamlit as st
import requests


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. Define your page content as functions
def admin_page():
    BASE_URL = "http://localhost:8000/api/v1"

    st.title("Document Query & Upload System")

    # --- Upload Section ---
    st.header("Upload PDF Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Upload"):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                response = requests.post(f"{BASE_URL}/admin/upload", files=files)
                if response.status_code == 200:
                    st.success(f"Upload successful: {response.json()['file']}")
                else:
                    st.error(f"Upload failed: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

def user_page():
    st.title("Streamlit RAG UI")

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
                full_response = data.get("answer", "No 'result' key found in API response.")
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                st.markdown(full_response)
                
            except requests.exceptions.RequestException as e:
                full_response = f"⚠️ Error connecting to API: {str(e)}"
                st.error(full_response)


st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Admin", "User"])

# 3. Logic to switch between pages
if selection == "Admin":
    admin_page()
elif selection == "User":
    user_page()