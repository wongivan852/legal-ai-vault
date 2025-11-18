// Legal AI Vault - Frontend JavaScript

const API_BASE_URL = 'http://localhost:8000';

// State
let currentHealth = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
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

    // Embeddings Form
    const embedForm = document.getElementById('embedForm');
    const clearEmbedBtn = document.getElementById('clearEmbed');

    embedForm.addEventListener('submit', handleEmbed);
    clearEmbedBtn.addEventListener('click', () => {
        embedForm.reset();
        document.getElementById('embedResult').style.display = 'none';
    });

    // RAG Form
    const ragForm = document.getElementById('ragForm');
    const clearRagBtn = document.getElementById('clearRag');

    ragForm.addEventListener('submit', handleRAG);
    clearRagBtn.addEventListener('click', () => {
        ragForm.reset();
        document.getElementById('ragResult').style.display = 'none';
    });

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
        apiVersion.textContent = health.api_version || 'v1.0.0';
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
        clearTimeout(timeoutMsg);  // Clear the timeout message
        btnLoading.innerHTML = '<span class="spinner"></span> Generating...';  // Reset message
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

// Embeddings
async function handleEmbed(e) {
    e.preventDefault();

    const btn = document.getElementById('embedBtn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    const resultPanel = document.getElementById('embedResult');

    const text = document.getElementById('embedText').value;

    // Show loading state
    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    resultPanel.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/api/embed`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (data.success) {
            displayEmbedResult(data);
        } else {
            showError('Embedding failed: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Embedding error:', error);
        showError('Failed to connect to API. Make sure the backend is running.');
    } finally {
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

function displayEmbedResult(data) {
    const resultPanel = document.getElementById('embedResult');
    const embedMeta = document.getElementById('embedMeta');
    const embedInfo = document.getElementById('embedInfo');
    const embedPreview = document.getElementById('embedPreview');

    // Meta
    embedMeta.textContent = `Model: ${data.model}`;

    // Info cards
    embedInfo.innerHTML = `
        <div class="info-card">
            <div class="info-label">Dimensions</div>
            <div class="info-value">${data.dimension}</div>
        </div>
        <div class="info-card">
            <div class="info-label">Vector Length</div>
            <div class="info-value">${data.embedding.length}</div>
        </div>
        <div class="info-card">
            <div class="info-label">Model</div>
            <div class="info-value" style="font-size: 0.9rem;">${data.model.split(':')[0]}</div>
        </div>
    `;

    // Preview (first 50 values)
    const preview = data.embedding.slice(0, 50);
    const previewText = `[\n  ${preview.map(v => v.toFixed(6)).join(',\n  ')}\n  ... (${data.embedding.length - 50} more values)\n]`;
    embedPreview.textContent = previewText;

    resultPanel.style.display = 'block';
    resultPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// RAG - Retrieval Augmented Generation
async function handleRAG(e) {
    e.preventDefault();

    const btn = document.getElementById('ragBtn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    const resultPanel = document.getElementById('ragResult');

    // Get form values
    const question = document.getElementById('ragQuestion').value;
    const topK = parseInt(document.getElementById('ragTopK').value);
    const searchType = document.getElementById('ragSearchType').value;

    // Show loading state
    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    resultPanel.style.display = 'none';

    // Show progress message after 10 seconds
    let timeoutMsg = setTimeout(() => {
        btnLoading.innerHTML = '<span class="spinner"></span> Still searching and generating answer... (This may take 30-60 seconds)';
    }, 10000);

    try {
        const response = await fetch(`${API_BASE_URL}/api/rag`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question,
                top_k: topK,
                search_type: searchType,
                min_score: 0.5
            })
        });

        const data = await response.json();

        if (data.success) {
            displayRAGResult(data);
        } else {
            showError('RAG query failed: ' + (data.error || data.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('RAG error:', error);
        showError('Failed to connect to API. Make sure the backend is running and legal documents are imported.');
    } finally {
        clearTimeout(timeoutMsg);
        btnLoading.innerHTML = '<span class="spinner"></span> Searching legal database...';
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

function displayRAGResult(data) {
    const resultPanel = document.getElementById('ragResult');
    const ragMeta = document.getElementById('ragMeta');
    const ragAnswer = document.getElementById('ragAnswer');
    const ragSources = document.getElementById('ragSources');

    // Meta
    ragMeta.textContent = `Retrieved ${data.retrieved_count} ${data.search_type}`;

    // Answer
    ragAnswer.innerHTML = `<p style="white-space: pre-wrap; line-height: 1.6;">${data.answer}</p>`;

    // Sources
    if (data.sources && data.sources.length > 0) {
        ragSources.innerHTML = `
            <h4 style="margin-top: 24px; margin-bottom: 12px; color: var(--text-secondary);">📚 Legal Sources</h4>
            <div class="sources-list">
                ${data.sources.map((source, index) => `
                    <div class="source-card">
                        <div class="source-header">
                            <span class="source-number">${index + 1}</span>
                            <div class="source-title">
                                <strong>${source.doc_name}</strong>: ${source.doc_title || 'Untitled'}
                            </div>
                            <span class="source-score">${(source.score * 100).toFixed(1)}% match</span>
                        </div>
                        ${source.section_number ? `
                            <div class="source-section">
                                <strong>Section ${source.section_number}</strong>: ${source.section_heading || ''}
                            </div>
                        ` : ''}
                        <div class="source-preview">${source.preview}</div>
                    </div>
                `).join('')}
            </div>
        `;
    } else {
        ragSources.innerHTML = `<p class="text-muted" style="margin-top: 20px;">No sources found</p>`;
    }

    resultPanel.style.display = 'block';
    resultPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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

        // Determine if this is an embedding model (typically smaller or has "embed" in name)
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
                        <span class="model-detail-label">Format</span>
                        <span class="model-detail-value">${model.details?.format?.toUpperCase() || 'N/A'}</span>
                    </div>
                    <div class="model-detail">
                        <span class="model-detail-label">Modified</span>
                        <span class="model-detail-value">${modifiedDate}</span>
                    </div>
                </div>
                <div class="model-actions" style="margin-top: 16px; display: flex; gap: 8px;">
                    ${!isActiveLLM ? `<button class="btn-model-select" data-model="${model.name}" data-type="llm" style="flex: 1;">
                        Use as LLM
                    </button>` : ''}
                    ${!isActiveEmbedding && isEmbeddingModel ? `<button class="btn-model-select" data-model="${model.name}" data-type="embedding" style="flex: 1;">
                        Use for Embeddings
                    </button>` : ''}
                </div>
            </div>
        `;
    }).join('');

    // Add event listeners to all model select buttons
    document.querySelectorAll('.btn-model-select').forEach(button => {
        button.addEventListener('click', (e) => {
            const modelName = e.target.dataset.model;
            const modelType = e.target.dataset.type;
            switchModel(modelName, modelType);
        });
    });
}

// Switch Model
async function switchModel(modelName, modelType) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/models/set`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model_name: modelName,
                model_type: modelType
            })
        });

        const data = await response.json();

        if (data.success) {
            // Show success message
            alert(`✓ ${data.message}\n\nActive models:\n• LLM: ${data.active_llm}\n• Embedding: ${data.active_embedding}`);

            // Reload models to update UI
            await loadModels();

            // Update health check
            await checkHealth();
        } else {
            showError('Failed to switch model: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Model switch error:', error);
        showError('Failed to switch model. Check if the API is running.');
    }
}

// Error Handling
function showError(message) {
    alert(message); // Simple error handling - can be enhanced with toast notifications
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
