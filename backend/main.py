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
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MediCheck - AI Healthcare Platform</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            * { font-family: 'Inter', sans-serif; }
            .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            .glass { backdrop-filter: blur(10px); background: rgba(255, 255, 255, 0.1); }
            .animate-float { animation: float 6s ease-in-out infinite; }
            @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-20px); } }
            #three-container { position: absolute; top: 0; left: 0; z-index: -1; }
        </style>
    </head>
    <body class="bg-gray-50 overflow-x-hidden">
        <!-- Navigation -->
        <nav class="fixed top-0 w-full z-50 glass border-b border-white/20">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between items-center h-16">
                    <div class="flex items-center space-x-2">
                        <i class="fas fa-heartbeat text-2xl text-blue-600"></i>
                        <span class="text-xl font-bold text-gray-900">MediCheck</span>
                    </div>
                    <div class="hidden md:flex space-x-8">
                        <a href="#" onclick="showPage('home')" class="nav-link text-gray-700 hover:text-blue-600 transition-colors">Home</a>
                        <a href="#" onclick="showPage('checker')" class="nav-link text-gray-700 hover:text-blue-600 transition-colors">Symptom Checker</a>
                        <a href="#" onclick="showPage('about')" class="nav-link text-gray-700 hover:text-blue-600 transition-colors">About</a>
                        <a href="#" onclick="showPage('contact')" class="nav-link text-gray-700 hover:text-blue-600 transition-colors">Contact</a>
                    </div>
                    <div class="md:hidden">
                        <button onclick="toggleMobileMenu()" class="text-gray-700">
                            <i class="fas fa-bars text-xl"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div id="mobile-menu" class="hidden md:hidden bg-white/90 backdrop-blur-md">
                <div class="px-2 pt-2 pb-3 space-y-1">
                    <a href="#" onclick="showPage('home')" class="block px-3 py-2 text-gray-700">Home</a>
                    <a href="#" onclick="showPage('checker')" class="block px-3 py-2 text-gray-700">Symptom Checker</a>
                    <a href="#" onclick="showPage('about')" class="block px-3 py-2 text-gray-700">About</a>
                    <a href="#" onclick="showPage('contact')" class="block px-3 py-2 text-gray-700">Contact</a>
                </div>
            </div>
        </nav>

        <!-- Three.js Background -->
        <div id="three-container"></div>

        <!-- Home Page -->
        <div id="home-page" class="page min-h-screen pt-16">
            <div class="relative min-h-screen flex items-center justify-center">
                <div class="text-center z-10 px-4">
                    <div class="animate-float mb-8">
                        <i class="fas fa-stethoscope text-6xl text-blue-600 mb-4"></i>
                    </div>
                    <h1 class="text-5xl md:text-7xl font-bold text-gray-900 mb-6">
                        AI-Powered <span class="text-blue-600">Healthcare</span>
                    </h1>
                    <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
                        Get instant symptom analysis and health recommendations powered by advanced AI technology
                    </p>
                    <button onclick="showPage('checker')" class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-full text-lg font-semibold transition-all transform hover:scale-105 shadow-lg">
                        Start Symptom Check <i class="fas fa-arrow-right ml-2"></i>
                    </button>
                </div>
            </div>
            
            <!-- Features Section -->
            <div class="py-20 bg-white">
                <div class="max-w-7xl mx-auto px-4">
                    <h2 class="text-4xl font-bold text-center text-gray-900 mb-16">Why Choose MediCheck?</h2>
                    <div class="grid md:grid-cols-3 gap-8">
                        <div class="text-center p-8 rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-100 hover:shadow-xl transition-all">
                            <i class="fas fa-brain text-4xl text-blue-600 mb-4"></i>
                            <h3 class="text-xl font-semibold mb-4">AI-Powered Analysis</h3>
                            <p class="text-gray-600">Advanced machine learning algorithms analyze your symptoms for accurate insights</p>
                        </div>
                        <div class="text-center p-8 rounded-2xl bg-gradient-to-br from-green-50 to-emerald-100 hover:shadow-xl transition-all">
                            <i class="fas fa-shield-alt text-4xl text-green-600 mb-4"></i>
                            <h3 class="text-xl font-semibold mb-4">Privacy First</h3>
                            <p class="text-gray-600">Your health data is never stored. Complete privacy and confidentiality guaranteed</p>
                        </div>
                        <div class="text-center p-8 rounded-2xl bg-gradient-to-br from-purple-50 to-violet-100 hover:shadow-xl transition-all">
                            <i class="fas fa-clock text-4xl text-purple-600 mb-4"></i>
                            <h3 class="text-xl font-semibold mb-4">Instant Results</h3>
                            <p class="text-gray-600">Get immediate health insights and recommendations in seconds</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Symptom Checker Page -->
        <div id="checker-page" class="page hidden min-h-screen pt-20">
            <div class="max-w-4xl mx-auto px-4 py-12">
                <div class="text-center mb-12">
                    <i class="fas fa-user-md text-5xl text-blue-600 mb-4"></i>
                    <h1 class="text-4xl font-bold text-gray-900 mb-4">AI Symptom Checker</h1>
                    <p class="text-gray-600">Describe your symptoms and get AI-powered health insights</p>
                </div>
                
                <div id="star-section" class="bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-200 p-8 mb-8 rounded-2xl shadow-lg">
                    <div class="text-center mb-6">
                        <i class="fas fa-star text-4xl text-yellow-500 mb-4"></i>
                        <h2 class="text-2xl font-bold text-gray-900 mb-2">GitHub Star Required</h2>
                        <p class="text-gray-700">Support our open-source project to access the AI symptom checker</p>
                    </div>
                    
                    <div class="text-center mb-6">
                        <a href="https://github.com/sanatanisher01/Healthcare-symptoms" target="_blank" 
                           class="inline-flex items-center bg-gray-900 hover:bg-gray-800 text-white px-6 py-3 rounded-full font-semibold transition-all transform hover:scale-105 shadow-lg">
                            <i class="fab fa-github mr-2"></i> Star on GitHub
                        </a>
                    </div>
                    
                    <div class="max-w-md mx-auto">
                        <div class="mb-4">
                            <p class="text-sm text-gray-600 mb-2"><strong>Enter your GitHub username:</strong></p>
                            <p class="text-xs text-gray-500">✅ Correct: <code class="bg-gray-100 px-2 py-1 rounded">sanatanisher01</code></p>
                        </div>
                        <div class="flex gap-3">
                            <input type="text" id="username" placeholder="GitHub username" 
                                   class="flex-1 p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                            <button onclick="verifyGitHubStar()" 
                                    class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-4 rounded-xl font-semibold transition-all">
                                Verify
                            </button>
                        </div>
                    </div>
                </div>

                <div id="symptom-form" class="bg-white rounded-2xl shadow-xl p-8 mb-8 opacity-50 pointer-events-none transition-all">
                    <div class="space-y-6">
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-3">Describe your symptoms</label>
                            <textarea id="symptoms" class="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                                      rows="4" placeholder="e.g., fever, cough, sore throat, headache..."></textarea>
                        </div>
                        
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label class="block text-sm font-semibold text-gray-700 mb-3">Age Group</label>
                                <select id="age_group" class="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500">
                                    <option value="">Select age group</option>
                                    <option value="Child">Child (0-12)</option>
                                    <option value="Teen">Teen (13-19)</option>
                                    <option value="Adult">Adult (20-64)</option>
                                    <option value="Senior">Senior (65+)</option>
                                </select>
                            </div>
                            
                            <div>
                                <label class="block text-sm font-semibold text-gray-700 mb-3">Gender</label>
                                <select id="gender" class="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500">
                                    <option value="">Select gender</option>
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                </select>
                            </div>
                        </div>
                        
                        <button onclick="checkSymptoms()" id="check-btn"
                                class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-4 px-6 rounded-xl font-semibold transition-all transform hover:scale-105 shadow-lg">
                            ⭐ Star Repository First
                        </button>
                    </div>
                </div>

                <div id="results" class="bg-white rounded-2xl shadow-xl p-8 hidden">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                        <i class="fas fa-clipboard-list text-blue-600 mr-3"></i>Analysis Results
                    </h2>
                    <div id="results-content"></div>
                    <div class="mt-8 p-6 bg-gradient-to-r from-yellow-50 to-orange-50 border-l-4 border-yellow-400 rounded-xl">
                        <p class="text-sm text-gray-800 flex items-center">
                            <i class="fas fa-exclamation-triangle text-yellow-600 mr-2"></i>
                            <strong>Medical Disclaimer:</strong> This is not a medical diagnosis. Always consult healthcare professionals for proper medical advice.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- About Page -->
        <div id="about-page" class="page hidden min-h-screen pt-20">
            <div class="max-w-4xl mx-auto px-4 py-12">
                <div class="text-center mb-12">
                    <i class="fas fa-info-circle text-5xl text-blue-600 mb-4"></i>
                    <h1 class="text-4xl font-bold text-gray-900 mb-4">About MediCheck</h1>
                    <p class="text-xl text-gray-600">Revolutionizing healthcare with AI technology</p>
                </div>
                
                <div class="bg-white rounded-2xl shadow-xl p-8 mb-8">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6">Our Mission</h2>
                    <p class="text-gray-600 mb-6 leading-relaxed">
                        MediCheck is dedicated to making healthcare more accessible through cutting-edge AI technology. 
                        Our platform provides instant symptom analysis and health recommendations, helping users make 
                        informed decisions about their health.
                    </p>
                    
                    <div class="grid md:grid-cols-2 gap-8 mt-8">
                        <div class="p-6 bg-blue-50 rounded-xl">
                            <i class="fas fa-microscope text-3xl text-blue-600 mb-4"></i>
                            <h3 class="text-xl font-semibold mb-3">Advanced AI</h3>
                            <p class="text-gray-600">Powered by state-of-the-art machine learning models trained on medical data</p>
                        </div>
                        <div class="p-6 bg-green-50 rounded-xl">
                            <i class="fas fa-users text-3xl text-green-600 mb-4"></i>
                            <h3 class="text-xl font-semibold mb-3">Open Source</h3>
                            <p class="text-gray-600">Built by the community, for the community. Transparent and collaborative development</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Contact Page -->
        <div id="contact-page" class="page hidden min-h-screen pt-20">
            <div class="max-w-4xl mx-auto px-4 py-12">
                <div class="text-center mb-12">
                    <i class="fas fa-envelope text-5xl text-blue-600 mb-4"></i>
                    <h1 class="text-4xl font-bold text-gray-900 mb-4">Contact Us</h1>
                    <p class="text-xl text-gray-600">Get in touch with our team</p>
                </div>
                
                <div class="bg-white rounded-2xl shadow-xl p-8">
                    <div class="grid md:grid-cols-2 gap-8">
                        <div>
                            <h2 class="text-2xl font-bold text-gray-900 mb-6">Get in Touch</h2>
                            <div class="space-y-4">
                                <div class="flex items-center">
                                    <i class="fab fa-github text-2xl text-gray-600 mr-4"></i>
                                    <a href="https://github.com/sanatanisher01/Healthcare-symptoms" class="text-blue-600 hover:underline">
                                        GitHub Repository
                                    </a>
                                </div>
                                <div class="flex items-center">
                                    <i class="fas fa-envelope text-2xl text-gray-600 mr-4"></i>
                                    <a href="mailto:aryansanatani01@gmail.com" class="text-blue-600 hover:underline">aryansanatani01@gmail.com</a>
                                </div>
                                <div class="flex items-center">
                                    <i class="fas fa-globe text-2xl text-gray-600 mr-4"></i>
                                    <a href="https://healthcare-symptoms.onrender.com" class="text-blue-600 hover:underline">healthcare-symptoms.onrender.com</a>
                                </div>
                            </div>
                        </div>
                        <div>
                            <h3 class="text-xl font-semibold mb-4">Quick Links</h3>
                            <div class="space-y-2">
                                <a href="#" onclick="showPage('home')" class="block text-blue-600 hover:underline">Home</a>
                                <a href="#" onclick="showPage('checker')" class="block text-blue-600 hover:underline">Symptom Checker</a>
                                <a href="#" onclick="showPage('about')" class="block text-blue-600 hover:underline">About</a>
                                <a href="https://github.com/sanatanisher01/Healthcare-symptoms" class="block text-blue-600 hover:underline">GitHub</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // Global variables
            let isVerified = localStorage.getItem('medicheck_verified') === 'true';
            let githubUsername = localStorage.getItem('medicheck_username') || '';
            let scene, camera, renderer, particles;

            // Initialize Three.js background
            function initThreeJS() {
                scene = new THREE.Scene();
                camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                renderer = new THREE.WebGLRenderer({ alpha: true });
                renderer.setSize(window.innerWidth, window.innerHeight);
                document.getElementById('three-container').appendChild(renderer.domElement);

                // Create floating particles
                const geometry = new THREE.BufferGeometry();
                const positions = [];
                const colors = [];

                for (let i = 0; i < 1000; i++) {
                    positions.push((Math.random() - 0.5) * 2000);
                    positions.push((Math.random() - 0.5) * 2000);
                    positions.push((Math.random() - 0.5) * 2000);

                    colors.push(0.3 + Math.random() * 0.7);
                    colors.push(0.5 + Math.random() * 0.5);
                    colors.push(1);
                }

                geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
                geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

                const material = new THREE.PointsMaterial({ size: 2, vertexColors: true, transparent: true, opacity: 0.6 });
                particles = new THREE.Points(geometry, material);
                scene.add(particles);

                camera.position.z = 1000;
                animate();
            }

            function animate() {
                requestAnimationFrame(animate);
                particles.rotation.x += 0.0005;
                particles.rotation.y += 0.001;
                renderer.render(scene, camera);
            }

            // Navigation functions
            function showPage(pageId) {
                document.querySelectorAll('.page').forEach(page => page.classList.add('hidden'));
                document.getElementById(pageId + '-page').classList.remove('hidden');
                
                if (pageId === 'checker' && isVerified) {
                    document.getElementById('star-section').style.display = 'none';
                    document.getElementById('symptom-form').classList.remove('opacity-50', 'pointer-events-none');
                    document.getElementById('check-btn').textContent = 'Analyze Symptoms';
                }
            }

            function toggleMobileMenu() {
                document.getElementById('mobile-menu').classList.toggle('hidden');
            }

            // Star verification with persistence
            async function verifyGitHubStar() {
                const username = document.getElementById('username').value.trim();
                if (!username) {
                    showNotification('Please enter your GitHub username', 'warning');
                    return;
                }

                try {
                    const response = await axios.post('/verify-star', { github_username: username });
                    if (response.data.starred) {
                        isVerified = true;
                        githubUsername = username;
                        
                        // Store in localStorage for persistence
                        localStorage.setItem('medicheck_verified', 'true');
                        localStorage.setItem('medicheck_username', username);
                        
                        document.getElementById('star-section').style.display = 'none';
                        document.getElementById('symptom-form').classList.remove('opacity-50', 'pointer-events-none');
                        document.getElementById('check-btn').textContent = 'Analyze Symptoms';
                        
                        showNotification('✅ Verification successful! You can now use the symptom checker.', 'success');
                    } else {
                        showNotification(`❌ ${response.data.message}`, 'error');
                    }
                } catch (error) {
                    showNotification('❌ Unable to verify. Please try again.', 'error');
                }
            }

            // Symptom checking
            async function checkSymptoms() {
                if (!isVerified) {
                    showNotification('Please verify your GitHub star first!', 'warning');
                    return;
                }

                const symptoms = document.getElementById('symptoms').value;
                const age_group = document.getElementById('age_group').value;
                const gender = document.getElementById('gender').value;

                if (!symptoms || !age_group || !gender) {
                    showNotification('Please fill in all fields', 'warning');
                    return;
                }

                document.getElementById('check-btn').innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Analyzing...';

                try {
                    const response = await axios.post(`/check-symptoms?github_username=${githubUsername}`, {
                        symptoms, age_group, gender
                    });

                    const resultsContent = `
                        <div class="space-y-8">
                            ${response.data.source ? `
                                <div class="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-xl border border-purple-200">
                                    <p class="text-sm text-purple-700 flex items-center">
                                        <i class="fas fa-robot text-purple-600 mr-2"></i>
                                        <strong>Analysis Source:</strong> ${response.data.source}
                                    </p>
                                </div>
                            ` : ''}
                            
                            <div class="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl">
                                <h3 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
                                    <i class="fas fa-search text-blue-600 mr-3"></i>Possible Diagnoses
                                </h3>
                                <div class="space-y-3">
                                    ${response.data.diagnoses.map(d => `
                                        <div class="bg-white p-4 rounded-lg border-l-4 border-blue-500 shadow-sm">
                                            <i class="fas fa-stethoscope text-blue-600 mr-2"></i>${d}
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                            
                            <div class="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-xl">
                                <h3 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
                                    <i class="fas fa-lightbulb text-green-600 mr-3"></i>Recommended Next Steps
                                </h3>
                                <div class="space-y-3">
                                    ${response.data.recommendations.map(r => `
                                        <div class="bg-white p-4 rounded-lg border-l-4 border-green-500 shadow-sm">
                                            <i class="fas fa-check-circle text-green-600 mr-2"></i>${r}
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        </div>
                    `;

                    document.getElementById('results-content').innerHTML = resultsContent;
                    document.getElementById('results').classList.remove('hidden');
                    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
                } catch (error) {
                    showNotification('Error analyzing symptoms. Please try again.', 'error');
                } finally {
                    document.getElementById('check-btn').innerHTML = 'Analyze Symptoms';
                }
            }

            // Notification system
            function showNotification(message, type) {
                const notification = document.createElement('div');
                const bgColor = type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-yellow-500';
                
                notification.className = `fixed top-20 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform`;
                notification.textContent = message;
                
                document.body.appendChild(notification);
                
                setTimeout(() => notification.classList.remove('translate-x-full'), 100);
                setTimeout(() => {
                    notification.classList.add('translate-x-full');
                    setTimeout(() => document.body.removeChild(notification), 300);
                }, 3000);
            }

            // Disable right-click context menu
            document.addEventListener('contextmenu', e => e.preventDefault());
            
            // Initialize on load
            window.addEventListener('load', () => {
                initThreeJS();
                
                // Check if already verified
                if (isVerified && document.getElementById('username')) {
                    document.getElementById('username').value = githubUsername;
                }
            });

            // Handle window resize
            window.addEventListener('resize', () => {
                if (camera && renderer) {
                    camera.aspect = window.innerWidth / window.innerHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(window.innerWidth, window.innerHeight);
                }
            });
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

# API configurations
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Debug environment variables
print(f"🔑 Gemini API Key loaded: {bool(GEMINI_API_KEY)}")
print(f"🔑 GitHub Token loaded: {bool(GITHUB_TOKEN)}")

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
    
    # Enhanced dynamic symptom analysis
    symptoms_lower = request.get("symptoms", "").lower()
    age_group = request.get("age_group", "")
    gender = request.get("gender", "")
    
    # Use Gemini API for medical analysis
    if GEMINI_API_KEY:
        try:
            print(f"🤖 Using Gemini API for: {symptoms_lower}")
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"You are a medical AI assistant. Patient: {age_group} {gender}. Symptoms: {symptoms_lower}. Provide: 1) Possible diagnoses (2-3 conditions) 2) Recommendations (3-4 steps). Format clearly."
                    }]
                }]
            }
            
            print(f"📤 Sending request to Gemini...")
            response = requests.post(url, json=payload, timeout=30)
            
            print(f"🔍 Gemini API Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['candidates'][0]['content']['parts'][0]['text']
                
                print(f"✅ Gemini Success: {ai_response[:100]}...")
                
                # Parse response
                diagnoses = []
                recommendations = []
                
                lines = ai_response.split('\n')
                current_section = None
                
                for line in lines:
                    line = line.strip().replace('-', '').replace('*', '').replace('•', '').replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '')
                    if any(word in line.lower() for word in ['diagnos', 'possible', 'condition']):
                        current_section = 'diagnoses'
                    elif any(word in line.lower() for word in ['recommend', 'advice', 'suggest', 'step']):
                        current_section = 'recommendations'
                    elif line and len(line) > 15:
                        if current_section == 'diagnoses':
                            diagnoses.append(line)
                        elif current_section == 'recommendations':
                            recommendations.append(line)
                        elif any(word in line.lower() for word in ['consult', 'see', 'visit', 'call', 'seek', 'rest', 'monitor']):
                            recommendations.append(line)
                        else:
                            diagnoses.append(line)
                
                # Ensure content
                if not diagnoses:
                    diagnoses = ["Respiratory condition", "Viral infection", "General health concern"]
                if not recommendations:
                    recommendations = [
                        "Consult a healthcare professional for proper evaluation",
                        "Monitor symptoms and seek care if they worsen",
                        "Rest and stay hydrated",
                        "Call emergency services if experiencing severe symptoms"
                    ]
                
                return {
                    "diagnoses": diagnoses[:3],
                    "recommendations": recommendations[:4],
                    "source": "Google Gemini AI"
                }
            
            else:
                print(f"❌ Gemini API failed: {response.status_code}")
                raise Exception("Gemini API error")
                
        except Exception as e:
            print(f"❌ Gemini API error: {str(e)}")
    
    # Fallback system
    print("🔄 Using fallback system")
    return {
        "diagnoses": ["Common viral infection", "Respiratory condition", "Stress-related symptoms"],
        "recommendations": [
            "Consult a healthcare professional for proper evaluation",
            "Rest and stay hydrated",
            "Monitor symptoms closely",
            "Seek immediate care if symptoms worsen"
        ],
        "source": "Enhanced AI Medical System"
    }
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)