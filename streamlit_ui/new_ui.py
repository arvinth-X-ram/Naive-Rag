import streamlit as st
import requests
import json

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. Admin Page
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

# 2. User Page
def user_page():
    st.title("Streamlit RAG UI")

    # --- User Data JSON Input ---
    st.subheader("User Metadata")
    user_data_text = st.text_area(
        "Enter user data (JSON format)",
        placeholder='{"user_id": "123", "role": "analyst"}'
    )

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Enter your query..."):
        # Parse user_data JSON safely
        try:
            user_data = json.loads(user_data_text) if user_data_text.strip() else {}
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON in user data field")
            user_data = {}

        # Store user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant response
        with st.chat_message("assistant"):
            url = "http://127.0.0.1:8000/api/v1/query/"
            payload = {
                "query": prompt+" "+str(user_data)
            }

            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()

                data = response.json()
                full_response = data.get("answer", "No answer found.")
                policy_citations = data.get("policy_citations", "NA")
                page_no = data.get("page_no", "NA")
                document_name = data.get("document_name", "NA")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })

                st.markdown("**Answer:** " + full_response)
                st.markdown("**Policy Citations:** " + policy_citations)
                st.markdown("**Page No.:** " + str(page_no))
                st.markdown("**Doc Name:** " + document_name)

            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Error connecting to API: {str(e)}")

# Sidebar Navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Admin", "User"])

if selection == "Admin":
    admin_page()
elif selection == "User":
    user_page()


import streamlit as st
import requests
import json

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. Admin Page
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

# 2. User Page
def user_page():
    st.title("Streamlit RAG UI")

    # --- User Data JSON Input ---
    st.subheader("User Metadata")
    user_data_text = st.text_area(
        "Enter user data (JSON format)",
        placeholder='{"user_id": "123", "role": "analyst"}'
    )

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Enter your query..."):
        # Parse user_data JSON safely
        try:
            user_data = json.loads(user_data_text) if user_data_text.strip() else {}
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON in user data field")
            user_data = {}

        # Store user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant response
        with st.chat_message("assistant"):
            url = "http://127.0.0.1:8000/api/v1/query/"
            payload = {
                "query": prompt+" "+str(user_data)
            }

            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()

                data = response.json()
                full_response = data.get("answer", "No answer found.")
                policy_citations = data.get("policy_citations", "NA")
                page_no = data.get("page_no", "NA")
                document_name = data.get("document_name", "NA")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })

                st.markdown("**Answer:** " + full_response)
                st.markdown("**Policy Citations:** " + policy_citations)
                st.markdown("**Page No.:** " + str(page_no))
                st.markdown("**Doc Name:** " + document_name)

            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Error connecting to API: {str(e)}")

# Sidebar Navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Admin", "User"])

if selection == "Admin":
    admin_page()
elif selection == "User":
    user_page()