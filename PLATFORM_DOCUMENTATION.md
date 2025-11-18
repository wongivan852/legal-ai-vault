# Legal AI Vault - General-Purpose Workflow Agentic AI Platform

**Version:** 2.0.0
**Last Updated:** 2025-11-18
**Architecture:** Single Unified Application

---

## Table of Contents

1. [Platform Overview](#platform-overview)
2. [Architecture](#architecture)
3. [Agent Catalog](#agent-catalog)
4. [Workflow Catalog](#workflow-catalog)
5. [REST API Reference](#rest-api-reference)
6. [Quick Start Guide](#quick-start-guide)
7. [Integration Guide](#integration-guide)
8. [Adding New Agents](#adding-new-agents)
9. [Adding New Workflows](#adding-new-workflows)
10. [Model Configuration](#model-configuration)

---

## Platform Overview

### What is this Platform?

The **Legal AI Vault** has evolved from a single-purpose Hong Kong legal ordinances RAG system into a **General-Purpose Workflow Agentic AI Platform** - an "AI in the Box" solution that supports multiple business domains through specialized AI agents and orchestrated workflows.

### Key Features

✅ **Multi-Domain Support**: Legal, HR, Customer Service, Finance, and more
✅ **Agentic AI**: Autonomous agents that execute complex multi-step workflows
✅ **Single Application Architecture**: One unified Docker stack for easy deployment
✅ **On-Premises**: 100% private, runs on your infrastructure
✅ **Local LLM**: Uses Ollama with llama3.3:70b (no external API calls)
✅ **Extensible**: Easy to add new agents, workflows, and domains
✅ **REST API**: Full API for external integration
✅ **RAG-Enabled**: Vector database for knowledge retrieval

### Technology Stack

- **LLM Server**: Ollama (llama3.3:70b, nomic-embed-text)
- **Application Framework**: FastAPI (Python async)
- **Vector Database**: Qdrant
- **Relational Database**: PostgreSQL
- **Container Orchestration**: Docker Compose
- **Architecture Pattern**: Agentic AI with Workflow Orchestration

### Use Cases

1. **Legal Research & Compliance**: Search Hong Kong ordinances, check policy compliance
2. **HR Operations**: Employee onboarding, policy queries, benefits information
3. **Customer Service**: Ticket handling, response generation, routing, escalation
4. **Document Analysis**: Multi-source analysis, synthesis, validation
5. **Cross-Domain Workflows**: Combining legal, HR, and business perspectives

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        REST API (FastAPI)                        │
│                    Port 8000 - /api/agents/*                     │
└─────────────────────────────────────────────────────────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
┌───────────▼─────────┐ ┌──────▼───────┐ ┌──────▼───────────┐
│  Workflow           │ │   Agent       │ │   Services       │
│  Orchestrator       │ │   Registry    │ │   - Ollama       │
│  - Multi-agent      │ │   - 7 agents  │ │   - RAG          │
│  - Sequential/      │ │   - Dynamic   │ │   - Database     │
│    Parallel         │ │     loading   │ │                  │
│  - 5 workflows      │ │               │ │                  │
└─────────────────────┘ └───────────────┘ └──────────────────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────▼────────┐  ┌──────────▼─────────┐  ┌────────▼──────┐
│   PostgreSQL   │  │      Qdrant        │  │   Ollama      │
│   Port 5432    │  │   Vector Store     │  │   LLM Server  │
│   - Metadata   │  │   Port 6333        │  │   Port 11434  │
│   - Documents  │  │   - Embeddings     │  │   - llama3.3  │
│   - Sections   │  │   - Similarity     │  │   - nomic     │
└────────────────┘  └────────────────────┘  └───────────────┘
```

### Component Descriptions

**1. REST API Layer (`/api/main.py`, `/api/routes/agents.py`)**
- FastAPI application exposing agents and workflows
- Endpoints for agent execution, workflow execution, health checks
- Auto-loads all agents and workflows on startup

**2. Agent Registry**
- Centralized registry of all available agents
- Lazy initialization for database-dependent agents
- Dynamic agent loading based on request

**3. Workflow Orchestrator (`/api/agents/orchestrator.py`)**
- Coordinates multi-agent workflows
- Sequential task execution with variable resolution
- Context management and result aggregation
- Pre-registered reference workflows

**4. Agents (7 specialized agents)**
- Domain-specific: Legal, HR, Customer Service
- Generic utilities: Analysis, Synthesis, Validation
- Base class providing common functionality

**5. Services**
- **OllamaService**: LLM text generation and embeddings
- **RAGService**: Vector search + retrieval augmented generation
- **Database**: PostgreSQL for metadata, Qdrant for vectors

---

## Agent Catalog

### Overview

The platform includes **7 specialized agents** divided into two categories:

1. **Domain Agents** (3): Specialized for specific business domains
2. **Generic Agents** (3): Cross-domain utility agents
3. **Base Agent**: Abstract foundation for all agents

### Domain Agents

#### 1. Legal Research Agent
- **Name**: `legal_research`
- **Domain**: Legal / Compliance
- **Description**: Searches Hong Kong legal ordinances using RAG
- **Capabilities**:
  - Search ordinances and sections
  - Retrieve legal text with citations
  - Confidence scoring
  - Source attribution
- **Tools**:
  - `search_ordinances`: Full-text search across ordinances
  - `search_sections`: Section-level granular search
  - `get_legal_context`: Retrieve context around specific sections
- **Requirements**: Database + RAG service (initialized on demand)
- **Example Task**:
  ```json
  {
    "question": "What are the requirements for construction insurance?",
    "search_type": "sections",
    "top_k": 5,
    "min_score": 0.5
  }
  ```

#### 2. HR Policy Agent
- **Name**: `hr_policy`
- **Domain**: Human Resources
- **Description**: Handles HR policies, onboarding, benefits queries
- **Capabilities**:
  - Search HR policies and employee handbook
  - Onboarding guidance (by employee type)
  - Benefits information
  - General HR Q&A
- **Tools**:
  - `search_policies`: Search HR policies
  - `get_onboarding_info`: Get onboarding steps
  - `answer_hr_question`: General HR questions
- **Task Types**:
  - `policy_search`: Search for specific policies
  - `onboarding`: Onboarding questions
  - `benefits`: Benefits-related queries
  - `general`: General HR questions
- **Example Task**:
  ```json
  {
    "question": "What is the vacation policy for full-time employees?",
    "task_type": "benefits",
    "employee_type": "full-time"
  }
  ```

#### 3. Customer Service Document Agent
- **Name**: `cs_document`
- **Domain**: Customer Service
- **Description**: CS knowledge base, ticket handling, routing
- **Capabilities**:
  - Search help documentation
  - Generate customer responses
  - Route tickets to appropriate teams
  - Escalate complex issues
- **Tools**:
  - `search_help_docs`: Search help articles
  - `generate_ticket_response`: Generate responses
  - `route_ticket`: Route to appropriate team
  - `escalate_to_human`: Escalate to human agent
- **Task Types**:
  - `search`: Search help documentation
  - `respond`: Generate ticket response
  - `route`: Route ticket to team
  - `escalate`: Escalate to human
- **Example Task**:
  ```json
  {
    "task_type": "respond",
    "ticket": "I can't access my account after password reset",
    "customer_info": {"type": "premium"},
    "priority": "medium",
    "category": "account_access"
  }
  ```

### Generic Utility Agents

#### 4. Analysis Agent
- **Name**: `analysis`
- **Domain**: General (cross-domain)
- **Description**: Analyzes data from any domain
- **Analysis Types**:
  - `themes`: Extract key themes and patterns
  - `comparison`: Compare multiple items
  - `risk`: Identify risks and concerns
  - `summary`: Summarize content
  - `structured`: Extract structured data
- **Output**: Analysis text, insights list, confidence score
- **Example Task**:
  ```json
  {
    "data": {"employee_handbook": "...", "legal_requirements": "..."},
    "analysis_type": "comparison",
    "focus": "Identify gaps between policy and legal requirements"
  }
  ```

#### 5. Synthesis Agent
- **Name**: `synthesis`
- **Domain**: General (cross-domain)
- **Description**: Combines multiple sources into cohesive output
- **Synthesis Types**:
  - `merge`: Combine all sources coherently
  - `reconcile`: Resolve conflicts between sources
  - `report`: Generate structured report
  - `summary`: Create executive summary
- **Output Formats**: `text`, `markdown`, `json`, `structured`
- **Example Task**:
  ```json
  {
    "sources": [
      {"type": "legal", "content": "..."},
      {"type": "hr", "content": "..."}
    ],
    "synthesis_type": "reconcile",
    "output_format": "markdown",
    "focus": "Create compliance report"
  }
  ```

#### 6. Validation Agent
- **Name**: `validation`
- **Domain**: General (cross-domain)
- **Description**: Validates quality and accuracy of outputs
- **Validation Types**:
  - `accuracy`: Check factual accuracy
  - `completeness`: Check if requirements met
  - `consistency`: Check for contradictions
  - `comprehensive`: All validation types
- **Output**: Pass/partial/fail, quality score (0-100), issues list
- **Example Task**:
  ```json
  {
    "content": "Generated response...",
    "validation_type": "comprehensive",
    "requirements": {
      "must_include": ["legal basis", "next steps"],
      "min_length": 200
    },
    "question": "Original question being answered"
  }
  ```

### Agent Comparison Matrix

| Agent | Domain | RAG-Enabled | Tools | Primary Use Case |
|-------|--------|-------------|-------|------------------|
| Legal Research | Legal | ✅ Yes | 3 | Search HK ordinances |
| HR Policy | HR | ❌ No* | 3 | Employee queries, onboarding |
| CS Document | Customer Service | ❌ No* | 4 | Ticket handling, support |
| Analysis | General | ❌ No | 0 | Data analysis, insights |
| Synthesis | General | ❌ No | 0 | Multi-source combination |
| Validation | General | ❌ No | 0 | Quality assurance |

*Can be RAG-enabled by connecting to domain-specific knowledge bases

---

## Workflow Catalog

### Overview

**5 pre-built workflows** demonstrating multi-agent coordination across different use cases.

### 1. HR Onboarding Workflow
- **Name**: `hr_onboarding`
- **Domain**: HR
- **Agents Used**: HR Policy, Analysis, Synthesis, Validation
- **Description**: Complete employee onboarding with personalized guide generation
- **Tasks**:
  1. Gather onboarding steps (HR agent)
  2. Get benefits information (HR agent)
  3. Analyze requirements (Analysis agent)
  4. Synthesize personalized guide (Synthesis agent)
  5. Validate completeness (Validation agent)
- **Input**:
  ```json
  {
    "employee_name": "John Doe",
    "employee_type": "full-time",
    "department": "Engineering",
    "start_date": "2024-01-15"
  }
  ```
- **Output**:
  - Personalized onboarding guide (markdown)
  - Key insights and deadlines
  - Validation score
  - Policy references

### 2. CS Ticket Response Workflow
- **Name**: `cs_ticket_response`
- **Domain**: Customer Service
- **Agents Used**: CS Document, Analysis, Validation
- **Description**: Intelligent ticket handling with sentiment analysis and validation
- **Tasks**:
  1. Analyze ticket sentiment (Analysis agent)
  2. Route ticket to team (CS agent)
  3. Generate response (CS agent)
  4. Validate response quality (Validation agent)
  5. Check escalation needs (CS agent)
- **Input**:
  ```json
  {
    "ticket_content": "Can't access account after password reset",
    "customer_type": "premium",
    "customer_history": "Customer for 2 years, no previous issues",
    "priority": "medium",
    "category": "account_access"
  }
  ```
- **Output**:
  - Generated response
  - Routing recommendation
  - Escalation status
  - Validation score
  - Sentiment analysis

### 3. Legal HR Compliance Workflow
- **Name**: `legal_hr_compliance`
- **Domain**: Cross-Domain (Legal + HR)
- **Agents Used**: HR Policy, Legal Research, Analysis, Synthesis, Validation
- **Description**: Check HR policy compliance against HK law
- **Tasks**:
  1. Retrieve HR policy (HR agent)
  2. Search legal requirements (Legal agent)
  3. Compare policy vs law (Analysis agent)
  4. Synthesize compliance report (Synthesis agent)
  5. Validate analysis (Validation agent)
- **Input**:
  ```json
  {
    "policy_topic": "employee leave and vacation",
    "context": "Review vacation policy for legal compliance"
  }
  ```
- **Output**:
  - Compliance report
  - Gap analysis
  - Legal citations
  - Recommendations
  - Validation score

### 4. Simple Q&A Workflow
- **Name**: `simple_qa`
- **Domain**: General
- **Agents Used**: Any domain agent + Validation
- **Description**: Simple question answering with validation
- **Tasks**:
  1. Answer question (domain agent)
  2. Validate answer (Validation agent)
- **Input**:
  ```json
  {
    "domain": "hr",
    "question": "What is the vacation policy for new employees?",
    "context": "Full-time employee starting next month"
  }
  ```
- **Output**:
  - Answer
  - Validation result
  - Quality score
  - Confidence

### 5. Multi-Agent Research Workflow
- **Name**: `multi_agent_research`
- **Domain**: Cross-Domain
- **Agents Used**: Legal Research, HR Policy, Analysis (2x), Synthesis, Validation
- **Description**: Comprehensive multi-perspective research
- **Tasks**:
  1. Gather legal info (Legal agent)
  2. Gather HR info (HR agent)
  3. Analyze legal perspective (Analysis agent)
  4. Analyze HR perspective (Analysis agent)
  5. Synthesize findings (Synthesis agent)
  6. Validate comprehensive analysis (Validation agent)
- **Input**:
  ```json
  {
    "research_question": "What are the requirements for maternity leave?",
    "context": "Need legal requirements and HR policy aspects"
  }
  ```
- **Output**:
  - Research report
  - Legal perspective + analysis
  - HR perspective + analysis
  - Validation result
  - Quality score

### Workflow Comparison

| Workflow | Agents | Tasks | Complexity | Use Case |
|----------|--------|-------|------------|----------|
| HR Onboarding | 4 | 5 | Medium | Employee onboarding |
| CS Ticket Response | 3 | 5 | Medium | Customer support |
| Legal HR Compliance | 5 | 5 | High | Cross-domain compliance |
| Simple Q&A | 2 | 2 | Low | Basic queries |
| Multi-Agent Research | 4 | 6 | High | Comprehensive research |

---

## REST API Reference

### Base URL
```
http://localhost:8000/api/agents
```

### Agent Endpoints

#### 1. List All Agents
```http
GET /api/agents/
```
**Response**:
```json
{
  "agents": [
    {
      "name": "legal_research",
      "description": "...",
      "tools": [...],
      "domain": "legal"
    },
    ...
  ]
}
```

#### 2. Get Agent Info
```http
GET /api/agents/{agent_name}/info
```
**Example**: `GET /api/agents/hr_policy/info`

#### 3. Execute Agent
```http
POST /api/agents/{agent_name}/execute
```
**Request Body**:
```json
{
  "task": {
    "question": "What is the vacation policy?",
    "task_type": "benefits",
    "employee_type": "full-time"
  }
}
```
**Response**:
```json
{
  "agent": "hr_policy",
  "status": "completed",
  "result": {
    "answer": "...",
    "policy_references": [...],
    "confidence": "high"
  },
  "execution_time": 2.34
}
```

### Workflow Endpoints

#### 4. List Workflows
```http
GET /api/agents/workflows
```
**Response**:
```json
{
  "workflows": [
    "hr_onboarding",
    "cs_ticket_response",
    "legal_hr_compliance",
    "simple_qa",
    "multi_agent_research"
  ]
}
```

#### 5. Get Workflow Info
```http
GET /api/agents/workflows/{workflow_name}
```
**Response**:
```json
{
  "name": "hr_onboarding",
  "description": "...",
  "tasks": [...]
}
```

#### 6. Get Workflow Example
```http
GET /api/agents/workflows/{workflow_name}/example
```
**Response**:
```json
{
  "workflow": "hr_onboarding",
  "description": "...",
  "example_input": {...},
  "usage": "POST /api/agents/workflows/hr_onboarding/execute with this data"
}
```

#### 7. Get All Workflow Examples
```http
GET /api/agents/workflows/examples/all
```

#### 8. Execute Workflow
```http
POST /api/agents/workflows/{workflow_name}/execute
```
**Request Body**:
```json
{
  "input_data": {
    "employee_name": "John Doe",
    "employee_type": "full-time",
    "department": "Engineering"
  }
}
```
**Response**:
```json
{
  "workflow": "hr_onboarding",
  "status": "completed",
  "results": {
    "gather_onboarding_info": {...},
    "get_benefits_info": {...},
    "analyze_requirements": {...},
    "synthesize_guide": {...},
    "validate_guide": {...}
  },
  "output": {
    "onboarding_guide": "...",
    "validation": "passed",
    "quality_score": 92
  },
  "execution_time": 15.67
}
```

### System Endpoints

#### 9. Health Check
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
    ...
  },
  "orchestrator": "ready",
  "total_agents": 7,
  "workflows_registered": 5
}
```

#### 10. Orchestrator Statistics
```http
GET /api/agents/stats
```
**Response**:
```json
{
  "workflows_executed": 42,
  "tasks_executed": 187,
  "average_execution_time": 8.3,
  "success_rate": 0.95
}
```

---

## Quick Start Guide

### Prerequisites
- Docker & Docker Compose installed
- At least 16GB RAM (32GB recommended for llama3.3:70b)
- Ollama with llama3.3:70b and nomic-embed-text models

### 1. Start the Platform
```bash
cd /Users/wongivan/Apps/legal-ai-vault
docker-compose up -d
```

### 2. Check Health
```bash
curl http://localhost:8000/api/agents/health
```

### 3. List Available Agents
```bash
curl http://localhost:8000/api/agents/
```

### 4. Execute a Simple Agent
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

### 5. List Workflows
```bash
curl http://localhost:8000/api/agents/workflows
```

### 6. Get Workflow Example
```bash
curl http://localhost:8000/api/agents/workflows/hr_onboarding/example
```

### 7. Execute a Workflow
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

### 8. Access API Documentation
```
http://localhost:8000/docs
```
Interactive Swagger UI with all endpoints documented.

---

## Integration Guide

### For SI Teams

#### Option 1: REST API Integration
Most common approach - call the REST API from your application:

```python
import requests

# Execute agent
response = requests.post(
    "http://localhost:8000/api/agents/hr_policy/execute",
    json={
        "task": {
            "question": "What is the vacation policy?",
            "task_type": "benefits"
        }
    }
)

result = response.json()
print(result["result"]["answer"])
```

#### Option 2: Python SDK Integration
For Python applications, you can import agents directly:

```python
from agents import HRPolicyAgent, WorkflowOrchestrator
from services.ollama_service import OllamaService

# Initialize
ollama = OllamaService()
hr_agent = HRPolicyAgent(ollama)

# Execute
result = await hr_agent.execute({
    "question": "What is the vacation policy?",
    "task_type": "benefits"
})
```

#### Option 3: Workflow Integration
For complex processes, use pre-built workflows:

```bash
# Get workflow example
curl http://localhost:8000/api/agents/workflows/cs_ticket_response/example

# Execute with your data
curl -X POST http://localhost:8000/api/agents/workflows/cs_ticket_response/execute \
  -d @your_ticket_data.json
```

### Authentication (TODO)
Currently no authentication. For production:
- Add API key authentication
- Implement JWT tokens
- Add role-based access control

### Rate Limiting (TODO)
Not yet implemented. Consider:
- Per-client rate limits
- Concurrent request limits
- Queue management

---

## Adding New Agents

### Step 1: Create Agent Class

Create `/api/agents/your_agent.py`:

```python
from typing import Dict, Any
from agents.base_agent import BaseAgent

class YourAgent(BaseAgent):
    """Your specialized agent"""

    def __init__(self, llm_service, knowledge_base=None):
        super().__init__(
            name="your_agent",
            llm_service=llm_service,
            description="Your agent description"
        )
        self.knowledge_base = knowledge_base

        # Register tools
        self.add_tool("your_tool", self._your_tool, "Tool description")

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent task"""
        # Your implementation here
        question = task.get("question")
        result = await self._process(question)

        return {
            "agent": self.name,
            "status": "completed",
            "answer": result,
            "confidence": "high"
        }

    async def _your_tool(self, param1: str, param2: str) -> str:
        """Your tool implementation"""
        # Tool logic here
        pass
```

### Step 2: Register Agent

Update `/api/agents/__init__.py`:

```python
from agents.your_agent import YourAgent

__all__ = [..., "YourAgent"]
```

### Step 3: Add to Registry

Update `/api/routes/agents.py`:

```python
from agents import YourAgent

_agent_registry = {
    ...,
    "your_agent": {
        "agent": YourAgent(ollama),
        "class": YourAgent,
        "domain": "your_domain"
    }
}
```

### Step 4: Test

```bash
curl http://localhost:8000/api/agents/your_agent/info
```

---

## Adding New Workflows

### Step 1: Define Workflow

Add to `/api/workflows/reference_workflows.py`:

```python
def register_your_workflow(orchestrator):
    workflow_def = {
        "name": "your_workflow",
        "description": "Your workflow description",
        "domain": "your_domain",
        "tasks": [
            {
                "id": "task1",
                "agent": "your_agent",
                "input": {
                    "param": "${input.param}",
                    "task_type": "your_type"
                },
                "description": "First task"
            },
            {
                "id": "task2",
                "agent": "validation",
                "input": {
                    "content": "${task1.answer}",
                    "validation_type": "accuracy"
                },
                "description": "Validate result"
            }
        ],
        "output": {
            "result": "${task1.answer}",
            "validation": "${task2.validation_result}"
        }
    }

    orchestrator.register_workflow("your_workflow", workflow_def)
```

### Step 2: Add Example

```python
def get_workflow_examples():
    return {
        ...,
        "your_workflow": {
            "param": "example value"
        }
    }
```

### Step 3: Register on Startup

Update `register_reference_workflows()`:

```python
def register_reference_workflows(orchestrator):
    # ... existing workflows ...
    register_your_workflow(orchestrator)
```

### Step 4: Test

```bash
curl http://localhost:8000/api/agents/workflows/your_workflow/example
curl -X POST http://localhost:8000/api/agents/workflows/your_workflow/execute -d @input.json
```

---

## Model Configuration

### Current Model Stack

**LLM**: llama3.3:70b (Ollama)
- Reasoning and text generation
- Temperature: 0.3 (configurable)
- Max tokens: 4096 (configurable)

**Embeddings**: nomic-embed-text (Ollama)
- 768-dimensional vectors
- Used for RAG similarity search

### Adding Alternative Models

The client mentioned interest in **Qwen** and **DeepSeek** models. Here's how to add them:

#### Option 1: Ollama Models

If available in Ollama:

1. **Pull the model**:
   ```bash
   ollama pull qwen:14b
   ollama pull deepseek-coder:33b
   ```

2. **Configure in OllamaService** (`/api/services/ollama_service.py`):
   ```python
   def __init__(self, base_url: str = None):
       self.model = os.getenv("LLM_MODEL", "llama3.3:70b")  # Support env var
       self.embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
   ```

3. **Set via environment**:
   ```bash
   export LLM_MODEL=qwen:14b
   docker-compose restart api
   ```

4. **Switch via API**:
   ```bash
   curl -X POST http://localhost:8000/api/models/set \
     -H "Content-Type: application/json" \
     -d '{"model_name": "qwen:14b", "model_type": "llm"}'
   ```

#### Option 2: Multi-Model Support

For production, implement model pooling:

1. **Define model profiles** (`/api/config/models.yaml`):
   ```yaml
   models:
     llama3.3:
       name: llama3.3:70b
       type: llm
       use_case: general
       cost: high
       speed: slow

     qwen:
       name: qwen:14b
       type: llm
       use_case: chinese_language
       cost: medium
       speed: fast

     deepseek:
       name: deepseek-coder:33b
       type: llm
       use_case: code_generation
       cost: medium
       speed: medium
   ```

2. **Implement model selector**:
   ```python
   class ModelSelector:
       def select_model(self, task_type: str, requirements: Dict) -> str:
           if task_type == "code":
               return "deepseek-coder:33b"
           elif requirements.get("language") == "chinese":
               return "qwen:14b"
           else:
               return "llama3.3:70b"
   ```

3. **Agent-level model override**:
   ```python
   class YourAgent(BaseAgent):
       def __init__(self, llm_service, preferred_model="qwen:14b"):
           super().__init__(...)
           self.preferred_model = preferred_model
   ```

### GPU Optimization

Client mentioned RTX GPU. For optimal performance:

1. **Ollama GPU support**: Automatically uses NVIDIA GPU if available
2. **Check GPU usage**:
   ```bash
   nvidia-smi
   ```
3. **Configure memory**:
   ```bash
   export OLLAMA_GPU_MEMORY=24GB
   ```

### Performance Tuning

For faster responses:

1. **Adjust temperature** (lower = faster, less creative):
   ```python
   result = await ollama.generate(prompt, temperature=0.1)
   ```

2. **Reduce max_tokens** (shorter responses):
   ```python
   result = await ollama.generate(prompt, max_tokens=512)
   ```

3. **Use smaller models** for specific tasks:
   - Simple Q&A: qwen:7b or llama3.1:8b
   - Code: deepseek-coder:7b
   - Complex reasoning: llama3.3:70b

---

## Deployment Checklist

### Development Environment ✅
- [x] Agents implemented
- [x] Workflows created
- [x] REST API functional
- [x] Documentation complete

### Production Readiness (TODO)
- [ ] Add authentication/authorization
- [ ] Implement rate limiting
- [ ] Add monitoring and logging
- [ ] Performance optimization
- [ ] Error handling improvements
- [ ] Security audit
- [ ] Load testing
- [ ] Backup and recovery procedures

### SI Team Customization Points

1. **Add domain agents** (Finance, Operations, etc.)
2. **Create customer-specific workflows**
3. **Connect to client knowledge bases**
4. **Customize prompt templates**
5. **Add authentication layer**
6. **Implement audit logging**
7. **Add model selection logic**
8. **Create domain-specific tools**

---

## Support and Contributions

### Getting Help

1. **API Documentation**: http://localhost:8000/docs
2. **Health Check**: http://localhost:8000/api/agents/health
3. **Workflow Examples**: http://localhost:8000/api/agents/workflows/examples/all

### Reporting Issues

Please provide:
- Agent or workflow name
- Input data used
- Error message or unexpected output
- Expected behavior

### Next Steps

Priority enhancements based on client feedback:

1. **Multi-model support** (Qwen, DeepSeek)
2. **Domain expansion** (Finance, Operations)
3. **Knowledge base integration** (HR docs, CS articles)
4. **Authentication & authorization**
5. **Performance monitoring**
6. **Batch processing** for high-volume workflows

---

**Document Version**: 2.0.0
**Platform Version**: 2.0.0
**Last Updated**: 2025-11-18
**Status**: ✅ Ready for SI Team Integration
