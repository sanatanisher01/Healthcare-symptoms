# MediCheck - AI Healthcare Symptom Checker

⭐ **Please star this repository to access the live app!** ⭐

A modern healthcare symptom checker portal powered by AI, built with React frontend and FastAPI backend.

## Features

- 🤖 AI-powered symptom analysis using Hugging Face models
- 💻 Modern React frontend with TailwindCSS
- ⚡ Fast FastAPI backend
- 📱 Responsive design
- 🔒 Privacy-focused approach
- ⭐ GitHub star verification system

## Project Structure

```
Med/
├── frontend/          # React + TailwindCSS frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── ...
│   └── package.json
├── backend/           # FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```bash
   copy .env.example .env
   ```

5. Add your Hugging Face API token to `.env`:
   ```
   HUGGINGFACE_API_TOKEN=your_token_here
   ```

6. Run the backend:
   ```bash
   python main.py
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

## API Endpoints

### POST /check-symptoms

Analyzes symptoms and returns possible diagnoses and recommendations.

**Request Body:**
```json
{
  "symptoms": "fever, cough, sore throat",
  "age_group": "Adult",
  "gender": "Male"
}
```

**Response:**
```json
{
  "diagnoses": ["Common Cold", "Flu", "COVID-19"],
  "recommendations": [
    "Drink fluids and rest",
    "Monitor temperature regularly",
    "Consult a doctor if fever persists > 3 days"
  ]
}
```

## Deployment

### Frontend (Netlify/Vercel)
1. Build the project: `npm run build`
2. Deploy the `dist` folder to Netlify or Vercel
3. Update API URL in production

### Backend (Render/Railway/Hugging Face Spaces)
1. Push code to GitHub
2. Connect to deployment platform
3. Set environment variables
4. Deploy

## Environment Variables

- `HUGGINGFACE_API_TOKEN`: Your Hugging Face API token for model access

## Tech Stack

- **Frontend**: React, TailwindCSS, Vite, React Router
- **Backend**: FastAPI, Python, Hugging Face Transformers
- **AI Model**: m42-health/Llama3-Med42-8B

## Important Notes

- This tool is for informational purposes only
- Not a replacement for professional medical advice
- Always consult healthcare professionals for serious symptoms
- Privacy-focused: no data is permanently stored

## License

MIT License