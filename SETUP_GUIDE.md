# Resume-to-Job Matching System - Complete Setup Guide

## 🎯 Overview

This guide will help you set up the complete Resume-to-Job Matching System on a new laptop from scratch.

## 📋 Prerequisites

### System Requirements
- **Operating System**: macOS, Linux (Ubuntu/Debian), or Windows
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: At least 2GB free space
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **Git**: For cloning the repository

### Required Software
- Python 3.8+
- Node.js 16+
- Git
- MongoDB
- npm or yarn

---

## 🚀 Quick Start (Automated Setup)

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd resume
```

### Step 2: Run the Automated Setup Script
```bash
# Make the setup script executable
chmod +x setup_complete_system.sh

# Run the complete setup
./setup_complete_system.sh
```

This script will automatically:
- Install all system dependencies
- Set up Python virtual environment
- Install Python packages
- Install Node.js dependencies
- Set up MongoDB
- Configure the database
- Start all services

---

## 📝 Manual Setup (Step-by-Step)

### Step 1: System Dependencies

#### macOS
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install python@3.11 node git mongodb-community

# Start MongoDB
brew services start mongodb-community
```

#### Linux (Ubuntu/Debian)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install Git
sudo apt install git -y

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install mongodb-org -y

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### Windows
1. Download and install Python from [python.org](https://www.python.org/downloads/)
2. Download and install Node.js from [nodejs.org](https://nodejs.org/)
3. Download and install Git from [git-scm.com](https://git-scm.com/)
4. Download and install MongoDB from [mongodb.com](https://www.mongodb.com/try/download/community)

### Step 2: Clone and Navigate to Project
```bash
git clone <your-repository-url>
cd resume
```

### Step 3: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements-basic.txt

# Install spaCy English model
python -m spacy download en_core_web_sm

# Download NLTK data
python -c "
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
"

# Setup MongoDB database
python setup_mongodb.py

# Create necessary directories
mkdir -p logs uploads data tests

# Run health check
./health_check.sh
```

### Step 4: Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install Node.js dependencies
npm install

# Build the application (optional)
npm run build
```

### Step 5: Environment Configuration

```bash
# Navigate back to backend
cd ../backend

# Create .env file if it doesn't exist
cat > .env << EOF
# Database Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=resume_matching

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis Configuration (for caching)
REDIS_URL=redis://localhost:6379

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=./uploads

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# Performance
CACHE_TTL=3600  # 1 hour
MAX_WORKERS=4
EOF
```

---

## 🏃‍♂️ Running the Application

### Option 1: Manual Start

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm start
```

### Option 2: Using the Start Script
```bash
# Make the start script executable
chmod +x start_system.sh

# Start the entire system
./start_system.sh
```

### Option 3: Using Docker (Alternative)
```bash
# Build and start all services
docker-compose -f docker-compose-full.yml up -d
```

---

## 🌐 Accessing the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MongoDB**: mongodb://localhost:27017

---

## 🧪 Testing the Setup

### 1. Health Check
```bash
cd backend
./health_check.sh
```

### 2. Test API Endpoints
```bash
# Test basic endpoint
curl http://localhost:8000/api/v1/health

# Test evaluation endpoint
curl http://localhost:8000/api/v1/evaluate

# Test performance metrics
curl http://localhost:8000/api/v1/performance/metrics
```

### 3. Test Frontend
1. Open http://localhost:3000 in your browser
2. Try uploading a resume
3. Create a job posting
4. Test the matching functionality

---

## 📊 Verification Checklist

- [ ] MongoDB is running and accessible
- [ ] Python virtual environment is activated
- [ ] All Python packages are installed
- [ ] spaCy English model is downloaded
- [ ] NLTK data is downloaded
- [ ] Database is set up with collections and indexes
- [ ] Node.js dependencies are installed
- [ ] Environment variables are configured
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] API endpoints are responding
- [ ] Frontend is accessible in browser

---

## 🔧 Troubleshooting

### Common Issues

#### 1. MongoDB Connection Issues
```bash
# Check if MongoDB is running
brew services list | grep mongodb  # macOS
sudo systemctl status mongod       # Linux

# Start MongoDB if not running
brew services start mongodb-community  # macOS
sudo systemctl start mongod            # Linux
```

#### 2. Python Package Issues
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall packages
pip install -r requirements-basic.txt --force-reinstall
```

#### 3. Node.js Issues
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

#### 4. Port Conflicts
```bash
# Check what's using the ports
lsof -i :8000  # Check port 8000
lsof -i :3000  # Check port 3000

# Kill processes if needed
kill -9 <PID>
```

#### 5. Permission Issues
```bash
# Fix file permissions
chmod +x *.sh
chmod +x scripts/*.py
```

---

## 📱 Development Workflow

### Daily Development
```bash
# Start development environment
cd resume
./start_dev.sh

# Make changes to code
# Test changes
# Commit and push
```

### Testing
```bash
# Run backend tests
cd backend
python -m pytest tests/ -v

# Run frontend tests
cd ../frontend
npm test
```

### Code Quality
```bash
# Format Python code
cd backend
black .
isort .

# Format JavaScript code
cd ../frontend
npm run format
```

---

## 🚀 Production Deployment

### 1. Environment Setup
```bash
# Update .env for production
DEBUG=False
SECRET_KEY=your-super-secure-production-key
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/resume_matching
```

### 2. Build for Production
```bash
# Backend
cd backend
pip install -r requirements-prod.txt

# Frontend
cd ../frontend
npm run build
```

### 3. Deploy
```bash
# Using Docker
docker-compose -f docker-compose-prod.yml up -d

# Or manual deployment
# Follow the MONGODB_HOSTING_GUIDE.md for cloud deployment
```

---

## 📚 Additional Resources

- **MongoDB Hosting Guide**: `MONGODB_HOSTING_GUIDE.md`
- **API Documentation**: http://localhost:8000/docs
- **Implementation Status**: `IMPLEMENTATION_STATUS.md`
- **Advanced Features**: `ADVANCED_FEATURES_README.md`

---

## 🆘 Getting Help

### If Something Goes Wrong

1. **Check the logs**:
   ```bash
   # Backend logs
   tail -f backend/logs/app.log
   
   # MongoDB logs
   tail -f /usr/local/var/log/mongodb/mongo.log
   ```

2. **Run health check**:
   ```bash
   cd backend
   ./health_check.sh
   ```

3. **Reset and restart**:
   ```bash
   # Stop all services
   brew services stop mongodb-community
   
   # Restart MongoDB
   brew services start mongodb-community
   
   # Restart application
   ./start_system.sh
   ```

4. **Complete reset**:
   ```bash
   # Remove virtual environment
   rm -rf backend/venv
   
   # Remove node_modules
   rm -rf frontend/node_modules
   
   # Run setup again
   ./setup_complete_system.sh
   ```

---

## 🎉 Success!

Once you've completed all the steps above, you should have a fully functional Resume-to-Job Matching System running on your laptop!

**Access Points:**
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs
- 🗄️ **Database**: MongoDB on localhost:27017

**Next Steps:**
1. Explore the application features
2. Upload sample resumes and jobs
3. Test the matching algorithm
4. Run the Jupyter notebook for analysis
5. Customize the system for your needs

Happy coding! 🚀 