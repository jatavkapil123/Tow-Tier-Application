# Architecture Documentation

## System Architecture Overview

This document provides detailed information about the two-tier application architecture deployed on Azure.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              INTERNET                                    │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ HTTPS
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      Azure Load Balancer                                 │
│                    (Public IP: 20.x.x.x)                                │
│                                                                          │
│  • Health Probe: HTTP /api/stats                                        │
│  • Frontend Port: 80                                                    │
│  • Backend Port: 5000                                                   │
│  • Distribution: Round Robin                                            │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ Private Network
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         VNet-2 (Application)                             │
│                         CIDR: 10.1.0.0/16                               │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │              Application Server (VM)                           │    │
│  │              Private IP: 10.1.1.4                              │    │
│  │                                                                │    │
│  │  ┌──────────────────────────────────────────────────────┐   │    │
│  │  │         Docker Container: Flask App                   │   │    │
│  │  │         Port: 5000                                    │   │    │
│  │  │                                                       │   │    │
│  │  │  Components:                                         │   │    │
│  │  │  • Flask Web Framework                               │   │    │
│  │  │  • JWT Authentication                                │   │    │
│  │  │  • REST API Endpoints                                │   │    │
│  │  │  • Frontend (HTML/CSS/JS)                            │   │    │
│  │  │  • PyMongo Driver                                    │   │    │
│  │  └──────────────────────────────────────────────────────┘   │    │
│  └───────────────────────────────────────────────────────────────┘    │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ VNet Peering
                                 │ (10.1.0.0/16 ↔ 10.2.0.0/16)
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         VNet-3 (Database)                                │
│                         CIDR: 10.2.0.0/16                               │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │              Database Server (VM)                              │    │
│  │              Private IP: 10.2.1.4                              │    │
│  │                                                                │    │
│  │  ┌──────────────────────────────────────────────────────┐   │    │
│  │  │         Docker Container: MongoDB                     │   │    │
│  │  │         Port: 27017                                   │   │    │
│  │  │                                                       │   │    │
│  │  │  Components:                                         │   │    │
│  │  │  • MongoDB 7.0                                       │   │    │
│  │  │  • Authentication Enabled                            │   │    │
│  │  │  • Persistent Volume                                 │   │    │
│  │  │  • Collections:                                      │   │    │
│  │  │    - users                                           │   │    │
│  │  │    - tasks                                           │   │    │
│  │  │    - categories                                      │   │    │
│  │  └──────────────────────────────────────────────────────┘   │    │
│  └───────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘

                                 ▲
                                 │ VNet Peering
                                 │ (10.0.0.0/16 ↔ 10.1.0.0/16)
                                 │
┌─────────────────────────────────────────────────────────────────────────┐
│                         VNet-1 (Jenkins)                                 │
│                         CIDR: 10.0.0.0/16                               │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │              Jenkins Master Server (VM)                        │    │
│  │              Private IP: 10.0.1.4                              │    │
│  │                                                                │    │
│  │  ┌──────────────────────────────────────────────────────┐   │    │
│  │  │         Docker Container: Jenkins                     │   │    │
│  │  │         Ports: 8080, 50000                            │   │    │
│  │  │                                                       │   │    │
│  │  │  Components:                                         │   │    │
│  │  │  • Jenkins Master                                    │   │    │
│  │  │  • Docker Engine                                     │   │    │
│  │  │  • Azure CLI                                         │   │    │
│  │  │  • Git                                               │   │    │
│  │  │  • SSH Client                                        │   │    │
│  │  └──────────────────────────────────────────────────────┘   │    │
│  └───────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                 │
                                 │ HTTPS
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   Azure Container Registry (ACR)                         │
│                   taskmanageracr.azurecr.io                             │
│                                                                          │
│  Docker Images:                                                         │
│  • flask-app:latest                                                     │
│  • flask-app:<build-number>                                             │
└─────────────────────────────────────────────────────────────────────────┘
```

## Network Architecture

### VNet Configuration

| Component | CIDR | Subnet | Purpose |
|-----------|------|--------|---------|
| VNet-1 | 10.0.0.0/16 | 10.0.1.0/24 | Jenkins CI/CD Infrastructure |
| VNet-2 | 10.1.0.0/16 | 10.1.1.0/24 | Application Tier |
| VNet-3 | 10.2.0.0/16 | 10.2.1.0/24 | Database Tier |

### VNet Peering

```
VNet-1 (Jenkins)  ←──────────→  VNet-2 (Application)
                                       │
                                       │
                                       ▼
                                VNet-3 (Database)
```

**Peering Properties:**
- Allow virtual network access: Enabled
- Allow forwarded traffic: Disabled
- Allow gateway transit: Disabled
- Use remote gateways: Disabled

### Traffic Flow

#### User Request Flow
```
User Browser
    │
    ▼
Load Balancer (Public IP)
    │
    ▼
App Server (10.1.1.4:5000)
    │
    ▼
MongoDB (10.2.1.4:27017)
    │
    ▼
Response back through same path
```

#### CI/CD Deployment Flow
```
Developer Push
    │
    ▼
Git Repository
    │
    ▼
Jenkins (10.0.1.4)
    │
    ├──→ Build Docker Image
    │
    ├──→ Push to ACR
    │
    └──→ Deploy to App Server (10.1.1.4)
```

## Security Architecture

### Network Security Groups (NSG)

#### NSG-Jenkins (VNet-1)
```
Priority | Direction | Action | Source      | Destination | Port  | Protocol
---------|-----------|--------|-------------|-------------|-------|----------
100      | Inbound   | Allow  | Bastion     | 10.0.1.4    | 22    | TCP
110      | Inbound   | Allow  | Admin IPs   | 10.0.1.4    | 8080  | TCP
120      | Inbound   | Allow  | VNet-2      | 10.0.1.4    | 50000 | TCP
1000     | Inbound   | Deny   | *           | *           | *     | *
100      | Outbound  | Allow  | 10.0.1.4    | Internet    | 443   | TCP
110      | Outbound  | Allow  | 10.0.1.4    | 10.1.0.0/16 | *     | TCP
```

#### NSG-App (VNet-2)
```
Priority | Direction | Action | Source      | Destination | Port | Protocol
---------|-----------|--------|-------------|-------------|------|----------
100      | Inbound   | Allow  | LB          | 10.1.1.4    | 5000 | TCP
110      | Inbound   | Allow  | Bastion     | 10.1.1.4    | 22   | TCP
120      | Inbound   | Allow  | 10.0.0.0/16 | 10.1.1.4    | *    | TCP
1000     | Inbound   | Deny   | *           | *           | *    | *
100      | Outbound  | Allow  | 10.1.1.4    | 10.2.1.4    | 27017| TCP
110      | Outbound  | Allow  | 10.1.1.4    | Internet    | 443  | TCP
```

#### NSG-Database (VNet-3)
```
Priority | Direction | Action | Source      | Destination | Port  | Protocol
---------|-----------|--------|-------------|-------------|-------|----------
100      | Inbound   | Allow  | 10.1.0.0/16 | 10.2.1.4    | 27017 | TCP
110      | Inbound   | Allow  | Bastion     | 10.2.1.4    | 22    | TCP
1000     | Inbound   | Deny   | *           | *           | *     | *
100      | Outbound  | Allow  | 10.2.1.4    | 10.1.0.0/16 | *     | TCP
1000     | Outbound  | Deny   | 10.2.1.4    | Internet    | *     | *
```

### Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Network Isolation                                  │
│ • Separate VNets for each tier                             │
│ • No public IPs on app/db servers                          │
│ • VNet peering for controlled communication                │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: Network Security Groups                           │
│ • Whitelist-based access control                           │
│ • Port-level restrictions                                  │
│ • Source/destination filtering                             │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: Application Security                              │
│ • JWT authentication                                        │
│ • Password hashing (bcrypt)                                │
│ • Input validation                                         │
│ • CORS configuration                                       │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: Database Security                                 │
│ • MongoDB authentication enabled                           │
│ • User-based access control                                │
│ • Network isolation                                        │
│ • Encrypted connections                                    │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 5: Container Security                                │
│ • Private container registry (ACR)                         │
│ • Image scanning                                           │
│ • Minimal base images                                      │
│ • Non-root user execution                                  │
└─────────────────────────────────────────────────────────────┘
```

## Application Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (SPA)                           │
│                                                             │
│  • HTML5 / CSS3 / JavaScript                               │
│  • Responsive Design                                       │
│  • JWT Token Management                                    │
│  • AJAX API Calls                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/JSON
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Flask Application                          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Authentication Layer                                │  │
│  │  • JWT Token Generation                             │  │
│  │  • Password Hashing (bcrypt)                        │  │
│  │  • User Registration/Login                          │  │
│  └─────────────────────────────────────────────────────┘  │
│                       │                                     │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  API Layer (REST)                                    │  │
│  │  • /api/register                                     │  │
│  │  • /api/login                                        │  │
│  │  • /api/tasks (CRUD)                                 │  │
│  │  • /api/categories                                   │  │
│  │  • /api/stats                                        │  │
│  └─────────────────────────────────────────────────────┘  │
│                       │                                     │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Business Logic Layer                                │  │
│  │  • Task Management                                   │  │
│  │  • Category Management                               │  │
│  │  • Statistics Calculation                            │  │
│  │  • Search & Filtering                                │  │
│  └─────────────────────────────────────────────────────┘  │
│                       │                                     │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Data Access Layer                                   │  │
│  │  • PyMongo Driver                                    │  │
│  │  • Connection Pooling                                │  │
│  │  • Query Optimization                                │  │
│  └─────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │ MongoDB Protocol
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    MongoDB Database                         │
│                                                             │
│  Collections:                                              │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  users                                               │  │
│  │  • _id (ObjectId)                                    │  │
│  │  • username (String, unique)                         │  │
│  │  • password (String, hashed)                         │  │
│  │  • created_at (DateTime)                             │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  tasks                                               │  │
│  │  • _id (ObjectId)                                    │  │
│  │  • user_id (String, indexed)                         │  │
│  │  • title (String)                                    │  │
│  │  • description (String)                              │  │
│  │  • category (String, indexed)                        │  │
│  │  • priority (String)                                 │  │
│  │  • due_date (DateTime)                               │  │
│  │  • completed (Boolean)                               │  │
│  │  • created_at (DateTime)                             │  │
│  │  • updated_at (DateTime)                             │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  categories                                          │  │
│  │  • _id (ObjectId)                                    │  │
│  │  • user_id (String)                                  │  │
│  │  • name (String)                                     │  │
│  │  • color (String)                                    │  │
│  │  • created_at (DateTime)                             │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## CI/CD Architecture

### Jenkins Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Git Repository                           │
│                    (GitHub/GitLab)                          │
└──────────────────────┬──────────────────────────────────────┘
                       │ Webhook
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Jenkins Master                             │
│                  (10.0.1.4)                                 │
│                                                             │
│  Pipeline Stages:                                          │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 1. Checkout                                          │  │
│  │    • Clone repository                                │  │
│  │    • Checkout branch                                 │  │
│  └─────────────────────────────────────────────────────┘  │
│                       │                                     │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 2. Build                                             │  │
│  │    • docker build                                    │  │
│  │    • Tag with build number                           │  │
│  └─────────────────────────────────────────────────────┘  │
│                       │                                     │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 3. Test                                              │  │
│  │    • Run unit tests                                  │  │
│  │    • Code quality checks                             │  │
│  └─────────────────────────────────────────────────────┘  │
│                       │                                     │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 4. Push to ACR                                       │  │
│  │    • docker login                                    │  │
│  │    • docker push                                     │  │
│  └─────────────────────────────────────────────────────┘  │
│                       │                                     │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 5. Deploy                                            │  │
│  │    • SSH to App Server                               │  │
│  │    • Pull image from ACR                             │  │
│  │    • Stop old container                              │  │
│  │    • Start new container                             │  │
│  └─────────────────────────────────────────────────────┘  │
│                       │                                     │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 6. Health Check                                      │  │
│  │    • Verify container running                        │  │
│  │    • Test application endpoint                       │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Scalability Considerations

### Horizontal Scaling

```
Current Architecture:
┌──────────────┐
│ Load Balancer│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  App Server  │
└──────────────┘

Scaled Architecture:
┌──────────────┐
│ Load Balancer│
└──────┬───────┘
       │
       ├────────┬────────┬────────┐
       ▼        ▼        ▼        ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│App Server│ │App Server│ │App Server│ │App Server│
│    1     │ │    2     │ │    3     │ │    4     │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

### Database Scaling

```
Current: Single MongoDB Instance

Future Options:
1. MongoDB Replica Set (High Availability)
2. MongoDB Sharding (Horizontal Scaling)
3. Azure Cosmos DB (Managed Service)
```

## Disaster Recovery

### Backup Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                    Backup Components                        │
├─────────────────────────────────────────────────────────────┤
│ 1. Database Backups                                         │
│    • Daily automated backups                                │
│    • Retention: 30 days                                     │
│    • Storage: Azure Blob Storage                            │
│                                                             │
│ 2. Application Code                                         │
│    • Git repository (version controlled)                    │
│    • Multiple branches                                      │
│                                                             │
│ 3. Docker Images                                            │
│    • Stored in ACR                                          │
│    • Tagged with build numbers                              │
│    • Retention policy: 90 days                              │
│                                                             │
│ 4. Configuration                                            │
│    • Infrastructure as Code (Terraform)                     │
│    • Environment variables (Azure Key Vault)                │
└─────────────────────────────────────────────────────────────┘
```

## Monitoring Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Azure Monitor                              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Metrics Collection                                  │  │
│  │  • CPU Usage                                         │  │
│  │  • Memory Usage                                      │  │
│  │  • Network Traffic                                   │  │
│  │  • Disk I/O                                          │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Log Analytics                                       │  │
│  │  • Application Logs                                  │  │
│  │  • System Logs                                       │  │
│  │  • Security Logs                                     │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Alerts                                              │  │
│  │  • High CPU/Memory                                   │  │
│  │  • Application Errors                                │  │
│  │  • Failed Deployments                                │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Cost Optimization

### Resource Sizing

| Resource | Current Size | Monthly Cost (Est.) | Notes |
|----------|-------------|---------------------|-------|
| Jenkins VM | Standard_B2s | $30 | Can be stopped when not in use |
| App VM | Standard_B2ms | $60 | Always running |
| DB VM | Standard_B2s | $30 | Always running |
| Load Balancer | Standard | $20 | Pay per rule |
| ACR | Basic | $5 | Pay per storage |
| VNet Peering | - | $10 | Pay per GB transferred |
| **Total** | - | **~$155/month** | Approximate |

### Cost Saving Strategies

1. Use Azure Reserved Instances (up to 72% savings)
2. Auto-shutdown Jenkins VM during off-hours
3. Implement auto-scaling for app servers
4. Use Azure Spot VMs for non-production
5. Optimize image sizes in ACR

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Maintained By:** DevOps Team
