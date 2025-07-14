# Resume & Job Matching Platform

A fullstack web application for uploading resumes, posting jobs, and matching candidates to job postings using NLP and machine learning.

---

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. MongoDB Setup](#2-mongodb-setup)
  - [3. Backend Setup](#3-backend-setup)
  - [4. Frontend Setup](#4-frontend-setup)
- [Environment Variables](#environment-variables)
- [Common Issues & Troubleshooting](#common-issues--troubleshooting)
- [Dependencies](#dependencies)
- [License](#license)

---

## Features
- Upload and parse resumes (PDF/DOCX)
- Post and edit job listings
- Match resumes to jobs using NLP and ML
- Modern React UI with dialogs and toasts
- MongoDB for data storage

---

## Project Structure
```
resume/
  backend/      # FastAPI backend (Python)
    app/        # API, models, services
    data/       # Data files (skills, etc.)
    models/     # ML models (e.g., vectorizer)
    scripts/    # Data/model setup scripts
    venv/       # Python virtual environment
    requirements.txt
    main.py     # FastAPI entrypoint
  frontend/     # React frontend (JS/TS)
    src/
    package.json
    ...
```

---

## Requirements
- Python 3.9+
- Node.js 18+
- npm 9+
- MongoDB (local or Atlas)

---

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd outsourcing
```

### 2. MongoDB Setup
- **Local:** Install MongoDB and start the service (`mongod`).
- **Atlas:** Create a free cluster and get your connection string.
- **Create a database:** The backend expects a database (e.g., `resume_db`).

### 3. Backend Setup
```sh
cd resume/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
# Download NLTK and spaCy data
python -m nltk.downloader punkt wordnet stopwords
python -m spacy download en_core_web_sm
# Prepare data and models
python setup_backend.py
# Set environment variables (see below)
# Start the server
uvicorn main:app --reload
```

### 4. Frontend Setup
```sh
cd resume/frontend
npm install
npm start
# App runs at http://localhost:3000
```

---

## Environment Variables
Create a `.env` file in `resume/backend/` with:
```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=resume_db
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
SECRET_KEY=your_secret_key
```

---

## Common Issues & Troubleshooting
- **CORS errors:** Ensure `BACKEND_CORS_ORIGINS` matches your frontend URL.
- **MongoDB connection:** Check your URI and that MongoDB is running.
- **ObjectId serialization:** The backend strips `_id` before returning documents.
- **Missing NLTK/spaCy data:** Run the download commands above.

---

## Dependencies

### Backend (see `requirements.txt`)
- fastapi, uvicorn, pymongo, python-multipart, scikit-learn, nltk, spacy, pandas, numpy, python-jose, pydantic[email], python-dotenv, and more

### Frontend (see `package.json`)
- react, @mui/material, @radix-ui/react-dialog, react-hot-toast, axios, styled-components, framer-motion, react-router-dom, and more

---

## License
MIT 