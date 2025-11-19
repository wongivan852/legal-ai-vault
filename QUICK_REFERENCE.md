# Vault AI Platform - Quick Reference Card

**Version 2.0.0** | [Full Manual](USER_MANUAL.md) | [Test Samples](QUICK_TEST_SAMPLES.md)

---

## 🚀 Quick Start (30 seconds)

```bash
# 1. Start platform
docker-compose up -d

# 2. Check health
curl -s http://localhost:8000/api/agents/health | python3 -m json.tool

# 3. Test legal search
curl -X POST http://localhost:8000/api/rag \
  -H "Content-Type: application/json" \
  -d '{"question": "Building Management Ordinance", "top_k": 3}' \
  | python3 -m json.tool
```

---

## 📊 6 AI Agents

| Agent | Purpose | Endpoint |
|-------|---------|----------|
| 🏛️ **Legal Research** | Search 1,699 HK ordinances | `/api/agents/legal_research/execute` |
| 👔 **HR Policy** | Employee policies & benefits | `/api/agents/hr_policy/execute` |
| 💬 **Customer Service** | Support documentation | `/api/agents/cs_document/execute` |
| 📊 **Analysis** | Extract insights | `/api/agents/analysis/execute` |
| 🔄 **Synthesis** | Combine multi-source info | `/api/agents/synthesis/execute` |
| ✓ **Validation** | Check consistency | `/api/agents/validation/execute` |

---

## 🎯 Common Tasks

### Legal Search
```bash
curl -X POST http://localhost:8000/api/agents/legal_research/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "search",
      "question": "YOUR LEGAL QUESTION HERE"
    }
  }'
```

### RAG Search (Fastest)
```bash
curl -X POST http://localhost:8000/api/rag \
  -H "Content-Type: application/json" \
  -d '{
    "question": "YOUR QUESTION",
    "top_k": 5,
    "search_type": "sections"
  }'
```

### HR Policy Query
```bash
curl -X POST http://localhost:8000/api/agents/hr_policy/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "question": "YOUR HR QUESTION",
      "context": "POLICY CONTENT HERE"
    }
  }'
```

---

## 🔗 Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/agents/health` | GET | Check status |
| `/api/agents` | GET | List agents |
| `/api/agents/{name}/execute` | POST | Execute agent |
| `/api/rag` | POST | RAG search |
| `/api/agents/workflows` | GET | List workflows |
| `/api/agents/workflows/{name}/execute` | POST | Run workflow |
| `/docs` | GET | API documentation |

---

## 🔍 Search Types

| Type | Use Case | Response Time | Precision |
|------|----------|---------------|-----------|
| **RAG Documents** | Broad search | 10-30s | Medium |
| **RAG Sections** | Precise search | 10-30s | High |
| **Agent** | Complex analysis | 20-45s | Highest |

---

## ⚡ Performance Tips

✅ **Do:**
- Use RAG for simple searches (faster)
- Specify `search_type: "sections"` for precision
- Set `top_k: 3-5` for most queries
- Wait for first query (cold start), then fast

❌ **Don't:**
- Send >10 concurrent requests
- Use vague queries ("tell me about laws")
- Expect instant first response (60s cold start is normal)

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| Timeout | Wait for cold start (60s), retry |
| Empty result | Rephrase query, check data loaded |
| Agent not ready | Wait 10s, retry |
| 503 error | `docker-compose restart api` |
| Slow response | First query is slow (cold start) |

---

## 📦 Platform Status

```bash
# Health check
curl -s http://localhost:8000/api/agents/health | python3 -m json.tool

# Database counts
docker-compose exec -T postgres psql -U legal_vault_user -d legal_ai_vault -c \
  "SELECT 'Docs' as type, COUNT(*) FROM hk_legal_documents
   UNION ALL
   SELECT 'Sections', COUNT(*) FROM hk_legal_sections;"

# Vector database
curl -s http://localhost:6333/collections/hk_legal_documents | \
  python3 -c "import sys,json; print(f\"Points: {json.load(sys.stdin)['result']['points_count']}\")"
```

**Expected**: 1,699 documents, 11,288 sections

---

## 🔄 5 Workflows

| Workflow | Use Case |
|----------|----------|
| `hr_onboarding` | Employee onboarding |
| `cs_ticket_response` | Support tickets |
| `legal_hr_compliance` | Legal compliance check |
| `simple_qa` | Quick Q&A |
| `multi_agent_research` | Comprehensive research |

**Execute Workflow:**
```bash
curl -X POST http://localhost:8000/api/agents/workflows/WORKFLOW_NAME/execute \
  -H "Content-Type: application/json" \
  -d '{"input_data": {...}}'
```

---

## 📡 Services & Ports

| Service | Port | URL |
|---------|------|-----|
| API | 8000 | http://localhost:8000 |
| Frontend | 3000 | http://localhost:3000 |
| Qdrant | 6333 | http://localhost:6333/dashboard |
| PostgreSQL | 5432 | localhost:5432 |
| Ollama | 11434 | http://localhost:11434 |

---

## 💾 Data Sources

| Dataset | Count | Agent |
|---------|-------|-------|
| HK Ordinances | 1,699 docs | Legal Research |
| HK Sections | 11,288 sections | Legal Research |
| Vector Embeddings | 12,987 (768-dim) | All agents |

---

## 🐳 Docker Commands

```bash
# Start platform
docker-compose up -d

# Stop platform
docker-compose down

# View logs
docker-compose logs -f api

# Restart service
docker-compose restart api

# Check status
docker-compose ps

# Resource usage
docker stats --no-stream
```

---

## 🔧 Maintenance

```bash
# Restart Ollama (if slow)
docker restart legal-ai-ollama

# Restart API
docker-compose restart api

# Restart all
docker-compose restart

# Check disk space
docker system df

# Clean up (careful!)
docker system prune
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [USER_MANUAL.md](USER_MANUAL.md) | Complete user manual |
| [QUICK_TEST_SAMPLES.md](QUICK_TEST_SAMPLES.md) | Ready-to-use test commands |
| [DATASET_REQUIREMENTS.md](DATASET_REQUIREMENTS.md) | Dataset info & creation |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | This document |
| http://localhost:8000/docs | Interactive API docs |

---

## ⚙️ Configuration

**Environment Variables** (`.env`):
```bash
DATABASE_URL=postgresql://...
QDRANT_HOST=qdrant
QDRANT_PORT=6333
OLLAMA_HOST=http://ollama:11434
EMBEDDING_MODEL=nomic-embed-text
LLM_MODEL=llama3.1:8b
```

---

## 🎓 Example Queries

**Legal:**
- "What are the insurance requirements under Building Management Ordinance?"
- "Director duties under Companies Ordinance"
- "Employment contract requirements in Hong Kong"

**HR:**
- "How many vacation days after 3 years?"
- "What health benefits are provided?"
- "Parental leave policy"

**Customer Service:**
- "How do I reset my password?"
- "How to create an account?"
- "Troubleshooting login issues"

---

## 📊 Response Format

```json
{
  "agent": "agent_name",
  "status": "success|failed",
  "result": {
    "answer": "Generated response...",
    "sources": [
      {
        "doc_number": "Cap. 344",
        "title": "Building Management Ordinance",
        "content": "...",
        "score": 0.89
      }
    ],
    "execution_time": 23.5
  },
  "execution_time": 23.5
}
```

---

## 🚨 Important Notes

⚠️ **First Query**: Takes 60-120s (cold start). Subsequent: 10-30s
⚠️ **Not Legal Advice**: AI-generated responses, verify important info
⚠️ **Rate Limit**: Max 5-10 concurrent requests recommended
⚠️ **Memory**: Requires 8GB+ RAM (16GB recommended)

---

## 🔐 Security

✅ **Default Setup**: localhost only
✅ **Production**: Configure firewall, reverse proxy, authentication
✅ **API Keys**: Add authentication layer for production
✅ **HTTPS**: Use SSL/TLS in production

---

## 🆘 Quick Help

```bash
# Platform not responding
docker-compose restart

# Agent errors
docker-compose logs api | tail -100

# Database issues
docker-compose restart postgres

# Slow queries
docker restart legal-ai-ollama

# Reset everything
docker-compose down && docker-compose up -d
```

---

## 📈 Monitoring

```bash
# Real-time logs
docker-compose logs -f api

# Resource usage
docker stats

# Check Ollama
curl -s http://localhost:11434/api/tags | python3 -m json.tool

# Database connection
docker-compose exec postgres psql -U legal_vault_user -d legal_ai_vault -c "SELECT 1;"
```

---

## 🎯 Best Use Cases

| Scenario | Best Approach |
|----------|--------------|
| Quick legal search | RAG endpoint with sections |
| Complex legal analysis | Legal Research Agent |
| Policy questions | HR Policy Agent with context |
| Multi-step research | Multi-agent workflow |
| Batch processing | Loop with RAG endpoint |
| Custom logic | Create custom workflow |

---

**Need More Help?**
- 📖 Full Manual: [USER_MANUAL.md](USER_MANUAL.md)
- 🧪 Test Samples: [QUICK_TEST_SAMPLES.md](QUICK_TEST_SAMPLES.md)
- 🌐 API Docs: http://localhost:8000/docs

---

*Vault AI Platform v2.0.0 - Quick Reference*
*Last Updated: 2025-11-19*
