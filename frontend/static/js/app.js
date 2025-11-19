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
    synthesisAgentForm.addEventListener('submit', handleSynthesisAgent);
    clearSynthesisBtn.addEventListener('click', () => {
        synthesisAgentForm.reset();
        document.getElementById('synthesisAgentResult').style.display = 'none';
    });
    addSourceBtn.addEventListener('click', addSynthesisSource);

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

        if (data.status === 'success') {
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

        if (data.status === 'success') {
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
                    question: question,
                    task_type: 'support',
                    context: context || undefined
                }
            })
        });

        const data = await response.json();

        if (data.status === 'success') {
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
                    task_type: 'analysis',
                    text: text,
                    focus: focus || undefined
                }
            })
        });

        const data = await response.json();

        if (data.status === 'success') {
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

// Synthesis Agent
async function handleSynthesisAgent(e) {
    e.preventDefault();

    const btn = document.getElementById('synthesisAgentBtn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    const resultPanel = document.getElementById('synthesisAgentResult');

    // Collect sources
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

    const focus = document.getElementById('synthesisFocus').value;

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
            body: JSON.stringify({
                task: {
                    task_type: 'synthesis',
                    sources: sources,
                    focus: focus || undefined
                }
            })
        });

        const data = await response.json();

        if (data.status === 'success') {
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
        const response = await fetch(`${API_BASE_URL}/api/agents/validation/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                task: {
                    task_type: 'validation',
                    documents: documents,
                    focus: focus || undefined
                }
            })
        });

        const data = await response.json();

        if (data.status === 'success') {
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

    resultPanel.innerHTML = `
        <div class="result-header">
            <h3>${title}</h3>
            <div class="result-meta">Agent: ${data.agent} | Time: ${data.execution_time?.toFixed(2)}s</div>
        </div>
        <div class="result-content">
            <p style="white-space: pre-wrap; line-height: 1.6;">${result.answer || result.response || JSON.stringify(result, null, 2)}</p>
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
