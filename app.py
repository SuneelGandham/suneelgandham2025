import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get backend URL from environment
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Ensure BACKEND_URL starts with http:// or https://
if not BACKEND_URL.startswith(("http://", "https://")):
    st.error("❌ Invalid BACKEND_URL: It must start with http:// or https://")
    st.stop()

st.title("AI Chatbot")

user_input = st.text_input("Enter your message:")
print("Request:", user_input)
print("backend url:", BACKEND_URL)
if st.button("Send"):
    try:
        response = requests.post(f"{BACKEND_URL}/chat/", json={"prompt": user_input})
        if response.status_code == 200:
            st.write("🤖 AI Response :", response.json()["response"])
        else:
            st.write(f"⚠️ Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {e}")
