# Quick Test Samples - Ready to Use

**Platform**: Vault AI Platform v2.0.0
**Purpose**: Immediate testing without creating datasets

---

## 🚀 Quick Start: Test All Agents in 5 Minutes

Copy and paste these commands to test each agent immediately.

---

## 1. Legal Research Agent ✅ (Data Already Loaded)

### Test Query 1: Building Management Ordinance

```bash
curl -X POST http://localhost:8000/api/agents/legal_research/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "search",
      "question": "What are the insurance requirements under the Building Management Ordinance?"
    }
  }' | python3 -m json.tool
```

### Test Query 2: Companies Ordinance

```bash
curl -X POST http://localhost:8000/api/agents/legal_research/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "search",
      "question": "What are the director duties under the Companies Ordinance?"
    }
  }' | python3 -m json.tool
```

---

## 2. HR Policy Agent (Inline Documents)

### Test: Vacation Policy Query

```bash
curl -X POST http://localhost:8000/api/agents/hr_policy/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "question": "How many vacation days do employees get after 3 years?",
      "task_type": "policy_search",
      "context": "VACATION POLICY: New employees receive 10 days. After 1 year: 15 days. After 3 years: 20 days. After 5 years: 25 days. Vacation requests require 2 weeks advance notice and manager approval."
    }
  }' | python3 -m json.tool
```

### Test: Benefits Query

```bash
curl -X POST http://localhost:8000/api/agents/hr_policy/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "question": "What health insurance benefits are provided?",
      "task_type": "benefits",
      "context": "HEALTH BENEFITS: Medical coverage 100% employer-paid for employees, 50% for dependents. Dental coverage available with 50% employer contribution. Vision coverage includes annual exam and $200 frames allowance. Life insurance at 2x annual salary included."
    }
  }' | python3 -m json.tool
```

---

## 3. Customer Service Agent (Inline Documents)

### Test: Password Reset

```bash
curl -X POST http://localhost:8000/api/agents/cs_document/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "question": "How do I reset my password?",
      "task_type": "support",
      "context": "PASSWORD RESET: 1. Go to login page 2. Click Forgot Password 3. Enter your email 4. Check email for reset link (valid 24 hours) 5. Click link and create new password 6. Password must be 8+ characters with uppercase, lowercase, and numbers. If no email within 5 minutes, check spam or contact support."
    }
  }' | python3 -m json.tool
```

### Test: Account Creation

```bash
curl -X POST http://localhost:8000/api/agents/cs_document/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "question": "How do I create a new account?",
      "task_type": "support",
      "context": "ACCOUNT CREATION: 1. Click Sign Up on homepage 2. Enter email and create password 3. Verify email address via link sent to your inbox 4. Complete profile with name, phone, and address 5. Set up two-factor authentication (recommended) 6. Start using your account. Need help? Contact support@example.com"
    }
  }' | python3 -m json.tool
```

---

## 4. Analysis Agent (General Purpose)

### Test: Sales Data Analysis

```bash
curl -X POST http://localhost:8000/api/agents/analysis/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "analysis",
      "text": "Q4 2024 Performance Summary: Revenue increased 25% to $5.2M compared to Q3. New product line contributed $2.1M (40% of revenue). Expanded to APAC, EU, and LATAM markets. Customer retention improved from 65% to 78%. Customer acquisition cost decreased 20% due to optimized marketing. Operating costs increased 15% due to new hires and infrastructure. Net profit margin at 18%.",
      "focus": "Identify key performance indicators and trends"
    }
  }' | python3 -m json.tool
```

### Test: Market Analysis

```bash
curl -X POST http://localhost:8000/api/agents/analysis/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "analysis",
      "text": "Market Research Findings: 67% of surveyed customers prefer mobile app over web. Average session time increased from 8 to 12 minutes. Feature requests show demand for offline mode (78%), dark theme (65%), and export functionality (53%). Competitor analysis reveals we lag in integration capabilities but lead in user experience and pricing.",
      "focus": "Extract actionable insights and recommendations"
    }
  }' | python3 -m json.tool
```

---

## 5. Synthesis Agent (Multi-Source Combination)

### Test: Synthesize Product Feedback

```bash
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "synthesis",
      "sources": [
        {
          "title": "Customer Survey",
          "content": "85% satisfaction rate. Top request: mobile app. Pricing rated as excellent. Customer support rated 4.5/5 stars."
        },
        {
          "title": "App Store Reviews",
          "content": "4.2 star average. Praise for ease of use. Complaints about occasional crashes. Users want dark mode and offline access."
        },
        {
          "title": "Support Tickets",
          "content": "Main issues: sync delays (35%), password reset problems (25%), billing questions (20%), feature requests (20%)."
        }
      ],
      "focus": "Create comprehensive product improvement plan"
    }
  }' | python3 -m json.tool
```

---

## 6. Validation Agent (Consistency Checking)

### Test: Validate Policy Documents

```bash
curl -X POST http://localhost:8000/api/agents/validation/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "validation",
      "documents": [
        {
          "title": "Employee Handbook",
          "content": "Vacation Policy: Full-time employees receive 15 days per year. Part-time employees receive 7 days per year."
        },
        {
          "title": "HR Website",
          "content": "All employees get 15 days vacation annually. Accrual starts on hire date."
        },
        {
          "title": "Offer Letter Template",
          "content": "You will receive 10 days of paid vacation in your first year, increasing to 15 days after one year of service."
        }
      ],
      "focus": "Check for inconsistencies in vacation policy"
    }
  }' | python3 -m json.tool
```

---

## RAG (Retrieval Augmented Generation) Testing

### Test RAG: Document Search

```bash
curl -X POST http://localhost:8000/api/rag \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Building Management Ordinance requirements",
    "top_k": 3,
    "search_type": "documents"
  }' | python3 -m json.tool
```

### Test RAG: Section Search (More Precise)

```bash
curl -X POST http://localhost:8000/api/rag \
  -H "Content-Type: application/json" \
  -d '{
    "question": "director duties fiduciary obligations companies",
    "top_k": 5,
    "search_type": "sections"
  }' | python3 -m json.tool
```

---

## Multi-Agent Workflows

### Test: Legal + HR Compliance Workflow

```bash
curl -X POST http://localhost:8000/api/agents/workflows/legal_hr_compliance/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "policy_type": "employment",
      "question": "What are the legal requirements for employment contracts in Hong Kong?",
      "context": "We are hiring 50 new employees and need to ensure compliance."
    }
  }' | python3 -m json.tool
```

### Test: Simple Q&A Workflow

```bash
curl -X POST http://localhost:8000/api/agents/workflows/simple_qa/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "question": "What is the purpose of the Employment Ordinance in Hong Kong?",
      "context": "legal"
    }
  }' | python3 -m json.tool
```

### Test: Multi-Agent Research Workflow

```bash
curl -X POST http://localhost:8000/api/agents/workflows/multi_agent_research/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "research_topic": "Hong Kong company director responsibilities and liabilities",
      "depth": "comprehensive"
    }
  }' | python3 -m json.tool
```

---

## Platform Health Checks

### Check Agent Status

```bash
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

### List All Agents

```bash
curl -s http://localhost:8000/api/agents | python3 -m json.tool
```

### List All Workflows

```bash
curl -s http://localhost:8000/api/agents/workflows | python3 -m json.tool
```

### Get Workflow Examples

```bash
curl -s http://localhost:8000/api/agents/workflows/examples/all | python3 -m json.tool
```

---

## Performance Testing

### Test Response Time (Legal Agent)

```bash
time curl -s -X POST http://localhost:8000/api/agents/legal_research/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "search",
      "question": "employment contracts requirements"
    }
  }' | python3 -m json.tool
```

### Test Concurrent Requests

```bash
# Run 3 requests in parallel
for i in {1..3}; do
  (curl -s -X POST http://localhost:8000/api/rag \
    -H "Content-Type: application/json" \
    -d "{\"question\": \"test query $i\", \"top_k\": 3, \"search_type\": \"documents\"}" \
    | python3 -m json.tool > /tmp/response_$i.json) &
done
wait
echo "All requests completed. Check /tmp/response_*.json for results."
```

---

## Database Verification

### Check Legal Data Count

```bash
docker-compose exec -T postgres psql -U legal_vault_user -d legal_ai_vault -c \
  "SELECT
    'Documents' as type, COUNT(*) as count FROM hk_legal_documents
   UNION ALL
   SELECT
    'Sections' as type, COUNT(*) as count FROM hk_legal_sections;"
```

**Expected Output**:
```
   type    | count
-----------+-------
 Documents |  1699
 Sections  | 11288
```

### Check Vector Database

```bash
# Documents collection
curl -s http://localhost:6333/collections/hk_legal_documents | python3 -m json.tool | grep points_count

# Sections collection
curl -s http://localhost:6333/collections/hk_legal_sections | python3 -m json.tool | grep points_count
```

---

## Troubleshooting

### If Agent Returns Empty Response

```bash
# Check agent logs
docker-compose logs api | tail -50

# Check Ollama is running
curl -s http://localhost:11434/api/tags | python3 -m json.tool | head -20

# Check Ollama resource usage
docker stats --no-stream legal-ai-ollama
```

### If Query is Slow (>30 seconds)

This is **normal** for the first query with llama3.1:8b (cold start). Subsequent queries should be faster (10-30 seconds).

To test with faster responses, use a smaller model or test the RAG endpoint directly (no LLM generation).

---

## Quick Test Script

Save this as `/tmp/test_all_agents.sh`:

```bash
#!/bin/bash
echo "Testing Vault AI Platform - All Agents"
echo "======================================"

echo "1. Agent Health..."
curl -s http://localhost:8000/api/agents/health | python3 -m json.tool | grep -A 10 "agents"

echo -e "\n2. Testing Legal Research Agent..."
curl -s -X POST http://localhost:8000/api/agents/legal_research/execute \
  -H "Content-Type: application/json" \
  -d '{"task": {"task_type": "search", "question": "companies ordinance"}}' \
  | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"Status: {d['status']}\")"

echo -e "\n3. Testing RAG Endpoint..."
curl -s -X POST http://localhost:8000/api/rag \
  -H "Content-Type: application/json" \
  -d '{"question": "building ordinance", "top_k": 3, "search_type": "documents"}' \
  | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"Found {len(d.get('sources', []))} sources\")"

echo -e "\n4. Database Status..."
docker-compose exec -T postgres psql -U legal_vault_user -d legal_ai_vault -t -c \
  "SELECT COUNT(*) FROM hk_legal_documents;" | tr -d ' ' | xargs echo "Documents:"

echo -e "\nAll tests completed!"
```

Make it executable and run:

```bash
chmod +x /tmp/test_all_agents.sh
/tmp/test_all_agents.sh
```

---

## Next Steps

1. ✅ Run the quick tests above
2. ✅ Check agent responses
3. ✅ Monitor performance
4. 📝 Create custom datasets if needed (see DATASET_REQUIREMENTS.md)
5. 🚀 Build your application on top of the platform

---

**All agents are ready to test immediately!**

- **Legal Research Agent**: ✅ Has 1,699 HK ordinances loaded
- **Other Agents**: ✅ Work with inline documents (no dataset required)
- **RAG Endpoints**: ✅ Operational for semantic search
- **Workflows**: ✅ Multi-agent workflows available

**Start testing now with the commands above!** 🚀
