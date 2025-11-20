// Vault AI Platform - Frontend JavaScript

const API_BASE_URL = 'http://localhost:8000';

// State
let currentHealth = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeAgentTabs();
    initializeForms();
    checkHealth();

    // Refresh health every 30 seconds
    setInterval(checkHealth, 30000);
});

// Tab Management
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;

            // Update active states
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            button.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
        });
    });
}

// Agent Sub-Tab Management
function initializeAgentTabs() {
    const agentTabButtons = document.querySelectorAll('.agent-tab-btn');
    const agentContents = document.querySelectorAll('.agent-content');

    agentTabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const agentName = button.dataset.agent;

            // Update active states
            agentTabButtons.forEach(btn => btn.classList.remove('active'));
            agentContents.forEach(content => content.classList.remove('active'));

            button.classList.add('active');
            document.getElementById(`${agentName}-agent`).classList.add('active');
        });
    });
}

// Form Initialization
function initializeForms() {
    // Text Generation Form
    const generateForm = document.getElementById('generateForm');
    const clearGenerateBtn = document.getElementById('clearGenerate');
    generateForm.addEventListener('submit', handleGenerate);
    clearGenerateBtn.addEventListener('click', () => {
        generateForm.reset();
        document.getElementById('generateResult').style.display = 'none';
    });

    // Legal Agent Form
    const legalAgentForm = document.getElementById('legalAgentForm');
    const clearLegalBtn = document.getElementById('clearLegal');
    legalAgentForm.addEventListener('submit', handleLegalAgent);
    clearLegalBtn.addEventListener('click', () => {
        legalAgentForm.reset();
        document.getElementById('legalAgentResult').style.display = 'none';
    });

    // HR Agent Form
    const hrAgentForm = document.getElementById('hrAgentForm');
    const clearHRBtn = document.getElementById('clearHR');
    hrAgentForm.addEventListener('submit', handleHRAgent);
    clearHRBtn.addEventListener('click', () => {
        hrAgentForm.reset();
        document.getElementById('hrAgentResult').style.display = 'none';
    });

    // CS Agent Form
    const csAgentForm = document.getElementById('csAgentForm');
    const clearCSBtn = document.getElementById('clearCS');
    csAgentForm.addEventListener('submit', handleCSAgent);
    clearCSBtn.addEventListener('click', () => {
        csAgentForm.reset();
        document.getElementById('csAgentResult').style.display = 'none';
    });

    // Analysis Agent Form
    const analysisAgentForm = document.getElementById('analysisAgentForm');
    const clearAnalysisBtn = document.getElementById('clearAnalysis');
    analysisAgentForm.addEventListener('submit', handleAnalysisAgent);
    clearAnalysisBtn.addEventListener('click', () => {
        analysisAgentForm.reset();
        document.getElementById('analysisAgentResult').style.display = 'none';
    });

    // Synthesis Agent Form
    const synthesisAgentForm = document.getElementById('synthesisAgentForm');
    const clearSynthesisBtn = document.getElementById('clearSynthesis');
    const addSourceBtn = document.getElementById('addSource');
    const autoRetrieveCheckbox = document.getElementById('synthesisAutoRetrieve');
    synthesisAgentForm.addEventListener('submit', handleSynthesisAgent);
    clearSynthesisBtn.addEventListener('click', () => {
        synthesisAgentForm.reset();
        document.getElementById('synthesisAgentResult').style.display = 'none';
        toggleSynthesisMode(); // Reset UI to manual mode
    });
    addSourceBtn.addEventListener('click', addSynthesisSource);
    autoRetrieveCheckbox.addEventListener('change', toggleSynthesisMode);

    // Validation Agent Form
    const validationAgentForm = document.getElementById('validationAgentForm');
    const clearValidationBtn = document.getElementById('clearValidation');
    const addValidationDocBtn = document.getElementById('addValidationDoc');
    validationAgentForm.addEventListener('submit', handleValidationAgent);
    clearValidationBtn.addEventListener('click', () => {
        validationAgentForm.reset();
        document.getElementById('validationAgentResult').style.display = 'none';
    });
    addValidationDocBtn.addEventListener('click', addValidationDoc);

    // Models
    document.getElementById('refreshModels').addEventListener('click', loadModels);
}

// Health Check
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        currentHealth = data;
        updateHealthDisplay(data);
    } catch (error) {
        console.error('Health check failed:', error);
        updateHealthDisplay(null);
    }
}

function updateHealthDisplay(health) {
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');
    const currentModel = document.getElementById('currentModel');
    const apiVersion = document.getElementById('apiVersion');

    if (health && health.status === 'healthy') {
        statusDot.className = 'status-dot healthy';
        statusText.textContent = 'System Healthy';
        currentModel.textContent = health.ollama?.llm_model || 'Unknown';
        apiVersion.textContent = health.api_version || 'v2.0.0';
    } else {
        statusDot.className = 'status-dot unhealthy';
        statusText.textContent = 'System Unhealthy';
        currentModel.textContent = 'Unavailable';
    }
}

// Text Generation
async function handleGenerate(e) {
    e.preventDefault();

    const btn = document.getElementById('generateBtn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    const resultPanel = document.getElementById('generateResult');

    // Get form values
    const prompt = document.getElementById('prompt').value;
    const systemPrompt = document.getElementById('systemPrompt').value;
    const maxTokens = parseInt(document.getElementById('maxTokens').value);
    const temperature = parseFloat(document.getElementById('temperature').value);

    // Show loading state
    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    resultPanel.style.display = 'none';

    // Show progress message after 10 seconds
    let timeoutMsg = setTimeout(() => {
        btnLoading.innerHTML = '<span class="spinner"></span> Still generating... (Large models may take 2-5 minutes)';
    }, 10000);

    try {
        const response = await fetch(`${API_BASE_URL}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt,
                system_prompt: systemPrompt || undefined,
                max_tokens: maxTokens,
                temperature
            })
        });

        const data = await response.json();

        if (data.success) {
            displayGenerateResult(data);
        } else {
            showError('Generation failed: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Generation error:', error);
        showError('Failed to connect to API. Make sure the backend is running.');
    } finally {
        clearTimeout(timeoutMsg);
        btnLoading.innerHTML = '<span class="spinner"></span> Generating...';
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

function displayGenerateResult(data) {
    const resultPanel = document.getElementById('generateResult');
    const responseMeta = document.getElementById('generateMeta');
    const responseContent = document.getElementById('generateResponse');
    const responseStats = document.getElementById('generateStats');

    // Meta
    responseMeta.textContent = `Model: ${data.model}`;

    // Content
    responseContent.textContent = data.response;

    // Stats
    const stats = data.stats;
    responseStats.innerHTML = `
        <div class="stat-item">
            <span class="stat-label">Duration</span>
            <span class="stat-value">${(stats.total_duration_ms / 1000).toFixed(2)}s</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Prompt Tokens</span>
            <span class="stat-value">${stats.prompt_tokens}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Completion Tokens</span>
            <span class="stat-value">${stats.completion_tokens}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Tokens/sec</span>
            <span class="stat-value">${((stats.completion_tokens / stats.total_duration_ms) * 1000).toFixed(1)}</span>
        </div>
    `;

    resultPanel.style.display = 'block';
    resultPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// RAG - Retrieval Augmented Generation (DEPRECATED - Use Legal Research Agent instead)
// Commenting out as we removed the standalone Legal RAG tab
// The Legal Research Agent in AI Agents tab provides the same functionality
/*
async function handleRAG(e) {
    // ... function removed to clean up code ...
}

function displayRAGResult(data) {
    // ... function removed to clean up code ...
}
*/

// Legal Research Agent
async function handleLegalAgent(e) {
    e.preventDefault();

    const btn = document.getElementById('legalAgentBtn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    const resultPanel = document.getElementById('legalAgentResult');

    const question = document.getElementById('legalQuestion').value;

    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    resultPanel.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/api/agents/legal_research/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                task: {
                    task_type: 'search',
                    question: question
                }
            })
        });

        const data = await response.json();

        if (data.status === 'completed' || data.status === 'success') {
            displayAgentResult(resultPanel, data, '⚖️ Legal Research Result');
        } else {
            showError('Legal research failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Legal agent error:', error);
        showError('Failed to execute legal research agent.');
    } finally {
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

// HR Policy Agent
async function handleHRAgent(e) {
    e.preventDefault();

    const btn = document.getElementById('hrAgentBtn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    const resultPanel = document.getElementById('hrAgentResult');

    const question = document.getElementById('hrQuestion').value;
    const context = document.getElementById('hrContext').value;

    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    resultPanel.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/api/agents/hr_policy/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                task: {
                    question: question,
                    task_type: 'policy_search',
                    context: context || undefined
                }
            })
        });

        const data = await response.json();

        if (data.status === 'completed' || data.status === 'success') {
            displayAgentResult(resultPanel, data, '👥 HR Policy Answer');
        } else {
            showError('HR policy query failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('HR agent error:', error);
        showError('Failed to execute HR policy agent.');
    } finally {
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

// Customer Service Agent
async function handleCSAgent(e) {
    e.preventDefault();

    const btn = document.getElementById('csAgentBtn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    const resultPanel = document.getElementById('csAgentResult');

    const question = document.getElementById('csQuestion').value;
    const context = document.getElementById('csContext').value;

    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    resultPanel.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/api/agents/cs_document/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                task: {
                    ticket: question + (context ? '\n\nContext: ' + context : ''),
                    task_type: 'respond',
                    category: 'general'
                }
            })
        });

        const data = await response.json();

        if (data.status === 'completed' || data.status === 'success') {
            displayAgentResult(resultPanel, data, '💬 Support Answer');
        } else {
            showError('Customer service query failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('CS agent error:', error);
        showError('Failed to execute customer service agent.');
    } finally {
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

// Analysis Agent
async function handleAnalysisAgent(e) {
    e.preventDefault();

    const btn = document.getElementById('analysisAgentBtn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    const resultPanel = document.getElementById('analysisAgentResult');

    const text = document.getElementById('analysisText').value;
    const focus = document.getElementById('analysisFocus').value;

    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    resultPanel.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/api/agents/analysis/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                task: {
                    analysis_type: 'summary',
                    data: text,
                    focus: focus || undefined
                }
            })
        });

        const data = await response.json();

        if (data.status === 'completed' || data.status === 'success') {
            displayAgentResult(resultPanel, data, '📊 Analysis Results');
        } else {
            showError('Analysis failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Analysis agent error:', error);
        showError('Failed to execute analysis agent.');
    } finally {
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

// Toggle Synthesis Agent Mode (Manual vs Auto-Retrieve)
function toggleSynthesisMode() {
    const autoRetrieveCheckbox = document.getElementById('synthesisAutoRetrieve');
    const autoRetrieveOptions = document.getElementById('synthesisAutoRetrieveOptions');
    const manualSources = document.getElementById('synthesisManualSources');

    const isAutoRetrieve = autoRetrieveCheckbox.checked;

    if (isAutoRetrieve) {
        // Show auto-retrieve options, hide manual sources
        autoRetrieveOptions.style.display = 'block';
        manualSources.style.display = 'none';

        // Remove required attribute from manual source fields
        const manualInputs = manualSources.querySelectorAll('input[required], textarea[required]');
        manualInputs.forEach(input => {
            input.removeAttribute('required');
            input.dataset.wasRequired = 'true'; // Remember for later
        });
    } else {
        // Show manual sources, hide auto-retrieve options
        autoRetrieveOptions.style.display = 'none';
        manualSources.style.display = 'block';

        // Restore required attribute to manual source fields
        const manualInputs = manualSources.querySelectorAll('input[data-was-required], textarea[data-was-required]');
        manualInputs.forEach(input => {
            if (input.dataset.wasRequired === 'true') {
                input.setAttribute('required', '');
            }
        });
    }
}

// Synthesis Agent
async function handleSynthesisAgent(e) {
    e.preventDefault();

    const btn = document.getElementById('synthesisAgentBtn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    const resultPanel = document.getElementById('synthesisAgentResult');

    const autoRetrieve = document.getElementById('synthesisAutoRetrieve').checked;
    const focus = document.getElementById('synthesisFocus').value;

    // Build task based on mode
    let task = {
        task_type: 'synthesis',
        focus: focus || undefined
    };

    if (autoRetrieve) {
        // Auto-retrieve mode: Build document queries
        const queriesText = document.getElementById('synthesisQueries').value.trim();

        if (!queriesText) {
            showError('Please enter at least one search query for document retrieval.');
            return;
        }

        // Split queries by newline
        const documentQueries = queriesText
            .split('\n')
            .map(q => q.trim())
            .filter(q => q.length > 0);

        if (documentQueries.length === 0) {
            showError('Please enter at least one valid search query.');
            return;
        }

        const topK = parseInt(document.getElementById('synthesisTopK').value) || 5;
        const minScore = parseFloat(document.getElementById('synthesisMinScore').value) || 0.6;

        task.auto_retrieve = true;
        task.document_queries = documentQueries;
        task.top_k_per_query = topK;
        task.min_score = minScore;
        task.question = documentQueries[0]; // Use first query as main question

        console.log('Auto-retrieve mode:', { documentQueries, topK, minScore });
    } else {
        // Manual mode: Collect sources from form
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

        task.sources = sources;
        console.log('Manual mode:', { sources: sources.length });
    }

    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    resultPanel.style.display = 'none';

    // Show extended progress message for auto-retrieve (vector search + synthesis takes longer)
    let timeoutMsg = null;
    if (autoRetrieve) {
        timeoutMsg = setTimeout(() => {
            btnLoading.innerHTML = '<span class="spinner"></span> Searching legal database and synthesizing... (may take 1-2 minutes)';
        }, 5000);
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/agents/synthesis/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ task })
        });

        const data = await response.json();

        if (data.status === 'completed' || data.status === 'success') {
            displayAgentResult(resultPanel, data, '🔗 Synthesis Results');
        } else {
            showError('Synthesis failed: ' + (data.error || data.result?.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Synthesis agent error:', error);
        showError('Failed to execute synthesis agent. Check console for details.');
    } finally {
        if (timeoutMsg) clearTimeout(timeoutMsg);
        btnLoading.innerHTML = '<span class="spinner"></span> Synthesizing...';
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

// Validation Agent
async function handleValidationAgent(e) {
    e.preventDefault();

    const btn = document.getElementById('validationAgentBtn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    const resultPanel = document.getElementById('validationAgentResult');

    // Collect documents
    const docElements = document.querySelectorAll('.validation-doc');
    const documents = [];

    docElements.forEach(docEl => {
        const title = docEl.querySelector('.doc-title').value;
        const content = docEl.querySelector('.doc-content').value;

        if (title && content) {
            documents.push({ title, content });
        }
    });

    if (documents.length < 2) {
        showError('Please provide at least 2 documents for validation.');
        return;
    }

    const focus = document.getElementById('validationFocus').value;

    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    resultPanel.style.display = 'none';

    try {
        // Prepare content - concatenate all documents
        const content = documents.map((doc, idx) =>
            `Document ${idx + 1}: ${doc.title}\n${doc.content}`
        ).join('\n\n---\n\n');

        const response = await fetch(`${API_BASE_URL}/api/agents/validation/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                task: {
                    validation_type: focus || 'comprehensive',
                    content: content,
                    question: 'Validate the following documents'
                }
            })
        });

        const data = await response.json();

        if (data.status === 'completed' || data.status === 'success') {
            displayAgentResult(resultPanel, data, '✅ Validation Results');
        } else {
            showError('Validation failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Validation agent error:', error);
        showError('Failed to execute validation agent.');
    } finally {
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

// Generic Agent Result Display
function displayAgentResult(resultPanel, data, title) {
    const result = data.result || {};

    // Extract content based on agent type
    let content = '';

    if (result.answer) {
        // Legal Research, HR Policy agents
        content = result.answer;
    } else if (result.response) {
        // Customer Service agent
        content = result.response;
    } else if (result.analysis && result.analysis.summary) {
        // Analysis agent
        content = result.analysis.summary;
    } else if (result.synthesized_output) {
        // Synthesis agent
        content = result.synthesized_output;
    } else if (result.validation_result) {
        // Validation agent - format validation results nicely
        content = formatValidationResult(result);
    } else {
        // Fallback to JSON
        content = JSON.stringify(result, null, 2);
    }

    resultPanel.innerHTML = `
        <div class="result-header">
            <h3>${title}</h3>
            <div class="result-meta">Agent: ${data.agent} | Time: ${data.execution_time?.toFixed(2)}s</div>
        </div>
        <div class="result-content">
            <p style="white-space: pre-wrap; line-height: 1.6;">${content}</p>
        </div>
        ${result.sources && result.sources.length > 0 ? `
            <div class="result-sources">
                <h4 style="margin-top: 24px; margin-bottom: 12px;">📚 Sources</h4>
                <div class="sources-list">
                    ${result.sources.map((source, index) => `
                        <div class="source-card">
                            <div class="source-header">
                                <span class="source-number">${index + 1}</span>
                                <div class="source-title">
                                    <strong>${source.title || source.doc_name || `Source ${index + 1}`}</strong>
                                </div>
                                ${source.score ? `<span class="source-score">${(source.score * 100).toFixed(1)}% match</span>` : ''}
                            </div>
                            <div class="source-preview">${source.content || source.preview || ''}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        ` : ''}
    `;

    resultPanel.style.display = 'block';
    resultPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Format validation results for display
function formatValidationResult(result) {
    const resultEmoji = result.validation_result === 'passed' ? '✅' :
                       result.validation_result === 'partial' ? '⚠️' : '❌';

    let formatted = `${resultEmoji} Validation Result: ${result.validation_result.toUpperCase()}\n`;
    formatted += `Quality Score: ${result.quality_score}/100\n\n`;

    if (result.issues && result.issues.length > 0) {
        formatted += `Issues Found (${result.issues.length}):\n`;
        result.issues.forEach((issue, idx) => {
            const issueText = typeof issue === 'string' ? issue : issue.description || JSON.stringify(issue);
            formatted += `${idx + 1}. ${issueText}\n`;
        });
        formatted += '\n';
    }

    if (result.recommendations && result.recommendations.length > 0) {
        formatted += `Recommendations:\n`;
        result.recommendations.forEach((rec, idx) => {
            const recText = typeof rec === 'string' ? rec : rec.description || JSON.stringify(rec);
            formatted += `${idx + 1}. ${recText}\n`;
        });
    }

    return formatted;
}

// Dynamic Source/Document Addition
function addSynthesisSource() {
    const container = document.getElementById('synthesisSourcesContainer');
    const sourceCount = container.querySelectorAll('.synthesis-source').length + 1;

    const newSource = document.createElement('div');
    newSource.className = 'synthesis-source';
    newSource.innerHTML = `
        <input type="text" class="input-field source-title" placeholder="Source ${sourceCount} Title">
        <textarea class="textarea-field source-content" rows="4" placeholder="Source ${sourceCount} Content"></textarea>
    `;

    container.appendChild(newSource);
}

function addValidationDoc() {
    const container = document.getElementById('validationDocsContainer');
    const docCount = container.querySelectorAll('.validation-doc').length + 1;

    const newDoc = document.createElement('div');
    newDoc.className = 'validation-doc';
    newDoc.innerHTML = `
        <input type="text" class="input-field doc-title" placeholder="Document ${docCount} Title">
        <textarea class="textarea-field doc-content" rows="4" placeholder="Document ${docCount} Content"></textarea>
    `;

    container.appendChild(newDoc);
}

// Load Models
async function loadModels() {
    const modelsGrid = document.getElementById('modelsResult');
    modelsGrid.innerHTML = '<p class="text-muted">Loading models...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/models`);
        const data = await response.json();

        if (data.success && data.models.length > 0) {
            displayModels(data);
        } else {
            modelsGrid.innerHTML = '<p class="text-muted">No models found</p>';
        }
    } catch (error) {
        console.error('Failed to load models:', error);
        modelsGrid.innerHTML = '<p class="text-muted">Failed to load models. Check if the API is running.</p>';
    }
}

function displayModels(data) {
    const modelsGrid = document.getElementById('modelsResult');
    const activeLLM = data.active_llm;
    const activeEmbedding = data.active_embedding;

    modelsGrid.innerHTML = data.models.map(model => {
        const isActiveLLM = model.name === activeLLM;
        const isActiveEmbedding = model.name === activeEmbedding;
        const isActive = isActiveLLM || isActiveEmbedding;

        const sizeGB = (model.size / (1024 * 1024 * 1024)).toFixed(2);
        const modifiedDate = new Date(model.modified_at).toLocaleDateString();

        const isEmbeddingModel = model.name.includes('embed') || sizeGB < 1;

        return `
            <div class="model-card ${isActive ? 'active' : ''}" data-model-name="${model.name}">
                <div class="model-name">
                    ${model.name}
                    ${isActiveLLM ? '<span class="model-badge">ACTIVE LLM</span>' : ''}
                    ${isActiveEmbedding ? '<span class="model-badge" style="background: var(--success-color);">ACTIVE EMBEDDING</span>' : ''}
                </div>
                <div class="model-info">
                    <div class="model-detail">
                        <span class="model-detail-label">Size</span>
                        <span class="model-detail-value">${sizeGB} GB</span>
                    </div>
                    <div class="model-detail">
                        <span class="model-detail-label">Parameters</span>
                        <span class="model-detail-value">${model.details?.parameter_size || 'N/A'}</span>
                    </div>
                    <div class="model-detail">
                        <span class="model-detail-label">Quantization</span>
                        <span class="model-detail-value">${model.details?.quantization_level || 'N/A'}</span>
                    </div>
                    <div class="model-detail">
                        <span class="model-detail-label">Modified</span>
                        <span class="model-detail-value">${modifiedDate}</span>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Error Handling
function showError(message) {
    alert(message);
}

// Utility Functions
function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function formatDuration(ms) {
    if (ms < 1000) return `${ms}ms`;
    return `${(ms / 1000).toFixed(2)}s`;
}

// ==========================================
// WORKFLOW TAB SWITCHING
// ==========================================

// Initialize workflow tab switching (called on DOM ready)
function initializeWorkflowTabs() {
    // Handle workflow tab switching
    document.querySelectorAll('[data-workflow]').forEach(btn => {
        btn.addEventListener('click', function() {
            const workflowId = this.getAttribute('data-workflow');

            // Update button states within the same tab group
            const tabGroup = this.closest('.agent-tabs');
            if (tabGroup) {
                tabGroup.querySelectorAll('[data-workflow]').forEach(b => b.classList.remove('active'));
            }
            this.classList.add('active');

            // Update workflow content visibility
            const parentPanel = this.closest('.panel');
            if (parentPanel) {
                parentPanel.querySelectorAll('[id^="workflow-"]').forEach(content => {
                    content.classList.remove('active');
                });
                const targetContent = document.getElementById(`workflow-${workflowId}`);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
            }
        });
    });
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', initializeWorkflowTabs);

// ==========================================
// WORKFLOW EXECUTION FUNCTIONS
// ==========================================

// Show loading state on button
function showLoading(buttonElement) {
    if (!buttonElement) return;

    buttonElement.disabled = true;
    buttonElement.dataset.originalText = buttonElement.innerHTML;
    buttonElement.innerHTML = '<span class="spinner"></span> Processing Workflow...';

    // Show extended timeout message after 15 seconds
    buttonElement.dataset.timeoutId = setTimeout(() => {
        buttonElement.innerHTML = '<span class="spinner"></span> Still processing... (Workflows may take 2-4 minutes)';
    }, 15000);
}

// Hide loading state on button
function hideLoading(buttonElement) {
    if (!buttonElement) return;

    buttonElement.disabled = false;
    buttonElement.innerHTML = buttonElement.dataset.originalText || 'Run Workflow';

    // Clear timeout
    if (buttonElement.dataset.timeoutId) {
        clearTimeout(parseInt(buttonElement.dataset.timeoutId));
        delete buttonElement.dataset.timeoutId;
    }
}

// Display error in result panel
function displayError(resultElementId, errorMessage) {
    const resultDiv = document.getElementById(resultElementId);
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `
        <div class="result-header">
            <h3>❌ Workflow Error</h3>
        </div>
        <div class="result-content" style="background: #dc354520; border-left: 4px solid #dc3545; padding: 15px; border-radius: 4px;">
            <strong style="color: #dc3545;">Error:</strong>
            <p style="margin: 10px 0 0 0;">${escapeHtml(errorMessage)}</p>
        </div>
    `;
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Escape HTML for safe display
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Format markdown-like text for better display
function formatMarkdown(text) {
    if (!text) return '';

    // Convert markdown-style formatting to HTML
    let formatted = String(text)
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold
        .replace(/\*(.*?)\*/g, '<em>$1</em>')              // Italic
        .replace(/^### (.*$)/gim, '<h4>$1</h4>')          // Headers
        .replace(/^## (.*$)/gim, '<h3>$1</h3>')
        .replace(/^# (.*$)/gim, '<h2>$1</h2>')
        .replace(/\n/g, '<br>');                           // Line breaks

    return `<div style="white-space: normal; line-height: 1.6;">${formatted}</div>`;
}

// Format validation results from workflow execution
function formatValidationWorkflowResult(result) {
    const resultEmoji = result.validation_result === 'passed' ? '✅' :
                       result.validation_result === 'partial' ? '⚠️' : '❌';
    const resultColor = result.validation_result === 'passed' ? '#28a745' :
                       result.validation_result === 'partial' ? '#ffc107' : '#dc3545';

    let html = `
        <div style="background: ${resultColor}20; border-left: 4px solid ${resultColor}; padding: 20px; border-radius: 4px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="margin: 0; color: ${resultColor};">${resultEmoji} ${result.validation_result.toUpperCase()}</h3>
                <div style="font-size: 2em; font-weight: bold; color: ${resultColor};">${result.quality_score}/100</div>
            </div>
            <div style="color: #666; font-size: 0.9em;">
                <strong>Validation Type:</strong> ${result.validation_type}
            </div>
        </div>
    `;

    // Show validation breakdown if details exist
    if (result.details) {
        html += `<h4 style="margin-top: 20px;">📊 Validation Breakdown:</h4>`;
        html += `<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 20px;">`;

        const categories = ['accuracy', 'completeness', 'consistency'];
        categories.forEach(category => {
            if (result.details[category]) {
                const detail = result.details[category];
                const score = detail.quality_score || 0;
                const resultText = detail.validation_result || 'unknown';
                const categoryEmoji = category === 'accuracy' ? '🎯' :
                                    category === 'completeness' ? '📋' : '🔄';
                const scoreColor = score >= 80 ? '#28a745' : score >= 60 ? '#ffc107' : '#dc3545';

                html += `
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 4px; border-left: 4px solid ${scoreColor};">
                        <div style="font-weight: bold; margin-bottom: 5px;">${categoryEmoji} ${category.charAt(0).toUpperCase() + category.slice(1)}</div>
                        <div style="font-size: 1.5em; color: ${scoreColor}; margin: 5px 0;">${score}/100</div>
                        <div style="color: #666; font-size: 0.85em; text-transform: capitalize;">${resultText}</div>
                    </div>
                `;
            }
        });

        html += `</div>`;
    }

    // Issues section
    if (result.issues && result.issues.length > 0) {
        html += `<h4 style="margin-top: 20px;">⚠️ Issues Found (${result.issues.length}):</h4>`;
        html += `<div style="background: #fff3cd; padding: 15px; border-radius: 4px; border-left: 4px solid #ffc107; margin-bottom: 20px;">`;
        html += `<ol style="margin: 0; padding-left: 20px;">`;

        // Group issues by category if possible
        const maxDisplay = 10; // Show max 10 issues initially
        result.issues.slice(0, maxDisplay).forEach(issue => {
            const issueText = typeof issue === 'string' ? escapeHtml(issue) : escapeHtml(issue.description || JSON.stringify(issue));
            html += `<li style="margin-bottom: 8px; line-height: 1.5;">${issueText}</li>`;
        });

        if (result.issues.length > maxDisplay) {
            html += `<li style="color: #666; font-style: italic;">... and ${result.issues.length - maxDisplay} more issues</li>`;
        }

        html += `</ol></div>`;
    }

    // Recommendations section
    if (result.recommendations && result.recommendations.length > 0) {
        html += `<h4 style="margin-top: 20px;">💡 Recommendations:</h4>`;
        html += `<div style="background: #d1ecf1; padding: 15px; border-radius: 4px; border-left: 4px solid #17a2b8;">`;
        html += `<ul style="margin: 0; padding-left: 20px;">`;

        result.recommendations.forEach(rec => {
            const recText = typeof rec === 'string' ? escapeHtml(rec) : escapeHtml(rec.description || JSON.stringify(rec));
            html += `<li style="margin-bottom: 8px; line-height: 1.5;">${recText}</li>`;
        });

        html += `</ul></div>`;
    }

    // Collapsible detailed results
    if (result.details) {
        html += `
            <details style="margin-top: 20px; background: #f8f9fa; padding: 15px; border-radius: 4px;">
                <summary style="cursor: pointer; font-weight: bold; margin-bottom: 10px;">🔍 View Detailed Validation Results</summary>
                <pre style="background: white; padding: 15px; border-radius: 4px; overflow-x: auto; margin-top: 10px;">${JSON.stringify(result.details, null, 2)}</pre>
            </details>
        `;
    }

    return html;
}

// Generic workflow execution function
async function executeWorkflow(workflowId, inputData, resultElementId, buttonElement) {
    try {
        showLoading(buttonElement);

        // Show result panel with "Processing..." message
        const resultDiv = document.getElementById(resultElementId);
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div class="result-header">
                <h3>🔄 Processing Workflow...</h3>
            </div>
            <div class="result-content" style="text-align: center; padding: 40px;">
                <div class="spinner" style="width: 40px; height: 40px; margin: 0 auto 20px;"></div>
                <p style="color: #666;">Executing multi-agent workflow...</p>
                <p style="color: #999; font-size: 0.9em; margin-top: 10px;">This may take 2-4 minutes</p>
            </div>
        `;

        const response = await fetch(`/api/workflows/${workflowId}/execute`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: inputData })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayWorkflowResult(data, resultElementId);

    } catch (error) {
        displayError(resultElementId, error.message);
    } finally {
        hideLoading(buttonElement);
    }
}

// Display workflow results with progress tracking
function displayWorkflowResult(data, resultElementId) {
    const resultDiv = document.getElementById(resultElementId);
    resultDiv.style.display = 'block';

    let html = '<div class="result-header"><h3>🔄 Workflow Results</h3></div>';

    // Workflow status
    const statusIcon = data.status === 'completed' ? '✅' : '❌';
    const statusColor = data.status === 'completed' ? '#28a745' : '#dc3545';

    html += `<div style="background: ${statusColor}20; border-left: 4px solid ${statusColor}; padding: 15px; margin-bottom: 20px; border-radius: 4px;">`;
    html += `<strong style="color: ${statusColor};">${statusIcon} Workflow Status: ${data.status.toUpperCase()}</strong>`;
    if (data.execution_time) {
        html += `<p style="margin: 5px 0 0 0; color: #666;">Total execution time: ${data.execution_time}s</p>`;
    }
    html += `</div>`;

    // Step-by-step results
    if (data.steps && data.steps.length > 0) {
        html += `<h4>📋 Execution Steps:</h4>`;

        data.steps.forEach((step, index) => {
            const stepNumber = index + 1;
            const stepIcon = step.status === 'completed' ? '✅' : step.status === 'failed' ? '❌' : '⏳';
            const stepColor = step.status === 'completed' ? '#28a745' : step.status === 'failed' ? '#dc3545' : '#ffc107';

            html += `<div style="background: #f8f9fa; border-left: 4px solid ${stepColor}; padding: 15px; margin-bottom: 15px; border-radius: 4px;">`;
            html += `<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">`;
            html += `<strong>${stepIcon} Step ${stepNumber}: ${step.name}</strong>`;
            if (step.execution_time) {
                html += `<span style="color: #666; font-size: 0.9em;">${step.execution_time}s</span>`;
            }
            html += `</div>`;

            html += `<p style="color: #666; margin: 5px 0;"><em>${step.description}</em></p>`;
            html += `<p style="margin: 5px 0; color: #666;"><strong>Agent:</strong> ${step.agent}</p>`;

            if (step.error) {
                html += `<div style="background: #fff; padding: 10px; border-radius: 4px; margin-top: 10px;">`;
                html += `<strong style="color: #dc3545;">Error:</strong> ${escapeHtml(step.error)}`;
                html += `</div>`;
            }

            html += `</div>`;
        });
    }

    // Final result
    if (data.final_result) {
        html += `<h4>🎯 Final Result:</h4>`;
        html += `<div class="result-content">`;

        if (typeof data.final_result === 'object') {
            // Check if this is a validation result
            if (data.final_result.agent === 'validation' && data.final_result.validation_result) {
                html += formatValidationWorkflowResult(data.final_result);
            }
            // Handle structured results
            else if (data.final_result.synthesized_output) {
                html += formatMarkdown(data.final_result.synthesized_output);
            } else if (data.final_result.answer) {
                html += formatMarkdown(data.final_result.answer);
            } else {
                html += `<pre>${JSON.stringify(data.final_result, null, 2)}</pre>`;
            }
        } else {
            html += formatMarkdown(String(data.final_result));
        }

        html += `</div>`;
    }

    resultDiv.innerHTML = html;
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ==========================================
// WORKFLOW FORM HANDLERS
// ==========================================

// 1. HR Onboarding Workflow
document.getElementById('hrOnboardingForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const inputData = {
        employee_name: document.getElementById('onboardingEmployeeName').value || undefined,
        role: document.getElementById('onboardingRole').value || undefined,
        employee_question: document.getElementById('onboardingQuestion').value || undefined,
        hr_policies: document.getElementById('onboardingPolicies').value || undefined
    };

    await executeWorkflow('hr_onboarding', inputData, 'hrOnboardingResult', e.target.querySelector('.btn-primary'));
});

// 2. CS Ticket Workflow
document.getElementById('csTicketForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const inputData = {
        customer_name: document.getElementById('ticketCustomerName').value || undefined,
        customer_query: document.getElementById('ticketQuery').value,
        support_docs: document.getElementById('ticketDocs').value || undefined
    };

    await executeWorkflow('cs_ticket', inputData, 'csTicketResult', e.target.querySelector('.btn-primary'));
});

// 3. Legal-HR Compliance Workflow
document.getElementById('legalComplianceForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const inputData = {
        compliance_area: document.getElementById('complianceArea').value,
        policy_name: document.getElementById('compliancePolicyName').value,
        policy_content: document.getElementById('compliancePolicyContent').value
    };

    await executeWorkflow('legal_hr_compliance', inputData, 'legalComplianceResult', e.target.querySelector('.btn-primary'));
});

// 4. Simple Q&A Workflow
document.getElementById('simpleQAForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const inputData = {
        question: document.getElementById('qaQuestion').value
    };

    await executeWorkflow('simple_qa', inputData, 'simpleQAResult', e.target.querySelector('.btn-primary'));
});

// 5. Multi-Agent Research Workflow
document.getElementById('multiResearchForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const inputData = {
        research_topic: document.getElementById('researchTopic').value,
        hr_context: document.getElementById('researchHRContext').value || undefined,
        cs_context: document.getElementById('researchCSContext').value || undefined
    };

    await executeWorkflow('multi_agent_research', inputData, 'multiResearchResult', e.target.querySelector('.btn-primary'));
});

// ==========================================
// WORKFLOW CLEAR BUTTONS
// ==========================================

document.querySelectorAll('.clear-workflow').forEach(btn => {
    btn.addEventListener('click', function() {
        const form = this.closest('form');
        form.reset();

        // Hide result panel
        const resultDiv = form.nextElementSibling;
        if (resultDiv && resultDiv.classList.contains('result-panel')) {
            resultDiv.style.display = 'none';
        }
    });
});

console.log('✅ Workflow handlers initialized');
