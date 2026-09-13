# Architecture-as-Code Generator - Installation & Setup Guide

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Configuration](#configuration)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS:** Linux, macOS, or Windows (WSL2)
- **Python:** 3.9 or higher
- **Memory:** 4GB RAM
- **Disk:** 2GB free space
- **Internet:** Required for initial setup

### Recommended Requirements
- **OS:** Linux (Ubuntu 20.04+)
- **Python:** 3.11+
- **Memory:** 8GB+ RAM
- **Disk:** 10GB+ SSD
- **Database:** PostgreSQL 13+ (for state storage, optional)

### Dependencies
- Git (for version control)
- Docker & Docker Compose (for containerization)
- Terraform 1.0+ (for IaC generation)
- AWS CLI v2 (for AWS deployment)
- kubectl (for Kubernetes operations, optional)

---

## Local Development Setup

### Step 1: Clone/Extract Repository

```bash
# If from GitHub
git clone https://github.com/yourusername/aac-generator.git
cd aac-generator

# Or if from ZIP
unzip aac-generator.zip
cd aac-generator
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
python -c "import streamlit; print(streamlit.__version__)"
```

### Step 4: Configure Environment

```bash
# Create environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

**Sample .env file:**
```env
# Application Settings
APP_NAME="Architecture-as-Code Generator"
APP_ENV=development
DEBUG=True

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost

# Database (optional)
DATABASE_URL=sqlite:///aac.db
# DATABASE_URL=postgresql://user:password@localhost:5432/aac

# API Keys (if using external AI services)
ANTHROPIC_API_KEY=sk-...
OPENAI_API_KEY=sk-...

# AWS Configuration (for cloud deployment)
AWS_REGION=us-east-1
AWS_PROFILE=default

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/aac.log
```

### Step 5: Initialize Database (if needed)

```bash
# For PostgreSQL
createdb aac
psql aac < schema.sql

# For SQLite (default)
python -c "from core.models import *; print('Ready to use')"
```

### Step 6: Run the Application

```bash
# Start Streamlit app
streamlit run ui/app.py

# App will be available at:
# http://localhost:8501
```

### Step 7: Verify Installation

Open browser and navigate to `http://localhost:8501`

You should see:
- ✅ Home page loads
- ✅ Navigation sidebar visible
- ✅ "Create Design" button functional
- ✅ No error messages in terminal

---

## Docker Deployment

### Option 1: Using Docker Compose (Recommended)

**Step 1: Build Docker Image**

```bash
# Build image
docker-compose build

# Verify build
docker images | grep aac
```

**Step 2: Create .env file**

```bash
cp docker/.env.example .env
```

**Step 3: Start Services**

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f aac-generator

# Check service status
docker-compose ps
```

**Step 4: Access Application**

```
Browser: http://localhost:8501
```

**Step 5: Stop Services**

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Option 2: Standalone Docker Container

**Step 1: Build Image**

```bash
docker build -t aac-generator:latest .
```

**Step 2: Run Container**

```bash
docker run -d \
  --name aac-generator \
  -p 8501:8501 \
  -e APP_ENV=production \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  aac-generator:latest
```

**Step 3: Verify**

```bash
# Check logs
docker logs aac-generator

# Access app
curl http://localhost:8501

# Inspect container
docker ps
docker inspect aac-generator
```

**Sample Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p logs data config

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501 || exit 1

# Run application
CMD ["streamlit", "run", "ui/app.py"]
```

---

## Cloud Deployment

### AWS Deployment (ECS + Fargate)

**Step 1: Create ECR Repository**

```bash
# Create repository
aws ecr create-repository --repository-name aac-generator

# Get login token
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag aac-generator:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/aac-generator:latest

# Push image
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/aac-generator:latest
```

**Step 2: Create ECS Task Definition**

```json
{
  "family": "aac-generator",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "aac-generator",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/aac-generator:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "hostPort": 8501,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/aac-generator",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "environment": [
        {
          "name": "APP_ENV",
          "value": "production"
        }
      ]
    }
  ]
}
```

**Step 3: Create ECS Service**

```bash
# Create service
aws ecs create-service \
  --cluster production \
  --service-name aac-generator \
  --task-definition aac-generator:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Kubernetes Deployment (Helm)

**Step 1: Create Helm Chart Structure**

```bash
helm create aac-generator-chart
cd aac-generator-chart
```

**Step 2: Update values.yaml**

```yaml
replicaCount: 3

image:
  repository: your-registry/aac-generator
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 8501

ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: aac-generator.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

**Step 3: Deploy with Helm**

```bash
# Add Helm repository
helm repo add aac-generator https://your-domain/helm-charts

# Install chart
helm install aac-generator aac-generator/aac-generator-chart \
  --namespace production \
  --create-namespace \
  --values values.yaml

# Verify deployment
kubectl get pods -n production
kubectl logs -n production deployment/aac-generator
```

---

## Configuration

### Application Configuration (config/settings.py)

```python
# Core settings
APP_NAME = "Architecture-as-Code Generator"
APP_VERSION = "1.0.0"
DEBUG = False

# API Configuration
API_PORT = 8501
API_HOST = "0.0.0.0"
API_WORKERS = 4

# Database
DATABASE_URL = "postgresql://user:pass@localhost/aac"
DATABASE_POOL_SIZE = 20
DATABASE_MAX_OVERFLOW = 40

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "json"  # json or text

# Authentication
AUTH_ENABLED = True
AUTH_PROVIDER = "oauth2"  # oauth2, ldap, saml

# Compliance Frameworks
COMPLIANCE_FRAMEWORKS = [
    "DORA",
    "MIFID_II",
    "GDPR",
    "SOX",
    "PCI_DSS"
]

# AWS Configuration
AWS_REGION = "us-east-1"
AWS_S3_BUCKET = "aac-artifacts"
AWS_KMS_KEY_ID = "arn:aws:kms:..."
```

### Policy Configuration (config/policies.yaml)

```yaml
policies:
  - id: POL-SEC-001
    name: Data Encryption at Rest
    enabled: true
    severity: CRITICAL
    frameworks:
      - GDPR
      - PCI_DSS
    condition: "encryption_required == True"

  - id: POL-DORA-001
    name: DORA Availability
    enabled: true
    severity: CRITICAL
    frameworks:
      - DORA
    condition: "availability >= 99.9 AND rto_minutes <= 15"
```

### Technology Standards (config/standards.yaml)

```yaml
standards:
  languages:
    - name: Java
      versions: ["11", "17", "21"]
      adoption: "Approved"
    - name: Python
      versions: ["3.9", "3.10", "3.11"]
      adoption: "Approved"

  databases:
    - name: PostgreSQL
      versions: ["13", "14", "15"]
      adoption: "Approved"
    - name: MySQL
      versions: ["8.0"]
      adoption: "Trial"

  cloud_providers:
    - name: AWS
      adoption: "Approved"
    - name: Azure
      adoption: "Approved"
```

---

## Verification

### Post-Installation Checklist

```bash
# 1. Application starts without errors
streamlit run ui/app.py &
sleep 5
curl -s http://localhost:8501 | grep -q "Architecture-as-Code" && echo "✅ App running"

# 2. Python modules importable
python -c "from core.models import ArchitectureDesign; print('✅ Models OK')"
python -c "from core.validators import PolicyValidator; print('✅ Validators OK')"
python -c "from core.generators import GeneratorOrchestrator; print('✅ Generators OK')"

# 3. Database connectivity (if configured)
python -c "from sqlalchemy import create_engine; engine = create_engine('sqlite:///test.db'); print('✅ Database OK')"

# 4. Policy validator initialization
python -c "from core.validators import PolicyValidator; v = PolicyValidator(); print(f'✅ {len(v.policies)} policies loaded')"

# 5. Test artifact generation
python -c "
from core.models import ArchitectureDesign, ArchitectureDecision
from core.generators import GeneratorOrchestrator

design = ArchitectureDesign(id='TEST-001', name='Test', architect='Test User', business_driver='Testing')
gen = GeneratorOrchestrator()
artifacts = gen.generate_all_artifacts(design)
print(f'✅ Generated {len(artifacts)} artifacts')
"
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-asyncio

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=core --cov=ui --cov-report=html

# Run specific test file
pytest tests/test_validators.py -v

# Run specific test
pytest tests/test_validators.py::test_policy_validation -v
```

---

## Troubleshooting

### Common Issues & Solutions

#### Issue 1: Port 8501 Already in Use

```bash
# Find process using port
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run ui/app.py --server.port 8502
```

#### Issue 2: Module Import Errors

```bash
# Ensure virtual environment activated
source venv/bin/activate

# Reinstall dependencies
pip install --upgrade --force-reinstall -r requirements.txt

# Check Python path
python -m site
```

#### Issue 3: Database Connection Errors

```bash
# Test connection
python -c "
from sqlalchemy import create_engine, text
engine = create_engine('postgresql://user:pass@localhost:5432/aac')
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print(result.fetchone())
"

# Or use psql directly
psql -h localhost -U postgres -d aac -c 'SELECT version();'
```

#### Issue 4: Streamlit Not Found

```bash
# Check installation
which streamlit
streamlit --version

# Reinstall
pip uninstall streamlit
pip install streamlit==1.28.1
```

#### Issue 5: Permission Denied Errors

```bash
# Fix file permissions
chmod +x ui/app.py
chmod -R 755 config/
chmod -R 755 logs/

# On Linux/Mac with Docker
sudo usermod -aG docker $USER
newgrp docker
```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
export PYTHONUNBUFFERED=1
streamlit run --logger.level=debug ui/app.py

# Or set in code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Tuning

```python
# In config/settings.py
# Increase cache size
CACHE_SIZE = 1000

# Adjust worker threads
WORKER_THREADS = 8

# Enable optimization
OPTIMIZE_MEMORY = True

# Database connection pooling
DATABASE_POOL_SIZE = 30
DATABASE_ECHO = False
```

---

## Upgrade Instructions

### From v1.x to v2.x

```bash
# 1. Backup current data
cp -r data data.backup.$(date +%Y%m%d)

# 2. Stash local changes
git stash

# 3. Fetch latest
git fetch origin
git checkout v2.0.0

# 4. Update dependencies
pip install --upgrade -r requirements.txt

# 5. Run migrations
python -m migrations.migrate

# 6. Restart application
streamlit run ui/app.py
```

---

## Support & Help

- **Documentation:** Read README.md and docs/
- **Issues:** Report via GitHub Issues
- **Community:** Join Slack/Discord channel
- **Commercial Support:** support@aac-generator.example.com

---

**Version:** 1.0  
**Last Updated:** January 2024
