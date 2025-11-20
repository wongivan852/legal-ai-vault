# Legal AI Vault - Ubuntu GPU Server Deployment Guide

**Target Environment:** Ubuntu Server 20.04/22.04 LTS with NVIDIA GPU  
**Last Updated:** 2025-11-20  
**Version:** 1.0

---

## Table of Contents

1. [Server Requirements](#1-server-requirements)
2. [Pre-Deployment Checklist](#2-pre-deployment-checklist)
3. [System Preparation](#3-system-preparation)
4. [GPU Configuration](#4-gpu-configuration)
5. [Application Deployment](#5-application-deployment)
6. [Post-Deployment Verification](#6-post-deployment-verification)
7. [Production Configuration](#7-production-configuration)
8. [Monitoring & Maintenance](#8-monitoring--maintenance)
9. [Troubleshooting](#9-troubleshooting)
10. [Security Hardening](#10-security-hardening)

---

## 1. Server Requirements

### Minimum Hardware Specifications

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 4 cores | 8+ cores |
| **RAM** | 16 GB | 32+ GB |
| **GPU** | NVIDIA GPU with 8GB VRAM | NVIDIA RTX 3090/4090 or A100 |
| **Disk** | 100 GB SSD | 500 GB NVMe SSD |
| **Network** | 100 Mbps | 1 Gbps |

### GPU Recommendations

**Supported GPUs:**
- NVIDIA RTX 3060/3070/3080/3090 (12-24GB VRAM)
- NVIDIA RTX 4090 (24GB VRAM)
- NVIDIA A100/A6000 (40-80GB VRAM)
- NVIDIA T4 (16GB VRAM) - Cloud instances

**CUDA Version:** 11.8 or higher required

### OS Requirements

- **Ubuntu 20.04 LTS** or **Ubuntu 22.04 LTS**
- **Kernel:** 5.4+ (Ubuntu 20.04) or 5.15+ (Ubuntu 22.04)
- **Architecture:** x86_64 (AMD64)

---

## 2. Pre-Deployment Checklist

Before starting deployment, ensure you have:

```bash
# System Access
- [ ] Root or sudo access to Ubuntu server
- [ ] SSH access configured
- [ ] Firewall rules reviewed

# Network Configuration
- [ ] Static IP or DNS configured
- [ ] Ports 8000 (API), 5432 (PostgreSQL), 6333 (Qdrant), 11434 (Ollama) available
- [ ] SSL certificates ready (if using HTTPS)

# Data Preparation
- [ ] HK ordinance dataset downloaded (783 MB compressed)
- [ ] Dataset extracted and ready for upload

# Credentials
- [ ] PostgreSQL password decided
- [ ] API keys/tokens prepared (if needed)
- [ ] GitHub access token (for private repos)
```

---

## 3. System Preparation

### Step 1: Update System

```bash
# Update package list and upgrade system
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y

# Install essential tools
sudo apt install -y \
    curl \
    wget \
    git \
    vim \
    htop \
    net-tools \
    software-properties-common \
    build-essential
```

### Step 2: Install Docker

```bash
# Remove old Docker versions
sudo apt remove docker docker-engine docker.io containerd runc

# Install Docker dependencies
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verify Docker installation
sudo docker --version
sudo docker compose version

# Add current user to docker group (optional, allows non-sudo docker)
sudo usermod -aG docker $USER
newgrp docker
```

### Step 3: Install NVIDIA Drivers

```bash
# Check if NVIDIA GPU is detected
lspci | grep -i nvidia

# Install NVIDIA driver (recommended: use ubuntu-drivers)
sudo ubuntu-drivers devices
sudo ubuntu-drivers autoinstall

# Alternative: Install specific driver version
# sudo apt install -y nvidia-driver-535

# Reboot system to load drivers
sudo reboot

# After reboot, verify NVIDIA driver
nvidia-smi
```

**Expected Output:**
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.xx.xx    Driver Version: 535.xx.xx    CUDA Version: 12.2   |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
...
```

---

## 4. GPU Configuration

### Step 1: Install NVIDIA Container Toolkit

```bash
# Add NVIDIA Container Toolkit repository
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/libnvidia-container/$distribution/$(ARCH) /" | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install NVIDIA Container Toolkit
sudo apt update
sudo apt install -y nvidia-container-toolkit

# Configure Docker to use NVIDIA runtime
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify GPU access in Docker
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### Step 2: Test GPU in Docker

```bash
# Run CUDA test container
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 bash -c "nvidia-smi && nvcc --version"

# If successful, you should see GPU info and CUDA version
```

---

## 5. Application Deployment

### Step 1: Clone Repository

```bash
# Navigate to deployment directory
cd /opt

# Clone repository
sudo git clone https://github.com/wongivan852/legal-ai-vault.git
cd legal-ai-vault

# Set proper ownership
sudo chown -R $USER:$USER /opt/legal-ai-vault
```

### Step 2: Upload HK Ordinance Dataset

```bash
# Create data directory if not exists
mkdir -p /opt/legal-ai-vault/data

# Upload dataset (use scp, rsync, or wget)
# Option 1: From local machine
scp -r /path/to/hkel_legal_import/ user@server:/opt/legal-ai-vault/data/

# Option 2: Download directly on server (if available via URL)
# cd /opt/legal-ai-vault/data
# wget https://your-storage-url/hkel_data.tar.gz
# tar -xzf hkel_data.tar.gz

# Verify dataset
ls -lh /opt/legal-ai-vault/data/hkel_legal_import/ | wc -l
# Should show ~1,709 XML files
```

### Step 3: Configure Docker Compose for GPU

```bash
# Backup original docker-compose.yml
cp docker-compose.yml docker-compose.yml.backup

# Create GPU-enabled docker-compose.yml
cat > docker-compose.override.yml << 'COMPOSE_EOF'
version: '3.8'

services:
  ollama:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility
COMPOSE_EOF
```

### Step 4: Configure Environment Variables

```bash
# Create .env file for production
cat > .env << 'ENV_EOF'
# Database Configuration
DB_USER=legal_vault_user
DB_PASSWORD=CHANGE_THIS_STRONG_PASSWORD
DB_NAME=legal_ai_vault
DB_HOST=postgres
DB_PORT=5432

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Ollama Configuration
OLLAMA_HOST=http://ollama:11434
OLLAMA_NUM_GPU=1
OLLAMA_GPU_LAYERS=35

# Qdrant Configuration
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# Application Settings
ENVIRONMENT=production
LOG_LEVEL=info
ENV_EOF

# Secure the .env file
chmod 600 .env

# IMPORTANT: Edit .env and change DB_PASSWORD
vim .env
```

### Step 5: Start Services

```bash
# Pull Docker images
docker compose pull

# Start services in detached mode
docker compose up -d

# Watch startup logs
docker compose logs -f

# Wait for all services to be healthy (may take 2-3 minutes)
watch -n 2 'docker compose ps'
```

### Step 6: Verify GPU Usage

```bash
# Check Ollama container GPU access
docker exec legal-ai-ollama nvidia-smi

# Monitor GPU usage in real-time
watch -n 1 nvidia-smi
```

### Step 7: Pull AI Models

```bash
# Pull LLaMA 3.1 8B model (takes 5-10 minutes)
docker compose exec ollama ollama pull llama3.1:8b

# Pull embedding model
docker compose exec ollama ollama pull nomic-embed-text:latest

# Verify models
docker compose exec ollama ollama list
```

### Step 8: Import HK Ordinances

```bash
# Run import script (takes 45-60 minutes)
docker compose exec api python3 /app/scripts/import_hk_ordinances.py

# Monitor import progress (in another terminal)
docker compose logs -f api | grep "Processing\|Imported"

# Check import status in database
docker exec -it legal-ai-postgres psql -U legal_vault_user -d legal_ai_vault -c "SELECT COUNT(*) FROM hk_legal_documents;"
# Expected: 1699

docker exec -it legal-ai-postgres psql -U legal_vault_user -d legal_ai_vault -c "SELECT COUNT(*) FROM hk_legal_sections;"
# Expected: 11288
```

---

## 6. Post-Deployment Verification

### Health Check

```bash
# Check API health
curl -s http://localhost:8000/health | jq

# Expected output:
# {
#   "status": "healthy",
#   "ollama": {
#     "status": "healthy",
#     "llm_available": true,
#     "embedding_available": true
#   }
# }
```

### Functional Testing

```bash
# Test legal research agent
cat > /tmp/test_query.json << 'TEST_EOF'
{
  "task": {
    "question": "What are the fire safety requirements for residential buildings?"
  }
}
TEST_EOF

curl -X POST http://localhost:8000/api/agents/legal_research/execute \
  -H "Content-Type: application/json" \
  -d @/tmp/test_query.json

# Should return answer with sources (takes 60-90 seconds)
```

### Performance Benchmarking

```bash
# Monitor GPU utilization during query
nvidia-smi dmon -s u -c 60 &
curl -X POST http://localhost:8000/api/agents/legal_research/execute \
  -H "Content-Type: application/json" \
  -d @/tmp/test_query.json
```

---

## 7. Production Configuration

### Reverse Proxy (Nginx)

```bash
# Install Nginx
sudo apt install -y nginx

# Configure Nginx as reverse proxy
sudo tee /etc/nginx/sites-available/legal-ai-vault << 'NGINX_EOF'
server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL certificates (use Let's Encrypt or your certificates)
    ssl_certificate /etc/ssl/certs/legal-ai-vault.crt;
    ssl_certificate_key /etc/ssl/private/legal-ai-vault.key;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Proxy settings
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts for long-running AI queries
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # API docs
    location /docs {
        proxy_pass http://localhost:8000/docs;
    }

    # Static files (if needed)
    location /static {
        alias /opt/legal-ai-vault/frontend/static;
        expires 30d;
    }
}
NGINX_EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/legal-ai-vault /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured by default
sudo certbot renew --dry-run
```

### Firewall Configuration

```bash
# Configure UFW firewall
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# Verify rules
sudo ufw status
```

### Systemd Service (Auto-restart)

```bash
# Create systemd service for auto-restart
sudo tee /etc/systemd/system/legal-ai-vault.service << 'SERVICE_EOF'
[Unit]
Description=Legal AI Vault Docker Compose Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/legal-ai-vault
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable legal-ai-vault.service

# Test service
sudo systemctl start legal-ai-vault.service
sudo systemctl status legal-ai-vault.service
```

---

## 8. Monitoring & Maintenance

### Container Monitoring

```bash
# Create monitoring script
cat > /opt/legal-ai-vault/monitor.sh << 'MONITOR_EOF'
#!/bin/bash

echo "=== Legal AI Vault System Status ==="
echo ""
echo "Container Status:"
docker compose ps

echo ""
echo "GPU Utilization:"
nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total --format=csv

echo ""
echo "Database Status:"
docker exec legal-ai-postgres psql -U legal_vault_user -d legal_ai_vault -c "SELECT COUNT(*) as documents FROM hk_legal_documents;"

echo ""
echo "API Health:"
curl -s http://localhost:8000/health | jq -r '.status'

echo ""
echo "Disk Usage:"
df -h /opt/legal-ai-vault

echo ""
echo "Memory Usage:"
free -h
MONITOR_EOF

chmod +x /opt/legal-ai-vault/monitor.sh

# Run monitoring
/opt/legal-ai-vault/monitor.sh
```

### Log Management

```bash
# View real-time logs
docker compose logs -f

# View specific service logs
docker compose logs -f api
docker compose logs -f ollama

# Export logs for analysis
docker compose logs --since 24h > /tmp/legal-ai-vault-logs-$(date +%Y%m%d).log

# Configure log rotation
sudo tee /etc/logrotate.d/legal-ai-vault << 'LOGROTATE_EOF'
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    missingok
    delaycompress
    copytruncate
}
LOGROTATE_EOF
```

### Database Backup

```bash
# Create backup script
cat > /opt/legal-ai-vault/backup.sh << 'BACKUP_EOF'
#!/bin/bash

BACKUP_DIR="/opt/legal-ai-vault/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker exec legal-ai-postgres pg_dump -U legal_vault_user legal_ai_vault | gzip > $BACKUP_DIR/postgres_$DATE.sql.gz

# Backup Qdrant data
docker exec legal-ai-qdrant tar czf - /qdrant/storage > $BACKUP_DIR/qdrant_$DATE.tar.gz

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
BACKUP_EOF

chmod +x /opt/legal-ai-vault/backup.sh

# Schedule daily backup (add to crontab)
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/legal-ai-vault/backup.sh >> /var/log/legal-ai-vault-backup.log 2>&1") | crontab -
```

---

## 9. Troubleshooting

### GPU Not Detected in Container

```bash
# Check NVIDIA Container Toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify GPU in test container
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# Check docker-compose.override.yml is present
cat docker-compose.override.yml
```

### Ollama Model Loading Slow

```bash
# Increase GPU layers in .env
OLLAMA_GPU_LAYERS=35  # Adjust based on VRAM (8GB: 25, 12GB: 35, 24GB: 50)

# Check GPU memory usage
docker exec legal-ai-ollama nvidia-smi

# Restart ollama service
docker compose restart ollama
```

### Import Script Fails

```bash
# Check file permissions
ls -lh /opt/legal-ai-vault/data/hkel_legal_import/

# Verify database connectivity
docker exec -it legal-ai-postgres psql -U legal_vault_user -d legal_ai_vault -c "\dt"

# Re-run import with verbose logging
docker compose exec api python3 /app/scripts/import_hk_ordinances.py 2>&1 | tee import_debug.log
```

### API Response Timeout

```bash
# Increase Nginx timeout (if using Nginx)
# Edit /etc/nginx/sites-available/legal-ai-vault
proxy_read_timeout 600s;

# Increase Docker healthcheck timeout
# Edit docker-compose.yml healthcheck intervals

# Check GPU performance
nvidia-smi dmon -s u
```

### Out of Memory (OOM)

```bash
# Check system memory
free -h
htop

# Reduce API workers in .env
API_WORKERS=2

# Use smaller LLM model
docker compose exec ollama ollama pull llama3.1:8b-q4_K_M

# Add swap space (if needed)
sudo fallocate -l 16G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 10. Security Hardening

### Docker Security

```bash
# Run containers as non-root user
# Add to docker-compose.yml:
user: "1000:1000"

# Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1

# Scan images for vulnerabilities
docker scan legal-ai-vault-api
```

### Database Security

```bash
# Strong password enforcement
# Edit .env with strong password (20+ chars, mixed case, symbols)

# Restrict PostgreSQL access
# Edit docker-compose.yml to bind to localhost only:
ports:
  - "127.0.0.1:5432:5432"
```

### Network Security

```bash
# Create isolated Docker network
docker network create legal-ai-network --driver bridge --subnet=172.25.0.0/16

# Update docker-compose.yml to use custom network

# Enable fail2ban for SSH
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Application Security

```bash
# Disable API docs in production (edit main.py)
# Set in .env:
DISABLE_DOCS=true

# Enable rate limiting (configure in API)

# Regular security updates
sudo apt update && sudo apt upgrade -y
docker compose pull
docker compose up -d
```

---

## Quick Reference Commands

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Restart specific service
docker compose restart api

# View logs
docker compose logs -f api

# Check GPU usage
nvidia-smi

# Monitor system
/opt/legal-ai-vault/monitor.sh

# Database backup
/opt/legal-ai-vault/backup.sh

# Check health
curl http://localhost:8000/health

# Update application
cd /opt/legal-ai-vault
git pull origin main
docker compose pull
docker compose up -d --build
```

---

## Support & Documentation

- **User Manual:** `USER_MANUAL.md`
- **System Validation:** `SYSTEM_VALIDATION_REPORT.md`
- **Deployment Summary:** `DEPLOYMENT_SUMMARY.md`
- **GitHub Repository:** https://github.com/wongivan852/legal-ai-vault

---

**Deployment Guide Version:** 1.0  
**Last Updated:** 2025-11-20  
**Tested On:** Ubuntu 22.04 LTS with NVIDIA RTX 3090

🚀 **Production Deployment Ready**
