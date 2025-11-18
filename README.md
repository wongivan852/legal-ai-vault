# Vault AI Platform

**Multi-Domain Agentic AI Platform with Extensible Workflow Orchestration**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/wongivan852/legal-ai-vault)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🚀 What is Vault AI Platform?

Vault AI Platform is a **general-purpose agentic AI system** that orchestrates specialized AI agents to solve complex, multi-step tasks across different business domains. Unlike traditional single-purpose AI tools, Vault AI enables sophisticated **multi-agent workflows** where autonomous agents collaborate to provide comprehensive solutions.

### Key Capabilities

- **🤖 Multi-Agent Architecture**: 7 specialized agents (Legal, HR, CS, Analysis, Synthesis, Validation)
- **🔄 Workflow Orchestration**: Pre-built and custom multi-step workflows
- **🏢 Multi-Domain Support**: Legal, HR, Customer Service, and extensible to any domain
- **🔧 100% On-Premises**: Your data never leaves your infrastructure
- **🌐 REST API**: Complete API with 10+ endpoints for easy integration
- **📦 Single App Deployment**: Simple Docker-based deployment (no microservices complexity)
- **🧠 LLM Agnostic**: Works with Ollama, OpenAI, or any LLM provider

---

## 🎯 Use Cases

### Enterprise Applications
- **HR Operations**: Automated onboarding, policy Q&A, benefits administration
- **Customer Support**: Intelligent ticket routing, response generation, escalation management
- **Legal Compliance**: Policy compliance checking, contract analysis, regulatory research
- **Business Analysis**: Multi-source data analysis, insight generation, report synthesis
- **Knowledge Management**: Cross-domain knowledge synthesis, quality validation

### System Integrator Applications
- **White-Label AI Platform**: Rebrand and customize for clients
- **Domain-Specific Solutions**: Add industry-specific agents (Finance, Healthcare, Manufacturing)
- **Workflow Automation**: Build custom workflows for client processes
- **Multi-Tenant SaaS**: Deploy as multi-tenant cloud service
- **API Integration**: Integrate with existing enterprise systems

---

## ✨ Key Features

### Specialized AI Agents

| Agent | Domain | Capabilities |
|-------|--------|-------------|
| **LegalResearchAgent** | Legal | HK ordinance search, section retrieval, legal Q&A |
| **HRPolicyAgent** | HR | Policy search, onboarding, benefits, general HR Q&A |
| **CSDocumentAgent** | Customer Service | Ticket routing, response generation, escalation |
| **AnalysisAgent** | Analytics | Data analysis, theme extraction, insights generation |
| **SynthesisAgent** | Integration | Multi-source synthesis, report generation |
| **ValidationAgent** | Quality | Accuracy checking, completeness validation |

### Pre-Built Workflows

1. **HR Onboarding** - Complete employee onboarding with personalized guides
2. **CS Ticket Response** - Intelligent ticket handling with sentiment analysis
3. **Legal-HR Compliance** - Cross-domain compliance checking
4. **Simple Q&A** - Single-agent question answering with validation
5. **Multi-Agent Research** - Comprehensive multi-perspective analysis

### REST API

```bash
# Platform health
GET /api/agents/health

# List all agents
GET /api/agents/

# Execute agent
POST /api/agents/{agent_name}/execute

# List workflows
GET /api/agents/workflows

# Execute workflow
POST /api/agents/workflows/{workflow_name}/execute

# Get workflow examples
GET /api/agents/workflows/{workflow_name}/example
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Vault AI Platform                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐│
│  │  FastAPI REST   │  │   Workflow      │  │   Agent      ││
│  │     API         │→│  Orchestrator   │→│  Registry    ││
│  └─────────────────┘  └─────────────────┘  └──────────────┘│
│                                                               │
│  ┌──────────────────────────────────────────────────────────┤
│  │             Specialized Domain Agents                     │
│  ├──────────┬──────────┬──────────┬──────────┬─────────────┤
│  │  Legal   │    HR    │    CS    │ Analysis │ Synthesis   │
│  │ Research │  Policy  │ Document │          │             │
│  └──────────┴──────────┴──────────┴──────────┴─────────────┘│
│                                                               │
│  ┌──────────────────────────────────────────────────────────┤
│  │                 Infrastructure Layer                      │
│  ├──────────────┬───────────────┬───────────────────────────┤
│  │    Ollama    │  PostgreSQL   │      Qdrant Vector DB     │
│  │   (LLM)      │  (Metadata)   │     (Embeddings)          │
│  └──────────────┴───────────────┴───────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **API Framework**: FastAPI (Python 3.10+)
- **LLM Server**: Ollama (llama3.1:8b, llama3.3:70b, Qwen, DeepSeek)
- **Vector Database**: Qdrant
- **Relational Database**: PostgreSQL 15
- **Embeddings**: nomic-embed-text
- **Deployment**: Docker Compose

---

## 🚀 Quick Start

### Prerequisites

- Docker Desktop (Mac: 8GB+ RAM allocation recommended)
- Ollama with at least one model installed (llama3.1:8b recommended)
- Git

### 1. Clone Repository

```bash
git clone https://github.com/wongivan852/legal-ai-vault.git
cd legal-ai-vault
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file
# - Set your preferred Ollama model (llama3.1:8b recommended)
# - Update database credentials if needed
# - Set secure JWT_SECRET and ENCRYPTION_KEY
nano .env
```

### 3. Start Platform

```bash
# Start all services
docker-compose up -d

# Check platform health
curl http://localhost:8000/api/agents/health | python3 -m json.tool
```

### 4. Verify Installation

```bash
# Expected output:
{
    "status": "healthy",
    "agents": {
        "hr_policy": "ready",
        "cs_document": "ready",
        "analysis": "ready",
        "synthesis": "ready",
        "validation": "ready"
    },
    "orchestrator": "ready",
    "total_agents": 6,
    "workflows_registered": 5
}
```

### 5. Test an Agent

```bash
# Test HR Policy Agent
curl -X POST http://localhost:8000/api/agents/hr_policy/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "question": "What are typical work hours?",
      "task_type": "general"
    }
  }' | python3 -m json.tool
```

### 6. Access Interactive Docs

```bash
open http://localhost:8000/docs
```

---

## 📖 Documentation

### Core Documentation

1. **[PLATFORM_DOCUMENTATION.md](PLATFORM_DOCUMENTATION.md)** - Complete platform reference (1000+ lines)
   - Architecture overview
   - Agent catalog with full capabilities
   - Workflow catalog with examples
   - Complete API reference
   - Integration guide
   - Extension guide (add agents/workflows)

2. **[PLATFORM_STATUS.md](PLATFORM_STATUS.md)** - Quick testing and status reference
   - Health check commands
   - Quick test commands
   - Known issues
   - Performance notes

3. **[INTEGRATION_TEST_COMPLETE.md](INTEGRATION_TEST_COMPLETE.md)** - Testing results
   - Integration test results
   - Performance metrics
   - Troubleshooting guide

### Quick Links

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/agents/health
- **Workflow Examples**: http://localhost:8000/api/agents/workflows/examples/all

---

## 🔧 Configuration

### Model Configuration

Edit `.env` file:

```bash
# Use 8B model for faster responses (recommended for development)
OLLAMA_MODEL=llama3.1:8b

# Or use 70B model for better quality (requires 48GB+ RAM)
# OLLAMA_MODEL=llama3.3:70b

# For Chinese language support
# OLLAMA_MODEL=qwen:14b
```

### Performance Tuning

| Model | Size | RAM | First Response | Subsequent | Use Case |
|-------|------|-----|----------------|------------|----------|
| llama3.2:3b | 2.0 GB | 4 GB | 10-20s | 5-10s | Simple Q&A |
| llama3.1:8b | 4.9 GB | 8 GB | 50-60s | 10-20s | General purpose (recommended) |
| llama3.3:70b | 42 GB | 48 GB | 180-300s | 60-120s | Complex analysis |
| qwen:14b | ~10 GB | 16 GB | 60-90s | 20-30s | Chinese language |

---

## 🛠️ For System Integrators

### Adding a New Agent

```python
# 1. Create agent class (api/agents/your_domain_agent.py)
from agents.base_agent import BaseAgent

class YourDomainAgent(BaseAgent):
    def __init__(self, ollama_service, qdrant_client=None, db_session=None):
        super().__init__(
            name="your_domain",
            domain="your_domain_name",
            description="Description of your agent",
            ollama_service=ollama_service,
            qdrant_client=qdrant_client,
            db_session=db_session
        )

    async def execute(self, task: dict) -> dict:
        # Your agent logic here
        pass

# 2. Register agent (api/agents/__init__.py)
from agents.your_domain_agent import YourDomainAgent

# 3. Add to agent registry (api/routes/agents.py)
_agents["your_domain"] = YourDomainAgent(ollama_service, qdrant, db)
```

See [PLATFORM_DOCUMENTATION.md](PLATFORM_DOCUMENTATION.md) Section 8 for complete guide.

### Adding a New Workflow

```python
# Add to api/workflows/reference_workflows.py
workflow = {
    "name": "your_workflow",
    "description": "Workflow description",
    "tasks": [
        {
            "id": "task1",
            "agent": "agent_name",
            "input": {
                "param": "${input.value}"
            }
        }
    ],
    "output": {
        "result": "${task1.output}"
    }
}

orchestrator.register_workflow("your_workflow", workflow)
```

See [PLATFORM_DOCUMENTATION.md](PLATFORM_DOCUMENTATION.md) Section 9 for complete guide.

### White-Label Deployment

1. **Rebrand**: Update app metadata in `api/main.py`
2. **Custom Agents**: Add domain-specific agents for your client
3. **Custom Workflows**: Build workflows for client processes
4. **Frontend**: Build custom UI (React, Vue, etc.) using the REST API
5. **Deploy**: Use included docker-compose.yml or deploy to cloud

---

## 🔒 Security & Production

### Security Checklist

- [ ] Change default database passwords in `.env`
- [ ] Generate secure JWT_SECRET and ENCRYPTION_KEY
- [ ] Configure ALLOWED_ORIGINS for CORS
- [ ] Enable HTTPS with nginx reverse proxy
- [ ] Add authentication (OAuth 2.0 or API keys)
- [ ] Implement rate limiting
- [ ] Enable audit logging
- [ ] Regular security updates

### Production Deployment

```bash
# 1. Update docker-compose.yml with nginx profile
docker-compose --profile production up -d

# 2. Configure nginx for HTTPS
# See nginx/nginx.conf for example

# 3. Set up monitoring
# - Prometheus + Grafana
# - Health check monitoring
# - Log aggregation

# 4. Configure backups
# - PostgreSQL database
# - Qdrant vector database
# - Application logs
```

---

## 📊 Performance & Scaling

### Current Performance (Development)

- **First agent request**: 50-60 seconds (model loading)
- **Subsequent requests**: 10-20 seconds
- **Workflow execution**: 2-5 minutes (multiple agents)
- **Concurrent users**: 10-20 (single Docker host)

### Scaling Options

1. **Vertical Scaling**
   - Increase Docker memory allocation
   - Use faster GPU for LLM inference
   - Use larger models for better quality

2. **Horizontal Scaling**
   - Deploy multiple API instances (load balancer)
   - Separate LLM server (dedicated GPU machine)
   - Separate database instances

3. **Optimization**
   - Model caching and pre-loading
   - Connection pooling
   - Async task queues (Celery/RQ)
   - Redis caching layer

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution

- New domain agents (Finance, Healthcare, Manufacturing)
- New workflow templates
- Frontend development (React/Vue UI)
- Performance optimizations
- Documentation improvements
- Test coverage
- Bug fixes

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙋 Support

### Getting Help

- **Documentation**: See [PLATFORM_DOCUMENTATION.md](PLATFORM_DOCUMENTATION.md)
- **Issues**: [GitHub Issues](https://github.com/wongivan852/legal-ai-vault/issues)
- **Discussions**: [GitHub Discussions](https://github.com/wongivan852/legal-ai-vault/discussions)

### Troubleshooting

**Platform not starting?**
```bash
# Check logs
docker-compose logs -f api

# Restart services
docker-compose restart

# Full reset
docker-compose down
docker-compose up -d
```

**Agent execution timeout?**
```bash
# Check model configuration
docker exec legal-ai-api env | grep OLLAMA_MODEL

# Should show: OLLAMA_MODEL=llama3.1:8b
# If showing 70b, update .env and recreate container
docker-compose up -d --force-recreate api
```

**Ollama out of memory?**
```bash
# Check Ollama memory usage
docker stats legal-ai-ollama

# If >80%, restart Ollama
docker restart legal-ai-ollama
```

See [INTEGRATION_TEST_COMPLETE.md](INTEGRATION_TEST_COMPLETE.md) for complete troubleshooting guide.

---

## 🎓 Examples

### Execute HR Agent

```bash
curl -X POST http://localhost:8000/api/agents/hr_policy/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "question": "What is the vacation policy?",
      "task_type": "benefits",
      "employee_type": "full-time"
    }
  }'
```

### Execute Workflow

```bash
curl -X POST http://localhost:8000/api/agents/workflows/hr_onboarding/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "employee_name": "John Doe",
      "employee_type": "full-time",
      "department": "Engineering",
      "start_date": "2024-01-15"
    }
  }'
```

### List All Agents

```bash
curl http://localhost:8000/api/agents/ | python3 -m json.tool
```

---

## 🗺️ Roadmap

### v2.1 (Q2 2025)
- [ ] Web UI (React-based)
- [ ] User authentication & authorization
- [ ] Multi-tenant support
- [ ] Advanced workflow builder
- [ ] Performance dashboard

### v2.2 (Q3 2025)
- [ ] Financial domain agents
- [ ] Healthcare domain agents
- [ ] Manufacturing domain agents
- [ ] Workflow marketplace
- [ ] Cloud deployment templates (AWS, Azure, GCP)

### v3.0 (Q4 2025)
- [ ] Multi-LLM support (OpenAI, Anthropic, Google)
- [ ] Advanced RAG with knowledge graphs
- [ ] Real-time streaming responses
- [ ] Mobile app (iOS/Android)
- [ ] Enterprise features (SSO, audit logs, compliance)

---

## 🏆 Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Ollama](https://ollama.ai/) - Local LLM server
- [Qdrant](https://qdrant.tech/) - Vector database
- [PostgreSQL](https://www.postgresql.org/) - Relational database
- [LangChain](https://langchain.com/) - LLM application framework

---

## 📞 Contact

- **GitHub**: [wongivan852](https://github.com/wongivan852)
- **Project**: [Vault AI Platform](https://github.com/wongivan852/legal-ai-vault)

---

**Made with ❤️ for the AI community**

*Transform your business with intelligent, autonomous AI agents*
