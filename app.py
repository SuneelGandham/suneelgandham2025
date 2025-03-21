import streamlit as st
import requests

st.title("GenAI Support Chatbot")

user_input = st.text_input("Ask a question:")
if st.button("Get Answer"):
    response = requests.post("http://127.0.0.1:8000/chat/", json={"prompt": user_input})
    st.write(response.json()["response"])