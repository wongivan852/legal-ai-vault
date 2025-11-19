# 📚 Synthesis Agent - Document Embedding Integration Guide

**Date**: 2025-11-19
**Purpose**: Enable Synthesis Agent to automatically retrieve embedded documents from Qdrant vector database
**Status**: Implementation Guide

---

## Current State vs. Desired State

### Current Implementation

**How it works now**:
Users manually input sources through the web UI:

```javascript
// User manually types in sources
{
  "task": {
    "sources": [
      {
        "title": "Building Management Ordinance",
        "content": "User manually types content here..."
      },
      {
        "title": "Safety Guidelines",
        "content": "User manually types more content..."
      }
    ],
    "task_type": "synthesis"
  }
}
```

**Limitations**:
- ❌ Users must manually copy/paste documents
- ❌ Cannot leverage existing embedded documents in Qdrant
- ❌ No automatic document retrieval
- ❌ Time-consuming for large documents

---

### Desired Implementation

**How it should work**:
Synthesis Agent automatically retrieves relevant documents from Qdrant:

```javascript
// User provides search query
{
  "task": {
    "question": "What are building owner responsibilities?",
    "document_queries": [
      "Building Management Ordinance requirements",
      "Building safety regulations"
    ],
    "task_type": "synthesis",
    "auto_retrieve": true,  // NEW: Auto-fetch from Qdrant
    "top_k_per_query": 3    // NEW: How many docs per query
  }
}
```

**Benefits**:
- ✅ Automatic document retrieval from embedded database
- ✅ Leverages existing Qdrant vector store
- ✅ Semantic search for relevant documents
- ✅ Faster workflow for users
- ✅ Access to entire legal document library

---

## System Architecture

### Current Components

```
┌─────────────────────────────────────────────┐
│         Synthesis Agent (Current)           │
│  • Receives manual sources from user        │
│  • Merges/reconciles content                │
│  • Generates synthesis output               │
└─────────────────────────────────────────────┘
                    ↑
                    │ Manual input
                    │
            ┌───────┴────────┐
            │   Web UI       │
            └────────────────┘


┌──────────────────────────────────────────────┐
│        Embedded Documents (Qdrant)           │
│  • HK Legal Ordinances                       │
│  • Vector embeddings                         │
│  • NOT connected to Synthesis Agent          │
└──────────────────────────────────────────────┘
```

### Proposed Architecture

```
┌─────────────────────────────────────────────┐
│      Enhanced Synthesis Agent (New)         │
│  1. Receives document queries               │
│  2. Queries Qdrant for relevant docs ──┐    │
│  3. Retrieves top K results            │    │
│  4. Merges/reconciles content          │    │
│  5. Generates synthesis output         │    │
└────────────────────────────────────────┘    │
                    ↑                          │
                    │                          ↓
            ┌───────┴────────┐       ┌────────────────┐
            │   Web UI       │       │  RAG Service   │
            └────────────────┘       │  • embed()     │
                                     │  • search()    │
                                     └────────┬───────┘
                                              ↓
                                    ┌──────────────────┐
                                    │  Qdrant Vector   │
                                    │  Database        │
                                    │  • HK Ordinances │
                                    │  • Embeddings    │
                                    └──────────────────┘
```

---

## Implementation Steps

### Step 1: Enhance Synthesis Agent with RAG Integration

Create a new version of the Synthesis Agent that can retrieve documents:

**File**: `/api/agents/synthesis_agent_enhanced.py`

```python
"""
Enhanced Synthesis Agent with Document Embedding Integration
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import json

from agents.synthesis_agent import SynthesisAgent
from services.rag_service import RAGService

logger = logging.getLogger(__name__)


class EnhancedSynthesisAgent(SynthesisAgent):
    """
    Synthesis Agent with automatic document retrieval from Qdrant
    """

    def __init__(self, llm_service, rag_service: RAGService):
        """
        Initialize enhanced synthesis agent

        Args:
            llm_service: OllamaService for LLM reasoning
            rag_service: RAGService for document retrieval
        """
        super().__init__(llm_service)
        self.rag_service = rag_service

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute synthesis task with optional auto-retrieval

        Args:
            task: Task specification with:
                - auto_retrieve: bool - Enable automatic document retrieval
                - document_queries: List[str] - Queries for document retrieval
                - top_k_per_query: int - Number of docs to retrieve per query
                - question: str - Original user question (for context)
                - sources: List[Dict] - Manual sources (if auto_retrieve=False)
                - synthesis_type: str - Type of synthesis
                - focus: str - Focus area

        Returns:
            Dict with synthesis results
        """
        start_time = datetime.now()

        try:
            auto_retrieve = task.get("auto_retrieve", False)

            if auto_retrieve:
                # Auto-retrieve documents from Qdrant
                logger.info("Auto-retrieving documents from Qdrant...")
                sources = await self._retrieve_documents(task)

                if not sources:
                    return {
                        "agent": self.name,
                        "status": "failed",
                        "error": "No relevant documents found in database"
                    }

                # Update task with retrieved sources
                task["sources"] = sources
                logger.info(f"Retrieved {len(sources)} documents for synthesis")

            # Execute standard synthesis
            return await super().execute(task)

        except Exception as e:
            logger.error(f"Enhanced synthesis execution error: {e}", exc_info=True)
            return {
                "agent": self.name,
                "status": "failed",
                "error": str(e),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

    async def _retrieve_documents(
        self,
        task: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Retrieve documents from Qdrant based on queries

        Args:
            task: Task containing document_queries and retrieval params

        Returns:
            List of retrieved documents formatted for synthesis
        """
        document_queries = task.get("document_queries", [])
        question = task.get("question", "")
        top_k_per_query = task.get("top_k_per_query", 3)
        min_score = task.get("min_score", 0.6)

        # If no document queries provided, use the main question
        if not document_queries and question:
            document_queries = [question]

        all_sources = []
        seen_docs = set()  # Prevent duplicates

        for query in document_queries:
            logger.info(f"Retrieving documents for query: {query}")

            # Use RAG service to retrieve relevant documents
            result = await self.rag_service.query(
                question=query,
                top_k=top_k_per_query,
                search_type="sections",  # or "documents"
                min_score=min_score,
                include_metadata=True
            )

            if result.get("success") and result.get("sources"):
                # Format sources for synthesis
                for source in result["sources"]:
                    # Create unique identifier
                    doc_id = f"{source['doc_number']}_{source.get('section_number', '')}"

                    if doc_id not in seen_docs:
                        seen_docs.add(doc_id)

                        # Format as synthesis source
                        formatted_source = {
                            "title": f"{source['doc_name']} - {source.get('section_heading', source['doc_title'])}",
                            "content": source.get("preview", source.get("content", "")),
                            "source": f"Cap. {source['doc_number']}, Section {source.get('section_number', 'N/A')}",
                            "score": source.get("score", 0),
                            "metadata": {
                                "doc_number": source["doc_number"],
                                "doc_name": source["doc_name"],
                                "section_number": source.get("section_number"),
                                "type": source.get("type", "section")
                            }
                        }

                        all_sources.append(formatted_source)

        logger.info(f"Total unique documents retrieved: {len(all_sources)}")
        return all_sources
```

---

### Step 2: Update Agent Router

Modify the agent initialization to use the enhanced version:

**File**: `/api/agents/__init__.py` (or where agents are initialized)

```python
from agents.synthesis_agent_enhanced import EnhancedSynthesisAgent
from services.rag_service import RAGService

def initialize_agents(db, llm_service, qdrant_client):
    """Initialize all agents"""

    # Create RAG service
    rag_service = RAGService(
        db_session=db,
        qdrant_client=qdrant_client,
        ollama_service=llm_service
    )

    # Initialize enhanced synthesis agent with RAG capability
    synthesis_agent = EnhancedSynthesisAgent(
        llm_service=llm_service,
        rag_service=rag_service
    )

    return {
        "legal_research": LegalResearchAgent(llm_service, rag_service),
        "hr_policy": HRPolicyAgent(llm_service),
        "cs_document": CSDocumentAgent(llm_service),
        "analysis": AnalysisAgent(llm_service),
        "synthesis": synthesis_agent,  # Enhanced version
        "validation": ValidationAgent(llm_service)
    }
```

---

### Step 3: Update Frontend UI

Add document query options to the Synthesis Agent form:

**File**: `/frontend/index.html`

```html
<!-- Enhanced Synthesis Agent Form -->
<div id="synthesis-agent" class="agent-content">
    <h3>🔗 Synthesis Agent</h3>
    <p>Combine multiple sources or auto-retrieve documents from database</p>

    <form id="synthesisAgentForm" class="agent-form">
        <!-- NEW: Auto-Retrieve Toggle -->
        <div class="form-group">
            <label>
                <input type="checkbox" id="synthesisAutoRetrieve" name="autoRetrieve">
                <strong>Auto-Retrieve Documents from Database</strong>
            </label>
            <small class="help-text">Automatically fetch relevant documents from HK Ordinances database</small>
        </div>

        <!-- NEW: Document Query Section (shown when auto-retrieve is enabled) -->
        <div id="synthesisAutoRetrieveSection" style="display: none;">
            <div class="form-group">
                <label for="synthesisQuestion">Main Question/Topic</label>
                <input type="text"
                       id="synthesisQuestion"
                       class="input-field"
                       placeholder="e.g., What are building owner responsibilities?">
            </div>

            <div class="form-group">
                <label for="synthesisQueries">Document Queries (Optional)</label>
                <div id="synthesisQueriesContainer">
                    <input type="text"
                           class="input-field synthesis-query"
                           placeholder="Query 1: e.g., Building Management Ordinance requirements">
                </div>
                <button type="button"
                        id="addQueryBtn"
                        class="btn-secondary"
                        style="margin-top: 10px;">
                    + Add Query
                </button>
                <small class="help-text">Leave empty to use main question only</small>
            </div>

            <div class="form-group">
                <label for="synthesisTopK">Documents per Query</label>
                <select id="synthesisTopK" class="input-field">
                    <option value="3">3 documents</option>
                    <option value="5" selected>5 documents</option>
                    <option value="10">10 documents</option>
                </select>
            </div>
        </div>

        <!-- Existing Manual Sources Section -->
        <div id="synthesisManualSection">
            <div class="form-group">
                <label>Manual Sources</label>
                <div id="synthesisSourcesContainer">
                    <div class="synthesis-source">
                        <input type="text" class="input-field source-title"
                               placeholder="Source 1 Title">
                        <textarea class="textarea-field source-content"
                                  rows="4"
                                  placeholder="Source 1 Content"></textarea>
                    </div>
                </div>
                <button type="button" id="addSource" class="btn-secondary">+ Add Source</button>
            </div>
        </div>

        <!-- Focus Field (common to both modes) -->
        <div class="form-group">
            <label for="synthesisFocus">Synthesis Focus (Optional)</label>
            <input type="text"
                   id="synthesisFocus"
                   class="input-field"
                   placeholder="e.g., compliance requirements, safety regulations">
        </div>

        <div class="button-group">
            <button type="submit" id="synthesisAgentBtn" class="btn-primary">
                <span class="btn-text">Synthesize</span>
                <span class="btn-loading" style="display: none;">
                    <span class="spinner"></span> Synthesizing...
                </span>
            </button>
            <button type="button" id="clearSynthesis" class="btn-secondary">Clear</button>
        </div>
    </form>

    <div id="synthesisAgentResult" class="result-panel" style="display: none;"></div>
</div>
```

---

### Step 4: Update Frontend JavaScript

Add logic to handle auto-retrieve mode:

**File**: `/frontend/static/js/app.js`

```javascript
// Toggle auto-retrieve section
document.getElementById('synthesisAutoRetrieve').addEventListener('change', function() {
    const autoRetrieveSection = document.getElementById('synthesisAutoRetrieveSection');
    const manualSection = document.getElementById('synthesisManualSection');

    if (this.checked) {
        autoRetrieveSection.style.display = 'block';
        manualSection.style.display = 'none';
    } else {
        autoRetrieveSection.style.display = 'none';
        manualSection.style.display = 'block';
    }
});

// Add query input field
document.getElementById('addQueryBtn').addEventListener('click', function() {
    const container = document.getElementById('synthesisQueriesContainer');
    const queryCount = container.querySelectorAll('.synthesis-query').length + 1;

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'input-field synthesis-query';
    input.placeholder = `Query ${queryCount}: e.g., Building safety regulations`;
    input.style.marginTop = '10px';

    container.appendChild(input);
});

// Enhanced Synthesis Agent handler
async function handleSynthesisAgent(e) {
    e.preventDefault();

    const btn = document.getElementById('synthesisAgentBtn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    const resultPanel = document.getElementById('synthesisAgentResult');

    const autoRetrieve = document.getElementById('synthesisAutoRetrieve').checked;
    const focus = document.getElementById('synthesisFocus').value;

    let requestBody = {
        task: {
            task_type: 'synthesis',
            focus: focus || undefined,
            auto_retrieve: autoRetrieve
        }
    };

    if (autoRetrieve) {
        // Auto-retrieve mode
        const question = document.getElementById('synthesisQuestion').value;
        const queryElements = document.querySelectorAll('.synthesis-query');
        const queries = Array.from(queryElements)
            .map(el => el.value)
            .filter(q => q.trim() !== '');
        const topK = parseInt(document.getElementById('synthesisTopK').value);

        if (!question && queries.length === 0) {
            showError('Please provide a question or at least one document query.');
            return;
        }

        requestBody.task.question = question;
        requestBody.task.document_queries = queries.length > 0 ? queries : undefined;
        requestBody.task.top_k_per_query = topK;

    } else {
        // Manual mode
        const sourceElements = document.querySelectorAll('.synthesis-source');
        const sources = [];

        sourceElements.forEach(sourceEl => {
            const title = sourceEl.querySelector('.source-title').value;
            const content = sourceEl.querySelector('.source-content').value;

            if (title && content) {
                sources.push({ title, content });
            }
        });

        if (sources.length < 2) {
            showError('Please provide at least 2 sources for synthesis.');
            return;
        }

        requestBody.task.sources = sources;
    }

    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    resultPanel.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/api/agents/synthesis/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        const data = await response.json();

        if (data.status === 'completed' || data.status === 'success') {
            displayAgentResult(resultPanel, data, '🔗 Synthesis Results');
        } else {
            showError('Synthesis failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Synthesis agent error:', error);
        showError('Failed to execute synthesis agent.');
    } finally {
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}
```

---

## Usage Examples

### Example 1: Auto-Retrieve Single Topic

**User Input** (Web UI):
- ✅ Auto-Retrieve: Enabled
- Question: "What are building owner responsibilities?"
- Documents per Query: 5

**API Request**:
```json
{
  "task": {
    "auto_retrieve": true,
    "question": "What are building owner responsibilities?",
    "top_k_per_query": 5,
    "task_type": "synthesis",
    "focus": "compliance requirements"
  }
}
```

**What Happens**:
1. Agent embeds the question
2. Searches Qdrant for top 5 relevant sections
3. Retrieves: BMO sections, Safety Ordinances, etc.
4. Synthesizes comprehensive answer
5. Returns merged content with citations

**Expected Output**:
```
Building Owner Responsibilities (Comprehensive Overview)

Based on Cap. 344 (Building Management Ordinance) and related ordinances:

1. Maintenance Obligations (Cap. 344, Section 12)
   - Building owners must maintain common areas...
   - Regular inspections required...

2. Safety Requirements (Cap. 123, Section 8)
   - Fire safety equipment must be maintained...
   - Emergency exits must remain accessible...

3. Financial Responsibilities
   - Owners corporations must maintain reserve funds...

[Content synthesized from 5 relevant ordinance sections]
```

---

### Example 2: Multiple Specific Queries

**User Input**:
- ✅ Auto-Retrieve: Enabled
- Question: "Building management compliance"
- Query 1: "Building Management Ordinance requirements"
- Query 2: "Fire safety regulations for buildings"
- Query 3: "Owners corporation duties"
- Documents per Query: 3

**API Request**:
```json
{
  "task": {
    "auto_retrieve": true,
    "question": "Building management compliance",
    "document_queries": [
      "Building Management Ordinance requirements",
      "Fire safety regulations for buildings",
      "Owners corporation duties"
    ],
    "top_k_per_query": 3,
    "task_type": "synthesis"
  }
}
```

**What Happens**:
1. Searches 3 separate queries
2. Retrieves up to 9 documents total (3 per query)
3. Removes duplicates
4. Synthesizes comprehensive compliance guide

---

### Example 3: Manual Mode (Current Functionality)

**User Input**:
- ❌ Auto-Retrieve: Disabled
- Source 1: [Manual input]
- Source 2: [Manual input]

**API Request**:
```json
{
  "task": {
    "auto_retrieve": false,
    "sources": [
      {
        "title": "BMO Requirements",
        "content": "User types content..."
      },
      {
        "title": "Safety Guidelines",
        "content": "User types content..."
      }
    ],
    "task_type": "synthesis"
  }
}
```

---

## Testing

### Test 1: Auto-Retrieve with Question

```bash
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "auto_retrieve": true,
      "question": "What are building owner responsibilities?",
      "top_k_per_query": 5,
      "task_type": "synthesis"
    }
  }'
```

**Expected**: Synthesis of 5 relevant ordinance sections

---

### Test 2: Auto-Retrieve with Multiple Queries

```bash
curl -X POST http://localhost:8000/api/agents/synthesis/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "auto_retrieve": true,
      "question": "Building compliance requirements",
      "document_queries": [
        "Building Management Ordinance",
        "Fire safety regulations"
      ],
      "top_k_per_query": 3,
      "task_type": "synthesis"
    }
  }'
```

**Expected**: Synthesis of up to 6 documents (3 per query, deduplicated)

---

## Benefits Summary

| Feature | Before | After |
|---------|--------|-------|
| **Document Input** | Manual copy/paste | Auto-retrieve from Qdrant |
| **Speed** | Slow (user types) | Fast (automated search) |
| **Access** | Limited to what user knows | Entire legal database |
| **Accuracy** | Depends on user selection | Semantic search finds best matches |
| **Sources** | User provides 2-3 | System retrieves 5-10+ relevant docs |
| **Citations** | Manual | Automatic with ordinance references |

---

## Implementation Checklist

- [ ] Create `synthesis_agent_enhanced.py`
- [ ] Update agent initialization with RAG service
- [ ] Modify frontend HTML with auto-retrieve toggle
- [ ] Update frontend JavaScript handlers
- [ ] Test auto-retrieve mode
- [ ] Test manual mode (ensure backwards compatibility)
- [ ] Update API documentation
- [ ] Create user guide
- [ ] Deploy to production

---

## Alternative Approach: Hybrid Mode

Allow users to mix auto-retrieved and manual sources:

```json
{
  "task": {
    "auto_retrieve": true,
    "question": "Building regulations",
    "top_k_per_query": 3,
    "manual_sources": [
      {
        "title": "Company Policy",
        "content": "Our company requires..."
      }
    ],
    "task_type": "synthesis"
  }
}
```

This retrieves 3 docs from Qdrant + includes 1 manual source = 4 total sources for synthesis.

---

## Conclusion

By integrating the Synthesis Agent with the RAG service and Qdrant vector database, users can:

✅ **Leverage existing embedded documents** instead of manual input
✅ **Perform semantic search** to find the most relevant sources
✅ **Synthesize comprehensive answers** from multiple ordinances
✅ **Save time** with automated document retrieval
✅ **Ensure accuracy** with proper citations and references

**Next Step**: Implement `EnhancedSynthesisAgent` and update the UI!

---

*End of Synthesis Agent Document Embedding Integration Guide*
