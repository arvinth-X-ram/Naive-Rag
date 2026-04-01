import streamlit as st
import requests
import json

# Base URL of your FastAPI backend
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

st.markdown("---")

# --- Query Section ---
st.header("Query Documents")
query_text = st.text_area("Enter your query here")

# New field for user data in JSON format
user_data_text = st.text_area("Enter user data (JSON format)", 
                              placeholder='{"user_id": "123", "role": "analyst"}')

if st.button("Submit Query"):
    if not query_text.strip():
        st.warning("Query cannot be empty")
    else:
        try:
            # Parse JSON safely
            try:
                user_data = json.loads(user_data_text) if user_data_text.strip() else {}
            except json.JSONDecodeError:
                st.error("Invalid JSON format in user data field")
                user_data = {}

            payload = {"query": query_text, "user_data": user_data}
            response = requests.post(f"{BASE_URL}/query", json=payload)

            if response.status_code == 200:
                data = response.json()
                st.subheader("Answer")
                st.write(data["answer"])

                st.subheader("Policy citation")
                st.write(data["policy_citations"])

                st.subheader("Page No.")
                st.write(data["page_no"])

                st.subheader("Document Name")
                st.write(data["document_name"])
                
            #     st.subheader("Top Results")
            #     for idx, result in enumerate(data["results"], start=1):
            #         st.markdown(f"**{idx}. {result}**")
            # else:
            #     st.error(f"Query failed: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")