@echo off
echo Starting MediCheck Backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python run.py