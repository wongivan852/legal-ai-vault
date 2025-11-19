# Strategic Pivot: From Legal RAG to Workflow Agentic AI Platform

## Executive Summary

**Current State**: Legal AI Vault - specialized RAG system for HK legal ordinances
**Target State**: General-purpose Workflow Agentic AI Platform ("AI in the Box")
**Timeline**: 4-6 weeks for MVP, 3 months for production-ready
**Impact**: Transform from single-purpose tool to enterprise AI orchestration platform

---

## 1. Vision: Workflow Agentic AI Platform

### What is Workflow Agentic AI?

An autonomous AI system that can:
- **Plan** multi-step workflows to achieve complex goals
- **Execute** tasks using specialized agents with different capabilities
- **Orchestrate** agent collaboration and information sharing
- **Adapt** workflows based on results and feedback
- **Integrate** with external tools, APIs, and data sources
- **Learn** from execution history to improve performance

### Key Differentiators from Current System

| Current (Legal RAG) | Target (Agentic Platform) |
|---------------------|---------------------------|
| Single-purpose: Legal search | Multi-purpose: Any workflow |
| One-shot Q&A | Multi-step task execution |
| Human drives each query | AI autonomously plans steps |
| No memory between queries | Persistent context & memory |
| Legal domain only | Domain-agnostic |
| No tool integration | Rich tool ecosystem |

---

## 2. Architecture Transformation

### Current Architecture
```
User Query → RAG Service → [Vector Search + LLM] → Answer
```

### Target Agentic Architecture
```
User Goal
    ↓
Workflow Planner (llama3.3:70b)
    ↓
[Task Queue] → Agent Orchestrator
    ↓
┌─────────────────────────────────────────┐
│  Specialized Agents:                    │
│  • Research Agent (RAG-powered)         │
│  • Analysis Agent (data processing)     │
│  • Code Agent (script generation)       │
│  • Integration Agent (API calls)        │
│  • Legal Agent (existing RAG)           │
│  • Custom Domain Agents...              │
└─────────────────────────────────────────┘
    ↓
Tool Ecosystem (APIs, DBs, Functions)
    ↓
Results Aggregator → User
```

---

## 3. Core Components to Build

### 3.1 Agent Orchestration Engine
**Purpose**: Coordinate multiple agents, manage workflow state

**Key Features**:
- Task decomposition & planning
- Agent selection based on capabilities
- Inter-agent communication
- State management & checkpointing
- Error handling & retry logic
- Parallel execution where possible

**Tech Stack**:
- LangGraph for workflow orchestration
- Redis for task queue & state
- PostgreSQL for workflow persistence

### 3.2 Agent Framework
**Purpose**: Template for creating new specialized agents

**Base Agent Capabilities**:
- Access to llama3.3:70b for reasoning
- Vector memory (Qdrant) for context
- Tool calling interface
- Structured output formatting
- Self-reflection & validation

**Agent Types to Support**:
1. **Reasoning Agents**: Complex analysis, planning
2. **Retrieval Agents**: RAG-based search (like current legal)
3. **Action Agents**: Execute tasks, call APIs
4. **Synthesis Agents**: Combine multiple sources
5. **Validation Agents**: Check outputs, ensure quality

### 3.3 Tool Integration Layer
**Purpose**: Enable agents to use external tools & APIs

**Tool Categories**:
- **Data Access**: SQL, vector DBs, file systems
- **Web Services**: REST APIs, webhooks
- **Code Execution**: Python, shell scripts
- **Document Processing**: PDF, DOCX, spreadsheets
- **Communication**: Email, Slack, notifications
- **Domain-Specific**: Legal databases, CRM systems, etc.

**Implementation**:
```python
class ToolRegistry:
    """Central registry of available tools"""

    @staticmethod
    def register_tool(name, description, function):
        """Register a new tool for agents to use"""

    @staticmethod
    def get_tool_descriptions() -> str:
        """Get formatted tool descriptions for LLM"""

    @staticmethod
    def execute_tool(name, **kwargs):
        """Execute a tool with parameters"""
```

### 3.4 Workflow Management System
**Purpose**: Define, execute, and monitor workflows

**Database Schema**:
```sql
-- Workflow definitions
CREATE TABLE workflows (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    workflow_definition JSONB,  -- DAG of tasks
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Workflow executions
CREATE TABLE workflow_executions (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER REFERENCES workflows(id),
    status VARCHAR(50),  -- pending, running, completed, failed
    input_data JSONB,
    output_data JSONB,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Task executions
CREATE TABLE task_executions (
    id SERIAL PRIMARY KEY,
    workflow_execution_id INTEGER,
    agent_name VARCHAR(100),
    task_type VARCHAR(50),
    input_data JSONB,
    output_data JSONB,
    status VARCHAR(50),
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Agent memory/context
CREATE TABLE agent_memory (
    id SERIAL PRIMARY KEY,
    execution_id INTEGER,
    agent_name VARCHAR(100),
    memory_type VARCHAR(50),  -- short_term, long_term, episodic
    content JSONB,
    vector_id VARCHAR(100),  -- Reference to Qdrant
    created_at TIMESTAMP
);
```

### 3.5 Workflow Builder UI
**Purpose**: Visual interface to create and monitor workflows

**Features**:
- Drag-and-drop workflow designer
- Pre-built workflow templates
- Real-time execution monitoring
- Agent performance analytics
- Tool marketplace/catalog

---

## 4. Migration Strategy

### Phase 1: Foundation (Week 1-2)
**Goal**: Build core orchestration infrastructure

Tasks:
1. ✅ Install LangGraph/LangChain for agent orchestration
2. ✅ Create base Agent class with llama3.3:70b integration
3. ✅ Implement task queue (Redis or PostgreSQL)
4. ✅ Build workflow state management
5. ✅ Create basic orchestrator loop

**Deliverable**: Simple 2-agent workflow (planner → executor)

### Phase 2: Agent Ecosystem (Week 3-4)
**Goal**: Build specialized agents and tool system

Tasks:
1. ✅ Migrate existing Legal RAG as "Legal Research Agent"
2. ✅ Create Web Search Agent (integrate SerpAPI/Tavily)
3. ✅ Create Code Agent (execute Python scripts)
4. ✅ Create Data Agent (SQL query generation)
5. ✅ Build Tool Registry and execution framework

**Deliverable**: 4-5 working agents with tool integration

### Phase 3: Workflow System (Week 5-6)
**Goal**: Workflow management and persistence

Tasks:
1. ✅ Database schema for workflows
2. ✅ Workflow definition language (JSON/YAML)
3. ✅ Workflow executor with checkpointing
4. ✅ API endpoints for workflow CRUD
5. ✅ Pre-built workflow templates

**Deliverable**: Workflow API + 3 example workflows

### Phase 4: UI & Polish (Week 7-8)
**Goal**: User interface for workflow creation

Tasks:
1. ✅ React workflow builder (or use existing tool)
2. ✅ Execution monitoring dashboard
3. ✅ Agent marketplace/catalog
4. ✅ Documentation and examples

**Deliverable**: Production-ready platform

---

## 5. Leveraging Existing Infrastructure

### What We Keep (90% reusable):
✅ **Ollama + llama3.3:70b**: Perfect for agent reasoning
✅ **PostgreSQL**: Extend for workflow state
✅ **Qdrant**: Agent memory & semantic search
✅ **FastAPI**: Add agent/workflow endpoints
✅ **Docker**: Container orchestration
✅ **Legal RAG**: Becomes "Legal Agent" in ecosystem

### What Changes:
🔄 **Frontend**: Legal search UI → Workflow dashboard
🔄 **API Layer**: Single RAG endpoint → Agent orchestration API
🔄 **Service Layer**: RAG service → Agent framework
🆕 **Orchestration**: Add LangGraph/task queue
🆕 **Tool System**: Plugin architecture for tools

---

## 6. Example Workflows (Use Cases)

### 6.1 Legal Due Diligence Workflow
```yaml
workflow: "Company Due Diligence"
goal: "Research legal compliance for Hong Kong company"

steps:
  1. Research Agent:
     - Search company records
     - Find relevant ordinances
  2. Analysis Agent:
     - Check compliance status
     - Identify regulatory gaps
  3. Report Agent:
     - Generate structured report
     - Include citations
  4. Validation Agent:
     - Verify all claims
     - Check data accuracy
```

### 6.2 Multi-Source Research Workflow
```yaml
workflow: "Comprehensive Research"
goal: "Answer complex question using multiple sources"

steps:
  1. Planner Agent:
     - Decompose question into sub-questions
  2. Parallel Execution:
     - Legal Agent: Search HK ordinances
     - Web Agent: Search internet
     - Database Agent: Query internal data
  3. Synthesis Agent:
     - Combine all findings
     - Resolve conflicts
     - Generate comprehensive answer
```

### 6.3 Automated Contract Analysis
```yaml
workflow: "Contract Review"
goal: "Analyze contract and flag issues"

steps:
  1. Document Agent:
     - Extract text from PDF
     - Identify contract type
  2. Legal Agent:
     - Find relevant regulations
     - Check standard clauses
  3. Analysis Agent:
     - Compare against templates
     - Flag unusual terms
  4. Risk Agent:
     - Assess compliance risks
     - Generate risk report
```

---

## 7. Technical Architecture Details

### 7.1 Agent Communication Protocol
```python
class AgentMessage:
    """Standard message format between agents"""
    sender: str
    recipient: str
    message_type: str  # task, result, question, notification
    content: dict
    context: dict
    timestamp: datetime
```

### 7.2 Tool Calling Interface
```python
class ToolCall:
    """LLM generates tool calls in this format"""
    tool_name: str
    parameters: dict
    reasoning: str  # Why this tool was chosen

# Example LLM output:
{
  "thought": "I need to search legal database for building regulations",
  "tool_calls": [
    {
      "tool_name": "legal_search",
      "parameters": {
        "query": "building safety requirements",
        "doc_types": ["ordinance"],
        "top_k": 5
      },
      "reasoning": "Building regulations are in ordinances"
    }
  ]
}
```

### 7.3 Workflow Definition Format
```json
{
  "workflow_id": "legal_research_v1",
  "name": "Legal Research Workflow",
  "description": "Multi-step legal research with validation",
  "input_schema": {
    "question": "string",
    "jurisdiction": "string",
    "depth": "enum[quick, standard, comprehensive]"
  },
  "tasks": [
    {
      "task_id": "plan",
      "agent": "planner",
      "input": "${workflow.input}",
      "output_var": "research_plan"
    },
    {
      "task_id": "search",
      "agent": "legal_rag",
      "input": {
        "query": "${plan.search_queries}",
        "top_k": 10
      },
      "output_var": "search_results"
    },
    {
      "task_id": "analyze",
      "agent": "analyst",
      "input": {
        "question": "${workflow.input.question}",
        "sources": "${search.results}"
      },
      "output_var": "analysis"
    },
    {
      "task_id": "validate",
      "agent": "validator",
      "input": "${analyze.output}",
      "output_var": "validated_result"
    }
  ],
  "output": "${validate.validated_result}"
}
```

---

## 8. Recommended Tech Stack Additions

### Core Orchestration
- **LangGraph**: Workflow orchestration (best for complex DAGs)
- **LangChain**: Agent framework & tool integrations
- **Redis**: Task queue & caching (alternative: use PostgreSQL)

### Agent Tools
- **SerpAPI** or **Tavily**: Web search
- **Firecrawl**: Web scraping
- **Pandas**: Data analysis
- **SQLAlchemy**: Database access
- **Requests**: API calls

### Workflow UI
- **React Flow**: Workflow builder (drag-and-drop)
- **D3.js**: Visualization
- **WebSockets**: Real-time updates

### Optional Enhancements
- **Celery**: Distributed task execution
- **MLflow**: Experiment tracking
- **Prometheus + Grafana**: Monitoring

---

## 9. Competitive Advantages

### vs. Commercial Platforms (Zapier, Make.com)
✅ **AI-native**: Agents plan workflows, not just execute
✅ **On-premise**: Full data control ("AI in the Box")
✅ **Reasoning**: llama3.3:70b for complex logic
✅ **Customizable**: Add domain-specific agents

### vs. AI Platforms (LangChain Cloud, AutoGPT)
✅ **Production-ready**: Docker, monitoring, UI included
✅ **Enterprise features**: Authentication, audit logs
✅ **Domain knowledge**: Pre-built legal agent
✅ **Cost-effective**: No API costs, runs locally

---

## 10. Business Value Propositions

### For Legal Teams
- Automated due diligence workflows
- Multi-jurisdiction legal research
- Contract analysis pipelines
- Compliance monitoring agents

### For Enterprises
- Customer support automation
- Data analysis workflows
- Report generation pipelines
- Integration orchestration

### For Developers
- Reusable agent marketplace
- Custom workflow templates
- API-first architecture
- Extensible tool ecosystem

---

## 11. Next Steps & Decision Points

### Immediate Actions (This Week)
1. ✅ Review and approve architecture plan
2. ✅ Choose orchestration framework (LangGraph recommended)
3. ✅ Define 3-5 priority workflows for MVP
4. ✅ Allocate development resources

### Key Decisions Needed
1. **Scope**: Start with 5 agents or 10+?
2. **UI**: Build custom or use existing tool (e.g., n8n, Temporal)?
3. **Deployment**: Single tenant or multi-tenant?
4. **Licensing**: Open-source or proprietary?

### Success Metrics
- **Week 2**: First 2-agent workflow running
- **Week 4**: 5 agents + tool system
- **Week 6**: 3 workflows deployable
- **Week 8**: Production UI launched

---

## 12. Risk Mitigation

### Technical Risks
| Risk | Mitigation |
|------|------------|
| llama3.3:70b too slow | Implement task queue, use smaller models for simple tasks |
| Agent hallucination | Validation agents, structured outputs, citations |
| Workflow complexity | Start simple, add complexity incrementally |
| Integration failures | Robust error handling, retry logic |

### Business Risks
| Risk | Mitigation |
|------|------------|
| Scope creep | Strict MVP definition, phased rollout |
| Adoption challenges | Excellent documentation, templates |
| Competition | Focus on "AI in Box" differentiator |

---

## Conclusion

The pivot from Legal RAG to Workflow Agentic AI Platform is **highly feasible** with existing infrastructure. The current system provides an excellent foundation:

- ✅ llama3.3:70b for powerful agent reasoning
- ✅ Vector database for agent memory
- ✅ Production-ready backend
- ✅ Proven legal domain expertise

**Recommendation**: Proceed with 8-week phased approach, starting with foundational orchestration in Week 1-2.

---

**Document Version**: 1.0
**Date**: November 18, 2025
**Author**: Legal AI Vault Development Team
