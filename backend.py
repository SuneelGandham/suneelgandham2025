import os
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

# ✅ Explicitly load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

app = FastAPI()

# ✅ Read API Key
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HF_API_KEY:
    raise ValueError("⚠️ Missing HUGGINGFACE_API_KEY in .env file!")

class ChatRequest(BaseModel):
    prompt: str

MODEL_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

@app.post("/chat/")
async def chat(request: ChatRequest):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": request.prompt}

    response = requests.post(MODEL_URL, headers=headers, json=payload)
    print("API Status Code:", response.status_code)
    print("Raw API Response:", response.text)  # Debugging Output
    result = response.json()
    if response.status_code == 200:
        return {"response": result[0]["generated_text"]}
    else:
        return {"error": response.text, "status_code": response.status_code}
    return response.json()
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Get PORT from Render or default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port) 
