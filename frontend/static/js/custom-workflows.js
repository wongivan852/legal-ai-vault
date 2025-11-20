/**
 * Custom Workflow Dynamic Loader
 *
 * Automatically loads custom workflows from the database and:
 * - Creates execution tabs dynamically
 * - Generates forms based on input schemas
 * - Handles workflow execution
 */

const API_BASE = window.API_BASE_URL || 'http://localhost:8000';

// Store loaded custom workflows
let customWorkflows = [];

/**
 * Initialize custom workflows on page load
 */
async function initializeCustomWorkflows() {
    try {
        console.log('🔄 Loading custom workflows...');

        // Fetch custom workflows from API
        const response = await fetch(`${API_BASE}/api/workflows/builder/list?include_system=false`);
        const data = await response.json();

        if (data.workflows && data.workflows.length > 0) {
            customWorkflows = data.workflows;
            console.log(`✅ Loaded ${customWorkflows.length} custom workflow(s)`);

            // Generate tabs and forms for each custom workflow
            for (const workflow of customWorkflows) {
                await loadWorkflowDetails(workflow.id);
            }

            // Re-initialize tab switching after adding new tabs
            if (typeof initializeWorkflowTabs === 'function') {
                initializeWorkflowTabs();
            }
        } else {
            console.log('ℹ️ No custom workflows found');
        }
    } catch (error) {
        console.error('❌ Failed to load custom workflows:', error);
    }
}

/**
 * Load full workflow details and create UI
 */
async function loadWorkflowDetails(workflowId) {
    try {
        const response = await fetch(`${API_BASE}/api/workflows/builder/${workflowId}`);
        const data = await response.json();

        if (data.success && data.workflow) {
            const workflow = data.workflow;
            createWorkflowTab(workflow);
            createWorkflowPanel(workflow);
        }
    } catch (error) {
        console.error(`Failed to load workflow ${workflowId}:`, error);
    }
}

/**
 * Create a tab button for the workflow
 */
function createWorkflowTab(workflow) {
    const tabsContainer = document.querySelector('#workflows-tab .agent-tabs');
    if (!tabsContainer) {
        console.error('Workflow tabs container not found');
        return;
    }

    // Find the Workflow Builder tab (should be last)
    const builderTab = tabsContainer.querySelector('[data-workflow="builder"]');

    // Create new tab button
    const tabButton = document.createElement('button');
    tabButton.className = 'agent-tab-btn';
    tabButton.setAttribute('data-workflow', workflow.workflow_id);

    // Get category emoji
    const categoryEmoji = getCategoryEmoji(workflow.category);
    tabButton.textContent = `${categoryEmoji} ${workflow.name}`;

    // Insert before the builder tab
    if (builderTab) {
        tabsContainer.insertBefore(tabButton, builderTab);
    } else {
        tabsContainer.appendChild(tabButton);
    }
}

/**
 * Create the workflow execution panel
 */
function createWorkflowPanel(workflow) {
    const panelsContainer = document.querySelector('#workflows-tab .panel');
    if (!panelsContainer) {
        console.error('Workflows panel container not found');
        return;
    }

    // Find the builder panel to insert before it
    const builderPanel = document.getElementById('workflow-builder');

    // Create panel
    const panel = document.createElement('div');
    panel.className = 'agent-content';
    panel.id = `workflow-${workflow.workflow_id}`;

    // Build panel HTML
    panel.innerHTML = `
        <div class="agent-header">
            <h3>${getCategoryEmoji(workflow.category)} ${workflow.name}</h3>
            <p>${workflow.description || 'Custom workflow'}</p>
            ${workflow.tags && workflow.tags.length > 0 ? `
                <div style="margin-top: 10px;">
                    ${workflow.tags.map(tag => `<span class="tag">${tag}</span>`).join(' ')}
                </div>
            ` : ''}
        </div>

        <div class="form-section">
            <form id="${workflow.workflow_id}Form" class="custom-workflow-form">
                ${generateFormFields(workflow)}

                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">
                        <span class="btn-text">▶️ Run Workflow</span>
                        <span class="btn-loading" style="display: none;">
                            <span class="spinner"></span> Processing...
                        </span>
                    </button>
                    <button type="button" class="btn btn-secondary clear-workflow">🔄 Clear</button>
                </div>
            </form>

            <!-- Result Panel -->
            <div id="${workflow.workflow_id}Result" class="result-panel" style="display: none;"></div>
        </div>
    `;

    // Insert panel
    if (builderPanel) {
        panelsContainer.insertBefore(panel, builderPanel);
    } else {
        panelsContainer.appendChild(panel);
    }

    // Attach event handlers
    attachWorkflowHandlers(workflow);
}

/**
 * Generate form fields based on input schema
 */
function generateFormFields(workflow) {
    if (!workflow.input_schema || !workflow.input_schema.fields) {
        return '<p class="text-muted">No input fields defined for this workflow.</p>';
    }

    const fields = workflow.input_schema.fields;
    let html = '';

    fields.forEach(field => {
        const fieldId = `${workflow.workflow_id}_${field.name}`;
        const required = field.required ? 'required' : '';
        const requiredLabel = field.required ? '<span class="required">*</span>' : '';

        html += `<div class="form-group">`;
        html += `<label for="${fieldId}">${field.label || field.name}${requiredLabel}</label>`;

        switch (field.type) {
            case 'textarea':
                html += `<textarea
                    id="${fieldId}"
                    name="${field.name}"
                    class="textarea-field"
                    rows="${field.rows || 4}"
                    placeholder="${field.placeholder || ''}"
                    ${required}
                ></textarea>`;
                break;

            case 'select':
                html += `<select
                    id="${fieldId}"
                    name="${field.name}"
                    class="select-field"
                    ${required}
                >`;
                if (field.options) {
                    field.options.forEach(option => {
                        const value = typeof option === 'string' ? option : option.value;
                        const label = typeof option === 'string' ? option : option.label;
                        html += `<option value="${value}">${label}</option>`;
                    });
                }
                html += `</select>`;
                break;

            case 'number':
                html += `<input
                    type="number"
                    id="${fieldId}"
                    name="${field.name}"
                    class="input-field"
                    placeholder="${field.placeholder || ''}"
                    min="${field.min || ''}"
                    max="${field.max || ''}"
                    step="${field.step || ''}"
                    ${required}
                />`;
                break;

            case 'text':
            default:
                html += `<input
                    type="text"
                    id="${fieldId}"
                    name="${field.name}"
                    class="input-field"
                    placeholder="${field.placeholder || ''}"
                    ${required}
                />`;
                break;
        }

        if (field.help) {
            html += `<small class="form-help">${field.help}</small>`;
        }

        html += `</div>`;
    });

    return html;
}

/**
 * Attach event handlers to the workflow form
 */
function attachWorkflowHandlers(workflow) {
    const form = document.getElementById(`${workflow.workflow_id}Form`);
    const clearBtn = form.querySelector('.clear-workflow');

    if (!form) {
        console.error(`Form not found for workflow ${workflow.workflow_id}`);
        return;
    }

    // Submit handler
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Collect form data
        const formData = new FormData(form);
        const inputData = {};

        for (const [key, value] of formData.entries()) {
            if (value) {
                inputData[key] = value;
            }
        }

        // Execute workflow using the global executeWorkflow function
        const submitBtn = form.querySelector('.btn-primary');
        const resultId = `${workflow.workflow_id}Result`;

        if (typeof executeWorkflow === 'function') {
            await executeWorkflow(workflow.workflow_id, inputData, resultId, submitBtn);
        } else {
            console.error('executeWorkflow function not found');
            alert('Error: Workflow execution function not available');
        }
    });

    // Clear button handler
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            form.reset();
            const resultPanel = document.getElementById(`${workflow.workflow_id}Result`);
            if (resultPanel) {
                resultPanel.style.display = 'none';
            }
        });
    }
}

/**
 * Get emoji based on category
 */
function getCategoryEmoji(category) {
    const emojiMap = {
        'legal': '⚖️',
        'hr': '👥',
        'cs': '💬',
        'general': '📋',
        'finance': '💰',
        'compliance': '✅',
        'research': '🔍'
    };

    return emojiMap[category] || '📄';
}

/**
 * Refresh custom workflows (useful after creating/editing)
 */
async function refreshCustomWorkflows() {
    console.log('🔄 Refreshing custom workflows...');

    // Remove existing custom workflow tabs and panels
    customWorkflows.forEach(workflow => {
        const tab = document.querySelector(`[data-workflow="${workflow.id}"]`);
        const panel = document.getElementById(`workflow-${workflow.id}`);

        if (tab) tab.remove();
        if (panel) panel.remove();
    });

    // Clear array
    customWorkflows = [];

    // Reload
    await initializeCustomWorkflows();
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initializeCustomWorkflows);

// Export for use by workflow builder
window.refreshCustomWorkflows = refreshCustomWorkflows;

console.log('✅ Custom workflow loader initialized');
