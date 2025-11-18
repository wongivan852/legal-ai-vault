# 🚀 Quick Start Guide

## Your Legal AI Vault is Ready!

This setup uses your **existing llama3.3:70b model (42GB)** from `~/.ollama/` - **no downloads needed!**

## 📍 Location

Your app is now in a **clean, dedicated folder**:
```
~/Apps/legal-ai-vault/
```

## ⚡ Start in 3 Steps

### Step 1: Configure Environment

```bash
cd ~/Apps/legal-ai-vault

# Copy environment template
cp .env.example .env

# Generate secure keys
echo "JWT_SECRET=$(openssl rand -hex 32)" >> .env
echo "ENCRYPTION_KEY=$(openssl rand -hex 32)" >> .env

# Edit database password
nano .env  # Change DB_PASSWORD from default
```

### Step 2: Start Services

```bash
# One command to start everything
./start.sh
```

**Or manually:**
```bash
docker-compose up -d
```

### Step 3: Test It!

```bash
# Check health
curl http://localhost:8000/health

# Test your 70B model
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain Hong Kong contract law in 3 sentences", "max_tokens": 200}'

# View API docs
open http://localhost:8000/docs
```

## 🎯 What's Running

| Service | Purpose | URL |
|---------|---------|-----|
| **Ollama** | Your llama3.3:70b model | http://localhost:11434 |
| **FastAPI** | Legal AI API | http://localhost:8000 |
| **PostgreSQL** | Document metadata | localhost:5432 |
| **Qdrant** | Vector embeddings | http://localhost:6333 |

## 💾 Your Models (No Copying!)

```
~/.ollama/models/  (60GB)
├── llama3.3:70b ────────► mounted read-only to Docker
├── nomic-embed-text ────► mounted read-only to Docker
└── [other models]
```

✅ **Mounted as read-only volume** - Docker uses your existing models without copying!

## 📊 Architecture

```
Your Mac                     Docker Containers
┌─────────────────┐         ┌──────────────────────┐
│ ~/.ollama/      │         │                      │
│ models/         ├────────►│ Ollama Container     │
│ (60GB, R/O)     │         │ llama3.3:70b         │
└─────────────────┘         │ Port: 11434          │
                            └──────┬───────────────┘
                                   │
                            ┌──────▼───────────────┐
                            │ FastAPI API          │
                            │ Port: 8000           │
                            └──────┬───────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
            ┌───────▼──────┐ ┌────▼─────┐  ┌─────▼──────┐
            │ PostgreSQL   │ │ Qdrant   │  │ Your Data  │
            │ Port: 5432   │ │ Port:6333│  │ ~/Docs     │
            └──────────────┘ └──────────┘  └────────────┘
```

## 🧪 Test Examples

### 1. Legal Question
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What are the key elements of a valid contract in Hong Kong?",
    "system_prompt": "You are a Hong Kong legal expert. Be concise and accurate.",
    "max_tokens": 500,
    "temperature": 0.3
  }'
```

### 2. Generate Embeddings
```bash
curl -X POST http://localhost:8000/api/embed \
  -H "Content-Type: application/json" \
  -d '{"text": "employment contract termination notice period"}'
```

### 3. List Available Models
```bash
curl http://localhost:8000/api/models
```

## 🔧 Common Commands

```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f ollama
docker-compose logs -f api

# Restart a service
docker-compose restart api

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# Rebuild after code changes
docker-compose build api
docker-compose up -d --force-recreate api
```

## 📈 Monitoring

```bash
# Check service status
docker-compose ps

# Resource usage
docker stats

# Ollama model info
curl http://localhost:11434/api/tags

# API health with details
curl http://localhost:8000/health | jq
```

## ⚙️ Configuration

All settings in `.env` file:

```env
# Your llama3.3:70b model
OLLAMA_MODEL=llama3.3:70b

# Embedding model
OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest

# Database
DB_USER=legal_vault_user
DB_PASSWORD=your_secure_password

# Security
JWT_SECRET=generated_32_char_hex
ENCRYPTION_KEY=generated_32_char_hex
```

## 🛠️ Troubleshooting

### Ollama not finding models

```bash
# Verify mount
docker-compose exec ollama ls -la /root/.ollama/models/

# Should show your model files
# If empty, check docker-compose.yml volume mount
```

### API slow to start

First request to 70B model takes ~30-60s to load into memory. Subsequent requests are much faster.

### Out of memory

The 70B model needs ~48GB RAM. Configure Docker Desktop:
- **Settings → Resources → Memory**: Set to 64GB+

### Port already in use

```bash
# Check what's using the port
lsof -i :8000
lsof -i :11434

# Stop conflicting service or change port in docker-compose.yml
```

## 📚 Next Steps

1. **Import HK Legal Data**: See `HK_LEGAL_DATA_INTEGRATION.md`
2. **API Documentation**: http://localhost:8000/docs
3. **Full Setup Guide**: See `SETUP.md`
4. **Development**: See `README.md`

## 💡 Pro Tips

- **First load is slow**: 70B model loads into RAM (~30-60s)
- **Keep it running**: Leave Ollama container running for fast responses
- **Model persistence**: Your models stay in `~/.ollama/` - not copied to Docker
- **Clean builds**: `.dockerignore` prevents large files in build context

## 🎉 Success!

Your Legal AI Vault is running with your local 70B model!

Try it: http://localhost:8000/docs

Questions? Check `SETUP.md` for detailed instructions.
