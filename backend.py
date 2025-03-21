from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Load Hugging Face API Key
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Store this in environment variables


class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat/")
async def chat(request: ChatRequest):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    data = {"inputs": request.prompt}

    response = requests.post(
        "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
        
        #"https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
        headers=headers,
        json=data
    )
    print("API Status Code:", response.status_code)
    print("Raw API Response:", response.text)  # Debugging Output
    result = response.json()
    return {"response": result[0]["generated_text"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)