#!/bin/bash
cd frontend
npm install
npm run build
cd ../backend
pip install -r requirements.txt