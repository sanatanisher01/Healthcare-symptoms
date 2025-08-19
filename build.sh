#!/bin/bash
cd frontend
npm install
npm run build
cd ../backend
python3.11 -m pip install -r requirements.txt