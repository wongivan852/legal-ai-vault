# Legal AI Vault Setup Guide

## ✅ Quick Start (Using Your Existing 70B Model)

This setup uses your **existing llama3.3:70b model** from `~/.ollama/` - no downloads needed!

### 1. Prerequisites

Ensure you have installed:
- Docker Desktop for Mac
- Docker Compose

### 2. Configure Environment

```bash
cd ~/Apps/legal-ai-vault

# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
nano .env
```

**Generate secure keys:**
```bash
# JWT Secret
openssl rand -hex 32

# Encryption Key
openssl rand -hex 32
```

### 3. Start Services

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Verify Setup

**Check Ollama is using your models:**
```bash
# List available models
curl http://localhost:11434/api/tags

# Should show llama3.3:70b and nomic-embed-text
```

**Check API health:**
```bash
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "ollama": {...}, "database": "connected"}
```

### 5. Initialize Database

```bash
# Run database migrations
docker-compose exec api python -c "from database import init_db; init_db()"

# Optional: Import HK legal data
docker-compose exec api python /app/scripts/ingest_hk_legal_data.py /path/to/hkel_data --init-db
```

### 6. Access Services

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Ollama**: http://localhost:11434
- **Qdrant**: http://localhost:6333/dashboard

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│  Your Mac                                │
│  ~/.ollama/models/ (60GB)                │
│  ├── llama3.3:70b (42GB)                 │
│  └── nomic-embed-text (274MB)            │
└──────────┬──────────────────────────────┘
           │ (mounted read-only)
           ▼
┌─────────────────────────────────────────┐
│  Docker Containers                       │
│                                          │
│  ┌──────────────┐  ┌─────────────────┐  │
│  │ Ollama       │  │ FastAPI API     │  │
│  │ Port: 11434  │←─│ Port: 8000      │  │
│  │ (70B model)  │  │ (Legal AI)      │  │
│  └──────────────┘  └────────┬────────┘  │
│                              │           │
│  ┌──────────────┐  ┌────────▼────────┐  │
│  │ PostgreSQL   │  │ Qdrant Vector   │  │
│  │ Port: 5432   │  │ Port: 6333      │  │
│  │ (Metadata)   │  │ (Embeddings)    │  │
│  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────┘
```

## 🔧 Troubleshooting

### Ollama can't find models

```bash
# Check if volume is mounted correctly
docker-compose exec ollama ls -la /root/.ollama/models

# Should show your model files
```

### Out of memory error

The 70B model needs ~48GB RAM. Adjust Docker Desktop settings:
- **Preferences → Resources → Memory**: Increase to 64GB+

### Database connection error

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# View logs
docker-compose logs postgres

# Restart if needed
docker-compose restart postgres
```

### API startup fails

```bash
# Check logs
docker-compose logs api

# Common issues:
# - Database not ready → wait 30 seconds and restart
# - Missing dependencies → rebuild: docker-compose build api
```

## 🎯 Testing the 70B Model

```bash
# Test text generation
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain contract law in Hong Kong",
    "max_tokens": 500
  }'

# Test embeddings
curl -X POST http://localhost:8000/api/embed \
  -H "Content-Type: application/json" \
  -d '{
    "text": "What are my employment rights?"
  }'
```

## 📝 Development

### Rebuild after code changes

```bash
# Rebuild API container
docker-compose build api

# Restart with new code
docker-compose up -d --force-recreate api
```

### Access database

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U legal_vault_user -d legal_ai_vault

# Common queries
SELECT COUNT(*) FROM hk_legal_documents;
SELECT doc_number, doc_name FROM hk_legal_documents LIMIT 10;
```

### View Qdrant vectors

Open http://localhost:6333/dashboard

## 🛑 Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

## 📚 Next Steps

1. **Import Legal Data**: Run HK legal data ingestion (see HK_LEGAL_DATA_INTEGRATION.md)
2. **Create Admin User**: Set up first administrator account
3. **Configure Security**: Update JWT secrets and encryption keys
4. **Test Endpoints**: Try the API documentation at `/docs`

## 💡 Performance Tips

- **GPU Acceleration**: If you have NVIDIA GPU, uncomment the GPU sections in docker-compose.yml
- **Model Caching**: First request is slow (~30s), subsequent requests are faster
- **Database Indexing**: Run indexing after importing data for faster searches
- **Vector Optimization**: Tune Qdrant settings for your dataset size

## 🔗 Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [HK e-Legislation](https://www.elegislation.gov.hk)
