# 📚 Vault AI Platform - Documentation Index

**Complete Guide to All Available Documentation**

---

## 🎓 Getting Started (For Beginners)

### 1. **Workflow Quick Reference Card**
📄 File: `WORKFLOW_QUICK_REFERENCE.md`

**Best for:** Quick lookup of common patterns and syntax
**Read time:** 5 minutes
**Contents:**
- Agent names and their correct spelling
- Basic workflow template (copy-paste ready)
- Common task builder patterns
- Quick troubleshooting guide
- File locations

👉 **Start here if:** You need a quick reminder of syntax or agent names

---

### 2. **Complete Workflow Creation Guide**
📄 File: `WORKFLOW_CREATION_GUIDE.md`

**Best for:** Learning how to create workflows from scratch
**Read time:** 30-60 minutes
**Contents:**
- What workflows are and why use them
- Detailed explanation of all 6 agents
- Step-by-step tutorial (create your first workflow)
- Advanced patterns and techniques
- Frontend integration (HTML + JavaScript)
- Complete working examples
- Troubleshooting common issues
- Testing strategies

👉 **Start here if:** You're new to coding or new to the workflow system

**Table of Contents:**
1. Introduction
2. Understanding the Workflow System
3. Prerequisites
4. Available Agents
5. Step-by-Step: Creating Your First Workflow
6. Advanced Workflow Patterns
7. Frontend Integration
8. Testing Your Workflow
9. Troubleshooting
10. Complete Examples

---

## 🔧 Technical Reference

### 3. **API Documentation (Interactive)**
🌐 URL: http://localhost:8000/docs

**Best for:** Testing API endpoints and understanding request/response formats
**Interactive:** Yes - you can test endpoints directly in the browser

**Available Endpoints:**

#### Agent Endpoints
- `GET /api/agents/` - List all agents
- `POST /api/agents/{agent_name}/execute` - Execute a specific agent
- `GET /api/agents/{agent_name}/info` - Get agent capabilities
- `GET /api/agents/health` - Check agent system health

#### Workflow Endpoints
- `GET /api/workflows/` - List all workflows
- `GET /api/workflows/{workflow_id}` - Get workflow details
- `POST /api/workflows/{workflow_id}/execute` - Execute a workflow
- `GET /api/workflows/{workflow_id}/schema` - Get input schema

#### Core Endpoints
- `GET /health` - System health check
- `POST /api/generate` - Direct LLM text generation
- `POST /api/rag` - RAG query (legal research)
- `GET /api/models` - List available AI models

👉 **Use this when:** You want to test API calls or understand exact request formats

---

### 4. **Source Code Documentation**

#### Backend Files

**Core Workflow System:**
```
/api/workflows/
├── workflow_engine.py        # Core orchestration engine
├── workflow_definitions.py   # All workflow definitions (EDIT THIS)
└── __init__.py              # Package initialization
```

**Agent Implementations:**
```
/api/agents/
├── __init__.py                      # Agent registry
├── base_agent.py                    # Base agent class
├── legal_research_agent.py          # Legal research agent
├── hr_policy_agent.py               # HR policy agent
├── cs_document_agent.py             # Customer service agent
├── analysis_agent.py                # Analysis agent
├── synthesis_agent_enhanced.py      # Synthesis agent
└── validation_agent.py              # Validation agent
```

**API Routes:**
```
/api/routes/
├── agents.py       # Agent API endpoints
└── workflows.py    # Workflow API endpoints
```

#### Frontend Files

**User Interface:**
```
/frontend/
├── index.html           # Main UI (add workflow forms here)
└── static/
    ├── css/style.css    # Styling
    └── js/app.js        # JavaScript (add workflow handlers here)
```

---

## 📖 Learning Path

### For Complete Beginners

**Path 1: Learn by Example (Recommended)**
1. Read Quick Reference Card (5 min)
2. Study one existing workflow in `workflow_definitions.py` (10 min)
3. Follow Step-by-Step Guide sections 1-5 (30 min)
4. Create your first simple 2-step workflow (60 min)
5. Test and iterate

**Path 2: Comprehensive Learning**
1. Read entire Workflow Creation Guide (60 min)
2. Study all 5 existing workflows (30 min)
3. Review API documentation (20 min)
4. Create 3 simple workflows for practice (2-3 hours)

---

### For Experienced Developers

**Quick Start:**
1. Skim Quick Reference Card (2 min)
2. Read "Advanced Workflow Patterns" section (10 min)
3. Check API docs for endpoint details (5 min)
4. Build your workflow

---

## 🧪 Testing & Development

### Local Development Environment

**Start the platform:**
```bash
cd /Users/wongivan/Apps/legal-ai-vault
docker-compose up -d
```

**Restart after changes:**
```bash
docker-compose restart api
```

**View logs:**
```bash
docker-compose logs -f api
```

**Stop platform:**
```bash
docker-compose down
```

### Testing Tools

**1. Browser DevTools (F12)**
- Console: See JavaScript errors
- Network: View API calls
- Elements: Inspect HTML

**2. API Testing (Command Line)**
```bash
# Test workflow
curl -X POST http://localhost:8000/api/workflows/hr_onboarding/execute \
  -H "Content-Type: application/json" \
  -d '{"input": {"employee_name": "John"}}'

# Test agent
curl -X POST http://localhost:8000/api/agents/legal_research/execute \
  -H "Content-Type: application/json" \
  -d '{"task": {"question": "test"}}'
```

**3. Interactive API Docs**
- Visit: http://localhost:8000/docs
- Click endpoint → "Try it out" → Fill form → "Execute"

---

## 🎯 Common Tasks Quick Guide

### Task: Create a New Workflow

**Files to Edit:**
1. `/api/workflows/workflow_definitions.py` - Add workflow function
2. `/api/workflows/workflow_definitions.py` - Register in `get_all_workflows()`
3. `/frontend/index.html` - Add UI form
4. `/frontend/static/js/app.js` - Add JavaScript handler

**Steps:**
1. Define workflow function (backend)
2. Register workflow (backend)
3. Restart API: `docker-compose restart api`
4. Add HTML form (frontend)
5. Add JS handler (frontend)
6. Refresh browser
7. Test

**Reference:** See "Step-by-Step: Creating Your First Workflow" in main guide

---

### Task: Modify Existing Workflow

**Files to Edit:**
1. `/api/workflows/workflow_definitions.py` - Modify workflow function

**Steps:**
1. Find workflow function (e.g., `create_hr_onboarding_workflow()`)
2. Modify steps, task builders, or descriptions
3. Save file
4. Restart API: `docker-compose restart api`
5. Test changes

**Warning:** Changes affect all users of that workflow

---

### Task: Add UI Form for Workflow

**Files to Edit:**
1. `/frontend/index.html` - Add form HTML
2. `/frontend/static/js/app.js` - Add form handler

**Steps:**
1. Copy existing workflow form as template
2. Change IDs to match your workflow
3. Update field names
4. Add JavaScript handler
5. Refresh browser
6. Test form submission

**Reference:** See "Frontend Integration" in main guide

---

### Task: Test Workflow Without UI

**Use API directly:**

```bash
# Simple test
curl -X POST http://localhost:8000/api/workflows/YOUR_WORKFLOW_ID/execute \
  -H "Content-Type: application/json" \
  -d '{"input": {"question": "test"}}'

# Formatted output
curl -X POST http://localhost:8000/api/workflows/YOUR_WORKFLOW_ID/execute \
  -H "Content-Type: application/json" \
  -d '{"input": {"question": "test"}}' | python3 -m json.tool
```

---

### Task: Debug Workflow Issues

**Check in this order:**

1. **API Logs**
   ```bash
   docker-compose logs -f api
   ```
   Look for error messages

2. **Browser Console (F12)**
   - Check for JavaScript errors
   - Verify form submission

3. **Network Tab (F12)**
   - Check API request was sent
   - View request/response

4. **API Response**
   - Each step shows status
   - Error field shows what failed

**Common Issues:** See "Troubleshooting" section in main guide

---

## 📋 Available Workflows (Examples)

All workflows are defined in `/api/workflows/workflow_definitions.py`

### 1. HR Employee Onboarding (`hr_onboarding`)
**Steps:** HR Policy → Analysis → Synthesis
**Purpose:** Create personalized onboarding guides
**Use case:** New employee onboarding

### 2. CS Ticket Response (`cs_ticket`)
**Steps:** CS Response → Sentiment Analysis → Final Response
**Purpose:** Generate empathetic customer support responses
**Use case:** Customer support tickets

### 3. Legal-HR Compliance (`legal_hr_compliance`)
**Steps:** Legal Research → Validation → Compliance Report
**Purpose:** Check HR policies against legal requirements
**Use case:** Compliance audits

### 4. Simple Q&A (`simple_qa`)
**Steps:** Legal Research → Validation
**Purpose:** Answer questions with accuracy verification
**Use case:** Quick legal questions

### 5. Multi-Agent Research (`multi_agent_research`)
**Steps:** Legal + HR + CS → Analysis → Synthesis
**Purpose:** Comprehensive multi-perspective analysis
**Use case:** Complex research projects

**Study these for examples!**

---

## 🔗 External Resources

### AI Models (Ollama)
- List models: `curl http://localhost:11434/api/tags`
- Current model: `llama3.3:70b` (LLM)
- Embedding model: `nomic-embed-text`

### Vector Database (Qdrant)
- Dashboard: http://localhost:6333/dashboard
- Collections: Legal ordinances, documents

### Platform URLs
- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

## 💡 Tips for Success

### Best Practices

1. **Start Small**
   - Begin with 2-step workflows
   - Test each step individually
   - Gradually add complexity

2. **Use Existing Code**
   - Copy from existing workflows
   - Modify for your needs
   - Don't reinvent the wheel

3. **Test Frequently**
   - Test after each change
   - Use curl for quick API tests
   - Check logs for errors

4. **Document Your Work**
   - Add clear descriptions
   - Comment complex logic
   - Update this index if needed

5. **Learn from Errors**
   - Read error messages carefully
   - Check troubleshooting guide
   - Study working examples

---

## 🆘 Getting Help

### Resources in Order

1. **Quick Reference Card** - Fast syntax lookup
2. **Troubleshooting Section** - Common errors and fixes
3. **Complete Examples** - Working code to study
4. **API Documentation** - Endpoint details
5. **Source Code** - Ultimate reference

### Common Questions

**Q: Where do I start?**
A: Read the Quick Reference Card, then follow the Step-by-Step guide.

**Q: How do I know what format each agent expects?**
A: See "Available Agents" section in main guide - includes all input/output formats.

**Q: My workflow doesn't appear in the UI**
A: Check you registered it in `get_all_workflows()` and restarted the API.

**Q: Form submission does nothing**
A: Check browser console (F12) for JavaScript errors.

**Q: Workflow executes but fails**
A: Check API logs (`docker-compose logs api`) for the error.

---

## 📌 Version History

**Version 1.0** (November 2025)
- Initial documentation
- Complete workflow creation guide
- Quick reference card
- API documentation
- 5 example workflows

---

## 🎯 Next Steps

**For Beginners:**
1. ✅ Read Quick Reference Card
2. ✅ Follow Step-by-Step tutorial
3. ✅ Create your first workflow
4. ✅ Study existing workflows
5. ✅ Experiment and iterate

**For Developers:**
1. ✅ Review API documentation
2. ✅ Study workflow_definitions.py
3. ✅ Build custom workflows
4. ✅ Integrate with frontend
5. ✅ Share with team

---

**📚 Happy Learning!**

All documentation is accurate as of November 2025 and reflects the current state of the Vault AI Platform.

For questions or issues, refer to the troubleshooting sections in the main guide.
