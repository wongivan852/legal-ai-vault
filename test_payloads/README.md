# Test Payloads for Synthesis Agent

Ready-to-use JSON payloads for testing the Enhanced Synthesis Agent with auto-retrieve feature.

---

## Quick Test Commands

### Test 1: Simple Auto-Retrieve (30 seconds)
```bash
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -H "Content-Type: application/json" \
  -d @test_payloads/synthesis_auto_retrieve_simple.json | jq .
```

**What it does**: Retrieves 5 documents about "director duties Hong Kong" and synthesizes them.

---

### Test 2: Comprehensive Corporate Governance (90 seconds)
```bash
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -H "Content-Type: application/json" \
  -d @test_payloads/synthesis_auto_retrieve_comprehensive.json | jq .
```

**What it does**: Retrieves documents from 4 different queries covering directors and company secretary duties, creates comprehensive guide.

---

### Test 3: Employment Law (60 seconds)
```bash
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -H "Content-Type: application/json" \
  -d @test_payloads/synthesis_employment_law.json | jq .
```

**What it does**: Retrieves employment-related provisions (contracts, termination, severance, leave) and creates practical guide.

---

### Test 4: Manual Mode - Backward Compatibility (20 seconds)
```bash
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -H "Content-Type: application/json" \
  -d @test_payloads/synthesis_manual_mode.json | jq .
```

**What it does**: Tests traditional manual mode with business reports (no auto-retrieve).

---

## Payload Details

### 1. synthesis_auto_retrieve_simple.json

**Purpose**: Quick test of basic auto-retrieve functionality

**Features**:
- Single query
- Default parameters (5 docs, 0.6 min score)
- Simple focus

**Expected Results**:
- 5 relevant documents about director duties
- Citations from Companies Ordinance (Cap. 622)
- ~30 second execution time

---

### 2. synthesis_auto_retrieve_comprehensive.json

**Purpose**: Test multi-query auto-retrieve with comprehensive synthesis

**Features**:
- 4 different queries
- 6 documents per query
- Corporate governance focus

**Expected Results**:
- 15-24 unique documents (after deduplication)
- Multi-perspective synthesis
- Citations from multiple Cap. chapters
- ~90 second execution time

**Queries**:
1. Director fiduciary duties
2. Director statutory obligations
3. Director liability/indemnification
4. Company secretary duties

---

### 3. synthesis_employment_law.json

**Purpose**: Test employment law topic with practical guide output

**Features**:
- 4 employment-related queries
- 5 documents per query
- Practical focus (guide for employers)

**Expected Results**:
- 12-20 documents about employment law
- Coverage of contracts, termination, severance, leave
- Practical guidance with legal citations
- ~60 second execution time

**Use Case**: Create employee handbook section or HR policy

---

### 4. synthesis_manual_mode.json

**Purpose**: Verify backward compatibility (no auto-retrieve)

**Features**:
- Traditional manual source input
- Business context (sales, feedback, market)
- Strategic focus

**Expected Results**:
- Synthesis of 3 provided sources
- Executive summary with recommendations
- ~20 second execution time (no retrieval)

**Use Case**: Non-legal synthesis, traditional workflow

---

## Expected Response Format

### Auto-Retrieve Response:
```json
{
  "agent": "synthesis",
  "status": "completed",
  "result": {
    "task_type": "synthesis",
    "synthesized_output": "# [Title]\n\n[Comprehensive synthesis with multiple sections]\n\n## [Section 1]\n\nAccording to Cap. XXX, Section YYY...",
    "synthesis_type": "merge",
    "sources_used": 12,
    "quality_score": "high",
    "sources": [
      {
        "title": "Companies Ordinance (Cap. 622) - Section Title",
        "content": "[Section content]",
        "source": "Cap. 622, Section 465",
        "score": 0.89,
        "query": "director duties Hong Kong",
        "metadata": {
          "doc_number": "622",
          "doc_name": "Companies Ordinance",
          "section_number": "465",
          "type": "section"
        }
      }
    ]
  },
  "execution_time": 45.2
}
```

---

## Customization Guide

### Adjusting Parameters

**Top-K Per Query**:
```json
"top_k_per_query": 3    // Fewer, more relevant docs
"top_k_per_query": 8    // More comprehensive coverage
"top_k_per_query": 15   // Maximum coverage (slower)
```

**Min Score**:
```json
"min_score": 0.7        // Very strict, only highly relevant
"min_score": 0.6        // Balanced (recommended)
"min_score": 0.5        // Broader, includes tangential content
```

**Focus**:
```json
"focus": "Create checklist"                    // Structured output
"focus": "Summarize key points"                // Brief summary
"focus": "Create comprehensive guide"          // Detailed coverage
"focus": "Compare and contrast provisions"     // Analytical
```

---

## Creating Your Own Payloads

### Template for Auto-Retrieve:
```json
{
  "task": {
    "task_type": "synthesis",
    "auto_retrieve": true,
    "document_queries": [
      "Your search query 1",
      "Your search query 2",
      "Your search query 3"
    ],
    "top_k_per_query": 5,
    "min_score": 0.6,
    "focus": "What you want to achieve"
  }
}
```

### Template for Manual Mode:
```json
{
  "task": {
    "task_type": "synthesis",
    "sources": [
      {
        "title": "Document 1 Title",
        "content": "Document 1 full content here"
      },
      {
        "title": "Document 2 Title",
        "content": "Document 2 full content here"
      }
    ],
    "focus": "What you want to achieve"
  }
}
```

---

## Testing Workflow

### 1. Start with Simple
```bash
# Test basic functionality first
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -d @test_payloads/synthesis_auto_retrieve_simple.json | jq .
```

### 2. Test Manual (Backward Compatibility)
```bash
# Ensure manual mode still works
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -d @test_payloads/synthesis_manual_mode.json | jq .
```

### 3. Try Comprehensive
```bash
# Test multi-query with deduplication
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -d @test_payloads/synthesis_auto_retrieve_comprehensive.json | jq .
```

### 4. Test Domain-Specific
```bash
# Test with employment law
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -d @test_payloads/synthesis_employment_law.json | jq .
```

---

## Performance Benchmarks

| Payload | Queries | Docs | Expected Time | Use Case |
|---------|---------|------|---------------|----------|
| Simple | 1 | ~5 | 30s | Quick test |
| Manual | 0 | 3 | 20s | Backward compatibility |
| Employment | 4 | ~15 | 60s | Domain-specific |
| Comprehensive | 4 | ~20 | 90s | Full feature test |

---

## Troubleshooting

### Test Fails with "No documents found"

**Try**:
1. Check Qdrant has documents: `curl http://localhost:6333/collections/legal_documents`
2. Test Legal Research agent works: Use frontend to ask a legal question
3. Lower min_score to 0.5 or 0.4

### Test Times Out

**Possible causes**:
- Too many queries (reduce to 2-3)
- Too high top_k (reduce to 3-5)
- LLM model too large (check Ollama)

**Solutions**:
- Reduce queries or top_k
- Increase timeout in curl: `curl --max-time 180 ...`

### Result Shows JSON Instead of Text

**Cause**: Display format issue (frontend only)

**Fix**: Hard refresh browser (Cmd/Ctrl + Shift + R)

---

## Next Steps

After testing payloads:

1. **Try in Frontend UI**: http://localhost:8000 → Synthesis Agent tab
2. **Create Custom Queries**: Modify payloads for your use cases
3. **Compare Modes**: Test same topic in auto-retrieve vs manual
4. **Optimize Parameters**: Tune top_k and min_score for your needs

---

For more information:
- **Implementation Guide**: `../SYNTHESIS_AUTO_RETRIEVE_IMPLEMENTATION.md`
- **Quick Start**: `../QUICK_START_SYNTHESIS_AUTO_RETRIEVE.md`
- **Test Script**: `../test_synthesis_auto_retrieve.sh`

---

*Ready to synthesize! 🔗*
