from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add parent directory to path to import core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.triage_system import TriageSystem
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow CORS for React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TriageRequest(BaseModel):
    symptoms: str
    age: str
    history: str

@app.post("/api/triage")
async def run_triage(request: TriageRequest):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API Key not found in environment")
            
        system = TriageSystem(api_key=api_key)
        
        inputs = {
            "symptoms": request.symptoms,
            "age": request.age,
            "history": request.history
        }
        
        result = system.run_simulation(inputs)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
