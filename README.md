<div align="center">

# 🩺 MediCheck - AI Healthcare Platform

### *Revolutionizing Healthcare with Artificial Intelligence*

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-healthcare--symptoms.onrender.com-blue?style=for-the-badge)](https://healthcare-symptoms.onrender.com/)
[![GitHub Stars](https://img.shields.io/github/stars/sanatanisher01/Healthcare-symptoms?style=for-the-badge&color=yellow)](https://github.com/sanatanisher01/Healthcare-symptoms/stargazers)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**⭐ Star this repository to unlock the AI symptom checker! ⭐**

*Get instant, AI-powered health insights and recommendations in seconds*

</div>

---

## 🚀 **Live Application**

🌐 **Access the app:** [healthcare-symptoms.onrender.com](https://healthcare-symptoms.onrender.com/)

📧 **Contact:** [aryansanatani01@gmail.com](mailto:aryansanatani01@gmail.com)

---

## ✨ **Key Features**

<table>
<tr>
<td align="center">🤖<br><b>AI-Powered Analysis</b><br>Advanced ML algorithms</td>
<td align="center">🔒<br><b>Privacy First</b><br>No data storage</td>
<td align="center">⚡<br><b>Instant Results</b><br>Real-time analysis</td>
</tr>
<tr>
<td align="center">📱<br><b>Responsive Design</b><br>Works on all devices</td>
<td align="center">🎨<br><b>Modern UI/UX</b><br>Beautiful interface</td>
<td align="center">⭐<br><b>GitHub Integration</b><br>Star verification system</td>
</tr>
</table>

## 🏗️ **Project Architecture**

```bash
🏥 MediCheck/
├── 🎨 frontend/              # React + TailwindCSS + Three.js
│   ├── 📁 src/
│   │   ├── 🧩 components/     # Reusable UI components
│   │   ├── 📄 pages/          # Application pages
│   │   └── 🎯 utils/          # Helper functions
│   └── 📦 package.json
├── ⚡ backend/               # FastAPI + Python
│   ├── 🐍 main.py            # Main application server
│   ├── 📋 requirements.txt   # Python dependencies
│   └── 🔐 .env.example       # Environment variables
└── 📖 README.md
```

## 🛠️ **Quick Start Guide**

### 🚀 **Option 1: Use Live App (Recommended)**

1. **Visit:** [healthcare-symptoms.onrender.com](https://healthcare-symptoms.onrender.com/)
2. **Star this repository** ⭐
3. **Enter your GitHub username** to verify
4. **Start using the AI symptom checker!** 🩺

### 💻 **Option 2: Local Development**

<details>
<summary><b>🔧 Backend Setup</b></summary>

```bash
# 📁 Navigate to backend
cd backend

# 🐍 Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 📦 Install dependencies
pip install -r requirements.txt

# 🔐 Setup environment
cp .env.example .env
# Add your tokens to .env file

# 🚀 Run the server
python main.py
```

</details>

<details>
<summary><b>🎨 Frontend Setup</b></summary>

```bash
# 📁 Navigate to frontend
cd frontend

# 📦 Install dependencies
npm install

# 🚀 Start development server
npm run dev
```

</details>

## 🔌 **API Documentation**

### 🩺 **Symptom Analysis Endpoint**

```http
POST /check-symptoms?github_username={username}
```

**📥 Request Body:**
```json
{
  "symptoms": "difficulty breathing, chest pain",
  "age_group": "Teen",
  "gender": "Male"
}
```

**📤 Response:**
```json
{
  "diagnoses": [
    "Asthma", 
    "Respiratory Infection", 
    "Anxiety/Panic Attack"
  ],
  "recommendations": [
    "🚨 SEEK IMMEDIATE MEDICAL ATTENTION if breathing is severely impaired",
    "Sit upright and try to remain calm",
    "Use prescribed inhaler if you have asthma",
    "Call emergency services (911) if symptoms are severe"
  ]
}
```

### ⭐ **Star Verification Endpoint**

```http
POST /verify-star
```

**📥 Request Body:**
```json
{
  "github_username": "your_username"
}
```

## 🌐 **Deployment**

### 🚀 **Current Deployment**
- **Platform:** Render.com
- **URL:** [healthcare-symptoms.onrender.com](https://healthcare-symptoms.onrender.com/)
- **Status:** ✅ Live and Running

### 🔧 **Environment Variables**

| Variable | Description | Required |
|----------|-------------|----------|
| `HUGGINGFACE_API_TOKEN` | Hugging Face API access | ✅ |
| `GITHUB_TOKEN` | GitHub API access | ✅ |
| `PORT` | Server port (default: 8000) | ❌ |

---

## 🛠️ **Tech Stack**

<div align="center">

| **Frontend** | **Backend** | **AI/ML** | **Deployment** |
|:------------:|:-----------:|:---------:|:--------------:|
| ![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black) | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) | ![Hugging Face](https://img.shields.io/badge/🤗_Hugging_Face-FFD21E?style=flat) | ![Render](https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white) |
| ![TailwindCSS](https://img.shields.io/badge/Tailwind-38B2AC?style=flat&logo=tailwind-css&logoColor=white) | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | ![AI Models](https://img.shields.io/badge/AI_Models-FF6B6B?style=flat) | ![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white) |
| ![Three.js](https://img.shields.io/badge/Three.js-000000?style=flat&logo=three.js&logoColor=white) | ![Uvicorn](https://img.shields.io/badge/Uvicorn-2F5F8F?style=flat) | | |

</div>

---

## ⚠️ **Important Disclaimers**

<div align="center">

| ⚕️ **Medical** | 🔒 **Privacy** | 📞 **Emergency** |
|:---------------:|:--------------:|:----------------:|
| This tool is for **informational purposes only** | **No data is stored** on our servers | For **medical emergencies**, call **911** |
| **Not a replacement** for professional medical advice | Complete **privacy and confidentiality** guaranteed | Always consult **healthcare professionals** |

</div>

---

## 📞 **Contact & Support**

<div align="center">

📧 **Email:** [aryansanatani01@gmail.com](mailto:aryansanatani01@gmail.com)

🐛 **Issues:** [GitHub Issues](https://github.com/sanatanisher01/Healthcare-symptoms/issues)

⭐ **Star this repo** if you found it helpful!

[![GitHub followers](https://img.shields.io/github/followers/sanatanisher01?style=social)](https://github.com/sanatanisher01)

</div>

---

## 📄 **License**

<div align="center">

**MIT License** - feel free to use this project for learning and development!

*Made with ❤️ for the open-source community*

</div>