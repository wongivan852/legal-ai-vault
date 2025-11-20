# 📘 Multi-Agent Workflow Creation Guide

**Complete Beginner's Guide to Creating Custom Workflows**

Version: 1.0
Last Updated: November 2025
Platform: Vault AI Platform (Legal AI)

---

## 📑 Table of Contents

1. [Introduction](#introduction)
2. [Understanding the Workflow System](#understanding-the-workflow-system)
3. [Prerequisites](#prerequisites)
4. [Available Agents](#available-agents)
5. [Step-by-Step: Creating Your First Workflow](#step-by-step-creating-your-first-workflow)
6. [Advanced Workflow Patterns](#advanced-workflow-patterns)
7. [Frontend Integration](#frontend-integration)
8. [Testing Your Workflow](#testing-your-workflow)
9. [Troubleshooting](#troubleshooting)
10. [Complete Examples](#complete-examples)

---

## 🎯 Introduction

### What is a Multi-Agent Workflow?

A **Multi-Agent Workflow** is a sequence of tasks where different AI agents work together to accomplish a complex goal. Think of it like an assembly line where each agent is a specialist that performs one part of the job, then passes the result to the next agent.

**Real-World Example:**
Instead of asking one person to research a legal question, validate the answer, and write a report, you have:
- **Step 1:** Legal Agent researches the question
- **Step 2:** Validation Agent checks the answer for accuracy
- **Step 3:** Synthesis Agent creates a polished report

Each agent is an expert in their field, producing better results than a single generalist.

### Why Use Workflows?

✅ **Quality:** Specialized agents produce better results
✅ **Validation:** Built-in quality checks between steps
✅ **Reusability:** Create once, use many times
✅ **Transparency:** See exactly what each agent did
✅ **Flexibility:** Easy to modify and improve

---

## 🏗️ Understanding the Workflow System

### Architecture Overview

```
┌─────────────────────────────────────────────────┐
│           USER SUBMITS WORKFLOW                 │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│        WORKFLOW ORCHESTRATOR                     │
│  (Controls the flow and manages agents)          │
└─────────────────┬───────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌────────┐   ┌────────┐   ┌────────┐
│ STEP 1 │   │ STEP 2 │   │ STEP 3 │
│ Agent A│──▶│ Agent B│──▶│ Agent C│
└────────┘   └────────┘   └────────┘
    │             │             │
    └─────────────┴─────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│           FINAL RESULT RETURNED                  │
└─────────────────────────────────────────────────┘
```

### Key Components

| Component | Description | File Location |
|-----------|-------------|---------------|
| **Workflow** | Container for steps | `workflow_definitions.py` |
| **WorkflowStep** | Individual task for an agent | `workflow_engine.py` |
| **Task Builder** | Function that creates agent tasks | Inside each step |
| **Context** | Shared memory between steps | Managed automatically |
| **Registry** | Storage for all workflows | `workflow_engine.py` |

---

## ✅ Prerequisites

### What You Need to Know

- ✅ **Basic Python syntax** (functions, dictionaries, strings)
- ✅ **Understanding of the 6 available agents** (see next section)
- ✅ **Text editor** (VS Code, Sublime, or any code editor)
- ✅ **How to restart the API** (using Docker Compose)

### File Structure

```
legal-ai-vault/
├── api/
│   ├── workflows/
│   │   ├── __init__.py              # Package initialization
│   │   ├── workflow_engine.py       # Core engine (DON'T MODIFY)
│   │   └── workflow_definitions.py  # YOUR WORKFLOWS GO HERE ✏️
│   └── routes/
│       └── workflows.py             # API endpoints (DON'T MODIFY)
├── frontend/
│   ├── index.html                   # Add UI forms here ✏️
│   └── static/js/app.js             # Add UI handlers here ✏️
└── docker-compose.yml
```

**Legend:**
- 📁 Files you'll read
- ✏️ Files you'll edit
- 🚫 Files you shouldn't modify

---

## 🤖 Available Agents

Before creating a workflow, you need to know what agents are available and what they can do.

### 1️⃣ Legal Research Agent (`legal_research`)

**What it does:** Searches Hong Kong legal ordinances and provides answers based on actual law.

**Input Format:**
```python
{
    "question": "What are the legal requirements for data privacy?",
    "task_type": "search"  # optional
}
```

**Output Format:**
```python
{
    "agent": "legal_research",
    "status": "completed",
    "answer": "Based on the Personal Data (Privacy) Ordinance...",
    "sources": [
        {
            "title": "Personal Data (Privacy) Ordinance",
            "content": "...",
            "score": 0.89
        }
    ],
    "confidence": "high",
    "execution_time": 12.5
}
```

**When to Use:**
- ✅ Legal questions about Hong Kong law
- ✅ Research on specific ordinances
- ✅ Compliance checking against HK regulations

---

### 2️⃣ HR Policy Agent (`hr_policy`)

**What it does:** Answers questions about HR policies, benefits, onboarding, etc.

**Input Format:**
```python
{
    "question": "What is the vacation policy for new employees?",
    "task_type": "benefits",  # benefits, onboarding, policy_search
    "context": "Additional company policy text..."  # optional
}
```

**Output Format:**
```python
{
    "agent": "hr_policy",
    "status": "completed",
    "answer": "New employees receive 10 days of vacation...",
    "task_type": "benefits",
    "policy_references": ["Employee Handbook Section 5.2"],
    "confidence": "high",
    "execution_time": 8.2
}
```

**When to Use:**
- ✅ Employee onboarding questions
- ✅ Benefits and compensation queries
- ✅ Company policy clarification

---

### 3️⃣ Customer Service Agent (`cs_document`)

**What it does:** Generates customer support responses and documentation.

**Input Format:**
```python
{
    "question": "How do I reset my password?",
    "context": "Product documentation...",  # optional
    "customer_name": "John Doe"  # optional
}
```

**Output Format:**
```python
{
    "agent": "cs_document",
    "status": "completed",
    "answer": "Hi John, to reset your password...",
    "response_tone": "helpful",
    "execution_time": 6.3
}
```

**When to Use:**
- ✅ Customer support ticket responses
- ✅ Help documentation generation
- ✅ FAQ answers

---

### 4️⃣ Analysis Agent (`analysis`)

**What it does:** Analyzes text, extracts insights, identifies patterns and themes.

**Input Format:**
```python
{
    "data": "Large text to analyze...",
    "focus": "Extract key themes about employee satisfaction",
    "analysis_type": "summary"  # summary, themes, comparison, risk, structured
}
```

**Output Format:**
```python
{
    "agent": "analysis",
    "status": "completed",
    "analysis_type": "summary",
    "analysis": {
        "summary": "The main themes are...",
        "type": "summary"
    },
    "insights": [
        "Key insight 1",
        "Key insight 2"
    ],
    "confidence": "high",
    "execution_time": 15.7
}
```

**When to Use:**
- ✅ Extracting insights from long documents
- ✅ Comparing multiple sources
- ✅ Risk assessment
- ✅ Theme identification

---

### 5️⃣ Synthesis Agent (`synthesis`)

**What it does:** Combines multiple sources into a coherent, unified output.

**Input Format:**
```python
{
    "task_type": "synthesis",
    "sources": [
        {
            "title": "Legal Requirements",
            "content": "According to the law..."
        },
        {
            "title": "Company Policy",
            "content": "Our policy states..."
        }
    ],
    "focus": "Create compliance report"
}
```

**Output Format:**
```python
{
    "agent": "synthesis",
    "status": "completed",
    "synthesized_output": "Combined report text...",
    "sources_used": 2,
    "confidence": "high",
    "execution_time": 18.9
}
```

**When to Use:**
- ✅ Combining multiple agent results
- ✅ Creating comprehensive reports
- ✅ Merging different perspectives
- ✅ Final output generation

---

### 6️⃣ Validation Agent (`validation`)

**What it does:** Checks accuracy, completeness, and quality of content.

**Input Format:**
```python
{
    "documents": [
        {
            "title": "Generated Answer",
            "content": "The answer is..."
        }
    ],
    "validation_type": "accuracy",  # accuracy, completeness, comprehensive
    "question": "What was the original question?"  # optional
}
```

**Output Format:**
```python
{
    "agent": "validation",
    "status": "completed",
    "validation_result": "passed",  # passed, partial, failed
    "quality_score": 85,
    "issues": ["Minor issue found..."],
    "recommendations": ["Suggestion 1..."],
    "execution_time": 10.2
}
```

**When to Use:**
- ✅ Quality checking generated content
- ✅ Verifying accuracy of answers
- ✅ Ensuring completeness of reports

---

## 🚀 Step-by-Step: Creating Your First Workflow

Let's create a simple **"Legal Question with Validation"** workflow from scratch.

### Step 1: Plan Your Workflow

**Goal:** Answer a legal question and validate the answer for accuracy.

**Steps:**
1. Legal Research Agent answers the question
2. Validation Agent checks the answer

**Input needed from user:**
- `question` (required): The legal question to answer

**Expected output:**
- Original answer from legal agent
- Validation results showing if answer is accurate

---

### Step 2: Open the Workflow Definitions File

Navigate to: `/api/workflows/workflow_definitions.py`

This file contains all workflow definitions. You'll add your new workflow here.

---

### Step 3: Write the Workflow Function

Add this code at the bottom of `workflow_definitions.py` (before the `get_all_workflows()` function):

```python
def create_legal_qa_validated_workflow() -> Workflow:
    """
    Legal Q&A with Validation Workflow

    This workflow answers a legal question and validates the accuracy
    of the answer using two agents in sequence.

    Steps:
    1. Legal Research Agent - Research and answer the question
    2. Validation Agent - Verify the answer is accurate

    Returns:
        Workflow: Configured workflow ready to execute
    """
    # Create the workflow container
    workflow = Workflow(
        name="Legal Q&A with Validation",
        description="Answer legal questions with automatic accuracy validation"
    )

    # STEP 1: Legal Research
    # This step uses the legal_research agent to answer the question
    workflow.add_step(WorkflowStep(
        name="answer_question",           # Internal step name (no spaces)
        agent_name="legal_research",       # Which agent to use (MUST MATCH EXACTLY)
        task_builder=lambda ctx, inp: {   # Function that builds the task
            "question": inp.get("question", "")
        },
        description="Research Hong Kong law and provide answer"  # Human-readable description
    ))

    # STEP 2: Validation
    # This step takes the answer from Step 1 and validates it
    workflow.add_step(WorkflowStep(
        name="validate_answer",                    # Internal step name
        agent_name="validation",                   # Which agent to use
        task_builder=lambda ctx, inp: {           # Function that builds the task
            "documents": [
                {
                    "title": "Generated Answer",
                    "content": ctx["answer_question"].get("answer", "")  # ← Get answer from Step 1
                }
            ],
            "validation_type": "accuracy",
            "question": inp.get("question", "")
        },
        description="Validate answer accuracy against legal sources"
    ))

    return workflow
```

**Let's Break This Down:**

#### 🔹 Workflow Container
```python
workflow = Workflow(
    name="Legal Q&A with Validation",  # Display name (shown in UI)
    description="Answer legal questions..."  # What it does
)
```

#### 🔹 WorkflowStep Components

```python
WorkflowStep(
    name="answer_question",        # ⚠️ IMPORTANT: No spaces, lowercase
    agent_name="legal_research",   # ⚠️ MUST MATCH agent registry name exactly
    task_builder=lambda ctx, inp: {...},  # Function explained below
    description="Human readable description"
)
```

#### 🔹 Task Builder Explained

The `task_builder` is a **function** that creates the task for the agent. It receives two parameters:

```python
task_builder=lambda ctx, inp: {
    # Return a dictionary that the agent expects
}
```

**Parameters:**
- `ctx` (context): Results from previous steps
- `inp` (input): User's original input

**Example Access Patterns:**

```python
# Access user input
inp.get("question", "")           # Get 'question' from user, default to ""
inp.get("employee_name")          # Get 'employee_name', returns None if missing

# Access previous step results
ctx["step_name"].get("answer")    # Get 'answer' from step named 'step_name'
ctx["step_1_result"]              # Get result from first step (alternative way)
```

---

### Step 4: Register Your Workflow

Find the `get_all_workflows()` function at the bottom of the file and add your workflow:

```python
def get_all_workflows():
    """Get all available workflow definitions"""
    return {
        "hr_onboarding": create_hr_onboarding_workflow(),
        "cs_ticket": create_cs_ticket_workflow(),
        "legal_hr_compliance": create_legal_hr_compliance_workflow(),
        "simple_qa": create_simple_qa_workflow(),
        "multi_agent_research": create_multi_agent_research_workflow(),

        # ✏️ ADD YOUR WORKFLOW HERE
        "legal_qa_validated": create_legal_qa_validated_workflow()  # ← New!
    }
```

**Important Rules:**
- ⚠️ The key (`"legal_qa_validated"`) must be unique
- ⚠️ Use lowercase with underscores (not spaces)
- ⚠️ This key becomes the workflow ID in the API

---

### Step 5: Restart the API

Your workflow is now defined in the backend. Restart the API to load it:

```bash
docker-compose restart api
```

Wait 5 seconds for the API to fully restart.

---

### Step 6: Test Your Workflow (API Only)

Test using curl or Postman:

```bash
curl -X POST http://localhost:8000/api/workflows/legal_qa_validated/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "question": "What are the key provisions of the Employment Ordinance in Hong Kong?"
    }
  }'
```

**Expected Response:**
```json
{
  "workflow": "Legal Q&A with Validation",
  "status": "completed",
  "steps": [
    {
      "name": "answer_question",
      "agent": "legal_research",
      "status": "completed",
      "result": {
        "answer": "The Employment Ordinance provides..."
      },
      "execution_time": 12.5
    },
    {
      "name": "validate_answer",
      "agent": "validation",
      "status": "completed",
      "result": {
        "validation_result": "passed",
        "quality_score": 88
      },
      "execution_time": 8.3
    }
  ],
  "final_result": {...},
  "execution_time": 20.8
}
```

✅ **If you see this, your workflow works!**

---

## 🎨 Frontend Integration

Now let's add a UI form so users can run your workflow from the browser.

### Step 7: Add HTML Form

Open: `/frontend/index.html`

Find the workflows section (around line 550-600) and add your workflow tab and form:

```html
<!-- Inside the workflow tabs section -->
<div class="agent-tabs">
    <button class="agent-tab-btn active" data-workflow="hr_onboarding">👥 HR Onboarding</button>
    <button class="agent-tab-btn" data-workflow="cs_ticket">💬 CS Ticket</button>
    <button class="agent-tab-btn" data-workflow="legal_compliance">⚖️ Legal Compliance</button>
    <button class="agent-tab-btn" data-workflow="simple_qa">💡 Q&A Validation</button>
    <button class="agent-tab-btn" data-workflow="multi_research">🔍 Multi-Research</button>

    <!-- ✏️ ADD YOUR TAB HERE -->
    <button class="agent-tab-btn" data-workflow="legal_qa_validated">✅ Legal QA+Validation</button>
</div>

<!-- Later in the file, add your form -->
<!-- Legal QA Validated Workflow Form -->
<div class="agent-content" id="workflow-legal_qa_validated">
    <h3>✅ Legal Q&A with Validation</h3>
    <p class="text-muted">Ask a legal question and get a validated answer</p>

    <form id="legalQAValidatedForm" class="form">
        <div class="form-group">
            <label for="legalQAQuestion">
                Legal Question <span style="color: #dc3545;">*</span>
            </label>
            <textarea
                id="legalQAQuestion"
                class="textarea-field"
                rows="4"
                placeholder="e.g., What are the requirements for employee termination in Hong Kong?"
                required
            ></textarea>
            <small class="text-muted">Ask any question about Hong Kong law</small>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">
                🚀 Run Workflow
            </button>
            <button type="button" class="btn btn-secondary clear-workflow">
                Clear
            </button>
        </div>
    </form>

    <!-- Result Panel -->
    <div id="legalQAValidatedResult" class="result-panel" style="display: none;">
        <!-- Results will appear here -->
    </div>
</div>
```

**HTML Breakdown:**

```html
<!-- Tab Button -->
<button class="agent-tab-btn" data-workflow="legal_qa_validated">
    ✅ Legal QA+Validation  ← Display text (can have emoji)
</button>
                                    ↑
                         Must match workflow ID

<!-- Form Container -->
<div class="agent-content" id="workflow-legal_qa_validated">
                                    ↑
                    Must be: workflow-{workflow_id}

<!-- Form -->
<form id="legalQAValidatedForm" class="form">
           ↑
    Unique form ID (used in JavaScript)

<!-- Input Field -->
<textarea id="legalQAQuestion" ...></textarea>
               ↑
    Unique field ID (used in JavaScript to get value)

<!-- Result Panel -->
<div id="legalQAValidatedResult" class="result-panel">
           ↑
    Unique result ID (where results are displayed)
```

---

### Step 8: Add JavaScript Handler

Open: `/frontend/static/js/app.js`

Find the workflow form handlers section (around line 1010-1075) and add:

```javascript
// Legal QA Validated Workflow
document.getElementById('legalQAValidatedForm').addEventListener('submit', async function(e) {
    e.preventDefault();  // Prevent page refresh

    // Collect user input from the form
    const inputData = {
        question: document.getElementById('legalQAQuestion').value  // Required field
    };

    // Execute the workflow
    await executeWorkflow(
        'legal_qa_validated',           // Workflow ID (must match backend)
        inputData,                       // Input data object
        'legalQAValidatedResult',        // Result panel ID
        e.target.querySelector('.btn-primary')  // Button element (for loading state)
    );
});
```

**JavaScript Breakdown:**

```javascript
document.getElementById('legalQAValidatedForm')
                         ↑
                Form ID from HTML

.addEventListener('submit', async function(e) {
    e.preventDefault();  // IMPORTANT: Stops page refresh

    const inputData = {
        question: document.getElementById('legalQAQuestion').value
                                           ↑
                                  Field ID from HTML
    };

    await executeWorkflow(
        'legal_qa_validated',      // ← Workflow ID (backend key)
        inputData,                 // ← Data to send
        'legalQAValidatedResult',  // ← Where to show results
        e.target.querySelector('.btn-primary')  // ← Button to show loading
    );
});
```

**Common Patterns:**

```javascript
// Single required field
const inputData = {
    question: document.getElementById('myField').value
};

// Multiple fields (some optional)
const inputData = {
    required_field: document.getElementById('field1').value,
    optional_field: document.getElementById('field2').value || undefined
};

// Multiple optional fields
const inputData = {
    name: document.getElementById('name').value || undefined,
    email: document.getElementById('email').value || undefined,
    message: document.getElementById('message').value || undefined
};
```

---

### Step 9: Test in Browser

1. **Refresh your browser** (F5 or Cmd+R)
2. Click on **"Multi-Agent Workflows"** tab
3. Click on your new **"✅ Legal QA+Validation"** tab
4. Enter a legal question
5. Click **"🚀 Run Workflow"**

**You should see:**
1. ✅ Button changes to "Processing Workflow..."
2. ✅ Spinner appears
3. ✅ After 20-40 seconds, results appear with both steps shown

---

## 🎓 Advanced Workflow Patterns

### Pattern 1: Accessing Previous Step Results

```python
# Step 2 accesses Step 1's answer
task_builder=lambda ctx, inp: {
    "data": ctx["step_1_name"].get("answer", "")  # Get 'answer' from step 1
}

# Alternative: Using step number
task_builder=lambda ctx, inp: {
    "data": ctx["step_1_result"].get("answer", "")
}
```

### Pattern 2: Combining Multiple Previous Results

```python
# Step 4 combines results from Steps 1, 2, and 3
workflow.add_step(WorkflowStep(
    name="final_synthesis",
    agent_name="synthesis",
    task_builder=lambda ctx, inp: {
        "task_type": "synthesis",
        "sources": [
            {
                "title": "Legal Analysis",
                "content": ctx["legal_step"].get("answer", "")
            },
            {
                "title": "HR Perspective",
                "content": ctx["hr_step"].get("answer", "")
            },
            {
                "title": "Risk Assessment",
                "content": str(ctx["risk_step"].get("analysis", ""))
            }
        ],
        "focus": "Create comprehensive compliance report"
    },
    description="Synthesize all perspectives into final report"
))
```

### Pattern 3: Conditional Data

```python
# Use user input if provided, otherwise use a default
task_builder=lambda ctx, inp: {
    "question": inp.get("custom_question") or "What is the default policy?",
    "context": inp.get("additional_context", "")  # Empty string if not provided
}
```

### Pattern 4: Formatted Context Strings

```python
# Combine multiple inputs into a formatted string
task_builder=lambda ctx, inp: {
    "data": f"""
    Employee: {inp.get('employee_name', 'Unknown')}
    Department: {inp.get('department', 'General')}

    Previous Analysis:
    {ctx['analysis_step'].get('analysis', {}).get('summary', '')}
    """,
    "focus": "Generate personalized onboarding plan"
}
```

---

## 🧪 Testing Your Workflow

### Test Checklist

Before considering your workflow complete, test:

- ✅ **Happy Path:** Normal input produces expected output
- ✅ **Empty Input:** Handle missing optional fields gracefully
- ✅ **Long Input:** Test with large text inputs
- ✅ **Error Handling:** Ensure failed steps show clear errors
- ✅ **Step Order:** Verify steps execute in correct sequence
- ✅ **Context Passing:** Confirm data flows between steps

### API Testing (Command Line)

```bash
# Test with minimal input
curl -X POST http://localhost:8000/api/workflows/YOUR_WORKFLOW_ID/execute \
  -H "Content-Type: application/json" \
  -d '{"input": {"question": "test"}}'

# Test with full input
curl -X POST http://localhost:8000/api/workflows/YOUR_WORKFLOW_ID/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "field1": "value1",
      "field2": "value2",
      "field3": "value3"
    }
  }' | python3 -m json.tool
```

### Browser Testing

1. Open Browser DevTools (F12)
2. Go to **Console** tab
3. Run workflow and watch for errors
4. Check **Network** tab for API calls

**Common Issues:**

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| No loading indicator | JavaScript error | Check browser console |
| 404 Not Found | Workflow ID mismatch | Verify ID matches between files |
| Agent not found error | Wrong agent name | Check agent_name matches registry |
| Empty results | Wrong field ID in JS | Verify getElementById IDs |
| Nothing happens | Form ID wrong | Check form ID in addEventListener |

---

## 🔧 Troubleshooting

### Problem: "Agent 'xxx' not found or not initialized"

**Cause:** Agent name doesn't match the registry.

**Solution:** Use exact names:
- ✅ `legal_research` (correct)
- ❌ `legal` (wrong)
- ✅ `hr_policy` (correct)
- ❌ `hr` (wrong)
- ✅ `cs_document` (correct)
- ❌ `cs` (wrong)

### Problem: "No data provided for analysis"

**Cause:** Analysis agent needs `data` field, not `content`.

**Solution:**
```python
# ❌ Wrong
task_builder=lambda ctx, inp: {
    "content": "text to analyze"
}

# ✅ Correct
task_builder=lambda ctx, inp: {
    "data": "text to analyze"
}
```

### Problem: Workflow not showing in UI

**Cause:** Not registered in `get_all_workflows()`

**Solution:** Add to the return dictionary:
```python
def get_all_workflows():
    return {
        "existing_workflow": create_existing_workflow(),
        "your_workflow": create_your_workflow()  # ← Add this
    }
```

### Problem: Form not submitting

**Cause:** JavaScript form ID doesn't match HTML form ID

**Solution:**
```javascript
// HTML
<form id="myWorkflowForm">

// JavaScript (must match exactly)
document.getElementById('myWorkflowForm').addEventListener(...)
```

### Problem: "KeyError" when accessing context

**Cause:** Step name doesn't match context key

**Solution:**
```python
# Step 1 definition
workflow.add_step(WorkflowStep(
    name="legal_research_step",  # ← This exact name
    ...
))

# Step 2 accessing Step 1
task_builder=lambda ctx, inp: {
    "data": ctx["legal_research_step"].get("answer")  # ← Use same name
}
```

---

## 📚 Complete Examples

### Example 1: Simple Two-Step Workflow

**Goal:** Research a topic and validate the answer.

```python
def create_research_validated_workflow() -> Workflow:
    workflow = Workflow(
        name="Research with Validation",
        description="Research a topic and validate accuracy"
    )

    # Step 1: Research
    workflow.add_step(WorkflowStep(
        name="research",
        agent_name="legal_research",
        task_builder=lambda ctx, inp: {
            "question": inp.get("topic", "")
        },
        description="Research the topic"
    ))

    # Step 2: Validate
    workflow.add_step(WorkflowStep(
        name="validate",
        agent_name="validation",
        task_builder=lambda ctx, inp: {
            "documents": [{
                "title": "Research Result",
                "content": ctx["research"].get("answer", "")
            }],
            "validation_type": "accuracy"
        },
        description="Validate research accuracy"
    ))

    return workflow
```

---

### Example 2: Three-Step Analysis Workflow

**Goal:** Get HR policy, analyze it, and create summary.

```python
def create_hr_analysis_workflow() -> Workflow:
    workflow = Workflow(
        name="HR Policy Analysis",
        description="Analyze HR policies and extract key points"
    )

    # Step 1: Get HR Policy
    workflow.add_step(WorkflowStep(
        name="get_policy",
        agent_name="hr_policy",
        task_builder=lambda ctx, inp: {
            "question": inp.get("policy_question", ""),
            "task_type": "policy_search"
        },
        description="Retrieve HR policy information"
    ))

    # Step 2: Analyze Policy
    workflow.add_step(WorkflowStep(
        name="analyze",
        agent_name="analysis",
        task_builder=lambda ctx, inp: {
            "data": ctx["get_policy"].get("answer", ""),
            "focus": inp.get("analysis_focus", "Extract key requirements"),
            "analysis_type": "themes"
        },
        description="Extract key themes from policy"
    ))

    # Step 3: Create Summary
    workflow.add_step(WorkflowStep(
        name="summarize",
        agent_name="synthesis",
        task_builder=lambda ctx, inp: {
            "task_type": "synthesis",
            "sources": [
                {
                    "title": "HR Policy",
                    "content": ctx["get_policy"].get("answer", "")
                },
                {
                    "title": "Analysis",
                    "content": str(ctx["analyze"].get("analysis", ""))
                }
            ],
            "focus": "Create employee-friendly policy summary"
        },
        description="Generate accessible summary"
    ))

    return workflow
```

---

### Example 3: Multi-Source Comparison

**Goal:** Get legal and HR perspectives, compare them.

```python
def create_compliance_comparison_workflow() -> Workflow:
    workflow = Workflow(
        name="Compliance Comparison",
        description="Compare legal requirements with current HR policies"
    )

    # Step 1: Legal Requirements
    workflow.add_step(WorkflowStep(
        name="legal_reqs",
        agent_name="legal_research",
        task_builder=lambda ctx, inp: {
            "question": f"What are the legal requirements for {inp.get('topic', '')}?"
        },
        description="Research legal requirements"
    ))

    # Step 2: Current HR Policy
    workflow.add_step(WorkflowStep(
        name="hr_policy",
        agent_name="hr_policy",
        task_builder=lambda ctx, inp: {
            "question": f"What is our current policy on {inp.get('topic', '')}?",
            "task_type": "policy_search"
        },
        description="Get current HR policy"
    ))

    # Step 3: Compare
    workflow.add_step(WorkflowStep(
        name="comparison",
        agent_name="analysis",
        task_builder=lambda ctx, inp: {
            "data": [
                f"Legal Requirements:\n{ctx['legal_reqs'].get('answer', '')}",
                f"HR Policy:\n{ctx['hr_policy'].get('answer', '')}"
            ],
            "focus": "Identify gaps between legal requirements and current policy",
            "analysis_type": "comparison"
        },
        description="Compare legal vs policy"
    ))

    # Step 4: Recommendations
    workflow.add_step(WorkflowStep(
        name="recommendations",
        agent_name="synthesis",
        task_builder=lambda ctx, inp: {
            "task_type": "synthesis",
            "sources": [
                {
                    "title": "Legal Requirements",
                    "content": ctx["legal_reqs"].get("answer", "")
                },
                {
                    "title": "Current Policy",
                    "content": ctx["hr_policy"].get("answer", "")
                },
                {
                    "title": "Gap Analysis",
                    "content": str(ctx["comparison"].get("analysis", ""))
                }
            ],
            "focus": "Generate actionable recommendations to ensure compliance"
        },
        description="Create compliance action plan"
    ))

    return workflow
```

---

## 🎯 Quick Reference

### Agent Name Reference
```python
"legal_research"  # Legal questions, HK ordinances
"hr_policy"       # HR policies, employee questions
"cs_document"     # Customer service, support
"analysis"        # Text analysis, insights
"synthesis"       # Combine sources, reports
"validation"      # Quality checking, accuracy
```

### Common Task Builder Patterns
```python
# Simple pass-through
task_builder=lambda ctx, inp: {
    "question": inp.get("question", "")
}

# Access previous step
task_builder=lambda ctx, inp: {
    "data": ctx["step_name"].get("answer", "")
}

# Multiple sources
task_builder=lambda ctx, inp: {
    "sources": [
        {"title": "Source 1", "content": ctx["step1"].get("answer", "")},
        {"title": "Source 2", "content": ctx["step2"].get("answer", "")}
    ]
}
```

### File Locations
```
✏️ Backend:  /api/workflows/workflow_definitions.py
✏️ Frontend: /frontend/index.html
✏️ Frontend: /frontend/static/js/app.js
🚫 Engine:   /api/workflows/workflow_engine.py (don't modify)
```

### Restart Commands
```bash
# Restart just the API
docker-compose restart api

# Restart everything
docker-compose restart

# View logs
docker-compose logs -f api
```

---

## 📞 Getting Help

### Resources

1. **Existing Workflows:** Study `/api/workflows/workflow_definitions.py`
2. **Agent Code:** Check `/api/agents/` for agent input/output formats
3. **API Docs:** Visit `http://localhost:8000/docs`
4. **Browser Console:** Press F12 to see JavaScript errors

### Common Questions

**Q: How many steps can a workflow have?**
A: Unlimited, but 2-5 steps is typical. More steps = longer execution time.

**Q: Can steps run in parallel?**
A: No, steps run sequentially. Each step waits for the previous one to complete.

**Q: Can I reuse the same agent twice?**
A: Yes! You can call the same agent multiple times with different tasks.

**Q: How do I debug a workflow?**
A: Check the API response - it shows each step's status and any errors.

**Q: Can I modify existing workflows?**
A: Yes, but be careful not to break existing functionality. Test thoroughly.

---

## ✅ Checklist for Creating a New Workflow

- [ ] Planned workflow steps and agent sequence
- [ ] Created workflow function in `workflow_definitions.py`
- [ ] Registered workflow in `get_all_workflows()`
- [ ] Used correct agent names (matching registry)
- [ ] Used correct field names for each agent
- [ ] Added HTML form in `index.html`
- [ ] Added workflow tab button
- [ ] Added JavaScript handler in `app.js`
- [ ] Restarted API (`docker-compose restart api`)
- [ ] Tested via API (curl)
- [ ] Tested via browser UI
- [ ] Verified loading indicators work
- [ ] Checked results display correctly
- [ ] Tested error handling (empty inputs, etc.)

---

**🎉 Congratulations!** You now know how to create custom Multi-Agent Workflows!

**Next Steps:**
1. Study the 5 existing workflows for more examples
2. Create simple 2-step workflows first
3. Gradually add more complexity
4. Share your workflows with the team

**Happy Coding!** 🚀
