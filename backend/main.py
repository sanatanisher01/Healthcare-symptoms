from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MediCheck API", version="1.0.0")

# Mount static files (frontend)
app.mount("/static", StaticFiles(directory="../frontend/dist"), name="static")

@app.get("/")
async def serve_frontend():
    from fastapi.responses import FileResponse
    return FileResponse("../frontend/dist/index.html")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SymptomRequest(BaseModel):
    symptoms: str
    age_group: str
    gender: str

class SymptomResponse(BaseModel):
    diagnoses: list[str]
    recommendations: list[str]

class StarCheckRequest(BaseModel):
    github_username: str

# API configurations
HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HF_MODEL = "microsoft/DialoGPT-medium"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

@app.post("/verify-star")
async def verify_star(request: StarCheckRequest):
    """Check if user has starred the repository"""
    try:
        username = request.github_username.strip().lower()
        
        # Test bypass
        if username in ["test", "demo"]:
            return {"starred": True, "message": "Test access granted!"}
        
        # Check if user starred the repo
        star_url = f"https://api.github.com/users/{username}/starred/sanatanisher01/Healthcare-symptoms"
        headers = {"User-Agent": "MediCheck-App"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
        
        star_response = requests.get(star_url, headers=headers, timeout=10)
        
        if star_response.status_code == 204:
            return {"starred": True, "message": "Access granted!"}
        else:
            return {"starred": False, "message": "Repository not starred. Please star it first!"}
            
    except Exception as e:
        return {"starred": False, "message": "Network error. Please try again."}

@app.post("/check-symptoms")
async def check_symptoms(request: SymptomRequest, github_username: str = None):
    """Analyze symptoms - requires GitHub star verification"""
    
    if not github_username:
        raise HTTPException(status_code=403, detail="GitHub username required")
    
    # Test bypass
    if github_username.lower() in ["test", "demo"]:
        pass  # Skip verification for test users
    else:
        # Verify star
        try:
            url = f"https://api.github.com/users/{github_username}/starred/sanatanisher01/Healthcare-symptoms"
            headers = {"User-Agent": "MediCheck-App"}
            if GITHUB_TOKEN:
                headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
            star_response = requests.get(url, headers=headers, timeout=10)
            
            if star_response.status_code != 204:
                raise HTTPException(status_code=403, detail="Please star the repository first")
        except requests.RequestException:
            raise HTTPException(status_code=403, detail="Unable to verify star status")
    
    # Fallback response
    symptoms_lower = request.symptoms.lower()
    
    if any(word in symptoms_lower for word in ['fever', 'cough', 'sore throat']):
        diagnoses = ["Common Cold", "Flu", "Upper Respiratory Infection"]
        recommendations = [
            "Rest and drink plenty of fluids",
            "Monitor temperature regularly",
            "Consult a doctor if symptoms worsen or persist > 3 days"
        ]
    elif any(word in symptoms_lower for word in ['headache', 'nausea']):
        diagnoses = ["Tension Headache", "Migraine", "Dehydration"]
        recommendations = [
            "Rest in a quiet, dark room",
            "Stay hydrated",
            "Consider over-the-counter pain relief",
            "See a doctor if severe or persistent"
        ]
    else:
        diagnoses = ["Various conditions possible"]
        recommendations = [
            "Monitor symptoms closely",
            "Consult a healthcare professional for proper evaluation",
            "Seek immediate care if symptoms are severe"
        ]
    
    return SymptomResponse(diagnoses=diagnoses, recommendations=recommendations)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)