# 🚀 Two-Tier Task Management Application on Azure

[![Azure](https://img.shields.io/badge/Azure-Cloud-0078D4?logo=microsoft-azure)](https://azure.microsoft.com)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)](https://www.docker.com/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins)](https://www.jenkins.io/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-47A248?logo=mongodb)](https://www.mongodb.com/)

A production-ready, enterprise-grade two-tier task management application deployed on Azure with complete CI/CD automation, private networking, and security best practices.

---

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Infrastructure Components](#-infrastructure-components)
- [Security Features](#-security-features)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Azure Deployment](#-azure-deployment)
- [CI/CD Pipeline](#-cicd-pipeline)
- [API Documentation](#-api-documentation)
- [Monitoring](#-monitoring)
- [Troubleshooting](#-troubleshooting)

---

## 🏗️ Architecture Overview

![Architecture Diagram](images/ar1.png)

### High-Level Architecture

The application follows a secure, scalable two-tier architecture deployed on Azure:

```
User → Load Balancer (Public) → App Server (Private) → Database Server (Private)
                                      ↑
                                Jenkins (Private) → ACR (Private)
```

### Key Architecture Principles

✅ **No Public IPs** - Application and database servers are completely private  
✅ **VNet Peering** - Secure communication between isolated virtual networks  
✅ **Private Container Registry** - Docker images stored in Azure ACR  
✅ **Bastion/Jump Host** - Secure SSH access to private servers  
✅ **Load Balancer** - High availability and traffic distribution  
✅ **Automated CI/CD** - Jenkins pipeline for continuous deployment


---

## ✨ Key Features

### Application Features
- 🔐 **User Authentication** - JWT-based secure authentication
- ✅ **Task Management** - Complete CRUD operations for tasks
- 🏷️ **Categories & Priorities** - Organize tasks with custom categories
- 📅 **Due Date Tracking** - Never miss a deadline with overdue alerts
- 🔍 **Advanced Search** - Filter and search tasks efficiently
- 📊 **Statistics Dashboard** - Real-time insights into your tasks
- 📱 **Responsive UI** - Works seamlessly on all devices
- 🎨 **Modern Interface** - Clean, intuitive user experience

### Infrastructure Features
- 🐳 **Fully Containerized** - Docker & Docker Compose
- 🔄 **CI/CD Automation** - Jenkins pipeline with automated deployments
- ☁️ **Azure Cloud Native** - Leveraging Azure services
- 🔒 **Enterprise Security** - Multi-layer security implementation
- 🌐 **Private Networking** - VNet isolation and peering
- ⚖️ **Load Balanced** - High availability with Azure Load Balancer
- 📦 **Private Registry** - Azure Container Registry (ACR)
- 🛡️ **Network Security** - NSG rules and firewall protection

---

## 🛠️ Technology Stack

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- Responsive Design
- AJAX for API communication

### Backend
- **Framework**: Flask 3.0
- **Language**: Python 3.11
- **Authentication**: Flask-JWT-Extended
- **Password Hashing**: bcrypt

### Database
- **MongoDB 7.0**
- Collections: users, tasks, categories
- Indexed queries for performance

### DevOps & Infrastructure
- **Cloud Provider**: Microsoft Azure
- **Containerization**: Docker, Docker Compose
- **CI/CD**: Jenkins
- **Container Registry**: Azure Container Registry (ACR)
- **Load Balancer**: Azure Standard Load Balancer
- **Networking**: Azure VNet, VNet Peering, NSG
- **Access**: Azure Bastion / Jump Host

---

## 🏢 Infrastructure Components

### Network Architecture

| Component | CIDR / Details | Purpose |
|-----------|---------------|---------|
| **VNet 1 (Jenkins)** | 10.0.0.0/16 | CI/CD Infrastructure |
| **VNet 2 (App)** | 10.1.0.0/16 | Application Tier |
| **VNet 3 (Database)** | 10.2.0.0/16 | Database Tier |
| **VNet Peering** | Bidirectional | Secure inter-VNet communication |

### Server Configuration

#### 1. Jenkins Master Server
- **Location**: VNet 1 (10.0.1.4)
- **Purpose**: CI/CD automation
- **Public IP**: None (accessed via Bastion)
- **Components**:
  - Jenkins Master (Docker)
  - Docker Engine
  - Azure CLI
  - SSH Client for deployment

#### 2. Application Server
- **Location**: VNet 2 (10.1.1.4)
- **Purpose**: Flask application hosting
- **Public IP**: None (behind Load Balancer)
- **Components**:
  - Flask App (Docker Compose)
  - Docker Engine
  - Connected to Load Balancer backend pool

#### 3. Database Server
- **Location**: VNet 3 (10.2.1.4)
- **Purpose**: MongoDB database
- **Public IP**: None (completely private)
- **Components**:
  - MongoDB 7.0 (Docker)
  - Persistent storage volume
  - Authentication enabled

### Azure Services

#### Azure Load Balancer
- **Type**: Standard Load Balancer
- **Frontend**: Public IP for user access
- **Backend Pool**: App Server (10.1.1.4:5000)
- **Health Probe**: HTTP probe on `/api/stats`
- **Rules**: Port 80 → 5000

#### Azure Container Registry (ACR)
- **Name**: taskmanageracr.azurecr.io
- **SKU**: Basic
- **Access**: Private (authentication required)
- **Images**:
  - `flask-app:latest`
  - `flask-app:<build-number>`

---

## 🔒 Security Features

### 1. Network Isolation
```
✓ Separate VNets for each tier
✓ No public IPs on app/database servers
✓ VNet peering for controlled communication
✓ Private endpoints for Azure services
```

### 2. Network Security Groups (NSG)

#### Jenkins Server NSG
```
Inbound:
  ✓ SSH (22) from Bastion only
  ✓ Jenkins (8080) from Admin IPs only
  ✓ Deny all other traffic

Outbound:
  ✓ HTTPS (443) to ACR
  ✓ Access to App VNet for deployment
```

#### App Server NSG
```
Inbound:
  ✓ Port 5000 from Load Balancer only
  ✓ SSH (22) from Bastion only
  ✓ Access from Jenkins VNet for deployment
  ✓ Deny all other traffic

Outbound:
  ✓ MongoDB (27017) to Database VNet
  ✓ HTTPS (443) to ACR
```

#### Database Server NSG
```
Inbound:
  ✓ MongoDB (27017) from App VNet only
  ✓ SSH (22) from Bastion only
  ✓ Deny all other traffic

Outbound:
  ✓ Deny all internet access
  ✓ Allow responses to App VNet
```

### 3. Application Security
- JWT token-based authentication
- Password hashing with bcrypt
- User session management
- Input validation and sanitization
- CORS configuration

### 4. Database Security
- MongoDB authentication enabled
- User-based access control
- Network isolation (no internet access)
- Encrypted connections
- Regular automated backups

### 5. Container Security
- Private container registry (ACR)
- Image vulnerability scanning
- Minimal base images
- Non-root user execution
- Secrets management via environment variables

---

## 📋 Prerequisites

### For Local Development
- Python 3.11 or higher
- Docker & Docker Compose
- Git
- MongoDB (local or Docker)

### For Azure Deployment
- Azure Subscription (active)
- Azure CLI installed and configured
- SSH key pair generated
- Terraform (optional, for IaC)
- Basic knowledge of Azure services

### Required Tools
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y
```

---

## 🚀 Quick Start

### Local Development Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Tow_Tier_Application
```

2. **Start with Docker Compose**
```bash
docker-compose up -d
```

3. **Access the application**
```
http://localhost:5000
```

4. **Create your first account**
- Click "Sign up"
- Enter username and password
- Start managing tasks!

### Manual Setup (Without Docker)

1. **Install dependencies**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Start MongoDB**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

3. **Configure environment**
```bash
export MONGO_URI="mongodb://localhost:27017/"
export JWT_SECRET_KEY="your-secret-key"
```

4. **Run the application**
```bash
python app.py
```

---

## ☁️ Azure Deployment

### Architecture Deployment Flow

```
1. Create Azure Infrastructure
   ├── Resource Group
   ├── Virtual Networks (3)
   ├── VNet Peering
   ├── Network Security Groups
   ├── Virtual Machines (3)
   ├── Load Balancer
   └── Container Registry

2. Setup Servers
   ├── Jenkins Server (CI/CD)
   ├── App Server (Flask)
   └── Database Server (MongoDB)

3. Configure CI/CD Pipeline
   ├── Jenkins Pipeline
   ├── ACR Integration
   └── Automated Deployment

4. Deploy Application
   └── Trigger Jenkins Pipeline
```

### Step-by-Step Deployment

#### Step 1: Create Azure Infrastructure

```bash
# Login to Azure
az login

# Create Resource Group
az group create --name rg-taskmanager --location eastus

# Create Virtual Networks
az network vnet create \
  --resource-group rg-taskmanager \
  --name vnet-jenkins \
  --address-prefix 10.0.0.0/16 \
  --subnet-name subnet-jenkins \
  --subnet-prefix 10.0.1.0/24

az network vnet create \
  --resource-group rg-taskmanager \
  --name vnet-app \
  --address-prefix 10.1.0.0/16 \
  --subnet-name subnet-app \
  --subnet-prefix 10.1.1.0/24

az network vnet create \
  --resource-group rg-taskmanager \
  --name vnet-db \
  --address-prefix 10.2.0.0/16 \
  --subnet-name subnet-db \
  --subnet-prefix 10.2.1.0/24
```

#### Step 2: Create VNet Peering

```bash
# Jenkins <-> App
az network vnet peering create \
  --resource-group rg-taskmanager \
  --name jenkins-to-app \
  --vnet-name vnet-jenkins \
  --remote-vnet vnet-app \
  --allow-vnet-access

az network vnet peering create \
  --resource-group rg-taskmanager \
  --name app-to-jenkins \
  --vnet-name vnet-app \
  --remote-vnet vnet-jenkins \
  --allow-vnet-access

# App <-> Database
az network vnet peering create \
  --resource-group rg-taskmanager \
  --name app-to-db \
  --vnet-name vnet-app \
  --remote-vnet vnet-db \
  --allow-vnet-access

az network vnet peering create \
  --resource-group rg-taskmanager \
  --name db-to-app \
  --vnet-name vnet-db \
  --remote-vnet vnet-app \
  --allow-vnet-access
```

#### Step 3: Create Azure Container Registry

```bash
az acr create \
  --resource-group rg-taskmanager \
  --name taskmanageracr \
  --sku Basic \
  --admin-enabled true

# Get ACR credentials
az acr credential show --name taskmanageracr
```

#### Step 4: Create Virtual Machines

```bash
# Jenkins Server
az vm create \
  --resource-group rg-taskmanager \
  --name vm-jenkins \
  --vnet-name vnet-jenkins \
  --subnet subnet-jenkins \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --admin-username azureuser \
  --ssh-key-values ~/.ssh/id_rsa.pub \
  --public-ip-address ""

# App Server
az vm create \
  --resource-group rg-taskmanager \
  --name vm-app \
  --vnet-name vnet-app \
  --subnet subnet-app \
  --image Ubuntu2204 \
  --size Standard_B2ms \
  --admin-username azureuser \
  --ssh-key-values ~/.ssh/id_rsa.pub \
  --public-ip-address ""

# Database Server
az vm create \
  --resource-group rg-taskmanager \
  --name vm-db \
  --vnet-name vnet-db \
  --subnet subnet-db \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --admin-username azureuser \
  --ssh-key-values ~/.ssh/id_rsa.pub \
  --public-ip-address ""
```

#### Step 5: Create Load Balancer

```bash
# Create public IP
az network public-ip create \
  --resource-group rg-taskmanager \
  --name pip-lb-app \
  --sku Standard

# Create load balancer
az network lb create \
  --resource-group rg-taskmanager \
  --name lb-app \
  --sku Standard \
  --public-ip-address pip-lb-app \
  --frontend-ip-name frontend-app \
  --backend-pool-name backend-app

# Create health probe
az network lb probe create \
  --resource-group rg-taskmanager \
  --lb-name lb-app \
  --name health-probe \
  --protocol http \
  --port 5000 \
  --path /api/stats

# Create load balancing rule
az network lb rule create \
  --resource-group rg-taskmanager \
  --lb-name lb-app \
  --name rule-http \
  --protocol tcp \
  --frontend-port 80 \
  --backend-port 5000 \
  --frontend-ip-name frontend-app \
  --backend-pool-name backend-app \
  --probe-name health-probe
```

#### Step 6: Setup Servers

**On each server, run the setup script:**

```bash
# Jenkins Server
./azure/scripts/setup-jenkins.sh

# App Server
./azure/scripts/setup-app.sh

# Database Server
./azure/scripts/setup-db.sh
```

#### Step 7: Configure Jenkins

1. Access Jenkins via Bastion/Jump Host
2. Install required plugins:
   - Docker Pipeline
   - SSH Agent
   - Git
   - Credentials Binding

3. Add credentials:
   - ACR username/password
   - SSH key for App Server
   - MongoDB URI (secret text)
   - JWT Secret Key (secret text)

4. Create Pipeline:
   - New Item → Pipeline
   - Configure Git repository
   - Use `Jenkinsfile` from repository

#### Step 8: Deploy Application

```bash
# Push code to trigger Jenkins pipeline
git add .
git commit -m "Initial deployment"
git push origin main

# Jenkins will automatically:
# 1. Build Docker image
# 2. Push to ACR
# 3. Deploy to App Server
# 4. Run health checks
```

---

## 🔄 CI/CD Pipeline

### Jenkins Pipeline Stages

```
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD Pipeline Flow                       │
└─────────────────────────────────────────────────────────────┘

1. 📥 Checkout
   └─ Clone repository from Git

2. 🔨 Build
   └─ docker build -t flask-app:${BUILD_NUMBER}

3. 🧪 Test (Optional)
   └─ Run unit tests and code quality checks

4. 🔐 Login to ACR
   └─ Authenticate with Azure Container Registry

5. 📤 Push to ACR
   ├─ Tag: flask-app:${BUILD_NUMBER}
   └─ Tag: flask-app:latest

6. 🚀 Deploy to App Server
   ├─ SSH to App Server (10.1.1.4)
   ├─ Pull image from ACR
   ├─ Stop old container
   └─ Start new container

7. ✅ Health Check
   ├─ Verify container is running
   └─ Test application endpoint

8. 📧 Notification
   └─ Send deployment status (Email/Slack)
```

### Jenkinsfile Overview

The pipeline is defined in `Jenkinsfile` with the following key features:

- **Automated Builds**: Triggered on Git push
- **Image Tagging**: Build number + latest tag
- **Zero-Downtime Deployment**: Rolling update strategy
- **Health Checks**: Automated verification
- **Rollback Capability**: Previous images retained
- **Notifications**: Success/failure alerts

### Triggering Deployments

```bash
# Automatic trigger (recommended)
git push origin main

# Manual trigger
# Go to Jenkins UI → Build Now

# Rollback to previous version
# Deploy specific build number from Jenkins
```

---

## 📚 API Documentation

### Base URL
```
Production: http://<LOAD_BALANCER_IP>
Local: http://localhost:5000
```

### Authentication

All protected endpoints require JWT token in header:
```
Authorization: Bearer <your_jwt_token>
```

### Endpoints

#### Authentication

**Register User**
```http
POST /api/register
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePass123!"
}

Response: 201 Created
{
  "access_token": "eyJ0eXAiOiJKV1Qi...",
  "username": "john_doe"
}
```

**Login**
```http
POST /api/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePass123!"
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1Qi...",
  "username": "john_doe"
}
```

#### Tasks

**Get All Tasks**
```http
GET /api/tasks?category=work&status=pending&search=meeting
Authorization: Bearer <token>

Response: 200 OK
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "title": "Team Meeting",
    "description": "Discuss Q4 roadmap",
    "category": "work",
    "priority": "high",
    "due_date": "2024-12-31",
    "completed": false,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
]
```

**Create Task**
```http
POST /api/tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Complete documentation",
  "description": "Write comprehensive README",
  "category": "work",
  "priority": "high",
  "due_date": "2024-12-31"
}

Response: 201 Created
```

**Update Task**
```http
PUT /api/tasks/<task_id>
Authorization: Bearer <token>
Content-Type: application/json

{
  "completed": true,
  "priority": "medium"
}

Response: 200 OK
```

**Delete Task**
```http
DELETE /api/tasks/<task_id>
Authorization: Bearer <token>

Response: 200 OK
{
  "message": "Task deleted"
}
```

#### Statistics

**Get Dashboard Stats**
```http
GET /api/stats
Authorization: Bearer <token>

Response: 200 OK
{
  "total": 25,
  "completed": 15,
  "pending": 10,
  "overdue": 3,
  "by_category": [
    {"_id": "work", "count": 12},
    {"_id": "personal", "count": 8},
    {"_id": "shopping", "count": 5}
  ]
}
```

---

## 📊 Monitoring

### Health Checks

**Application Health**
```bash
curl http://<LOAD_BALANCER_IP>/api/stats
```

**Container Status**
```bash
# On App Server
docker ps
docker logs flask-app

# On Database Server
docker ps
docker logs mongodb
```

**MongoDB Health**
```bash
# From App Server
docker exec -it mongodb mongosh -u admin -p password \
  --eval "db.adminCommand('ping')"
```

### Logs

**Application Logs**
```bash
docker logs -f flask-app
```

**MongoDB Logs**
```bash
docker logs -f mongodb
```

**Jenkins Logs**
```bash
docker logs -f jenkins
```

### Performance Monitoring

```bash
# Resource usage
docker stats

# System metrics
top
htop

# Network connections
netstat -tulpn

# Disk usage
df -h
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Cannot Access Application

**Problem**: Load Balancer not responding

**Solution**:
```bash
# Check Load Balancer health
az network lb show --resource-group rg-taskmanager --name lb-app

# Verify app is running
ssh azureuser@<BASTION_IP>
ssh 10.1.1.4
docker ps | grep flask-app
curl http://localhost:5000
```

#### 2. Database Connection Failed

**Problem**: App cannot connect to MongoDB

**Solution**:
```bash
# Check VNet peering
az network vnet peering list \
  --resource-group rg-taskmanager \
  --vnet-name vnet-app

# Test connectivity
telnet 10.2.1.4 27017

# Check NSG rules
az network nsg rule list \
  --resource-group rg-taskmanager \
  --nsg-name nsg-app
```

#### 3. Jenkins Deployment Failed

**Problem**: Pipeline fails at deployment stage

**Solution**:
```bash
# Check SSH connectivity
ssh azureuser@10.1.1.4

# Verify ACR credentials
docker login taskmanageracr.azurecr.io

# Check Jenkins logs
docker logs jenkins
```

#### 4. Container Won't Start

**Problem**: Docker container exits immediately

**Solution**:
```bash
# Check container logs
docker logs flask-app

# Verify environment variables
docker inspect flask-app | grep -A 10 Env

# Test MongoDB connection
docker run --rm taskmanageracr.azurecr.io/flask-app:latest \
  python -c "from pymongo import MongoClient; \
  client = MongoClient('mongodb://admin:password@10.2.1.4:27017/'); \
  print(client.server_info())"
```

### Getting Help

- Check logs: `docker logs <container_name>`
- Review NSG rules: `az network nsg rule list`
- Test connectivity: `telnet <ip> <port>`
- Verify VNet peering: `az network vnet peering list`

---

## 📁 Project Structure

```
Tow_Tier_Application/
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Application container
├── docker-compose.yml              # Local development
├── Jenkinsfile                     # CI/CD pipeline
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
│
├── templates/
│   └── index.html                  # Frontend SPA
│
├── azure/
│   └── scripts/
│       ├── setup-jenkins.sh        # Jenkins setup
│       ├── setup-app.sh            # App server setup
│       └── setup-db.sh             # Database setup
│
├── mongodb-vm/
│   ├── docker-compose.yml          # MongoDB deployment
│   └── mongod.conf                 # MongoDB config
│
├── app-vm/
│   └── docker-compose.yml          # App deployment
│
├── docs/
│   ├── ARCHITECTURE.md             # Architecture details
│   ├── DEPLOYMENT.md               # Deployment guide
│   └── architecture-diagram.png    # Architecture diagram
│
└── README.md                       # This file
```

---

## 💰 Cost Estimation

### Monthly Azure Costs (Approximate)

| Resource | Size/SKU | Monthly Cost |
|----------|----------|--------------|
| Jenkins VM | Standard_B2s | $30 |
| App VM | Standard_B2ms | $60 |
| Database VM | Standard_B2s | $30 |
| Load Balancer | Standard | $20 |
| ACR | Basic | $5 |
| VNet Peering | Data transfer | $10 |
| Storage | 128GB Premium SSD | $20 |
| **Total** | | **~$175/month** |

### Cost Optimization Tips

1. Use Azure Reserved Instances (save up to 72%)
2. Auto-shutdown Jenkins VM during off-hours
3. Implement auto-scaling for app servers
4. Use Azure Spot VMs for non-production
5. Optimize Docker image sizes

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - *Initial work* - [GitHub Profile](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Flask framework and community
- MongoDB team
- Docker and containerization ecosystem
- Jenkins CI/CD platform
- Microsoft Azure cloud platform
- Open source community

---

## 📞 Support

For issues, questions, or contributions:

- 📧 Email: support@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/repo/issues)
- 📖 Documentation: [Full Docs](docs/)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/repo/discussions)

---

## 🔗 Related Documentation

- [Architecture Details](ARCHITECTURE.md) - Comprehensive architecture documentation
- [Deployment Guide](DEPLOYMENT.md) - Step-by-step deployment instructions
- [API Documentation](docs/API.md) - Complete API reference
- [Security Guide](docs/SECURITY.md) - Security best practices

---

<div align="center">

**Built with ❤️ using Flask, MongoDB, Docker, Jenkins, and Azure**

[![Azure](https://img.shields.io/badge/Deployed%20on-Azure-0078D4?style=for-the-badge&logo=microsoft-azure)](https://azure.microsoft.com)
[![Docker](https://img.shields.io/badge/Containerized%20with-Docker-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![Jenkins](https://img.shields.io/badge/CI%2FCD-Jenkins-D24939?style=for-the-badge&logo=jenkins)](https://www.jenkins.io/)

</div>
