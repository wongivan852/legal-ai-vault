# 🚀 Vault AI Platform - Ready to Deploy

**Status:** ✅ All configurations ready for deployment
**Branch:** `claude/validate-app-check-discrepancies-01M3A5WFqBJLcGed3bcNaKk5`

---

## 📦 What's Included

This repository now contains TWO complete deployment configurations:

### 1️⃣ Production (GPU Server) - `docker-compose.yml`
- ✅ 4x NVIDIA GPU support enabled
- ✅ llama3.3:70b model (70B parameters)
- ✅ Production security (no default passwords)
- ✅ Nginx reverse proxy with SSL/TLS
- ✅ Performance optimizations
- ✅ Complete monitoring setup

### 2️⃣ Development (Local) - `docker-compose.dev.yml`
- ✅ No GPU required (CPU-only)
- ✅ llama3.1:8b model (8B parameters)
- ✅ Development defaults included
- ✅ Auto-configured environment
- ✅ Quick startup script

---

## 🎯 Quick Start

### Option A: Development Mode (Easiest)

Perfect for testing on your laptop/desktop:

```bash
# 1. Clone repository
git clone https://github.com/wongivan852/legal-ai-vault.git
cd legal-ai-vault
git checkout claude/validate-app-check-discrepancies-01M3A5WFqBJLcGed3bcNaKk5

# 2. Run startup script
./start-dev.sh

# 3. Pull models (first time only, ~4GB download)
docker compose -f docker-compose.dev.yml exec ollama ollama pull llama3.1:8b
docker compose -f docker-compose.dev.yml exec ollama ollama pull nomic-embed-text

# 4. Access the app
# Web UI: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**Requirements:**
- Docker Desktop installed and running
- 8GB RAM minimum
- 10GB disk space for models

---

### Option B: Production Mode (GPU Server)

For your Linux server with 4 NVIDIA GPUs:

```bash
# 1. Clone repository on GPU server
git clone https://github.com/wongivan852/legal-ai-vault.git
cd legal-ai-vault
git checkout claude/validate-app-check-discrepancies-01M3A5WFqBJLcGed3bcNaKk5

# 2. Install prerequisites (if not already done)
# See GPU_SERVER_DEPLOYMENT.md for complete guide

# 3. Configure environment
cp .env.production .env

# Generate secure secrets
JWT_SECRET=$(openssl rand -hex 32)
ENCRYPTION_KEY=$(openssl rand -hex 32)
DB_PASSWORD=$(openssl rand -base64 32)

# Edit .env and paste the generated values
nano .env

# 4. Pull models (one-time, ~40GB download)
docker compose up -d ollama
sleep 10
docker compose exec ollama ollama pull llama3.3:70b
docker compose exec ollama ollama pull nomic-embed-text
docker compose down

# 5. Deploy
docker compose up -d

# 6. Verify
docker compose ps
nvidia-smi  # Check GPU utilization

# 7. Access the app
# Web UI: http://your-server-ip:8000
# API Docs: http://your-server-ip:8000/docs
```

**Requirements:**
- Ubuntu 22.04 or 24.04 LTS
- 4x NVIDIA GPUs (24GB+ VRAM each)
- NVIDIA drivers 525+
- Docker with NVIDIA Container Toolkit
- 64-128GB RAM
- 500GB+ storage

---

## 📁 File Structure

```
legal-ai-vault/
├── docker-compose.yml          # Production (GPU) configuration
├── docker-compose.dev.yml      # Development (CPU) configuration
├── .env.production             # Production environment template
├── .env.development            # Development environment defaults
├── start-dev.sh                # Development startup script
│
├── GPU_SERVER_DEPLOYMENT.md    # Complete GPU deployment guide (600+ lines)
├── GPU_REVAMP_SUMMARY.md       # Summary of all GPU optimizations
├── VALIDATION_DISCREPANCIES_REPORT.md  # Validation report
│
├── nginx/
│   ├── nginx.conf              # Production reverse proxy config
│   └── ssl/
│       └── README.md           # SSL certificate setup guide
│
├── api/                        # FastAPI application
│   ├── main.py                 # Entry point (CORS fixed)
│   ├── requirements.txt        # Python dependencies
│   ├── agents/                 # AI agents
│   ├── services/               # Business logic
│   └── ...
│
└── frontend/                   # Web UI
    ├── index.html
    └── static/
```

---

## 🔑 Environment Variables

### Required (Production)
These MUST be set in `.env`:

```bash
# Database
DB_USER=legal_vault_user
DB_PASSWORD=<generate with: openssl rand -base64 32>

# Security
JWT_SECRET=<generate with: openssl rand -hex 32>
ENCRYPTION_KEY=<generate with: openssl rand -hex 32>

# CORS (update with your domain)
ALLOWED_ORIGINS=https://yourdomain.com
```

### Optional (With Sensible Defaults)

```bash
# Model Selection
OLLAMA_MODEL=llama3.3:70b  # or llama3.1:8b for development
GPU_COUNT=all              # or 1, 2, 3, 4

# Performance
API_WORKERS=4
MAX_CONCURRENT_REQUESTS=100
POSTGRES_SHARED_BUFFERS=2GB

# Ports
API_PORT=8000
POSTGRES_PORT=5432
QDRANT_HTTP_PORT=6333
```

---

## 🧪 Testing After Deployment

```bash
# Check all services are running
docker compose ps

# Check API health
curl http://localhost:8000/health

# List available agents
curl http://localhost:8000/api/agents/

# Test text generation
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain contract law", "max_tokens": 200}'

# Check GPU utilization (production only)
docker compose exec ollama nvidia-smi
```

---

## 📊 Expected Performance

### Development (CPU-only, llama3.1:8b)
- First query: 30-60 seconds
- Subsequent: 15-30 seconds
- Concurrent users: 5-10
- Good for: Testing, development, demos

### Production (4x A100 GPUs, llama3.3:70b)
- First query: 10-30 seconds
- Subsequent: 5-15 seconds
- Concurrent users: 100+
- Tokens/second: 40-60
- Good for: Production, high-traffic deployments

### Production (4x RTX 4090 GPUs, llama3.3:70b)
- First query: 20-40 seconds
- Subsequent: 10-20 seconds
- Concurrent users: 30-50
- Tokens/second: 20-30
- Good for: Production, medium-traffic deployments

---

## 🔧 Management Commands

### Development Mode

```bash
# Start
./start-dev.sh

# View logs
docker compose -f docker-compose.dev.yml logs -f

# Stop
docker compose -f docker-compose.dev.yml down

# Restart a service
docker compose -f docker-compose.dev.yml restart api

# Shell into container
docker compose -f docker-compose.dev.yml exec api bash
```

### Production Mode

```bash
# Start
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down

# Restart a service
docker compose restart api

# With nginx (production profile)
docker compose --profile production up -d
docker compose --profile production down
```

---

## 📚 Documentation Reference

| Document | Purpose |
|----------|---------|
| `README.md` | Main project documentation |
| `GPU_SERVER_DEPLOYMENT.md` | **Complete GPU deployment guide** (START HERE for production) |
| `GPU_REVAMP_SUMMARY.md` | Summary of GPU optimizations |
| `VALIDATION_DISCREPANCIES_REPORT.md` | Issues found and resolved |
| `PLATFORM_DOCUMENTATION.md` | API reference and agent catalog |
| `QUICK_START_GUIDE.md` | 5-minute quick start |
| `.env.production` | Production configuration template |
| `.env.development` | Development configuration |
| `nginx/ssl/README.md` | SSL certificate setup |

---

## ⚠️ Important Notes

### Security
- ✅ **Never commit `.env` to git** (it's in `.gitignore`)
- ✅ `.env.production` is a **template only** (no real secrets)
- ✅ Generate unique secrets for each deployment
- ✅ Use strong passwords (32+ characters)
- ✅ Configure `ALLOWED_ORIGINS` for production

### GPU Deployment
- ✅ Read `GPU_SERVER_DEPLOYMENT.md` completely before deploying
- ✅ Install NVIDIA drivers **before** starting containers
- ✅ Test GPU access: `docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi`
- ✅ Monitor GPU usage during operation

### Model Downloads
- 📥 llama3.1:8b: ~4.7GB (development)
- 📥 llama3.3:70b: ~40GB (production)
- 📥 nomic-embed-text: ~274MB (both)
- ⏱️ First download will take time based on internet speed
- 💾 Models are cached in Docker volumes

---

## 🆘 Troubleshooting

### Docker won't start
```bash
# Check Docker is installed
docker --version

# Check Docker daemon is running
docker ps

# On macOS: Open Docker Desktop
# On Linux: sudo systemctl start docker
```

### GPU not detected
```bash
# Check NVIDIA drivers
nvidia-smi

# Check Docker GPU support
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi

# If fails, install NVIDIA Container Toolkit
# See GPU_SERVER_DEPLOYMENT.md Section 4
```

### Models not loading
```bash
# Pull models manually
docker compose exec ollama ollama pull llama3.1:8b

# Check Ollama logs
docker compose logs ollama

# Verify models are downloaded
docker compose exec ollama ollama list
```

### Port already in use
```bash
# Find what's using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Change port in .env
echo "API_PORT=8080" >> .env
docker compose up -d
```

---

## ✅ Deployment Checklist

### Development
- [ ] Docker Desktop installed and running
- [ ] Repository cloned
- [ ] Run `./start-dev.sh`
- [ ] Models downloaded (llama3.1:8b)
- [ ] Access http://localhost:8000
- [ ] Test API endpoints

### Production (GPU Server)
- [ ] Ubuntu 22.04/24.04 installed
- [ ] NVIDIA drivers installed (525+)
- [ ] Docker with NVIDIA Container Toolkit
- [ ] Repository cloned
- [ ] `.env` configured with secure values
- [ ] Firewall configured (ports 80, 443, 8000)
- [ ] SSL certificates generated (Let's Encrypt)
- [ ] Models downloaded (llama3.3:70b)
- [ ] GPU access verified (`nvidia-smi`)
- [ ] Services started (`docker compose up -d`)
- [ ] Health checks passing
- [ ] Monitoring set up

---

## 🎉 You're Ready to Deploy!

Choose your deployment mode:
- 💻 **Development:** Run `./start-dev.sh` on your local machine
- 🚀 **Production:** Follow `GPU_SERVER_DEPLOYMENT.md` for GPU server

**Need Help?**
- Review documentation in the repository
- Check troubleshooting sections
- Verify all prerequisites are met

---

**Version:** 2.0.0 GPU-Optimized
**Last Updated:** 2025-11-20
**Branch:** claude/validate-app-check-discrepancies-01M3A5WFqBJLcGed3bcNaKk5
