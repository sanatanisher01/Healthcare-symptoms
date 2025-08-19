from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MediCheck API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "MediCheck API is running"}

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple dict-based models to avoid pydantic issues

# API configurations
HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HF_MODEL = "microsoft/DialoGPT-medium"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

@app.post("/verify-star")
async def verify_star(request: dict):
    """Check if user has starred the repository"""
    username = request.get("github_username", "").strip()
    
    # Test bypass
    if username.lower() in ["test", "demo"]:
        return {"starred": True, "message": "Test access granted!"}
    
    # Special bypass for repo owner
    if username.lower() == "sanatanisher01":
        return {"starred": True, "message": "Repository owner access granted!"}
    
    try:
        # First check if user exists
        user_url = f"https://api.github.com/users/{username}"
        headers = {"User-Agent": "MediCheck-App/1.0"}
        
        if GITHUB_TOKEN:
            headers["Authorization"] = f"token {GITHUB_TOKEN}"
        
        print(f"Checking user: {username}")
        user_response = requests.get(user_url, headers=headers, timeout=15)
        print(f"User API status: {user_response.status_code}")
        
        if user_response.status_code != 200:
            return {"starred": False, "message": f"GitHub user '{username}' not found"}
        
        # Check if user starred the repo
        star_url = f"https://api.github.com/users/{username}/starred/sanatanisher01/Healthcare-symptoms"
        star_response = requests.get(star_url, headers=headers, timeout=15)
        
        print(f"Star API status: {star_response.status_code}")
        print(f"Rate limit remaining: {star_response.headers.get('X-RateLimit-Remaining', 'unknown')}")
        
        if star_response.status_code == 204:
            return {"starred": True, "message": "Access granted!"}
        elif star_response.status_code == 404:
            return {"starred": False, "message": "Repository not starred. Please star it first!"}
        elif star_response.status_code == 403:
            return {"starred": False, "message": "Rate limit exceeded. Try again later."}
        else:
            return {"starred": False, "message": f"Verification failed (Status: {star_response.status_code})"}
            
    except requests.exceptions.Timeout:
        return {"starred": False, "message": "Request timeout. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"starred": False, "message": "Connection error. Check your internet."}
    except Exception as e:
        print(f"Star verification error: {str(e)}")
        return {"starred": False, "message": f"Error: {str(e)[:50]}..."}

@app.post("/check-symptoms")
async def check_symptoms(request: dict, github_username: str = None):
    """Analyze symptoms - requires GitHub star verification"""
    
    if not github_username:
        raise HTTPException(status_code=403, detail="GitHub username required")
    
    # Test bypass
    if github_username.lower() in ["test", "demo", "sanatanisher01"]:
        pass  # Skip verification for test users and repo owner
    else:
        # Verify star
        try:
            url = f"https://api.github.com/users/{github_username}/starred/sanatanisher01/Healthcare-symptoms"
            headers = {"User-Agent": "MediCheck-App/1.0"}
            if GITHUB_TOKEN:
                headers["Authorization"] = f"token {GITHUB_TOKEN}"
            star_response = requests.get(url, headers=headers, timeout=15)
            
            if star_response.status_code != 204:
                raise HTTPException(status_code=403, detail="Please star the repository first")
        except requests.RequestException:
            raise HTTPException(status_code=403, detail="Unable to verify star status")
    
    # Fallback response
    symptoms_lower = request.get("symptoms", "").lower()
    
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
    
    return {"diagnoses": diagnoses, "recommendations": recommendations}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)