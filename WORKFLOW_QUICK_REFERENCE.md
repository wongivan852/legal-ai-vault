# 🚀 Workflow Quick Reference Card

**One-Page Cheat Sheet for Multi-Agent Workflows**

---

## 📋 Agent Names (MUST USE EXACTLY)

```python
"legal_research"  # Legal questions, HK law research
"hr_policy"       # HR policies, employee benefits
"cs_document"     # Customer service, support tickets
"analysis"        # Text analysis, pattern recognition
"synthesis"       # Combine sources, create reports
"validation"      # Quality checking, accuracy verification
```

---

## 🔧 Basic Workflow Template

```python
def create_my_workflow() -> Workflow:
    """Your workflow description"""
    workflow = Workflow(
        name="Display Name",
        description="What this workflow does"
    )

    # Step 1
    workflow.add_step(WorkflowStep(
        name="step1_name",              # Internal name (no spaces)
        agent_name="legal_research",    # Agent to use
        task_builder=lambda ctx, inp: { # Task configuration
            "question": inp.get("question", "")
        },
        description="Human readable description"
    ))

    # Step 2 (uses Step 1 result)
    workflow.add_step(WorkflowStep(
        name="step2_name",
        agent_name="validation",
        task_builder=lambda ctx, inp: {
            "documents": [{
                "title": "Step 1 Result",
                "content": ctx["step1_name"].get("answer", "")  # ← Access Step 1
            }],
            "validation_type": "accuracy"
        },
        description="Validate Step 1 result"
    ))

    return workflow
```

---

## 📝 Task Builder Patterns

### Access User Input
```python
task_builder=lambda ctx, inp: {
    "question": inp.get("field_name", "default_value")
}
```

### Access Previous Step
```python
task_builder=lambda ctx, inp: {
    "data": ctx["step_name"].get("answer", "")
}
```

### Combine Multiple Steps
```python
task_builder=lambda ctx, inp: {
    "sources": [
        {"title": "Step 1", "content": ctx["step1"].get("answer", "")},
        {"title": "Step 2", "content": ctx["step2"].get("answer", "")}
    ]
}
```

---

## 🤖 Agent Input Formats

### Legal Research Agent
```python
{
    "question": "Legal question here"
}
```

### HR Policy Agent
```python
{
    "question": "HR question here",
    "task_type": "benefits",  # or "onboarding", "policy_search"
    "context": "Additional context"  # optional
}
```

### Customer Service Agent
```python
{
    "question": "Customer question",
    "context": "Product docs",  # optional
    "customer_name": "John"     # optional
}
```

### Analysis Agent
```python
{
    "data": "Text to analyze",
    "focus": "What to focus on",
    "analysis_type": "summary"  # or "themes", "comparison", "risk"
}
```

### Synthesis Agent
```python
{
    "task_type": "synthesis",
    "sources": [
        {"title": "Source 1", "content": "..."},
        {"title": "Source 2", "content": "..."}
    ],
    "focus": "What to create"
}
```

### Validation Agent
```python
{
    "documents": [
        {"title": "Doc to validate", "content": "..."}
    ],
    "validation_type": "accuracy"  # or "completeness", "comprehensive"
}
```

---

## 📂 File Locations

| File | Purpose | Edit? |
|------|---------|-------|
| `/api/workflows/workflow_definitions.py` | Add workflows | ✅ YES |
| `/api/workflows/workflow_engine.py` | Core engine | 🚫 NO |
| `/frontend/index.html` | Add UI forms | ✅ YES |
| `/frontend/static/js/app.js` | Add handlers | ✅ YES |

---

## 🔄 Registration Steps

### 1. Backend Registration
In `workflow_definitions.py`:
```python
def get_all_workflows():
    return {
        "existing": create_existing_workflow(),
        "my_workflow": create_my_workflow()  # ← Add here
    }
```

### 2. Frontend HTML
In `index.html`:
```html
<!-- Tab Button -->
<button class="agent-tab-btn" data-workflow="my_workflow">
    🎯 My Workflow
</button>

<!-- Form -->
<div class="agent-content" id="workflow-my_workflow">
    <form id="myWorkflowForm" class="form">
        <textarea id="myInput" required></textarea>
        <button type="submit" class="btn btn-primary">Run</button>
    </form>
    <div id="myWorkflowResult" class="result-panel"></div>
</div>
```

### 3. Frontend JavaScript
In `app.js`:
```javascript
document.getElementById('myWorkflowForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const inputData = {
        field_name: document.getElementById('myInput').value
    };
    await executeWorkflow('my_workflow', inputData, 'myWorkflowResult',
                         e.target.querySelector('.btn-primary'));
});
```

---

## 🧪 Testing Commands

### API Test
```bash
curl -X POST http://localhost:8000/api/workflows/my_workflow/execute \
  -H "Content-Type: application/json" \
  -d '{"input": {"question": "test"}}'
```

### Restart API
```bash
docker-compose restart api
```

### View Logs
```bash
docker-compose logs -f api
```

---

## ⚠️ Common Errors

| Error | Fix |
|-------|-----|
| Agent 'xxx' not found | Use exact agent names from list above |
| No data provided | Analysis agent needs `"data"` not `"content"` |
| KeyError in context | Step name in `ctx["name"]` must match `name="name"` |
| Form not submitting | Form ID must match `getElementById('formId')` |
| Workflow not in UI | Register in `get_all_workflows()` |

---

## 📊 Workflow ID Rules

✅ **Good IDs:**
- `legal_qa_validated`
- `hr_onboarding_v2`
- `customer_support_flow`

❌ **Bad IDs:**
- `Legal QA` (no spaces)
- `hr-onboarding` (use underscores)
- `HR_Policy` (lowercase only)

---

## 🎯 Step Naming Rules

✅ **Good Names:**
- `answer_question`
- `validate_result`
- `create_report`

❌ **Bad Names:**
- `Answer Question` (no spaces)
- `step-1` (use underscores)
- `validate` (too generic, be specific)

---

## 💡 Best Practices

1. **Start Simple:** Begin with 2-step workflows
2. **Test Incrementally:** Test each step individually
3. **Use Descriptive Names:** Make step names self-documenting
4. **Handle Errors:** Use `.get()` with defaults
5. **Document Well:** Add clear descriptions
6. **Check Logs:** Monitor `docker-compose logs api`
7. **Browser DevTools:** Use F12 to debug JavaScript

---

## 🔗 Quick Links

- **Full Guide:** `WORKFLOW_CREATION_GUIDE.md`
- **API Docs:** http://localhost:8000/docs
- **Existing Workflows:** `/api/workflows/workflow_definitions.py`
- **Agent Code:** `/api/agents/`

---

## 📞 Need Help?

1. Read the full guide: `WORKFLOW_CREATION_GUIDE.md`
2. Study existing workflows for examples
3. Check browser console (F12) for errors
4. Review API response for error details

---

**🎉 You're Ready to Build Workflows!**

Start with the template above and modify it for your needs.
