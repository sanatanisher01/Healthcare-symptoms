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
    allow_origins=["*"],  # Allow all origins for production
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
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Optional: for higher rate limits
HF_MODEL = "microsoft/DialoGPT-medium"  # More reliable model
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

def query_huggingface_model(prompt: str) -> str:
    """Query the Hugging Face model with the given prompt"""
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.3,
            "do_sample": True,
            "return_full_text": False
        }
    }
    
    print(f"Querying Hugging Face model: {HF_MODEL}")
    print(f"Token available: {bool(HF_API_TOKEN)}")
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 503:
            print("Model is loading, this may take a few minutes...")
            return ""
            
        response.raise_for_status()
        result = response.json()
        print(f"Raw AI response: {result}")
        
        if isinstance(result, list) and len(result) > 0:
            generated_text = result[0].get("generated_text", "")
            print(f"Generated text: {generated_text}")
            return generated_text
        elif isinstance(result, dict) and "generated_text" in result:
            print(f"Generated text: {result['generated_text']}")
            return result["generated_text"]
        return ""
    except Exception as e:
        print(f"Error querying Hugging Face: {e}")
        if 'response' in locals():
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")
        return ""

def parse_ai_response(response_text: str) -> dict:
    """Parse AI response and extract diagnoses and recommendations"""
    try:
        # Try to find JSON in the response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != -1:
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
    except:
        pass
    
    # Fallback parsing if JSON extraction fails
    lines = response_text.split('\n')
    diagnoses = []
    recommendations = []
    
    current_section = None
    for line in lines:
        line = line.strip()
        if 'diagnoses' in line.lower() or 'diagnosis' in line.lower():
            current_section = 'diagnoses'
        elif 'recommendation' in line.lower() or 'next step' in line.lower():
            current_section = 'recommendations'
        elif line.startswith('-') or line.startswith('•') or line.startswith('*'):
            item = line[1:].strip()
            if current_section == 'diagnoses':
                diagnoses.append(item)
            elif current_section == 'recommendations':
                recommendations.append(item)
    
    return {
        "diagnoses": diagnoses if diagnoses else ["Unable to determine specific diagnoses"],
        "recommendations": recommendations if recommendations else ["Consult a healthcare professional"]
    }



@app.get("/test-github/{username}")
async def test_github(username: str):
    """Test GitHub API connectivity"""
    try:
        # Test basic user API first
        user_url = f"https://api.github.com/users/{username}"
        headers = {"User-Agent": "MediCheck-App"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
        user_response = requests.get(user_url, headers=headers, timeout=10)
        
        # Test starred repo API
        star_url = f"https://api.github.com/users/{username}/starred/sanatanisher01/Healthcare-symptoms"
        star_response = requests.get(star_url, headers=headers, timeout=10)
        
        return {
            "user_api": {
                "status": user_response.status_code,
                "exists": user_response.status_code == 200
            },
            "star_api": {
                "status": star_response.status_code,
                "starred": star_response.status_code == 204
            },
            "rate_limit": star_response.headers.get("X-RateLimit-Remaining", "unknown")
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/verify-star")
async def verify_star(request: StarCheckRequest):
    """Check if user has starred the repository"""
    try:
        username = request.github_username.strip()
        
        # First check if user exists
        user_url = f"https://api.github.com/users/{username}"
        headers = {"User-Agent": "MediCheck-App"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"token {GITHUB_TOKEN}"
        user_response = requests.get(user_url, headers=headers, timeout=10)
        
        if user_response.status_code != 200:
            return {"starred": False, "message": f"GitHub user '{username}' not found"}
        
        # Check if user starred the repo
        star_url = f"https://api.github.com/users/{username}/starred/sanatanisher01/Healthcare-symptoms"
        star_response = requests.get(star_url, headers=headers, timeout=10)
        
        print(f"User: {username}")
        print(f"User API: {user_response.status_code}")
        print(f"Star API: {star_response.status_code}")
        print(f"Rate limit: {star_response.headers.get('X-RateLimit-Remaining', 'unknown')}")
        
        if star_response.status_code == 204:
            return {"starred": True, "message": "Access granted!"}
        elif star_response.status_code == 404:
            return {"starred": False, "message": "Repository not starred. Please star it first!"}
        elif star_response.status_code == 403:
            return {"starred": False, "message": "Rate limit exceeded. Please try again in a few minutes."}
        else:
            return {"starred": False, "message": f"Verification failed (Status: {star_response.status_code})"}
            
    except Exception as e:
        print(f"Star verification error: {e}")
        return {"starred": False, "message": "Network error. Please try again."}

@app.post("/check-symptoms")
async def check_symptoms(request: SymptomRequest, github_username: str = None):
    """Analyze symptoms - requires GitHub star verification"""
    
    # Verify star first
    if not github_username:
        raise HTTPException(status_code=403, detail="GitHub username required")
        
    try:
        url = f"https://api.github.com/users/{github_username}/starred/sanatanisher01/Healthcare-symptoms"
        headers = {"User-Agent": "MediCheck-App"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
        star_response = requests.get(url, headers=headers, timeout=10)
        
        if star_response.status_code != 204:
            raise HTTPException(status_code=403, detail="Please star the repository first")
    except requests.RequestException as e:
        print(f"Star verification error: {e}")
        raise HTTPException(status_code=403, detail="Unable to verify star status")
    
    # Create prompt for the AI model
    prompt = f"""You are a medical assistant AI. 
Input: A {request.age_group} {request.gender} reports the following symptoms: {request.symptoms}.  
Task: Provide:
1. A list of possible diagnoses (in simple terms).  
2. Recommended next steps (doctor consultation, home care, emergency, etc.).  
Format response in JSON:  
{{
  "diagnoses": ["...", "..."],
  "recommendations": ["...", "..."]
}}"""

    # Query the AI model
    print(f"API Token present: {bool(HF_API_TOKEN)}")
    if HF_API_TOKEN:
        print("Attempting to use Hugging Face AI model...")
        ai_response = query_huggingface_model(prompt)
        if ai_response:
            print("AI model responded successfully")
            parsed_response = parse_ai_response(ai_response)
            parsed_response["diagnoses"] = [f"[AI] {d}" for d in parsed_response["diagnoses"]]
            return SymptomResponse(**parsed_response)
        else:
            print("AI model failed, using fallback")
    else:
        print("No API token, using fallback")
    
    # Fallback response if AI is unavailable
    print("Using fallback responses (AI not available)")
    symptoms_lower = request.symptoms.lower()
    
    if any(word in symptoms_lower for word in ['fever', 'cough', 'sore throat']):
        fallback_diagnoses = ["[FALLBACK] Common Cold", "[FALLBACK] Flu", "[FALLBACK] Upper Respiratory Infection"]
        fallback_recommendations = [
            "Rest and drink plenty of fluids",
            "Monitor temperature regularly",
            "Consult a doctor if symptoms worsen or persist > 3 days"
        ]
    elif any(word in symptoms_lower for word in ['headache', 'nausea']):
        fallback_diagnoses = ["[FALLBACK] Tension Headache", "[FALLBACK] Migraine", "[FALLBACK] Dehydration"]
        fallback_recommendations = [
            "Rest in a quiet, dark room",
            "Stay hydrated",
            "Consider over-the-counter pain relief",
            "See a doctor if severe or persistent"
        ]
    else:
        fallback_diagnoses = ["[FALLBACK] Various conditions possible"]
        fallback_recommendations = [
            "Monitor symptoms closely",
            "Consult a healthcare professional for proper evaluation",
            "Seek immediate care if symptoms are severe"
        ]
    
    return SymptomResponse(
        diagnoses=fallback_diagnoses,
        recommendations=fallback_recommendations
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port))
        if ai_response:
            print("AI model responded successfully")
            parsed_response = parse_ai_response(ai_response)
            # Add AI indicator to response
            parsed_response["diagnoses"] = [f"[AI] {d}" for d in parsed_response["diagnoses"]]
            return SymptomResponse(**parsed_response)
        else:
            print("AI model failed, using fallback")
    else:
        print("No API token, using fallback")
    
    # Fallback response if AI is unavailable
    print("Using fallback responses (AI not available)")
    fallback_diagnoses = []
    fallback_recommendations = []
    
    symptoms_lower = request.symptoms.lower()
    
    # Simple symptom matching for demo
    if any(word in symptoms_lower for word in ['fever', 'cough', 'sore throat']):
        fallback_diagnoses = ["[FALLBACK] Common Cold", "[FALLBACK] Flu", "[FALLBACK] Upper Respiratory Infection"]
        fallback_recommendations = [
            "Rest and drink plenty of fluids",
            "Monitor temperature regularly",
            "Consult a doctor if symptoms worsen or persist > 3 days"
        ]
    elif any(word in symptoms_lower for word in ['headache', 'nausea']):
        fallback_diagnoses = ["[FALLBACK] Tension Headache", "[FALLBACK] Migraine", "[FALLBACK] Dehydration"]
        fallback_recommendations = [
            "Rest in a quiet, dark room",
            "Stay hydrated",
            "Consider over-the-counter pain relief",
            "See a doctor if severe or persistent"
        ]
    else:
        fallback_diagnoses = ["[FALLBACK] Various conditions possible"]
        fallback_recommendations = [
            "Monitor symptoms closely",
            "Consult a healthcare professional for proper evaluation",
            "Seek immediate care if symptoms are severe"
        ]
    
    return SymptomResponse(
        diagnoses=fallback_diagnoses,
        recommendations=fallback_recommendations
    )

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)