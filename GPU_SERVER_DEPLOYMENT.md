# Vault AI Platform - GPU Server Deployment Guide

**Target Environment:** Linux server with 4 NVIDIA GPUs
**Optimized for:** llama3.3:70b model with GPU acceleration

---

## 📋 Table of Contents

1. [Hardware Requirements](#hardware-requirements)
2. [Pre-Deployment Setup](#pre-deployment-setup)
3. [NVIDIA Driver Installation](#nvidia-driver-installation)
4. [Docker GPU Support](#docker-gpu-support)
5. [Application Configuration](#application-configuration)
6. [Deployment Steps](#deployment-steps)
7. [Performance Optimization](#performance-optimization)
8. [Monitoring & Maintenance](#monitoring--maintenance)
9. [Troubleshooting](#troubleshooting)

---

## 🖥️ Hardware Requirements

### Minimum Specifications

- **CPU:** 16+ cores (Intel Xeon or AMD EPYC recommended)
- **RAM:** 64GB DDR4 (128GB recommended for llama3.3:70b)
- **GPU:** 4x NVIDIA GPUs with 24GB+ VRAM each
  - Recommended: A100 (40GB/80GB), A6000 (48GB), RTX 4090 (24GB)
  - Minimum: RTX 3090 (24GB)
- **Storage:**
  - 500GB+ NVMe SSD for OS and models
  - 1TB+ for data and logs
- **Network:** 1Gbps minimum, 10Gbps recommended

### Recommended Server Configurations

#### Configuration 1: High Performance
- **GPUs:** 4x NVIDIA A100 80GB
- **CPU:** 2x AMD EPYC 7543 (32 cores / 64 threads each)
- **RAM:** 512GB DDR4
- **Storage:** 2TB NVMe SSD + 10TB HDD
- **Expected Performance:** 100+ concurrent users, <5s response time

#### Configuration 2: Balanced
- **GPUs:** 4x NVIDIA A6000 48GB
- **CPU:** Intel Xeon Gold 6248R (24 cores / 48 threads)
- **RAM:** 256GB DDR4
- **Storage:** 1TB NVMe SSD + 4TB HDD
- **Expected Performance:** 50-80 concurrent users, 5-10s response time

#### Configuration 3: Budget-Friendly
- **GPUs:** 4x NVIDIA RTX 4090 24GB
- **CPU:** AMD Ryzen Threadripper 3970X (32 cores / 64 threads)
- **RAM:** 128GB DDR4
- **Storage:** 1TB NVMe SSD
- **Expected Performance:** 30-50 concurrent users, 10-15s response time

---

## 🔧 Pre-Deployment Setup

### 1. Operating System Installation

Recommended: **Ubuntu 22.04 LTS Server**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y \
    build-essential \
    curl \
    git \
    vim \
    htop \
    nvtop \
    python3-pip \
    ufw \
    fail2ban
```

### 2. System Configuration

```bash
# Increase file descriptor limits
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Optimize network settings
sudo tee -a /etc/sysctl.conf << EOF
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.ip_local_port_range = 1024 65535
EOF

sudo sysctl -p
```

### 3. Firewall Configuration

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow API (if exposing directly)
sudo ufw allow 8000/tcp

# Check status
sudo ufw status
```

---

## 🎮 NVIDIA Driver Installation

### Method 1: Automatic Installation (Recommended)

```bash
# Add NVIDIA package repository
distribution=$(. /etc/os-release;echo $ID$VERSION_ID | sed -e 's/\.//g')
wget https://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb

# Update and install driver
sudo apt update
sudo apt install -y nvidia-driver-535 nvidia-utils-535

# Reboot
sudo reboot
```

### Method 2: Manual Installation

```bash
# Download latest driver from NVIDIA website
# https://www.nvidia.com/Download/index.aspx

# Install dependencies
sudo apt install -y gcc make

# Run installer
sudo bash NVIDIA-Linux-x86_64-535.xx.xx.run
```

### Verify Installation

```bash
# Check NVIDIA driver
nvidia-smi

# Expected output:
# +-----------------------------------------------------------------------------+
# | NVIDIA-SMI 535.xx.xx    Driver Version: 535.xx.xx    CUDA Version: 12.2    |
# |-------------------------------+----------------------+----------------------+
# | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
# | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
# |===============================+======================+======================|
# |   0  NVIDIA A100-SXM...  Off  | 00000000:00:04.0 Off |                    0 |
# | N/A   30C    P0    50W / 400W |      0MiB / 81920MiB |      0%      Default |
# ...

# Check CUDA
nvcc --version
```

---

## 🐳 Docker GPU Support

### 1. Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
```

### 2. Install NVIDIA Container Toolkit

```bash
# Add NVIDIA Container Toolkit repository
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# Install NVIDIA Container Toolkit
sudo apt update
sudo apt install -y nvidia-container-toolkit

# Configure Docker daemon
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### 3. Verify GPU Access in Docker

```bash
# Test GPU access
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi

# Should show all 4 GPUs
```

### 4. Install Docker Compose V2

```bash
# Install Docker Compose plugin
sudo apt update
sudo apt install -y docker-compose-plugin

# Verify installation
docker compose version
```

---

## ⚙️ Application Configuration

### 1. Clone Repository

```bash
# Clone the repository
git clone https://github.com/wongivan852/legal-ai-vault.git
cd legal-ai-vault
```

### 2. Configure Environment

```bash
# Copy production environment template
cp .env.production .env

# Generate secure secrets
JWT_SECRET=$(openssl rand -hex 32)
ENCRYPTION_KEY=$(openssl rand -hex 32)
DB_PASSWORD=$(openssl rand -base64 32)

# Edit .env file
nano .env
```

**Required .env settings:**

```bash
# Database
DB_USER=legal_vault_user
DB_PASSWORD=<generated_password>

# Security
JWT_SECRET=<generated_secret>
ENCRYPTION_KEY=<generated_key>

# Ollama (GPU-optimized)
OLLAMA_MODEL=llama3.3:70b
OLLAMA_MODELS_PATH=ollama_models  # or /path/to/existing/models

# GPU
GPU_COUNT=all  # Use all 4 GPUs

# CORS (update with your domain)
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Performance
API_WORKERS=4
MAX_CONCURRENT_REQUESTS=100
```

### 3. Pull Ollama Models

**Important:** Download models before deployment to avoid long startup times.

```bash
# Start Ollama service temporarily
docker compose up -d ollama

# Wait for Ollama to be ready
sleep 10

# Pull llama3.3:70b (this will take time - ~40GB download)
docker compose exec ollama ollama pull llama3.3:70b

# Pull embedding model
docker compose exec ollama ollama pull nomic-embed-text:latest

# Verify models
docker compose exec ollama ollama list

# Expected output:
# NAME                    ID              SIZE      MODIFIED
# llama3.3:70b            [id]            40 GB     X minutes ago
# nomic-embed-text:latest [id]            274 MB    X minutes ago

# Stop Ollama
docker compose down
```

---

## 🚀 Deployment Steps

### Option 1: Development Deployment (No SSL)

```bash
# Build and start all services
docker compose up -d

# Check logs
docker compose logs -f

# Wait for services to be ready (2-3 minutes)
# First model load may take 60-120 seconds

# Verify deployment
./verify_deployment.sh

# Access the application
# UI: http://your-server-ip:8000
# API Docs: http://your-server-ip:8000/docs
```

### Option 2: Production Deployment (With SSL)

```bash
# Set up SSL certificates (see nginx/ssl/README.md)
# Option A: Let's Encrypt (recommended)
sudo certbot certonly --standalone -d yourdomain.com

# Option B: Self-signed (testing only)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem

# Update nginx.conf with your domain and SSL paths
nano nginx/nginx.conf

# Update docker-compose.yml to mount SSL certificates
# (if using Let's Encrypt, add volume mount)

# Start with production profile
docker compose --profile production up -d

# Verify
curl https://yourdomain.com/health

# Access the application
# UI: https://yourdomain.com
# API Docs: https://yourdomain.com/docs
```

### Deployment Checklist

- [ ] NVIDIA drivers installed (535+)
- [ ] Docker GPU support verified
- [ ] `.env` file configured with secure values
- [ ] Ollama models downloaded (llama3.3:70b, nomic-embed-text)
- [ ] Firewall configured (UFW)
- [ ] SSL certificates configured (production)
- [ ] DNS pointed to server (production)
- [ ] Health checks passing
- [ ] GPU utilization confirmed

---

## 🎯 Performance Optimization

### GPU Optimization

#### 1. Verify GPU Utilization

```bash
# Monitor GPU usage
watch -n 1 nvidia-smi

# Monitor in detail
nvtop

# Check GPU usage in Ollama container
docker compose exec ollama nvidia-smi
```

#### 2. Ollama GPU Configuration

Create `ollama-config.json` (optional):

```json
{
  "num_gpu": 4,
  "gpu_layers": -1,
  "main_gpu": 0,
  "tensor_split": [1.0, 1.0, 1.0, 1.0]
}
```

#### 3. Model-Specific Optimizations

For **llama3.3:70b** with 4 GPUs:

```bash
# Set environment variables in docker-compose.yml
environment:
  - OLLAMA_NUM_GPU=4
  - OLLAMA_GPU_LAYERS=-1  # Use all layers on GPU
  - OLLAMA_NUM_THREAD=32  # Adjust to CPU core count
```

### Database Optimization

```bash
# Tune PostgreSQL for your RAM
# Edit .env:
POSTGRES_SHARED_BUFFERS=4GB       # 25% of RAM
POSTGRES_EFFECTIVE_CACHE_SIZE=12GB  # 75% of RAM
POSTGRES_MAX_CONNECTIONS=200
```

### API Performance

```bash
# Increase API workers for multi-core systems
# Edit .env:
API_WORKERS=8  # Match CPU core count
MAX_CONCURRENT_REQUESTS=100  # Adjust based on GPU memory

# Enable connection pooling
POOL_SIZE=20
MAX_OVERFLOW=40
```

---

## 📊 Monitoring & Maintenance

### System Monitoring

```bash
# Monitor GPU usage
nvidia-smi dmon -s pucvmet

# Monitor Docker stats
docker stats

# Monitor logs
docker compose logs -f --tail=100 api

# Check disk usage
df -h
du -sh /var/lib/docker/volumes/*
```

### Performance Metrics

```bash
# Test API response time
time curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain contract law", "max_tokens": 100}'

# Expected response times (llama3.3:70b, 4x A100):
# - First request: 10-30 seconds (model loading)
# - Subsequent: 5-15 seconds (depending on complexity)
```

### Health Checks

```bash
# Automated health check script
cat > health_check.sh << 'EOF'
#!/bin/bash
echo "=== Vault AI Platform Health Check ==="
echo -n "API: "
curl -sf http://localhost:8000/health > /dev/null && echo "✓" || echo "✗"
echo -n "Ollama: "
curl -sf http://localhost:11434/api/tags > /dev/null && echo "✓" || echo "✗"
echo -n "Qdrant: "
curl -sf http://localhost:6333/health > /dev/null && echo "✓" || echo "✗"
echo -n "PostgreSQL: "
docker compose exec -T postgres pg_isready -U legal_vault_user > /dev/null && echo "✓" || echo "✗"
echo -n "GPUs: "
nvidia-smi > /dev/null && echo "✓ ($(nvidia-smi --query-gpu=count --format=csv,noheader))" || echo "✗"
EOF

chmod +x health_check.sh
./health_check.sh

# Add to cron for automated checks
crontab -e
# */5 * * * * /path/to/health_check.sh >> /var/log/vault-ai-health.log
```

### Backup Strategy

```bash
# Database backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=/mnt/backup/vault-ai
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker compose exec -T postgres pg_dump -U legal_vault_user legal_ai_vault | \
  gzip > $BACKUP_DIR/postgres_$DATE.sql.gz

# Backup Qdrant
docker compose exec -T qdrant tar czf - /qdrant/storage > \
  $BACKUP_DIR/qdrant_$DATE.tar.gz

# Backup environment config
cp .env $BACKUP_DIR/env_$DATE

# Keep last 30 days
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
EOF

chmod +x backup.sh

# Schedule daily backups
crontab -e
# 0 2 * * * /path/to/backup.sh >> /var/log/vault-ai-backup.log
```

---

## 🔍 Troubleshooting

### GPU Not Detected

**Problem:** `nvidia-smi` shows no GPUs or driver errors

**Solutions:**
```bash
# Reinstall NVIDIA drivers
sudo apt purge nvidia-*
sudo apt autoremove
sudo apt install nvidia-driver-535

# Reboot
sudo reboot

# Verify
nvidia-smi
```

### Docker Container Cannot Access GPU

**Problem:** Container starts but no GPU access

**Solutions:**
```bash
# Verify NVIDIA Container Toolkit
nvidia-ctk --version

# Reconfigure Docker runtime
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Test GPU access
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

### Ollama Model Loading Slow

**Problem:** First query takes 2+ minutes

**Solutions:**
```bash
# Pre-load model at startup
docker compose exec ollama ollama run llama3.3:70b "test" &

# Increase GPU memory allocation
# Edit docker-compose.yml:
environment:
  - OLLAMA_GPU_MEMORY_FRACTION=0.95
```

### Out of Memory Errors

**Problem:** GPU OOM or system RAM exhausted

**Solutions:**
```bash
# Check GPU memory
nvidia-smi

# Reduce concurrent requests
# Edit .env:
MAX_CONCURRENT_REQUESTS=50  # Reduce from 100

# Use smaller model for testing
OLLAMA_MODEL=llama3.1:8b

# Increase system swap (temporary)
sudo fallocate -l 32G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Slow API Response

**Problem:** Queries take longer than expected

**Solutions:**
```bash
# Check GPU utilization
nvidia-smi

# Verify all GPUs are being used
docker compose exec ollama nvidia-smi

# Increase API workers
# Edit .env:
API_WORKERS=8

# Check network latency
ping your-server-ip

# Check database connections
docker compose exec postgres psql -U legal_vault_user -c "SELECT count(*) FROM pg_stat_activity;"
```

### Container Crashes

**Problem:** API or Ollama container keeps restarting

**Solutions:**
```bash
# Check logs
docker compose logs api --tail=100
docker compose logs ollama --tail=100

# Check resource usage
docker stats

# Increase container memory limit
# Edit docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 16G

# Check disk space
df -h
```

---

## 📈 Performance Benchmarks

### Expected Performance (4x NVIDIA A100 80GB)

| Metric | Value |
|--------|-------|
| First Query (Cold Start) | 10-30s |
| Subsequent Queries | 5-15s |
| Concurrent Users | 100+ |
| Tokens/Second | 40-60 |
| GPU Utilization | 80-95% |
| RAM Usage | 40-60GB |

### Expected Performance (4x NVIDIA RTX 4090)

| Metric | Value |
|--------|-------|
| First Query (Cold Start) | 20-40s |
| Subsequent Queries | 10-20s |
| Concurrent Users | 30-50 |
| Tokens/Second | 20-30 |
| GPU Utilization | 85-100% |
| RAM Usage | 30-50GB |

---

## 🎓 Production Best Practices

1. **Security**
   - Use strong passwords and secrets
   - Enable SSL/TLS
   - Configure firewall properly
   - Regular security updates
   - Implement rate limiting

2. **Monitoring**
   - Set up Prometheus + Grafana
   - Enable alert notifications
   - Monitor GPU temperature and utilization
   - Track API response times
   - Monitor disk space

3. **Backup**
   - Daily automated backups
   - Offsite backup storage
   - Test restoration regularly
   - Document recovery procedures

4. **Scaling**
   - Use load balancer for multiple API instances
   - Implement caching (Redis)
   - Database read replicas
   - CDN for static content

5. **Maintenance**
   - Regular log rotation
   - Monthly security patches
   - Quarterly model updates
   - Annual hardware review

---

## 📞 Support & Resources

- **Documentation:** `/home/user/legal-ai-vault/README.md`
- **NVIDIA Docs:** https://docs.nvidia.com/datacenter/cloud-native/
- **Docker GPU Support:** https://docs.docker.com/config/containers/resource_constraints/#gpu
- **Ollama Documentation:** https://github.com/ollama/ollama

---

**Last Updated:** 2025-11-20
**Version:** 2.0.0 (GPU-Optimized)
