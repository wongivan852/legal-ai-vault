# Legal AI Vault - Comprehensive User Manual
**Version:** 1.0
**Last Updated:** 2025-11-20
**Platform:** Legal AI Research & Analysis Platform

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Overview](#2-system-overview)
3. [Getting Started](#3-getting-started)
4. [Core Features](#4-core-features)
5. [Using AI Agents](#5-using-ai-agents)
6. [Custom Workflows](#6-custom-workflows)
7. [Understanding Results](#7-understanding-results)
8. [Best Practices](#8-best-practices)
9. [Troubleshooting](#9-troubleshooting)
10. [Technical Reference](#10-technical-reference)

---

## 1. Introduction

### What is Legal AI Vault?

Legal AI Vault is an intelligent legal research platform that combines artificial intelligence with Hong Kong's comprehensive legal database. The platform enables users to:

- **Research legal questions** using natural language queries
- **Validate content quality** with multi-dimensional analysis
- **Create custom workflows** for specialized legal research tasks
- **Access 1,699 Hong Kong ordinances** with instant semantic search
- **Analyze legal documents** across multiple dimensions

### Key Capabilities

✅ **Natural Language Processing**: Ask questions in plain English
✅ **Semantic Search**: Find relevant legal sections by meaning, not just keywords
✅ **Multi-Agent System**: 6 specialized AI agents for different tasks
✅ **Quality Validation**: Automated accuracy and consistency checking
✅ **Custom Workflows**: Build multi-step research processes
✅ **Source Citations**: Every answer includes relevant ordinance references

### Who Should Use This Platform?

- Legal researchers and paralegals
- Law students and academics
- Legal compliance officers
- Building management professionals
- Anyone researching Hong Kong law

---

## 2. System Overview

### Architecture Components

- **Frontend**: Web-based user interface
- **Backend**: FastAPI with 6 specialized AI agents
- **Database**: PostgreSQL with 1,699 HK ordinances, 11,288 sections
- **Vector Store**: Qdrant for semantic search
- **AI Engine**: Ollama with LLaMA 3.1 8B model

### Data Coverage

- **Total Ordinances**: 1,699 Hong Kong legal documents
- **Legal Sections**: 11,288 indexed sections
- **Categories**: Main ordinances and subsidiary legislation
- **Language**: English versions
- **Update Date**: August 2024 snapshot

---

## 3. Getting Started

### Accessing the Platform

1. Open web browser
2. Navigate to: `http://localhost:8000`
3. Main dashboard displays with AI Agents and Custom Workflows

---

## 4. Core Features

### 4.1 Semantic Search (RAG)

The platform uses Retrieval Augmented Generation:
1. Question converted to vector embedding
2. Search 11,288 legal sections
3. Retrieve top 5 most relevant sections
4. AI generates answer with citations

### 4.2 Agent-Based Architecture

| Agent | Purpose |
|-------|---------|
| Legal Research | Search HK ordinances |
| Validation | Quality checking |
| HR Policy | HR queries |
| CS Document | Customer service |
| Analysis | Document analysis |
| Synthesis | Multi-source synthesis |

### 4.3 Multi-Dimensional Validation

Three validation dimensions:
- **Accuracy** (0-100): Factual correctness
- **Completeness** (0-100): Coverage assessment
- **Consistency** (0-100): Logical consistency

---

## 5. Using AI Agents

### 5.1 Legal Research Agent

**Step-by-Step:**
1. Click "Legal Research" in sidebar
2. Enter your legal question
3. Click "Execute"
4. Wait 55-88 seconds
5. Review answer and sources

**Example Question:**
"What are the responsibilities of incorporated owners when a flat owner receives a removal order from the Building Department?"

**Result Includes:**
- Natural language answer
- 5 relevant source documents
- Relevance scores (0.60-0.70)
- Section numbers and headings
- Confidence rating
- Execution time

**Best Practices:**
✅ Be specific in questions
✅ Use legal terminology when known
✅ Ask one focused question at a time
❌ Don't ask multiple unrelated questions
❌ Don't expect non-HK jurisdiction answers

### 5.2 Validation Agent

**Step-by-Step:**
1. Click "Validation" in sidebar
2. Paste content to validate
3. Click "Execute"
4. Wait ~120 seconds
5. Review validation report

**Result Includes:**
- Overall quality score (0-100)
- Accuracy, Completeness, Consistency scores
- List of issues found
- Recommendations for improvement
- Validation status (Passed/Partial/Failed)

**Quality Score Ranges:**
- 80-100: Excellent
- 60-79: Good
- 40-59: Moderate
- 0-39: Poor

---

## 6. Custom Workflows

### What Are Workflows?

Multi-step processes that chain agents together. Output from one step becomes input to the next.

### Example: Building Ordinance Check

**2-Step Workflow:**
1. Legal Search: Research the question
2. Legal Validate: Check answer quality

**Execution Time:** ~178 seconds total

### Using Workflows

1. Click "Custom Workflows" tab
2. Select workflow (e.g., "Building Ordinance Check")
3. Fill in required fields
4. Click "Execute Workflow"
5. Watch progress through each step
6. Review aggregated results

---

## 7. Understanding Results

### Legal Research Results

**Answer Section:**
- Natural language explanation
- Cites specific legal sections
- Acknowledges limitations
- Includes disclaimer

**Sources Section:**
Each source shows:
- Document number (e.g., "Cap. 131")
- Section number and heading
- Relevance score (0.60-0.70)
- Text preview

**Confidence Levels:**
- High: Direct answer found
- Medium: Requires interpretation
- Low: Limited information

### Validation Reports

**Excellent (80-100):**
```
✅ PASSED                Quality: 92/100
No issues found
Minor enhancements suggested
```

**Poor (0-39):**
```
❌ FAILED                Quality: 18/100
Major issues found
Significant revision required
```

### Execution Times

| Operation | Duration |
|-----------|----------|
| Legal Research | 55-88 seconds |
| Validation | 120-130 seconds |
| 2-Step Workflow | 175-200 seconds |

---

## 8. Best Practices

### Effective Queries

**✅ Good:**
"What are the notice requirements for removal of unauthorized building works under the Building Management Ordinance?"

**❌ Poor:**
"Tell me about building law"

### Legal Research Workflow

1. Formulate clear question
2. Execute legal research
3. Validate critical information
4. Cross-reference sources
5. Consult legal professional

### Quality Assurance

**Before Relying on Results:**
- Check relevance scores (>0.65)
- Verify citations
- Review confidence ratings
- Consider validation for critical content
- Seek professional review

**Red Flags:**
- Low confidence rating
- No source citations
- Contradictory information
- Relevance scores <0.60

---

## 9. Troubleshooting

### Common Issues

**Slow Response:**
- Wait for completion (normal: 1-3 minutes)
- Simplify complex queries
- Check system health

**No Relevant Sources:**
- Rephrase with different terms
- Broaden question scope
- Use general legal terms

**Validation Parsing Issues:**
- Handled automatically by fallback
- Review consistency scores
- System still provides feedback

**Workflow Fails:**
- Check required fields filled
- Retry workflow
- Try individual agents first

### Health Check

Visit: `http://localhost:8000/health`

---

## 10. Technical Reference

### System Requirements

**Client:**
- Modern browser
- JavaScript enabled
- 1280x720 minimum resolution

**Server:**
- Docker
- 8GB RAM minimum (16GB recommended)
- 50GB disk space

### API Endpoints

```
GET  /health
POST /api/agents/{agent_name}/execute
POST /api/workflows/{workflow_id}/execute
GET  /api/workflows
```

### Environment Variables

```bash
DB_USER=legal_vault_user
DATABASE_URL=postgresql://...
OLLAMA_HOST=http://ollama:11434
QDRANT_HOST=qdrant
```

---

## Legal Disclaimer

⚠️ **IMPORTANT LEGAL NOTICE**

This platform provides **research assistance only** and does not constitute legal advice. Users should:

- Verify all information against official sources
- Consult qualified legal professionals
- Not rely solely on AI-generated content
- Understand laws may be more recent than dataset
- Recognize AI limitations in legal interpretation

---

## Quick Reference

### Common Tasks

| Task | Steps |
|------|-------|
| Research question | Agents → Legal Research → Enter → Execute |
| Validate content | Agents → Validation → Paste → Execute |
| Run workflow | Workflows → Select → Fill → Execute |

### Support

- System Health: `/health` endpoint
- Validation Report: `SYSTEM_VALIDATION_REPORT.md`
- GitHub: wongivan852/legal-ai-vault

---

**End of User Manual**

Version 1.0 - 2025-11-20
