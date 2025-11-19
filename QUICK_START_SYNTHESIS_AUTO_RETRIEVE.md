# 🚀 Quick Start: Synthesis Agent Auto-Retrieve

**5-Minute Guide to Using the Enhanced Synthesis Agent**

---

## Step 1: Start Services (1 minute)

```bash
# Start Docker Desktop, then:
cd /Users/wongivan/Apps/legal-ai-vault
docker-compose restart api

# Verify it's running:
curl http://localhost:8000/health | jq .
```

**Expected**: `{"status": "healthy"}`

---

## Step 2: Open Frontend (30 seconds)

```bash
open http://localhost:8000
```

- Click the **"🔗 Synthesis"** agent tab
- You'll see a new checkbox: **"🔍 Auto-retrieve documents from Legal Database"**

---

## Step 3: Try Auto-Retrieve (2 minutes)

### Example 1: Single Topic - Director Duties

1. ✅ **Check** "Auto-retrieve documents from Legal Database"
2. **Enter query**:
   ```
   What are the director duties under Hong Kong Companies Ordinance?
   ```
3. **Click** "🔗 Synthesize"
4. **Wait** ~30-60 seconds
5. **See** comprehensive synthesis with Cap. citations!

### Example 2: Multiple Topics - Corporate Compliance

1. ✅ **Check** "Auto-retrieve documents from Legal Database"
2. **Enter queries** (one per line):
   ```
   director fiduciary duties Hong Kong
   company secretary statutory obligations
   corporate governance requirements
   ```
3. **Adjust parameters** (optional):
   - Documents per Query: `5`
   - Min Relevance Score: `0.65`
4. **Add focus**: "Create corporate compliance checklist"
5. **Click** "🔗 Synthesize"
6. **Wait** ~60-90 seconds
7. **Get** multi-perspective synthesis!

---

## Step 4: Compare with Manual Mode (1 minute)

1. ❌ **Uncheck** "Auto-retrieve" to see manual mode
2. Notice you now need to **paste documents manually**
3. **Switch back** to auto-retrieve mode - much easier!

---

## Ready-to-Use API Examples

### Example A: Company Directors

```bash
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -H "Content-Type: application/json" \
  -d '{
  "task": {
    "task_type": "synthesis",
    "auto_retrieve": true,
    "document_queries": [
      "director duties and responsibilities",
      "director liability provisions",
      "director indemnification rules"
    ],
    "top_k_per_query": 5,
    "min_score": 0.6,
    "focus": "Create comprehensive director duties guide"
  }
}' | jq '.result.synthesized_output' -r
```

### Example B: Employment Law

```bash
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -H "Content-Type: application/json" \
  -d '{
  "task": {
    "task_type": "synthesis",
    "auto_retrieve": true,
    "document_queries": [
      "employment contract requirements Hong Kong",
      "termination notice periods",
      "severance pay provisions"
    ],
    "top_k_per_query": 4,
    "min_score": 0.65,
    "focus": "Summarize employment termination rules"
  }
}' | jq .
```

### Example C: Property Law

```bash
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -H "Content-Type: application/json" \
  -d '{
  "task": {
    "task_type": "synthesis",
    "auto_retrieve": true,
    "document_queries": [
      "landlord tenant obligations Hong Kong",
      "lease agreement requirements",
      "rental deposit rules"
    ],
    "top_k_per_query": 5,
    "min_score": 0.6,
    "focus": "Create landlord-tenant rights summary"
  }
}' | jq '.result.synthesized_output' -r
```

---

## 💡 Pro Tips

### Query Writing Tips

**✅ Good Queries** (Specific, clear topics):
```
director duties under Companies Ordinance
employment termination notice periods
property lease registration requirements
```

**❌ Poor Queries** (Too broad or vague):
```
company law
employment
property
```

### Parameter Tuning

| Use Case | Top-K | Min Score |
|----------|-------|-----------|
| **Quick Summary** | 3-4 | 0.70 |
| **Balanced** | 5-6 | 0.60-0.65 |
| **Comprehensive** | 8-10 | 0.55 |
| **Exploratory** | 10-15 | 0.50 |

### Performance Expectations

| Queries | Docs/Query | Expected Time |
|---------|------------|---------------|
| 1 query | 3-5 docs | 20-30 seconds |
| 2-3 queries | 5 docs | 45-60 seconds |
| 4-5 queries | 5-8 docs | 90-120 seconds |

---

## 🐛 Troubleshooting

### Issue: "Synthesis agent requires database connection"

**Fix**: Restart API container
```bash
docker-compose restart api
```

### Issue: "No relevant documents found"

**Try**:
- Lower `min_score` to 0.5
- Use broader queries
- Check different keywords

### Issue: Auto-retrieve UI not showing

**Fix**: Hard refresh browser
- Mac: `Cmd + Shift + R`
- Windows/Linux: `Ctrl + Shift + R`

### Issue: Taking too long

**This is normal!** Auto-retrieve performs:
1. Vector search across 1,699 ordinances (per query)
2. Content retrieval from database
3. LLM synthesis of all sources

Expected: **30-120 seconds depending on queries**

---

## 📊 Understanding Results

### Sample Output

```markdown
# Director Duties in Hong Kong

## Fiduciary Duties

According to Cap. 622, Section 465, directors must act in good faith...

## Statutory Obligations

Under Cap. 622, Section 466, directors must exercise reasonable care...

## Liability Protection

Cap. 622, Section 468 provides that directors may be indemnified...

---
📚 Sources Retrieved: 12 documents from 3 queries
⏱️ Execution Time: 68.5 seconds
```

### Source Card Example

```
Source 1: Companies Ordinance (Cap. 622) - Director Duties
Citation: Cap. 622, Section 465
Relevance: 89% match
Query: "director fiduciary duties Hong Kong"

Content: [Relevant section text with context]
```

---

## 🎯 Use Cases

### 1. Legal Research
**Queries**:
- Specific legal topic from different angles
- Compare provisions across ordinances
- Find related sections

**Example**:
```
contract formation requirements
contract breach remedies
contract dispute resolution
```

### 2. Compliance Checklists
**Queries**:
- Requirements from different regulations
- Obligations across different laws
- Compliance procedures

**Example**:
```
data protection compliance Hong Kong
personal data handling requirements
data breach notification obligations
```

### 3. Client Briefings
**Queries**:
- Client's specific situation
- Related legal provisions
- Practical implications

**Example**:
```
company registration procedures
share capital requirements
director appointment rules
```

---

## 🔄 Switching Between Modes

### When to Use Auto-Retrieve:
- ✅ Legal research across HK ordinances
- ✅ Need comprehensive multi-source synthesis
- ✅ Want automatic citations
- ✅ Exploring broad legal topics

### When to Use Manual:
- ✅ Have specific documents already
- ✅ Non-legal content (customer feedback, reports)
- ✅ Documents not in HK ordinances database
- ✅ Need full control over sources

---

## 📁 Example Workflows

### Workflow 1: Research Question

1. **Client asks**: "What are my obligations as a company director?"
2. **Auto-retrieve queries**:
   ```
   director fiduciary duties Hong Kong
   director statutory obligations Companies Ordinance
   director liability and indemnification
   ```
3. **Focus**: "Summarize key director obligations with practical examples"
4. **Result**: Comprehensive guide with Cap. citations

### Workflow 2: Compliance Review

1. **Need**: Update employment policies for compliance
2. **Auto-retrieve queries**:
   ```
   employment contract statutory requirements
   minimum wage provisions Hong Kong
   annual leave entitlements
   termination notice periods
   severance pay calculations
   ```
3. **Focus**: "Create employment policy compliance checklist"
4. **Result**: Detailed checklist with legal references

### Workflow 3: Comparative Analysis

1. **Question**: "How do director duties differ from secretary duties?"
2. **Auto-retrieve queries**:
   ```
   director duties responsibilities Companies Ordinance
   company secretary duties responsibilities
   director secretary comparison
   ```
3. **Focus**: "Create comparison table of duties"
4. **Result**: Side-by-side comparison with citations

---

## 🎓 Next Steps

### Learn More:
- **Full Documentation**: `SYNTHESIS_AUTO_RETRIEVE_IMPLEMENTATION.md`
- **Technical Guide**: `SYNTHESIS_DOCUMENT_EMBEDDING_GUIDE.md`
- **Test Script**: `./test_synthesis_auto_retrieve.sh`

### Explore More Agents:
- **Legal Research Agent**: Direct Q&A on HK ordinances
- **Validation Agent**: Check consistency across documents
- **Analysis Agent**: Extract insights from text

### Advanced Features:
- Combine auto-retrieve with manual sources (future)
- Export synthesis with citations as PDF (future)
- Save frequently used query sets (future)

---

## ✅ Checklist

Before reporting issues, verify:

- [ ] Docker is running
- [ ] API container restarted after code changes
- [ ] Browser hard-refreshed (Cmd/Ctrl + Shift + R)
- [ ] At least 1 search query entered
- [ ] Min score between 0.4-0.8 (not too strict)
- [ ] Waited sufficient time (30-120 seconds)
- [ ] Qdrant collection has documents (check Legal Research agent works)

---

## 🎉 You're Ready!

The Synthesis Agent can now automatically search and synthesize information from **1,699 Hong Kong ordinances**!

**Start here**: http://localhost:8000 → Synthesis Agent tab → ✅ Auto-retrieve

---

*Happy Synthesizing! 🔗📚*
