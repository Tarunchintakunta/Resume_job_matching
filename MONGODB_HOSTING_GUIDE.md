# MongoDB Hosting Guide for Resume-to-Job Matching System

## 🎯 Overview

This guide covers different ways to host MongoDB for your Resume-to-Job Matching System, from local development to production deployment.

## 📋 Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Cloud Hosting Options](#cloud-hosting-options)
3. [Docker Deployment](#docker-deployment)
4. [Production Configuration](#production-configuration)
5. [Security Best Practices](#security-best-practices)
6. [Monitoring & Backup](#monitoring--backup)
7. [Troubleshooting](#troubleshooting)

---

## 🏠 Local Development Setup

### Option 1: Homebrew (macOS) - ✅ Already Done

```bash
# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB service
brew services start mongodb-community

# Stop MongoDB service
brew services stop mongodb-community

# Restart MongoDB service
brew services restart mongodb-community

# Check status
brew services list | grep mongodb
```

### Option 2: Manual Installation

#### macOS
```bash
# Download MongoDB Community Server
curl -O https://fastdl.mongodb.org/osx/mongodb-macos-x86_64-6.0.tgz

# Extract and install
tar -zxvf mongodb-macos-x86_64-6.0.tgz
sudo mv mongodb-macos-x86_64-6.0 /usr/local/mongodb

# Create data directory
sudo mkdir -p /usr/local/var/mongodb
sudo chown -R $(whoami) /usr/local/var/mongodb

# Start MongoDB
/usr/local/mongodb/bin/mongod --dbpath /usr/local/var/mongodb
```

#### Linux (Ubuntu/Debian)
```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Create list file for MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Update package database
sudo apt-get update

# Install MongoDB
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod

# Enable MongoDB to start on boot
sudo systemctl enable mongod
```

#### Windows
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Run the installer
3. Create data directory: `C:\data\db`
4. Start MongoDB: `"C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" --dbpath="C:\data\db"`

### Verify Installation

```bash
# Test connection
mongosh --eval "db.runCommand('ping')"

# Should return: { ok: 1 }
```

---

## ☁️ Cloud Hosting Options

### Option 1: MongoDB Atlas (Recommended)

#### Setup Steps:
1. **Create Account**: Go to [mongodb.com/atlas](https://www.mongodb.com/atlas)
2. **Create Cluster**: Choose free tier (M0) for development
3. **Configure Network Access**: Add your IP or `0.0.0.0/0` for all IPs
4. **Create Database User**: Username and password
5. **Get Connection String**: Copy the connection string

#### Connection String Format:
```
mongodb+srv://username:password@cluster.mongodb.net/resume_matching?retryWrites=true&w=majority
```

#### Update Environment Variables:
```bash
# In your .env file
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/resume_matching?retryWrites=true&w=majority
```

### Option 2: AWS DocumentDB

#### Setup Steps:
1. **Create DocumentDB Cluster** in AWS Console
2. **Configure Security Groups** to allow connections
3. **Create Database User**
4. **Get Connection String**

#### Connection String:
```
mongodb://username:password@cluster-endpoint:27017/resume_matching?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem
```

### Option 3: Google Cloud Firestore

#### Setup Steps:
1. **Enable Firestore** in Google Cloud Console
2. **Create Database** (Native mode)
3. **Configure Security Rules**
4. **Use Firestore SDK** instead of MongoDB driver

### Option 4: Azure Cosmos DB

#### Setup Steps:
1. **Create Cosmos DB Account** with MongoDB API
2. **Create Database and Collections**
3. **Get Connection String**

#### Connection String:
```
mongodb://account-name:password@account-name.mongo.cosmos.azure.com:10255/resume_matching?ssl=true&replicaSet=globaldb
```

---

## 🐳 Docker Deployment

### Option 1: Single MongoDB Container

```bash
# Create docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'
services:
  mongodb:
    image: mongo:6.0
    container_name: resume-matching-mongodb
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
      MONGO_INITDB_DATABASE: resume_matching
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
      - ./mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro

volumes:
  mongodb_data:
EOF

# Start MongoDB
docker-compose up -d

# Stop MongoDB
docker-compose down
```

### Option 2: MongoDB with Authentication

```bash
# Create mongo-init.js
cat > mongo-init.js << EOF
db = db.getSiblingDB('resume_matching');

// Create user for the application
db.createUser({
  user: 'app_user',
  pwd: 'app_password',
  roles: [
    { role: 'readWrite', db: 'resume_matching' }
  ]
});

// Create collections
db.createCollection('resumes');
db.createCollection('jobs');
db.createCollection('skills');
db.createCollection('matches');
db.createCollection('users');
db.createCollection('evaluations');
db.createCollection('performance_metrics');
db.createCollection('system_logs');
EOF

# Update connection string
MONGODB_URL=mongodb://app_user:app_password@localhost:27017/resume_matching
```

### Option 3: Complete Stack with Docker

```bash
# Create complete docker-compose.yml
cat > docker-compose-full.yml << EOF
version: '3.8'
services:
  mongodb:
    image: mongo:6.0
    container_name: resume-matching-mongodb
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
      MONGO_INITDB_DATABASE: resume_matching
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
      - ./mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
    networks:
      - resume-network

  redis:
    image: redis:7-alpine
    container_name: resume-matching-redis
    restart: always
    ports:
      - "6379:6379"
    networks:
      - resume-network

  backend:
    build: ./backend
    container_name: resume-matching-backend
    restart: always
    environment:
      - MONGODB_URL=mongodb://admin:password123@mongodb:27017/resume_matching
      - REDIS_URL=redis://redis:6379
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
      - redis
    networks:
      - resume-network

  frontend:
    build: ./frontend
    container_name: resume-matching-frontend
    restart: always
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - resume-network

volumes:
  mongodb_data:

networks:
  resume-network:
    driver: bridge
EOF
```

---

## 🚀 Production Configuration

### Environment Variables

```bash
# Production .env file
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/resume_matching?retryWrites=true&w=majority
DATABASE_NAME=resume_matching
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://localhost:6379
MAX_FILE_SIZE=10485760
UPLOAD_DIR=./uploads
LOG_LEVEL=WARNING
LOG_FILE=./logs/app.log
CACHE_TTL=3600
MAX_WORKERS=8
```

### MongoDB Configuration

#### Production mongod.conf:
```yaml
# /etc/mongod.conf
systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true

storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true

processManagement:
  timeZoneInfo: /usr/share/zoneinfo

net:
  port: 27017
  bindIp: 127.0.0.1

security:
  authorization: enabled

operationProfiling:
  slowOpThresholdMs: 100
  mode: slowOp

replication:
  replSetName: rs0
```

### Performance Optimization

```bash
# Create indexes for better performance
mongosh resume_matching --eval "
db.resumes.createIndex({skills: 'text', category: 'text'});
db.jobs.createIndex({title: 'text', skills_required: 'text'});
db.matches.createIndex({resume_id: 1, job_id: 1});
db.matches.createIndex({score: -1});
db.performance_metrics.createIndex({timestamp: -1});
"

# Enable WiredTiger compression
mongosh admin --eval "
db.adminCommand({
  setParameter: 1,
  wiredTigerConcurrentReadTransactions: 128
});
"
```

---

## 🔒 Security Best Practices

### 1. Authentication & Authorization

```bash
# Create admin user
mongosh admin --eval "
db.createUser({
  user: 'admin',
  pwd: 'secure_password',
  roles: ['userAdminAnyDatabase', 'dbAdminAnyDatabase', 'readWriteAnyDatabase']
});
"

# Create application user
mongosh resume_matching --eval "
db.createUser({
  user: 'app_user',
  pwd: 'app_secure_password',
  roles: [
    { role: 'readWrite', db: 'resume_matching' }
  ]
});
"
```

### 2. Network Security

```bash
# Bind to localhost only (development)
mongod --bind_ip 127.0.0.1

# Use firewall rules (production)
sudo ufw allow from 192.168.1.0/24 to any port 27017
sudo ufw deny 27017
```

### 3. SSL/TLS Configuration

```bash
# Generate SSL certificate
openssl req -newkey rsa:2048 -new -x509 -days 365 -nodes -out mongodb-cert.crt -keyout mongodb-cert.key

# Start MongoDB with SSL
mongod --sslMode requireSSL --sslPEMKeyFile mongodb-cert.pem --sslCAFile ca.pem
```

### 4. Data Encryption

```bash
# Enable encryption at rest
mongod --enableEncryption --encryptionKeyFile /path/to/keyfile
```

---

## 📊 Monitoring & Backup

### 1. MongoDB Monitoring

```bash
# Install MongoDB Ops Manager
# Or use MongoDB Atlas built-in monitoring

# Enable database profiling
mongosh resume_matching --eval "
db.setProfilingLevel(1, {slowms: 100});
"

# Check slow queries
db.system.profile.find().sort({ts: -1}).limit(10);
```

### 2. Automated Backups

```bash
# Create backup script
cat > backup_mongodb.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/mongodb"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="resume_matching"

# Create backup directory
mkdir -p $BACKUP_DIR

# Create backup
mongodump --db $DB_NAME --out $BACKUP_DIR/backup_$DATE

# Compress backup
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz -C $BACKUP_DIR backup_$DATE

# Remove uncompressed backup
rm -rf $BACKUP_DIR/backup_$DATE

# Keep only last 7 days of backups
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: backup_$DATE.tar.gz"
EOF

chmod +x backup_mongodb.sh

# Add to crontab for daily backups
echo "0 2 * * * /path/to/backup_mongodb.sh" | crontab -
```

### 3. Health Checks

```bash
# Create health check script
cat > health_check.sh << 'EOF'
#!/bin/bash

# Check MongoDB connection
if mongosh --eval "db.runCommand('ping')" > /dev/null 2>&1; then
    echo "✅ MongoDB is running"
else
    echo "❌ MongoDB is not responding"
    exit 1
fi

# Check database size
DB_SIZE=$(mongosh resume_matching --quiet --eval "db.stats().dataSize")
echo "📊 Database size: $DB_SIZE bytes"

# Check collection counts
echo "📋 Collection counts:"
mongosh resume_matching --quiet --eval "
db.getCollectionNames().forEach(function(collection) {
    print(collection + ': ' + db[collection].countDocuments());
});
"
EOF

chmod +x health_check.sh
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Connection Refused
```bash
# Check if MongoDB is running
brew services list | grep mongodb
sudo systemctl status mongod

# Check port
netstat -an | grep 27017
lsof -i :27017
```

#### 2. Authentication Failed
```bash
# Reset admin password
mongosh admin --eval "
db.changeUserPassword('admin', 'new_password');
"
```

#### 3. Permission Denied
```bash
# Fix data directory permissions
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown -R mongodb:mongodb /var/log/mongodb
```

#### 4. Out of Disk Space
```bash
# Check disk usage
df -h

# Clean up old logs
sudo find /var/log/mongodb -name "*.log.*" -mtime +7 -delete
```

### Performance Issues

#### 1. Slow Queries
```bash
# Enable profiling
mongosh resume_matching --eval "
db.setProfilingLevel(2);
"

# Check slow queries
db.system.profile.find({millis: {$gt: 100}}).sort({ts: -1});
```

#### 2. Memory Issues
```bash
# Check memory usage
mongosh admin --eval "
db.serverStatus().mem;
"

# Optimize memory
mongosh admin --eval "
db.adminCommand({
  setParameter: 1,
  wiredTigerConcurrentReadTransactions: 64
});
"
```

---

## 📝 Quick Start Commands

### Local Development
```bash
# Start MongoDB
brew services start mongodb-community

# Setup database
python setup_mongodb.py

# Start backend
python main.py

# Start frontend
cd ../frontend && npm start
```

### Production Deployment
```bash
# Using Docker
docker-compose -f docker-compose-full.yml up -d

# Using MongoDB Atlas
# Update MONGODB_URL in .env file
# Start application
python main.py
```

### Monitoring
```bash
# Check MongoDB status
brew services list | grep mongodb

# Check database health
./health_check.sh

# View logs
tail -f /var/log/mongodb/mongod.log
```

---

## 🎯 Summary

Your MongoDB is now successfully set up and running! Here's what we accomplished:

✅ **MongoDB Installation**: Installed via Homebrew  
✅ **Service Management**: MongoDB is running as a service  
✅ **Database Setup**: Created collections and indexes  
✅ **Sample Data**: Inserted initial data for testing  
✅ **Connection Test**: Verified connectivity  

### Next Steps:
1. **Start your backend**: `python main.py`
2. **Start your frontend**: `cd ../frontend && npm start`
3. **Test the system**: Access http://localhost:3000
4. **Monitor performance**: Use the health check script

### For Production:
1. **Choose cloud hosting** (MongoDB Atlas recommended)
2. **Configure security** (authentication, SSL, firewall)
3. **Set up monitoring** and automated backups
4. **Optimize performance** with proper indexes

Your Resume-to-Job Matching System is now ready to run with a fully configured MongoDB database! 🚀 