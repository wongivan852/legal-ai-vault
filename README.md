# Legal/Financial AI Vault

**On-premises AI inference system for legal and financial workflows**

Powered by vLLM, Qdrant, and FastAPI running on 6-GPU server infrastructure.

## Features

- **GPU-Accelerated Inference**: Multi-GPU vLLM deployment for high-throughput AI processing
- **Vector Database**: Qdrant for semantic search and RAG (Retrieval Augmented Generation)
- **Specialized AI Agents**:
  - Contract Review Agent
  - Compliance Monitoring Agent
  - Legal Research Agent
  - Document Router Agent
- **Hong Kong Legal Database**: Complete HK legislation and instruments with AI-powered search
- **Enterprise Security**: On-premises deployment, encrypted storage, comprehensive audit logging
- **Multi-language Support**: English, Traditional Chinese, Simplified Chinese

## System Requirements

### Hardware
- 6x NVIDIA GPUs (recommended: RTX 4090 or A100)
- 128GB+ RAM
- 4TB+ Storage (NVMe recommended)
- 10GbE Network

### Software
- Ubuntu 22.04 LTS Server
- Docker 24.x + Docker Compose
- NVIDIA Driver 525+
- CUDA 12.1+

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/wongivan852/legal_financial_ai_vault.git
cd legal_financial_ai_vault
```

### 2. Configure Environment

```bash
cp .env.example .env.production
nano .env.production
```

Set the following variables:
```env
# Database
DB_USER=legal_vault_user
DB_PASSWORD=<secure_password>

# Security
JWT_SECRET=<generate_with_openssl_rand_hex_32>
ENCRYPTION_KEY=<generate_with_openssl_rand_hex_32>
GRAFANA_PASSWORD=<admin_password>

# vLLM Models
VLLM_CONTRACT_URL=http://vllm-contract:8001/v1
VLLM_COMPLIANCE_URL=http://vllm-compliance:8002/v1
VLLM_ROUTER_URL=http://vllm-router:8003/v1
EMBEDDING_URL=http://embedding-service:8004
```

### 3. Download AI Models

```bash
# Download Qwen models
mkdir -p /data/models
cd /data/models

# Qwen 2.5 14B Instruct (for contract review and compliance)
git clone https://huggingface.co/Qwen/Qwen2.5-14B-Instruct qwen2.5-14b-instruct

# Qwen 2.5 7B Instruct (for routing)
git clone https://huggingface.co/Qwen/Qwen2.5-7B-Instruct qwen2.5-7b-instruct

# BGE Large English v1.5 (for embeddings)
git clone https://huggingface.co/BAAI/bge-large-en-v1.5 bge-large-en-v1.5
```

### 4. Start Services

```bash
# Start all services
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f api
```

### 5. Initialize Database

```bash
# Create admin user
docker-compose exec api python scripts/create_admin.py

# Import Hong Kong legal data (optional)
./scripts/quick_start_hk_legal.sh
```

### 6. Access Services

- **API Documentation**: https://your-server/api/docs
- **Web UI**: https://your-server/
- **Grafana Dashboard**: http://your-server:3001
- **Prometheus**: http://your-server:9091

## Hong Kong Legal Data Integration

This system includes a comprehensive Hong Kong legal database with AI-powered search.

### Features
- **1,150+ Legal Documents** in English (3,450+ across all languages)
- **Instruments**: A-series legal instruments
- **Ordinances**: Cap. 1 to Cap. 600+
- **Semantic Search**: AI-powered natural language queries
- **Section-level Retrieval**: Granular search across all sections
- **RAG Integration**: Retrieve relevant law sections for contract analysis

### Quick Setup

```bash
# Run automated setup
./scripts/quick_start_hk_legal.sh

# Or manual setup
python scripts/ingest_hk_legal_data.py ~/Downloads/hkel_data --init-db --language en
```

### API Examples

```bash
# Search for employment law
curl -X GET "http://localhost:8000/api/hk-legal/search?query=employment%20rights&language=en" \
     -H "Authorization: Bearer YOUR_TOKEN"

# Get statistics
curl -X GET "http://localhost:8000/api/hk-legal/stats" \
     -H "Authorization: Bearer YOUR_TOKEN"

# Get Basic Law
curl -X GET "http://localhost:8000/api/hk-legal/by_number/A101?language=en" \
     -H "Authorization: Bearer YOUR_TOKEN"
```

See [HK_LEGAL_DATA_INTEGRATION.md](HK_LEGAL_DATA_INTEGRATION.md) for complete documentation.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  LEGAL AI VAULT                          │
└─────────────────────────────────────────────────────────┘

                    Nginx Reverse Proxy (443)
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   React UI           FastAPI Backend      Admin Dashboard
   (Port 3000)        (Port 8000)         (Port 9090)
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    Dify Workflow Engine
                    (Agent Orchestration)
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   vLLM GPU0-1         vLLM GPU2          vLLM GPU3-4
   (Qwen-14B)          (Qwen-14B)         (Qwen-7B)
   Contract Review     Compliance         Routing
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    Embedding Service (GPU5)
                    (bge-large-en-v1.5)
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   Qdrant Vector DB    PostgreSQL          Encrypted Storage
   (Embeddings)        (Metadata)          (Documents/Models)
```

## API Documentation

### Authentication

```bash
# Login
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@example.com", "password": "password"}'

# Returns JWT token
```

### Contract Review

```bash
# Upload document
curl -X POST "http://localhost:8000/api/documents/upload" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -F "file=@contract.pdf"

# Analyze contract
curl -X POST "http://localhost:8000/api/agents/contract-review" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"document_id": "doc_123", "analysis_type": "comprehensive"}'
```

### HK Legal Search

```bash
# Semantic search
curl -X GET "http://localhost:8000/api/hk-legal/search?query=employment&language=en" \
     -H "Authorization: Bearer YOUR_TOKEN"

# Browse by type
curl -X GET "http://localhost:8000/api/hk-legal/documents?doc_type=ordinance" \
     -H "Authorization: Bearer YOUR_TOKEN"
```

## Development

### Project Structure

```
legal-ai-vault/
├── api/                      # FastAPI backend
│   ├── models/              # Database models
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic
│   ├── agents/              # AI agents
│   ├── parsers/             # Data parsers
│   └── security/            # Authentication
├── frontend/                # React frontend
├── scripts/                 # Utility scripts
├── monitoring/              # Prometheus/Grafana
├── docker-compose.yml       # Service orchestration
└── docs/                    # Documentation
```

### Running Tests

```bash
# API tests
docker-compose exec api pytest

# Frontend tests
docker-compose exec frontend npm test
```

### Database Migrations

```bash
# Create migration
docker-compose exec api alembic revision --autogenerate -m "description"

# Apply migration
docker-compose exec api alembic upgrade head
```

## Monitoring

### Grafana Dashboards

Access at `http://localhost:3001`

- **GPU Metrics**: GPU utilization, memory, temperature
- **API Performance**: Request latency, throughput, error rates
- **Vector DB**: Query performance, index size
- **System Health**: CPU, memory, disk usage

### Prometheus Metrics

Available at `http://localhost:9091`

Custom metrics:
- `inference_requests_total`
- `inference_latency_seconds`
- `tokens_processed_total`
- `vector_search_latency_seconds`

## Security

### Data Protection
- **Encryption at Rest**: AES-256 for document storage
- **Encryption in Transit**: TLS 1.3 for all communications
- **Access Control**: Role-based access control (RBAC)
- **Audit Logging**: 7-year retention for compliance

### Network Security
- **Firewall**: UFW with restrictive rules
- **Intrusion Detection**: fail2ban
- **AppArmor**: Mandatory Access Control
- **VPN Only**: Restrict access to internal network

## Performance

### Benchmarks

- **Contract Review**: ~2-3 seconds for 10-page contract
- **Vector Search**: <100ms per query
- **Concurrent Users**: 50+ simultaneous sessions
- **Throughput**: 100+ documents per hour

### Optimization

```bash
# GPU memory optimization
VLLM_GPU_MEMORY_UTILIZATION=0.95

# Batch size tuning
VLLM_MAX_NUM_SEQS=256

# Enable quantization (optional)
VLLM_QUANTIZATION=awq
```

## Troubleshooting

### GPU Issues

```bash
# Check GPU status
nvidia-smi

# Restart vLLM services
docker-compose restart vllm-contract vllm-compliance vllm-router

# Check GPU logs
docker-compose logs vllm-contract
```

### Database Issues

```bash
# Check PostgreSQL status
docker-compose exec postgres pg_isready

# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d postgres
docker-compose exec api python scripts/init_database.py
```

### Vector Database Issues

```bash
# Check Qdrant health
curl http://localhost:6333/health

# Rebuild collection
docker-compose exec api python scripts/rebuild_vectors.py
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Copyright © 2025 Legal AI Vault Contributors

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

## Support

For technical support:
- **GitHub Issues**: https://github.com/wongivan852/legal_financial_ai_vault/issues
- **Email**: support@legal-ai-vault.com
- **Documentation**: https://docs.legal-ai-vault.com

## Acknowledgments

- **vLLM**: High-performance LLM inference
- **Qdrant**: Vector database engine
- **FastAPI**: Modern web framework
- **Qwen**: Large language models
- **Hong Kong Department of Justice**: e-Legislation data
