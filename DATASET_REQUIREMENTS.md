# Dataset Requirements for Vault AI Platform Testing

**Platform**: Vault AI Platform v2.0.0
**Date**: 2025-11-19

---

## Overview

The Vault AI Platform has **6 specialized agents** that require different types of data for testing. This document outlines what datasets are currently available and what additional datasets you may need to create for comprehensive testing.

---

## Current Dataset Status

### ✅ Available Datasets

#### 1. **HK Legal Ordinances** (Legal Research Agent)
**Status**: ✅ **IMPORTED & READY**

| Metric | Value |
|--------|-------|
| Documents | 1,699 ordinances |
| Sections | 11,288 legal sections |
| Vector Embeddings | 12,987 (768-dim) |
| Data Location | `/app/data/hkel_legal_import/` |
| Database | PostgreSQL + Qdrant |

**Agent**: Legal Research Agent
**Use Cases**:
- Search Hong Kong legal ordinances
- Find specific legal provisions
- RAG-powered legal analysis
- Multi-document legal research

**Test Queries**:
```json
{
  "task": {
    "task_type": "search",
    "question": "What are the insurance requirements for construction under Building Management Ordinance?"
  }
}
```

---

### ⚠️ Missing Datasets (Need to be Created)

The following agents are **operational** but don't have dedicated datasets loaded. They work with any text/document content you provide in the API request.

#### 2. **HR Policy Documents** (HR Policy Agent)
**Status**: ⚠️ **NO DATASET LOADED** (Agent uses documents from API requests)

**What This Agent Needs**:
- Employee handbooks
- HR policy documents
- Benefits documentation
- Vacation policies
- Leave policies
- Code of conduct
- Onboarding guides

**Recommended Format**:
```
/app/data/hr_policies/
├── employee_handbook.pdf
├── vacation_policy.md
├── benefits_guide.md
├── code_of_conduct.pdf
└── leave_policy.md
```

**Test Without Dataset**:
The HR Policy Agent can work by providing document content directly in the request:

```json
{
  "task": {
    "question": "What is the vacation policy?",
    "task_type": "policy_search",
    "documents": [
      {
        "title": "Employee Handbook",
        "content": "Vacation Policy: Full-time employees receive 15 days of paid vacation per year..."
      }
    ]
  }
}
```

---

#### 3. **Customer Service Documents** (CS Document Agent)
**Status**: ⚠️ **NO DATASET LOADED** (Agent uses documents from API requests)

**What This Agent Needs**:
- Product documentation
- FAQ documents
- Troubleshooting guides
- User manuals
- Knowledge base articles
- Support ticket history

**Recommended Format**:
```
/app/data/cs_documents/
├── product_faqs.md
├── troubleshooting_guide.md
├── user_manual.pdf
├── known_issues.md
└── support_articles/
    ├── article_001.md
    ├── article_002.md
    └── ...
```

**Test Without Dataset**:
```json
{
  "task": {
    "question": "How do I reset my password?",
    "task_type": "support",
    "documents": [
      {
        "title": "Password Reset Guide",
        "content": "To reset your password: 1. Go to login page 2. Click 'Forgot Password'..."
      }
    ]
  }
}
```

---

#### 4. **General Documents** (Analysis, Synthesis, Validation Agents)
**Status**: ✅ **OPERATIONAL** (Work with any documents provided)

These agents are **general-purpose** and work with any text/documents you provide:

- **Analysis Agent**: Analyzes documents for insights
- **Synthesis Agent**: Combines information from multiple sources
- **Validation Agent**: Validates and checks consistency

**Test Approach**: Provide documents directly in API requests.

---

## How to Test Each Agent

### Option 1: Test with Existing Data (Legal Research Agent Only)

✅ **Legal Research Agent** - Already has 1,699 HK ordinances imported

```bash
curl -X POST http://localhost:8000/api/agents/legal_research/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "search",
      "question": "What are the requirements for building permits in Hong Kong?"
    }
  }'
```

---

### Option 2: Test with Sample Data (All Other Agents)

Create test datasets for each agent or provide documents in the API request.

#### HR Policy Agent Test

```bash
# Create sample HR policy
cat > /tmp/sample_hr_policy.json << 'EOF'
{
  "task": {
    "question": "What is the vacation policy for full-time employees?",
    "task_type": "policy_search",
    "documents": [
      {
        "title": "Employee Handbook 2025",
        "content": "VACATION POLICY\n\nFull-time employees receive the following vacation benefits:\n- First year: 10 days\n- After 1 year: 15 days\n- After 3 years: 20 days\n- After 5 years: 25 days\n\nVacation must be requested 2 weeks in advance and approved by manager."
      }
    ]
  }
}
EOF

# Test HR Policy Agent
curl -X POST http://localhost:8000/api/agents/hr_policy/execute \
  -H "Content-Type: application/json" \
  -d @/tmp/sample_hr_policy.json
```

#### CS Document Agent Test

```bash
# Create sample CS document
cat > /tmp/sample_cs_doc.json << 'EOF'
{
  "task": {
    "question": "How do I reset my password?",
    "task_type": "support",
    "documents": [
      {
        "title": "Password Reset Guide",
        "content": "PASSWORD RESET INSTRUCTIONS\n\n1. Go to the login page at https://app.example.com/login\n2. Click 'Forgot Password' link below the login form\n3. Enter your email address\n4. Check your email for a reset link (valid for 24 hours)\n5. Click the link and create a new password\n6. Password must be at least 8 characters with uppercase, lowercase, and numbers\n\nIf you don't receive the email within 5 minutes, check your spam folder or contact support."
      }
    ]
  }
}
EOF

# Test CS Document Agent
curl -X POST http://localhost:8000/api/agents/cs_document/execute \
  -H "Content-Type: application/json" \
  -d @/tmp/sample_cs_doc.json
```

#### Analysis Agent Test

```bash
# Create sample analysis task
cat > /tmp/sample_analysis.json << 'EOF'
{
  "task": {
    "task_type": "analysis",
    "text": "Our Q4 sales data shows a 25% increase in revenue compared to Q3. The main drivers were: 1) Launch of new product line contributing 40% of new sales, 2) Expansion to 3 new markets (APAC, EU, LATAM), 3) Improved customer retention rate from 65% to 78%. However, operational costs also increased by 15% due to hiring and infrastructure investments. Customer acquisition cost decreased by 20% due to more efficient marketing campaigns.",
    "focus": "Identify key performance indicators and trends"
  }
}
EOF

# Test Analysis Agent
curl -X POST http://localhost:8000/api/agents/analysis/execute \
  -H "Content-Type: application/json" \
  -d @/tmp/sample_analysis.json
```

---

## Creating Custom Datasets

### For HR Policy Agent

If you want to create a proper HR policy dataset:

```bash
# 1. Create directory structure
mkdir -p /Users/wongivan/Apps/legal-ai-vault/api/data/hr_policies

# 2. Create sample HR documents
cat > /Users/wongivan/Apps/legal-ai-vault/api/data/hr_policies/vacation_policy.md << 'EOF'
# Vacation Policy

## Eligibility
All full-time employees are eligible for paid vacation time.

## Accrual Rates
- 0-1 year: 10 days per year
- 1-3 years: 15 days per year
- 3-5 years: 20 days per year
- 5+ years: 25 days per year

## Request Process
1. Submit vacation request via HR portal
2. Manager approval required
3. Minimum 2 weeks advance notice
4. Blackout periods apply during peak business seasons

## Carryover
Up to 5 days can be carried over to the next year.
EOF

cat > /Users/wongivan/Apps/legal-ai-vault/api/data/hr_policies/benefits.md << 'EOF'
# Employee Benefits

## Health Insurance
- Medical coverage: 100% employer-paid for employee, 50% for dependents
- Dental coverage: Available with 50% employer contribution
- Vision coverage: Annual eye exam and $200 frames allowance

## Retirement
- 401(k) with 5% employer match
- Vesting: Immediate for employee contributions, 4-year vesting for employer match

## Other Benefits
- Life insurance: 2x annual salary
- Disability insurance: Short-term and long-term
- Flexible Spending Account (FSA)
- Employee Assistance Program (EAP)
EOF
```

### For CS Document Agent

```bash
# 1. Create directory
mkdir -p /Users/wongivan/Apps/legal-ai-vault/api/data/cs_documents

# 2. Create FAQ document
cat > /Users/wongivan/Apps/legal-ai-vault/api/data/cs_documents/faqs.md << 'EOF'
# Frequently Asked Questions

## Account Management

### How do I create an account?
1. Click "Sign Up" on the homepage
2. Enter your email and create a password
3. Verify your email address
4. Complete your profile

### How do I reset my password?
1. Click "Forgot Password" on login page
2. Enter your registered email
3. Check email for reset link
4. Create new password (min 8 characters)

### How do I update my profile?
1. Log in to your account
2. Go to Settings > Profile
3. Update your information
4. Click "Save Changes"

## Technical Support

### The app is not loading
1. Clear your browser cache
2. Disable browser extensions
3. Try a different browser
4. Check your internet connection

### I'm getting an error message
1. Note the exact error message
2. Check the status page for known issues
3. Try logging out and back in
4. Contact support if issue persists
EOF
```

---

## RAG (Retrieval Augmented Generation) Testing

The platform supports RAG queries without using agents directly:

```bash
# RAG Search - Document Level
curl -X POST http://localhost:8000/api/rag \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the Building Management Ordinance?",
    "top_k": 3,
    "search_type": "documents"
  }'

# RAG Search - Section Level (more precise)
curl -X POST http://localhost:8000/api/rag \
  -H "Content-Type: application/json" \
  -d '{
    "question": "insurance requirements construction",
    "top_k": 5,
    "search_type": "sections"
  }'
```

---

## Multi-Agent Workflows

Test workflows that combine multiple agents:

```bash
# Legal + HR Compliance Workflow
curl -X POST http://localhost:8000/api/agents/workflows/legal_hr_compliance/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "policy_type": "employment",
      "question": "What are the legal requirements for employee contracts in Hong Kong?"
    }
  }'
```

---

## Dataset Import Scripts

If you want to import larger datasets, you can create import scripts similar to the HK ordinance import:

### Template Import Script

```python
#!/usr/bin/env python3
"""
Import custom documents into the platform
"""
import asyncio
from pathlib import Path
from database import get_db
from qdrant_client import QdrantClient
from services.ollama_service import OllamaService

async def import_documents(doc_type: str, doc_dir: Path):
    """Import documents of a specific type"""
    # Initialize services
    db = next(get_db())
    qdrant = QdrantClient(host='qdrant', port=6333)
    ollama = OllamaService()

    # Process documents
    for doc_file in doc_dir.glob('*.md'):
        content = doc_file.read_text()

        # Generate embedding
        embedding = await ollama.generate_embedding(content)

        # Store in database and Qdrant
        # ... (implementation details)

    db.close()

if __name__ == "__main__":
    asyncio.run(import_documents('hr_policies', Path('/app/data/hr_policies')))
```

---

## Summary: What You Need

### ✅ Already Available
1. **HK Legal Ordinances** - 1,699 documents, 11,288 sections, READY for Legal Research Agent

### 📝 Create As Needed
2. **HR Policy Documents** - For HR Policy Agent testing
3. **CS Documents** - For Customer Service Agent testing
4. **Sample Text/Data** - For Analysis, Synthesis, Validation agents

### 🎯 Quick Start Testing

**Without creating datasets**, you can test all agents by providing documents directly in API requests (see examples above).

**With datasets**, create markdown/PDF files in the appropriate directories and optionally write import scripts.

---

## Next Steps

### Immediate Testing (No Dataset Needed)
1. ✅ Test Legal Research Agent (data already imported)
2. ✅ Test other agents with inline documents (see examples above)
3. ✅ Test multi-agent workflows
4. ✅ Test RAG endpoints

### Optional: Create Custom Datasets
1. Create HR policy documents in `/app/data/hr_policies/`
2. Create CS documents in `/app/data/cs_documents/`
3. Write import scripts if needed
4. Load documents into vector database

---

## Testing Tools Provided

```bash
# Monitor agent health
curl -s http://localhost:8000/api/agents/health | python3 -m json.tool

# List all agents
curl -s http://localhost:8000/api/agents | python3 -m json.tool

# List workflows
curl -s http://localhost:8000/api/agents/workflows | python3 -m json.tool

# Get workflow examples
curl -s http://localhost:8000/api/agents/workflows/examples/all | python3 -m json.tool
```

---

**Platform Status**: ✅ **FULLY OPERATIONAL**
**Ready for Testing**: ✅ **YES** (with or without additional datasets)
**Legal Research Agent**: ✅ **READY** (1,699 HK ordinances loaded)

---

*The Vault AI Platform is designed to work flexibly - agents can process documents provided in API requests OR search pre-loaded datasets like the HK ordinances. Choose the approach that works best for your testing needs.*
