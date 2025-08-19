#!/bin/bash
set -e
cd frontend
npm install
npm run build
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt