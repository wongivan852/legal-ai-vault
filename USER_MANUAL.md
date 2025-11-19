# Vault AI Platform - User Manual

**Version**: 2.0.0
**Date**: 2025-11-19
**Platform**: Multi-Agent AI System with RAG Capabilities

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Platform Architecture](#platform-architecture)
4. [Agent Reference](#agent-reference)
5. [API Endpoints](#api-endpoints)
6. [Workflows](#workflows)
7. [Usage Examples](#usage-examples)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Features](#advanced-features)
11. [FAQ](#faq)

---

## Introduction

### What is Vault AI Platform?

Vault AI Platform is a **multi-agent AI system** that provides intelligent document analysis, research, and workflow automation capabilities. The platform combines:

- **6 Specialized AI Agents** for different domains
- **RAG (Retrieval Augmented Generation)** for accurate, context-aware responses
- **Multi-Agent Workflows** for complex, multi-step tasks
- **Vector Database Search** across 1,699+ HK legal ordinances
- **RESTful API** for easy integration

### Key Features

✅ **Legal Research** - Search and analyze 1,699 Hong Kong ordinances
✅ **HR Policy Analysis** - Query employee policies and benefits
✅ **Customer Support** - Answer questions using support documentation
✅ **Document Analysis** - Extract insights from any text
✅ **Multi-Source Synthesis** - Combine information from multiple documents
✅ **Validation** - Check consistency across documents
✅ **Workflow Automation** - Chain multiple agents for complex tasks

### Who Should Use This?

- **Legal Professionals** - Research HK law and legal requirements
- **HR Teams** - Query policies and employee benefits
- **Customer Support** - Provide accurate answers from documentation
- **Business Analysts** - Analyze documents and extract insights
- **Developers** - Integrate AI capabilities into applications

---

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- 8GB+ RAM recommended (16GB for optimal performance)
- 10GB+ free disk space
- Internet connection for initial setup

### Quick Start

#### 1. Start the Platform

```bash
cd /Users/wongivan/Apps/legal-ai-vault
docker-compose up -d
```

#### 2. Verify Platform is Running

```bash
# Check agent health
curl -s http://localhost:8000/api/agents/health | python3 -m json.tool
```

**Expected Output**:
```json
{
  "status": "healthy",
  "agents": {
    "legal_research": "ready",
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

#### 3. Run Your First Query

```bash
curl -X POST http://localhost:8000/api/rag \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the Building Management Ordinance?",
    "top_k": 3,
    "search_type": "documents"
  }' | python3 -m json.tool
```

### Platform URLs

| Service | URL | Description |
|---------|-----|-------------|
| **API** | http://localhost:8000 | Main API endpoint |
| **Frontend** | http://localhost:3000 | Web interface (if enabled) |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Qdrant** | http://localhost:6333/dashboard | Vector database dashboard |

---

## Platform Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Vault AI Platform v2.0.0                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   6 AI       │  │   Workflow   │  │     RAG      │    │
│  │   Agents     │  │ Orchestrator │  │   Service    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│         │                  │                  │            │
│  ┌──────┴──────────────────┴──────────────────┴────────┐  │
│  │              FastAPI REST API Layer                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
├───────────────────────────┼─────────────────────────────────┤
│  ┌─────────────┐  ┌──────┴──────┐  ┌──────────────┐      │
│  │ PostgreSQL  │  │   Ollama    │  │    Qdrant    │      │
│  │  (Metadata) │  │ (LLM+Embed) │  │   (Vectors)  │      │
│  └─────────────┘  └─────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Request** → REST API
2. **Agent Selection** → Appropriate agent for the task
3. **Document Retrieval** → Vector search in Qdrant
4. **LLM Processing** → Ollama generates response
5. **Response** → Structured JSON output

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **API Framework** | FastAPI | REST API endpoints |
| **AI Agents** | Custom Python | Specialized task handlers |
| **LLM** | Ollama (llama3.1:8b) | Text generation |
| **Embeddings** | nomic-embed-text | Vector embeddings (768-dim) |
| **Vector DB** | Qdrant | Semantic search |
| **Relational DB** | PostgreSQL | Metadata storage |
| **Containerization** | Docker Compose | Service orchestration |

---

## Agent Reference

### 1. Legal Research Agent 🏛️

**Purpose**: Search and analyze Hong Kong legal ordinances

**Capabilities**:
- Search across 1,699 HK ordinances
- Section-level precise search (11,288 sections)
- Context-aware legal analysis
- Multi-document legal research

**When to Use**:
- Finding specific legal provisions
- Understanding legal requirements
- Researching case law and statutes
- Compliance questions

**Example Request**:
```json
{
  "task": {
    "task_type": "search",
    "question": "What are the insurance requirements for construction under the Building Management Ordinance?"
  }
}
```

**API Endpoint**: `POST /api/agents/legal_research/execute`

---

### 2. HR Policy Agent 👔

**Purpose**: Answer questions about HR policies, benefits, and employee information

**Capabilities**:
- Query HR policies and procedures
- Explain benefits and compensation
- Answer leave and vacation questions
- Provide onboarding information

**When to Use**:
- Employee benefit questions
- Policy clarification
- HR compliance
- Onboarding new employees

**Example Request**:
```json
{
  "task": {
    "question": "How many vacation days do employees get after 3 years?",
    "task_type": "policy_search",
    "context": "Full-time employees: Year 1: 10 days, Year 3: 20 days, Year 5: 25 days"
  }
}
```

**API Endpoint**: `POST /api/agents/hr_policy/execute`

---

### 3. Customer Service Agent 💬

**Purpose**: Answer customer questions using support documentation

**Capabilities**:
- Answer FAQs
- Provide troubleshooting guidance
- Explain product features
- Guide through processes

**When to Use**:
- Customer support inquiries
- Product documentation questions
- Troubleshooting help
- How-to guidance

**Example Request**:
```json
{
  "task": {
    "question": "How do I reset my password?",
    "task_type": "support",
    "context": "Password Reset: 1. Go to login page 2. Click Forgot Password 3. Enter email..."
  }
}
```

**API Endpoint**: `POST /api/agents/cs_document/execute`

---

### 4. Analysis Agent 📊

**Purpose**: Analyze documents and extract insights

**Capabilities**:
- Extract key information
- Identify trends and patterns
- Summarize complex documents
- Generate insights

**When to Use**:
- Document analysis
- Data interpretation
- Trend identification
- Summary generation

**Example Request**:
```json
{
  "task": {
    "task_type": "analysis",
    "text": "Q4 revenue increased 25% to $5.2M. New product contributed $2.1M...",
    "focus": "Identify key performance indicators"
  }
}
```

**API Endpoint**: `POST /api/agents/analysis/execute`

---

### 5. Synthesis Agent 🔄

**Purpose**: Combine information from multiple sources

**Capabilities**:
- Synthesize multi-source information
- Create comprehensive summaries
- Identify common themes
- Generate unified responses

**When to Use**:
- Combining multiple documents
- Creating comprehensive reports
- Multi-source research
- Information consolidation

**Example Request**:
```json
{
  "task": {
    "task_type": "synthesis",
    "sources": [
      {"title": "Customer Survey", "content": "..."},
      {"title": "App Reviews", "content": "..."},
      {"title": "Support Tickets", "content": "..."}
    ],
    "focus": "Create product improvement plan"
  }
}
```

**API Endpoint**: `POST /api/agents/synthesis/execute`

---

### 6. Validation Agent ✓

**Purpose**: Validate consistency across documents

**Capabilities**:
- Check for inconsistencies
- Validate data accuracy
- Identify contradictions
- Verify compliance

**When to Use**:
- Document consistency checks
- Policy validation
- Data verification
- Compliance audits

**Example Request**:
```json
{
  "task": {
    "task_type": "validation",
    "documents": [
      {"title": "Employee Handbook", "content": "15 days vacation"},
      {"title": "HR Website", "content": "15 days vacation"},
      {"title": "Offer Letter", "content": "10 days first year"}
    ],
    "focus": "Check vacation policy consistency"
  }
}
```

**API Endpoint**: `POST /api/agents/validation/execute`

---

## API Endpoints

### Agent Execution Endpoints

#### Execute Agent
```http
POST /api/agents/{agent_name}/execute
Content-Type: application/json

{
  "task": {
    "task_type": "string",
    "question": "string",
    // ... agent-specific parameters
  }
}
```

**Available Agents**:
- `legal_research`
- `hr_policy`
- `cs_document`
- `analysis`
- `synthesis`
- `validation`

**Response**:
```json
{
  "agent": "agent_name",
  "status": "success|failed",
  "result": {
    "answer": "...",
    "sources": [...],
    "execution_time": 45.2
  },
  "execution_time": 45.2
}
```

---

### RAG Endpoints

#### RAG Search
```http
POST /api/rag
Content-Type: application/json

{
  "question": "your question here",
  "top_k": 5,
  "search_type": "documents|sections"
}
```

**Parameters**:
- `question` (required): Your search query
- `top_k` (optional, default: 5): Number of results to return
- `search_type` (optional, default: "documents"): Search documents or sections

**Response**:
```json
{
  "success": true,
  "answer": "Generated answer based on retrieved documents",
  "sources": [
    {
      "doc_number": "Cap. 344",
      "title": "Building Management Ordinance",
      "content": "...",
      "score": 0.89
    }
  ],
  "execution_time": 12.5
}
```

---

### Workflow Endpoints

#### List Workflows
```http
GET /api/agents/workflows
```

**Response**:
```json
[
  "hr_onboarding",
  "cs_ticket_response",
  "legal_hr_compliance",
  "simple_qa",
  "multi_agent_research"
]
```

#### Execute Workflow
```http
POST /api/agents/workflows/{workflow_name}/execute
Content-Type: application/json

{
  "input_data": {
    // workflow-specific input
  }
}
```

#### Get Workflow Info
```http
GET /api/agents/workflows/{workflow_name}
```

#### Get Workflow Example
```http
GET /api/agents/workflows/{workflow_name}/example
```

---

### Health & Status Endpoints

#### Agent Health
```http
GET /api/agents/health
```

**Response**:
```json
{
  "status": "healthy",
  "agents": {
    "legal_research": "ready",
    "hr_policy": "ready",
    // ...
  },
  "orchestrator": "ready",
  "total_agents": 6,
  "workflows_registered": 5
}
```

#### Platform Health
```http
GET /health
```

#### List All Agents
```http
GET /api/agents
```

---

## Workflows

### What are Workflows?

Workflows are **pre-configured multi-agent processes** that combine multiple agents to accomplish complex tasks.

### Available Workflows

#### 1. HR Onboarding (`hr_onboarding`)

**Purpose**: Automate employee onboarding process

**Agents Used**: HR Policy, Validation

**Example**:
```bash
curl -X POST http://localhost:8000/api/agents/workflows/hr_onboarding/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "employee_name": "John Doe",
      "position": "Software Engineer",
      "start_date": "2025-01-15"
    }
  }'
```

---

#### 2. CS Ticket Response (`cs_ticket_response`)

**Purpose**: Automated customer support ticket responses

**Agents Used**: CS Document, Synthesis

**Example**:
```bash
curl -X POST http://localhost:8000/api/agents/workflows/cs_ticket_response/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "ticket_id": "CS-12345",
      "customer_question": "How do I reset my password?",
      "priority": "medium"
    }
  }'
```

---

#### 3. Legal HR Compliance (`legal_hr_compliance`)

**Purpose**: Check HR policies against legal requirements

**Agents Used**: Legal Research, HR Policy, Validation

**Example**:
```bash
curl -X POST http://localhost:8000/api/agents/workflows/legal_hr_compliance/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "policy_type": "employment",
      "question": "Are our employment contracts compliant with HK law?"
    }
  }'
```

---

#### 4. Simple Q&A (`simple_qa`)

**Purpose**: Quick question answering

**Agents Used**: Analysis

**Example**:
```bash
curl -X POST http://localhost:8000/api/agents/workflows/simple_qa/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "question": "What is the purpose of the Employment Ordinance?",
      "context": "legal"
    }
  }'
```

---

#### 5. Multi-Agent Research (`multi_agent_research`)

**Purpose**: Comprehensive research using multiple agents

**Agents Used**: Legal Research, Analysis, Synthesis

**Example**:
```bash
curl -X POST http://localhost:8000/api/agents/workflows/multi_agent_research/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "research_topic": "HK company director responsibilities",
      "depth": "comprehensive"
    }
  }'
```

---

## Usage Examples

### Example 1: Legal Research

**Scenario**: You need to find insurance requirements for construction projects.

```bash
curl -X POST http://localhost:8000/api/agents/legal_research/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "search",
      "question": "What are the insurance requirements for minor works construction under the Building Management Ordinance?"
    }
  }' | python3 -m json.tool
```

**Expected Response**:
```json
{
  "agent": "legal_research",
  "status": "success",
  "result": {
    "answer": "Under the Building Management Ordinance...",
    "sources": [
      {
        "doc_number": "Cap. 344",
        "section": "Section 28",
        "content": "Insurance requirements...",
        "relevance_score": 0.92
      }
    ],
    "execution_time": 23.5
  }
}
```

---

### Example 2: HR Policy Query

**Scenario**: Employee asks about vacation days.

```bash
curl -X POST http://localhost:8000/api/agents/hr_policy/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "question": "How many vacation days do I get after working here for 3 years?",
      "task_type": "benefits",
      "context": "VACATION POLICY: New employees: 10 days. After 1 year: 15 days. After 3 years: 20 days. After 5 years: 25 days."
    }
  }' | python3 -m json.tool
```

---

### Example 3: Customer Support

**Scenario**: Customer needs help resetting password.

```bash
curl -X POST http://localhost:8000/api/agents/cs_document/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "question": "How do I reset my password?",
      "task_type": "support",
      "context": "PASSWORD RESET: 1. Go to login page 2. Click Forgot Password 3. Enter email 4. Check email for reset link 5. Create new password"
    }
  }' | python3 -m json.tool
```

---

### Example 4: Document Analysis

**Scenario**: Analyze quarterly sales data.

```bash
curl -X POST http://localhost:8000/api/agents/analysis/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "analysis",
      "text": "Q4 2024: Revenue $5.2M (+25% from Q3). New product line contributed $2.1M (40%). Expanded to APAC, EU, LATAM. Customer retention 78% (up from 65%). CAC decreased 20%. Operating costs +15%.",
      "focus": "Identify key trends and recommendations"
    }
  }' | python3 -m json.tool
```

---

### Example 5: Multi-Source Synthesis

**Scenario**: Combine feedback from multiple sources.

```bash
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "synthesis",
      "sources": [
        {
          "title": "Customer Survey",
          "content": "85% satisfaction. Want mobile app. Pricing excellent."
        },
        {
          "title": "App Store Reviews",
          "content": "4.2 stars. Easy to use. Crashes occasionally. Want dark mode."
        },
        {
          "title": "Support Tickets",
          "content": "Issues: sync delays 35%, password resets 25%, billing 20%"
        }
      ],
      "focus": "Create comprehensive product roadmap"
    }
  }' | python3 -m json.tool
```

---

### Example 6: Validation

**Scenario**: Check consistency across policy documents.

```bash
curl -X POST http://localhost:8000/api/agents/validation/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "validation",
      "documents": [
        {
          "title": "Employee Handbook",
          "content": "All employees receive 15 days vacation"
        },
        {
          "title": "Offer Letter",
          "content": "You will receive 10 days vacation in first year, 15 days after one year"
        }
      ],
      "focus": "Check vacation policy consistency"
    }
  }' | python3 -m json.tool
```

---

## Best Practices

### 1. Query Formulation

**✅ Good Queries**:
- Specific and clear: "What are the insurance requirements for construction?"
- Include context: "...under the Building Management Ordinance"
- Focus on single topic: "director duties" not "director duties and shareholder rights"

**❌ Poor Queries**:
- Too vague: "Tell me about laws"
- Multiple questions: "What about A and B and also C?"
- Missing context: "What are the requirements?" (requirements for what?)

### 2. Agent Selection

| Use Case | Best Agent | Why |
|----------|-----------|-----|
| HK law questions | Legal Research | Has 1,699 ordinances loaded |
| Policy questions | HR Policy | Specialized in HR/benefits |
| Support questions | CS Document | Optimized for customer support |
| Data analysis | Analysis | Extracts insights |
| Multi-source info | Synthesis | Combines information |
| Consistency check | Validation | Identifies contradictions |

### 3. Performance Optimization

**Faster Responses**:
1. Use RAG endpoint (`/api/rag`) instead of agents for simple searches
2. Specify `search_type: "sections"` for more precise results
3. Set appropriate `top_k` (3-5 for most cases)
4. First query is slower (cold start), subsequent queries are faster

**Better Results**:
1. Provide context in your queries
2. Use specific document references when possible
3. For multi-step tasks, use workflows instead of individual agents

### 4. Error Handling

**Common Issues & Solutions**:

| Issue | Cause | Solution |
|-------|-------|----------|
| Timeout after 30s | LLM cold start | Wait for first query, subsequent will be faster |
| Empty response | No relevant documents | Rephrase query or check if data is loaded |
| "Agent not ready" | Agent initializing | Wait 5-10 seconds and retry |
| 503 error | Service not available | Check `docker-compose ps` and restart if needed |

### 5. Rate Limiting

- Recommended: **5-10 concurrent requests max**
- Each query takes 10-30 seconds with llama3.1:8b
- For high throughput, consider queueing requests

---

## Troubleshooting

### Platform Not Starting

**Problem**: Containers won't start

**Solution**:
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose down
docker-compose up -d

# Check resource usage
docker stats --no-stream
```

---

### Agent Returns Error

**Problem**: Agent execution fails

**Solution**:
```bash
# Check agent health
curl -s http://localhost:8000/api/agents/health | python3 -m json.tool

# Check API logs
docker-compose logs api | tail -100

# Restart API
docker-compose restart api
```

---

### Slow Response Times

**Problem**: Queries take >60 seconds

**Possible Causes & Solutions**:

1. **Cold Start** (First Query)
   - Solution: Wait for first query to complete (60-120s)
   - Subsequent queries will be 10-30s

2. **High Resource Usage**
   - Check: `docker stats legal-ai-ollama`
   - Solution: Restart Ollama: `docker restart legal-ai-ollama`

3. **Complex Query**
   - Solution: Simplify query or use RAG endpoint instead

---

### Empty or No Results

**Problem**: Agent returns no information

**Possible Causes**:

1. **No Relevant Documents**
   - Solution: Rephrase query with different keywords

2. **Data Not Loaded** (Legal Agent)
   - Check: `curl -s http://localhost:6333/collections/hk_legal_documents`
   - Solution: Verify 1,699 documents are imported

3. **Missing Context** (Other Agents)
   - Solution: Provide document content in request

---

### Database Connection Errors

**Problem**: "Database connection failed"

**Solution**:
```bash
# Check PostgreSQL
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres

# Verify connection
docker-compose exec postgres psql -U legal_vault_user -d legal_ai_vault -c "SELECT 1;"
```

---

## Advanced Features

### Custom Workflows

You can create custom workflows by combining agents:

```python
from agents import WorkflowOrchestrator

# Define custom workflow
custom_workflow = {
    "name": "my_custom_workflow",
    "description": "Custom multi-step process",
    "tasks": [
        {
            "agent": "legal_research",
            "task": {"task_type": "search", "question": "..."}
        },
        {
            "agent": "analysis",
            "task": {"task_type": "analysis", "text": "{previous_result}"}
        },
        {
            "agent": "synthesis",
            "task": {"task_type": "synthesis", "sources": [...]}
        }
    ]
}

# Register workflow
orchestrator.register_workflow(custom_workflow)
```

---

### Batch Processing

Process multiple queries in batch:

```bash
# Create batch file
cat > /tmp/batch_queries.txt << 'EOF'
What is the Employment Ordinance?
What are director duties under Companies Ordinance?
Building permit requirements Hong Kong
EOF

# Process batch
while IFS= read -r query; do
  curl -s -X POST http://localhost:8000/api/rag \
    -H "Content-Type: application/json" \
    -d "{\"question\": \"$query\", \"top_k\": 3}" \
    > "/tmp/result_$(echo $query | tr ' ' '_').json"
done < /tmp/batch_queries.txt
```

---

### Monitoring & Analytics

Track platform usage and performance:

```bash
# View agent statistics
curl -s http://localhost:8000/api/agents/stats | python3 -m json.tool

# Monitor Qdrant metrics
curl -s http://localhost:6333/metrics

# Check PostgreSQL stats
docker-compose exec postgres psql -U legal_vault_user -d legal_ai_vault -c \
  "SELECT schemaname, tablename, n_tup_ins, n_tup_upd FROM pg_stat_user_tables;"
```

---

### Integration Examples

#### Python Integration

```python
import requests
import json

class VaultAIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def search_legal(self, question: str):
        """Search legal ordinances"""
        response = requests.post(
            f"{self.base_url}/api/agents/legal_research/execute",
            json={
                "task": {
                    "task_type": "search",
                    "question": question
                }
            }
        )
        return response.json()

    def rag_search(self, question: str, top_k: int = 5):
        """RAG search"""
        response = requests.post(
            f"{self.base_url}/api/rag",
            json={
                "question": question,
                "top_k": top_k,
                "search_type": "sections"
            }
        )
        return response.json()

# Usage
client = VaultAIClient()
result = client.search_legal("What is the Building Management Ordinance?")
print(json.dumps(result, indent=2))
```

#### JavaScript/Node.js Integration

```javascript
const axios = require('axios');

class VaultAIClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async searchLegal(question) {
    const response = await axios.post(
      `${this.baseUrl}/api/agents/legal_research/execute`,
      {
        task: {
          task_type: 'search',
          question: question
        }
      }
    );
    return response.data;
  }

  async ragSearch(question, topK = 5) {
    const response = await axios.post(
      `${this.baseUrl}/api/rag`,
      {
        question: question,
        top_k: topK,
        search_type: 'sections'
      }
    );
    return response.data;
  }
}

// Usage
const client = new VaultAIClient();
client.searchLegal('What is the Building Management Ordinance?')
  .then(result => console.log(JSON.stringify(result, null, 2)));
```

---

## FAQ

### General Questions

**Q: How many documents are in the legal database?**
A: 1,699 Hong Kong ordinances with 11,288 sections, all with vector embeddings for semantic search.

**Q: What LLM model is used?**
A: llama3.1:8b via Ollama for text generation, nomic-embed-text for embeddings.

**Q: Can I use my own documents?**
A: Yes, you can provide documents inline in API requests or import them into the vector database.

**Q: Is there a rate limit?**
A: No hard limit, but recommended max 5-10 concurrent requests for optimal performance.

**Q: What's the difference between agents and RAG?**
A: RAG is direct search + generation. Agents add specialized logic, tools, and multi-step reasoning.

---

### Technical Questions

**Q: Why is the first query slow?**
A: LLM cold start. First query loads the model (60-120s). Subsequent queries are faster (10-30s).

**Q: Can I run this on a server?**
A: Yes, it's Docker-based. Deploy on any server with Docker support. Update ports/URLs in `.env` file.

**Q: How do I backup the data?**
A: Backup PostgreSQL database and Qdrant storage volumes.

**Q: Can I use a different LLM?**
A: Yes, modify Ollama configuration to use different models (llama3, mistral, etc).

**Q: How much disk space is needed?**
A: ~10GB for LLM models, vector database, and document storage.

---

### Usage Questions

**Q: Which agent should I use for legal questions?**
A: Legal Research Agent - it has 1,699 HK ordinances pre-loaded.

**Q: How do I search for specific law sections?**
A: Use `search_type: "sections"` in RAG endpoint for section-level precision.

**Q: Can I combine multiple agents?**
A: Yes, use workflows or create custom multi-agent sequences.

**Q: How accurate are the responses?**
A: Responses are based on actual documents with citations. Always verify critical information.

**Q: Can I export the results?**
A: Yes, API returns JSON. Save responses and process as needed.

---

## Appendix

### API Response Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 400 | Bad Request | Check request format |
| 404 | Not Found | Verify agent/endpoint name |
| 500 | Server Error | Check logs, retry |
| 503 | Service Unavailable | Wait and retry |

### Document Format Guidelines

**Supported Formats**:
- Plain text
- Markdown
- JSON (structured)
- PDF (via import scripts)

**Best Practices**:
- Keep sections under 1000 words for optimal embedding
- Use clear headings and structure
- Include metadata (title, date, category)

### Performance Benchmarks

| Operation | Time | Notes |
|-----------|------|-------|
| Vector Search | 0.1-0.5s | Fast |
| RAG (no LLM) | 0.5-2s | Search + retrieval |
| RAG (with LLM) | 10-30s | After cold start |
| Agent Execution | 15-45s | Depends on complexity |
| Workflow | 30-120s | Multi-agent tasks |

---

## Getting Help

### Documentation
- **User Manual**: This document
- **Quick Start**: `QUICK_TEST_SAMPLES.md`
- **Dataset Guide**: `DATASET_REQUIREMENTS.md`
- **API Docs**: http://localhost:8000/docs (when running)

### Support Channels
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check official docs
- **Logs**: `docker-compose logs` for troubleshooting

### Version History
- **v2.0.0** (2025-11-19): Multi-agent platform with 1,699 HK ordinances
- **v1.0.0**: Initial release

---

## Legal Disclaimer

This platform provides AI-generated responses based on document analysis. While we strive for accuracy:

- **Legal Advice**: This is NOT legal advice. Consult qualified legal professionals.
- **Accuracy**: AI responses may contain errors. Verify important information.
- **Currency**: Legal documents may be outdated. Check official sources.
- **Liability**: No warranty provided. Use at your own risk.

---

**End of User Manual**

*Vault AI Platform v2.0.0 - Empowering Intelligent Document Analysis*
