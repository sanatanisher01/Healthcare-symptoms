from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MediCheck API", version="1.0.0")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MediCheck - AI Healthcare Symptom Checker</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    </head>
    <body class="bg-gray-50">
        <div id="app">
            <div class="max-w-4xl mx-auto px-4 py-12">
                <h1 class="text-4xl font-bold text-center text-gray-900 mb-12">AI Symptom Checker</h1>
                
                <div id="star-section" class="bg-yellow-50 border-l-4 border-yellow-400 p-6 mb-8 rounded-lg">
                    <h2 class="text-xl font-semibold text-yellow-800 mb-4">⭐ Star Required</h2>
                    <p class="text-yellow-700 mb-4">Please star our repository to access the AI symptom checker:</p>
                    <a href="https://github.com/sanatanisher01/Healthcare-symptoms" target="_blank" class="inline-block bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700 mb-4">⭐ Star Repository</a>
                    
                    <div class="mb-3">
                        <p class="text-sm text-yellow-700 mb-2"><strong>Username Format:</strong> Enter only your GitHub username (not full URL)</p>
                        <p class="text-xs text-yellow-600">✅ Correct: <code class="bg-yellow-100 px-1 rounded">sanatanisher01</code><br/>❌ Wrong: <code class="bg-red-100 px-1 rounded">https://github.com/sanatanisher01</code></p>
                    </div>
                    
                    <div class="flex gap-2">
                        <input type="text" id="username" placeholder="username (e.g., sanatanisher01)" class="flex-1 p-3 border border-gray-300 rounded-lg">
                        <button onclick="verifyGitHubStar()" class="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700">Verify</button>
                    </div>
                </div>

                <div id="symptom-form" class="bg-white rounded-2xl shadow-xl p-8 mb-8 opacity-50 pointer-events-none">
                    <div class="space-y-6">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Describe your symptoms</label>
                            <textarea id="symptoms" class="w-full p-4 border border-gray-300 rounded-lg" rows="4" placeholder="e.g., fever, cough, sore throat, headache..."></textarea>
                        </div>
                        
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Age Group</label>
                                <select id="age_group" class="w-full p-3 border border-gray-300 rounded-lg">
                                    <option value="">Select age group</option>
                                    <option value="Child">Child (0-12)</option>
                                    <option value="Teen">Teen (13-19)</option>
                                    <option value="Adult">Adult (20-64)</option>
                                    <option value="Senior">Senior (65+)</option>
                                </select>
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Gender</label>
                                <select id="gender" class="w-full p-3 border border-gray-300 rounded-lg">
                                    <option value="">Select gender</option>
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                        </div>
                        
                        <button onclick="checkSymptoms()" class="w-full bg-blue-600 text-white py-4 px-6 rounded-lg font-semibold hover:bg-blue-700">⭐ Star Repository First</button>
                    </div>
                </div>

                <div id="results" class="bg-white rounded-2xl shadow-xl p-8 hidden">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6">Results</h2>
                    <div id="results-content"></div>
                    <div class="mt-8 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-lg">
                        <p class="text-sm text-yellow-800"><strong>Disclaimer:</strong> This is not a medical diagnosis. Please consult a doctor for proper medical advice.</p>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let isVerified = false;
            let githubUsername = '';

            async function verifyGitHubStar() {
                const username = document.getElementById('username').value.trim();
                if (!username) {
                    alert('Please enter your GitHub username');
                    return;
                }

                try {
                    const response = await axios.post('/verify-star', { github_username: username });
                    if (response.data.starred) {
                        isVerified = true;
                        githubUsername = username;
                        document.getElementById('star-section').style.display = 'none';
                        document.getElementById('symptom-form').classList.remove('opacity-50', 'pointer-events-none');
                        document.querySelector('#symptom-form button').textContent = 'Check Symptoms';
                        alert('✅ Verification successful! You can now use the symptom checker.');
                    } else {
                        alert(`❌ ${response.data.message}`);
                    }
                } catch (error) {
                    alert('❌ Unable to verify. Please try again.');
                }
            }

            async function checkSymptoms() {
                if (!isVerified) {
                    alert('Please verify your GitHub star first!');
                    return;
                }

                const symptoms = document.getElementById('symptoms').value;
                const age_group = document.getElementById('age_group').value;
                const gender = document.getElementById('gender').value;

                if (!symptoms || !age_group || !gender) {
                    alert('Please fill in all fields');
                    return;
                }

                try {
                    const response = await axios.post(`/check-symptoms?github_username=${githubUsername}`, {
                        symptoms, age_group, gender
                    });

                    const resultsContent = `
                        <div class="space-y-6">
                            <div>
                                <h3 class="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                                    <span class="text-2xl mr-2">🔍</span>Possible Diagnoses
                                </h3>
                                <div class="space-y-2">
                                    ${response.data.diagnoses.map(d => `<div class="bg-blue-50 p-3 rounded-lg border-l-4 border-blue-500">${d}</div>`).join('')}
                                </div>
                            </div>
                            
                            <div>
                                <h3 class="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                                    <span class="text-2xl mr-2">💡</span>Recommended Next Steps
                                </h3>
                                <div class="space-y-2">
                                    ${response.data.recommendations.map(r => `<div class="bg-green-50 p-3 rounded-lg border-l-4 border-green-500">${r}</div>`).join('')}
                                </div>
                            </div>
                        </div>
                    `;

                    document.getElementById('results-content').innerHTML = resultsContent;
                    document.getElementById('results').classList.remove('hidden');
                } catch (error) {
                    alert('Error checking symptoms. Please try again.');
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/api")
async def api_status():
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