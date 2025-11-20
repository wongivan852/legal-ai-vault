/**
 * Workflow Builder JavaScript
 *
 * Handles the visual workflow builder UI for creating custom multi-agent workflows
 */

// Available agents configuration
const AVAILABLE_AGENTS = [
    { value: 'legal_research', label: '⚖️ Legal Research', description: 'Research HK legal questions' },
    { value: 'hr_policy', label: '👥 HR Policy', description: 'HR policies and employee benefits' },
    { value: 'cs_document', label: '💬 Customer Service', description: 'Support documentation and FAQs' },
    { value: 'analysis', label: '📊 Analysis', description: 'Extract insights and patterns' },
    { value: 'synthesis', label: '🔗 Synthesis', description: 'Combine multiple sources' },
    { value: 'validation', label: '✅ Validation', description: 'Verify accuracy and compliance' }
];

// Global state
let workflowSteps = [];
let inputFields = [];
let stepCounter = 0;
let inputFieldCounter = 0;
let editingWorkflowId = null;

// ============================================================================
// Builder Mode Switching
// ============================================================================

document.querySelectorAll('[data-builder-mode]').forEach(btn => {
    btn.addEventListener('click', function() {
        const mode = this.dataset.builderMode;

        // Update button states
        document.querySelectorAll('[data-builder-mode]').forEach(b => b.classList.remove('active'));
        this.classList.add('active');

        // Update content visibility
        document.querySelectorAll('.builder-mode').forEach(m => m.style.display = 'none');
        document.getElementById(`builder-${mode}-mode`).style.display = 'block';

        // Load workflows if switching to manage mode
        if (mode === 'manage') {
            loadWorkflowList();
        }
    });
});

// ============================================================================
// Step Builder Functions
// ============================================================================

document.getElementById('addWorkflowStep').addEventListener('click', function() {
    addWorkflowStep();
});

function addWorkflowStep(stepData = null) {
    const stepId = stepCounter++;
    const step = stepData || {
        name: '',
        agent_name: '',
        description: '',
        task_config: {
            input_mappings: {},
            static_fields: {}
        }
    };

    workflowSteps.push({ id: stepId, data: step });

    const container = document.getElementById('workflowStepsContainer');
    const noStepsMsg = document.getElementById('noStepsMessage');
    noStepsMsg.style.display = 'none';

    const stepEl = document.createElement('div');
    stepEl.className = 'workflow-step';
    stepEl.dataset.stepId = stepId;
    stepEl.style.cssText = 'background: #fff; border: 2px solid #ddd; padding: 20px; border-radius: 8px; margin-bottom: 15px; position: relative;';

    stepEl.innerHTML = `
        <div style="position: absolute; top: 10px; right: 10px;">
            <button type="button" class="btn-step-delete" data-step-id="${stepId}"
                    style="background: #dc3545; color: white; border: none; padding: 5px 12px; border-radius: 4px; cursor: pointer; font-size: 14px;">
                🗑️ Delete
            </button>
        </div>

        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
            <div style="background: #2196F3; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 18px;">
                ${workflowSteps.length}
            </div>
            <h4 style="margin: 0; color: #333;">Step ${workflowSteps.length}</h4>
        </div>

        <div class="form-row" style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
            <div class="form-group">
                <label>Step Name *</label>
                <input type="text" class="input-field step-name" required
                       placeholder="e.g., legal_research"
                       pattern="[a-z0-9_]+"
                       value="${step.name}"
                       title="Lowercase, numbers, underscores only">
                <small class="form-hint">Internal identifier (lowercase, underscores)</small>
            </div>

            <div class="form-group">
                <label>Agent *</label>
                <select class="input-field step-agent" required>
                    <option value="">Select agent...</option>
                    ${AVAILABLE_AGENTS.map(a => `
                        <option value="${a.value}" ${step.agent_name === a.value ? 'selected' : ''}>
                            ${a.label} - ${a.description}
                        </option>
                    `).join('')}
                </select>
            </div>
        </div>

        <div class="form-group" style="margin-bottom: 15px;">
            <label>Description</label>
            <textarea class="textarea-field step-description" rows="2"
                      placeholder="What does this step do?">${step.description}</textarea>
        </div>

        <!-- Field Mappings -->
        <div style="background: #f8f9fa; padding: 15px; border-radius: 6px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <strong style="color: #495057;">🔗 Field Mappings</strong>
                <button type="button" class="btn-add-mapping" data-step-id="${stepId}"
                        style="background: #28a745; color: white; border: none; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 12px;">
                    ➕ Add Mapping
                </button>
            </div>
            <div class="step-mappings" data-step-id="${stepId}">
                ${Object.keys(step.task_config.input_mappings || {}).length === 0 ?
                    '<p style="color: #999; font-size: 13px; margin: 10px 0;">No field mappings yet</p>' :
                    generateMappingsHTML(step.task_config.input_mappings, stepId)
                }
            </div>
        </div>

        <!-- Static Fields -->
        <div style="background: #fff3cd; padding: 15px; border-radius: 6px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <strong style="color: #856404;">📌 Static Fields</strong>
                <button type="button" class="btn-add-static" data-step-id="${stepId}"
                        style="background: #ffc107; color: #333; border: none; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 12px;">
                    ➕ Add Static Field
                </button>
            </div>
            <div class="step-static-fields" data-step-id="${stepId}">
                ${Object.keys(step.task_config.static_fields || {}).length === 0 ?
                    '<p style="color: #856404; font-size: 13px; margin: 10px 0;">No static fields yet</p>' :
                    generateStaticFieldsHTML(step.task_config.static_fields, stepId)
                }
            </div>
        </div>
    `;

    container.appendChild(stepEl);

    // Attach event listeners
    attachStepEventListeners(stepEl, stepId);
}

function generateMappingsHTML(mappings, stepId) {
    return Object.entries(mappings).map(([taskField, mapping]) => `
        <div class="mapping-item" style="display: grid; grid-template-columns: 1fr 1fr 1fr auto; gap: 10px; margin-bottom: 8px; padding: 8px; background: white; border-radius: 4px;">
            <input type="text" class="input-field mapping-task-field" placeholder="Task field"
                   value="${taskField}" style="font-size: 13px;">
            <select class="input-field mapping-source" style="font-size: 13px;">
                <option value="input" ${mapping.source === 'input' ? 'selected' : ''}>User Input</option>
                <option value="step" ${mapping.source === 'step' ? 'selected' : ''}>Previous Step</option>
                <option value="static" ${mapping.source === 'static' ? 'selected' : ''}>Static Value</option>
            </select>
            <input type="text" class="input-field mapping-field" placeholder="Field/Step name"
                   value="${mapping.field || mapping.step_name || mapping.value || ''}" style="font-size: 13px;">
            <button type="button" class="btn-remove-mapping" style="background: #dc3545; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 12px;">
                🗑️
            </button>
        </div>
    `).join('');
}

function generateStaticFieldsHTML(staticFields, stepId) {
    return Object.entries(staticFields).map(([key, value]) => `
        <div class="static-field-item" style="display: grid; grid-template-columns: 1fr 1fr auto; gap: 10px; margin-bottom: 8px; padding: 8px; background: white; border-radius: 4px;">
            <input type="text" class="input-field static-key" placeholder="Field name"
                   value="${key}" style="font-size: 13px;">
            <input type="text" class="input-field static-value" placeholder="Value"
                   value="${value}" style="font-size: 13px;">
            <button type="button" class="btn-remove-static" style="background: #dc3545; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 12px;">
                🗑️
            </button>
        </div>
    `).join('');
}

function attachStepEventListeners(stepEl, stepId) {
    // Delete step
    stepEl.querySelector('.btn-step-delete').addEventListener('click', function() {
        workflowSteps = workflowSteps.filter(s => s.id !== stepId);
        stepEl.remove();

        // Renumber remaining steps
        const container = document.getElementById('workflowStepsContainer');
        container.querySelectorAll('.workflow-step').forEach((el, idx) => {
            el.querySelector('h4').textContent = `Step ${idx + 1}`;
            el.querySelector('div[style*="background: #2196F3"]').textContent = idx + 1;
        });

        if (workflowSteps.length === 0) {
            document.getElementById('noStepsMessage').style.display = 'block';
        }
    });

    // Add mapping
    stepEl.querySelector('.btn-add-mapping').addEventListener('click', function() {
        const mappingsContainer = stepEl.querySelector('.step-mappings');
        const emptyMsg = mappingsContainer.querySelector('p');
        if (emptyMsg) emptyMsg.remove();

        const mappingEl = document.createElement('div');
        mappingEl.className = 'mapping-item';
        mappingEl.style.cssText = 'display: grid; grid-template-columns: 1fr 1fr 1fr auto; gap: 10px; margin-bottom: 8px; padding: 8px; background: white; border-radius: 4px;';
        mappingEl.innerHTML = `
            <input type="text" class="input-field mapping-task-field" placeholder="Task field (e.g., question)" style="font-size: 13px;">
            <select class="input-field mapping-source" style="font-size: 13px;">
                <option value="input">User Input</option>
                <option value="step">Previous Step</option>
                <option value="static">Static Value</option>
            </select>
            <input type="text" class="input-field mapping-field" placeholder="Source field name" style="font-size: 13px;">
            <button type="button" class="btn-remove-mapping" style="background: #dc3545; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 12px;">
                🗑️
            </button>
        `;

        mappingEl.querySelector('.btn-remove-mapping').addEventListener('click', function() {
            mappingEl.remove();
            if (mappingsContainer.children.length === 0) {
                mappingsContainer.innerHTML = '<p style="color: #999; font-size: 13px; margin: 10px 0;">No field mappings yet</p>';
            }
        });

        mappingsContainer.appendChild(mappingEl);
    });

    // Add static field
    stepEl.querySelector('.btn-add-static').addEventListener('click', function() {
        const staticContainer = stepEl.querySelector('.step-static-fields');
        const emptyMsg = staticContainer.querySelector('p');
        if (emptyMsg) emptyMsg.remove();

        const staticEl = document.createElement('div');
        staticEl.className = 'static-field-item';
        staticEl.style.cssText = 'display: grid; grid-template-columns: 1fr 1fr auto; gap: 10px; margin-bottom: 8px; padding: 8px; background: white; border-radius: 4px;';
        staticEl.innerHTML = `
            <input type="text" class="input-field static-key" placeholder="Field name (e.g., task_type)" style="font-size: 13px;">
            <input type="text" class="input-field static-value" placeholder="Value (e.g., benefits)" style="font-size: 13px;">
            <button type="button" class="btn-remove-static" style="background: #dc3545; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 12px;">
                🗑️
            </button>
        `;

        staticEl.querySelector('.btn-remove-static').addEventListener('click', function() {
            staticEl.remove();
            if (staticContainer.children.length === 0) {
                staticContainer.innerHTML = '<p style="color: #856404; font-size: 13px; margin: 10px 0;">No static fields yet</p>';
            }
        });

        staticContainer.appendChild(staticEl);
    });
}

// ============================================================================
// Input Field Builder Functions
// ============================================================================

document.getElementById('addInputField').addEventListener('click', function() {
    addInputField();
});

function addInputField(fieldData = null) {
    const fieldId = inputFieldCounter++;
    const field = fieldData || {
        name: '',
        type: 'text',
        required: false,
        label: '',
        placeholder: ''
    };

    inputFields.push({ id: fieldId, data: field });

    const container = document.getElementById('inputFieldsContainer');
    const noInputMsg = document.getElementById('noInputMessage');
    noInputMsg.style.display = 'none';

    const fieldEl = document.createElement('div');
    fieldEl.className = 'input-field-item';
    fieldEl.style.cssText = 'background: white; border: 1px solid #ddd; padding: 15px; border-radius: 6px; margin-bottom: 10px; position: relative;';
    fieldEl.dataset.fieldId = fieldId;

    fieldEl.innerHTML = `
        <button type="button" class="btn-remove-input" data-field-id="${fieldId}"
                style="position: absolute; top: 10px; right: 10px; background: #dc3545; color: white; border: none; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 12px;">
            🗑️
        </button>

        <div class="form-row" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div class="form-group" style="margin: 0;">
                <label style="font-size: 13px; font-weight: 600;">Field Name *</label>
                <input type="text" class="input-field input-name" required
                       placeholder="e.g., question"
                       pattern="[a-z0-9_]+"
                       value="${field.name}"
                       style="font-size: 13px;">
                <small class="form-hint" style="font-size: 11px;">Internal name (lowercase, underscores)</small>
            </div>

            <div class="form-group" style="margin: 0;">
                <label style="font-size: 13px; font-weight: 600;">Field Type *</label>
                <select class="input-field input-type" style="font-size: 13px;">
                    <option value="text" ${field.type === 'text' ? 'selected' : ''}>Text</option>
                    <option value="textarea" ${field.type === 'textarea' ? 'selected' : ''}>Textarea</option>
                    <option value="number" ${field.type === 'number' ? 'selected' : ''}>Number</option>
                    <option value="select" ${field.type === 'select' ? 'selected' : ''}>Dropdown</option>
                </select>
            </div>
        </div>

        <div class="form-row" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
            <div class="form-group" style="margin: 0;">
                <label style="font-size: 13px; font-weight: 600;">Label *</label>
                <input type="text" class="input-field input-label" required
                       placeholder="e.g., Legal Question"
                       value="${field.label}"
                       style="font-size: 13px;">
            </div>

            <div class="form-group" style="margin: 0;">
                <label style="font-size: 13px; font-weight: 600;">Placeholder</label>
                <input type="text" class="input-field input-placeholder"
                       placeholder="e.g., Enter your question..."
                       value="${field.placeholder || ''}"
                       style="font-size: 13px;">
            </div>
        </div>

        <div class="form-group" style="margin-top: 10px; margin-bottom: 0;">
            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
                <input type="checkbox" class="input-required" ${field.required ? 'checked' : ''}
                       style="width: 16px; height: 16px;">
                <span style="font-size: 13px; font-weight: 600;">Required field</span>
            </label>
        </div>
    `;

    container.appendChild(fieldEl);

    // Delete input field
    fieldEl.querySelector('.btn-remove-input').addEventListener('click', function() {
        inputFields = inputFields.filter(f => f.id !== fieldId);
        fieldEl.remove();

        if (inputFields.length === 0) {
            noInputMsg.style.display = 'block';
        }
    });
}

// ============================================================================
// Form Submission
// ============================================================================

document.getElementById('workflowBuilderForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const btn = document.getElementById('saveWorkflowBtn');
    const resultDiv = document.getElementById('builderResult');

    try {
        // Show loading
        btn.querySelector('.btn-text').style.display = 'none';
        btn.querySelector('.btn-loading').style.display = 'inline-block';
        btn.disabled = true;

        // Collect workflow data
        const workflowData = collectWorkflowData();

        // Validate
        if (workflowData.steps.length === 0) {
            throw new Error('Please add at least one workflow step');
        }

        // Save workflow
        const endpoint = editingWorkflowId
            ? `/api/workflows/builder/${editingWorkflowId}`
            : '/api/workflows/builder/create';

        const method = editingWorkflowId ? 'PUT' : 'POST';

        const response = await fetch(endpoint, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(workflowData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Failed to save workflow');
        }

        // Show success
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div class="result-header" style="background: #d4edda; border-color: #c3e6cb;">
                <h3 style="color: #155724;">✅ ${editingWorkflowId ? 'Workflow Updated' : 'Workflow Created Successfully'}!</h3>
            </div>
            <div class="result-content">
                <p style="color: #155724; margin-bottom: 15px;"><strong>${result.message}</strong></p>
                <p style="color: #155724;">Workflow ID: <code style="background: #c3e6cb; padding: 2px 6px; border-radius: 3px;">${workflowData.workflow_id}</code></p>
                <p style="color: #155724; margin-top: 10px;">The workflow is now available for execution in the workflows list!</p>
            </div>
        `;

        // Clear form
        clearBuilderForm();

    } catch (error) {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div class="result-header" style="background: #f8d7da; border-color: #f5c6cb;">
                <h3 style="color: #721c24;">❌ Error Saving Workflow</h3>
            </div>
            <div class="result-content">
                <p style="color: #721c24;"><strong>Error:</strong> ${error.message}</p>
            </div>
        `;
    } finally {
        // Hide loading
        btn.querySelector('.btn-text').style.display = 'inline-block';
        btn.querySelector('.btn-loading').style.display = 'none';
        btn.disabled = false;
    }
});

function collectWorkflowData() {
    const steps = [];

    document.querySelectorAll('.workflow-step').forEach(stepEl => {
        const step = {
            name: stepEl.querySelector('.step-name').value.trim(),
            agent_name: stepEl.querySelector('.step-agent').value,
            description: stepEl.querySelector('.step-description').value.trim(),
            task_config: {
                input_mappings: {},
                static_fields: {}
            }
        };

        // Collect mappings
        stepEl.querySelectorAll('.mapping-item').forEach(mappingEl => {
            const taskField = mappingEl.querySelector('.mapping-task-field').value.trim();
            const source = mappingEl.querySelector('.mapping-source').value;
            const field = mappingEl.querySelector('.mapping-field').value.trim();

            if (taskField && field) {
                step.task_config.input_mappings[taskField] = {
                    source: source,
                    [source === 'step' ? 'step_name' : 'field']: field,
                    default: ""
                };
            }
        });

        // Collect static fields
        stepEl.querySelectorAll('.static-field-item').forEach(staticEl => {
            const key = staticEl.querySelector('.static-key').value.trim();
            const value = staticEl.querySelector('.static-value').value.trim();

            if (key) {
                step.task_config.static_fields[key] = value;
            }
        });

        steps.push(step);
    });

    // Collect input schema
    const inputSchema = { fields: [] };
    document.querySelectorAll('.input-field-item').forEach(fieldEl => {
        inputSchema.fields.push({
            name: fieldEl.querySelector('.input-name').value.trim(),
            type: fieldEl.querySelector('.input-type').value,
            label: fieldEl.querySelector('.input-label').value.trim(),
            placeholder: fieldEl.querySelector('.input-placeholder').value.trim(),
            required: fieldEl.querySelector('.input-required').checked
        });
    });

    // Build workflow data
    const tags = document.getElementById('builderTags').value
        .split(',')
        .map(t => t.trim())
        .filter(t => t);

    return {
        workflow_id: document.getElementById('builderWorkflowId').value.trim(),
        name: document.getElementById('builderWorkflowName').value.trim(),
        description: document.getElementById('builderWorkflowDesc').value.trim(),
        steps: steps,
        input_schema: inputSchema,
        category: document.getElementById('builderCategory').value,
        tags: tags
    };
}

// ============================================================================
// Clear and Preview
// ============================================================================

document.getElementById('clearBuilder').addEventListener('click', function() {
    if (confirm('Are you sure you want to clear all fields?')) {
        clearBuilderForm();
    }
});

function clearBuilderForm() {
    document.getElementById('workflowBuilderForm').reset();
    document.getElementById('workflowStepsContainer').innerHTML = '';
    document.getElementById('noStepsMessage').style.display = 'block';
    document.getElementById('inputFieldsContainer').innerHTML = '';
    document.getElementById('noInputMessage').style.display = 'block';
    workflowSteps = [];
    inputFields = [];
    stepCounter = 0;
    inputFieldCounter = 0;
    editingWorkflowId = null;
    document.getElementById('builderResult').style.display = 'none';
}

document.getElementById('previewWorkflow').addEventListener('click', function() {
    try {
        const workflowData = collectWorkflowData();
        document.getElementById('jsonPreviewContent').textContent = JSON.stringify(workflowData, null, 2);
        document.getElementById('jsonPreviewModal').style.display = 'flex';
    } catch (error) {
        alert('Error generating preview: ' + error.message);
    }
});

document.getElementById('closePreview').addEventListener('click', function() {
    document.getElementById('jsonPreviewModal').style.display = 'none';
});

// ============================================================================
// Workflow Management
// ============================================================================

document.getElementById('refreshWorkflowList').addEventListener('click', function() {
    loadWorkflowList();
});

async function loadWorkflowList() {
    const container = document.getElementById('workflowListContainer');

    try {
        container.innerHTML = '<p style="text-align: center; padding: 20px;">⏳ Loading workflows...</p>';

        const response = await fetch('/api/workflows/builder/list');
        const data = await response.json();

        if (data.workflows.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #999;">
                    <p style="font-size: 18px;">📭 No custom workflows yet</p>
                    <p>Create your first workflow using the "Create New" tab!</p>
                </div>
            `;
            return;
        }

        // Display workflows
        container.innerHTML = data.workflows.map(wf => `
            <div class="workflow-card" style="background: white; border: 2px solid #e0e0e0; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <h4 style="margin: 0 0 10px 0; color: #333;">
                            ${wf.name}
                            ${wf.is_system ? '<span style="background: #6c757d; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-left: 8px;">SYSTEM</span>' : ''}
                        </h4>
                        <p style="color: #666; margin: 0 0 10px 0;">${wf.description || 'No description'}</p>
                        <div style="display: flex; gap: 15px; font-size: 13px; color: #777;">
                            <span>📁 ${wf.category}</span>
                            <span>🔗 ${wf.step_count} steps</span>
                            <span>▶️ ${wf.execution_count || 0} executions</span>
                            ${wf.tags && wf.tags.length > 0 ? `<span>🏷️ ${wf.tags.join(', ')}</span>` : ''}
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        ${!wf.is_system ? `
                            <button class="btn-edit-workflow" data-workflow-id="${wf.id}"
                                    style="background: #ffc107; color: #333; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 13px;">
                                ✏️ Edit
                            </button>
                            <button class="btn-delete-workflow" data-workflow-id="${wf.id}" data-workflow-name="${wf.name}"
                                    style="background: #dc3545; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 13px;">
                                🗑️ Delete
                            </button>
                        ` : ''}
                    </div>
                </div>
            </div>
        `).join('');

        // Attach event listeners
        container.querySelectorAll('.btn-edit-workflow').forEach(btn => {
            btn.addEventListener('click', function() {
                editWorkflow(this.dataset.workflowId);
            });
        });

        container.querySelectorAll('.btn-delete-workflow').forEach(btn => {
            btn.addEventListener('click', function() {
                deleteWorkflow(this.dataset.workflowId, this.dataset.workflowName);
            });
        });

    } catch (error) {
        container.innerHTML = `
            <div style="background: #f8d7da; border: 1px solid #f5c6cb; padding: 20px; border-radius: 8px; color: #721c24;">
                <strong>Error loading workflows:</strong> ${error.message}
            </div>
        `;
    }
}

async function editWorkflow(workflowId) {
    try {
        const response = await fetch(`/api/workflows/builder/${workflowId}`);
        const data = await response.json();

        if (!data.success) {
            throw new Error('Failed to load workflow details');
        }

        const workflow = data.workflow;

        // Clear form
        clearBuilderForm();

        // Set editing mode
        editingWorkflowId = workflowId;

        // Fill basic info
        document.getElementById('builderWorkflowId').value = workflow.workflow_id;
        document.getElementById('builderWorkflowId').disabled = true; // Can't change ID when editing
        document.getElementById('builderWorkflowName').value = workflow.name;
        document.getElementById('builderWorkflowDesc').value = workflow.description || '';
        document.getElementById('builderCategory').value = workflow.category || 'general';
        document.getElementById('builderTags').value = (workflow.tags || []).join(', ');

        // Add steps
        workflow.steps.forEach(step => addWorkflowStep(step));

        // Add input fields
        if (workflow.input_schema && workflow.input_schema.fields) {
            workflow.input_schema.fields.forEach(field => addInputField(field));
        }

        // Switch to create tab
        document.querySelector('[data-builder-mode="create"]').click();

        // Update button text
        document.getElementById('saveWorkflowBtn').querySelector('.btn-text').textContent = '💾 Update Workflow';

        // Show message
        const resultDiv = document.getElementById('builderResult');
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div class="result-header" style="background: #d1ecf1; border-color: #bee5eb;">
                <h3 style="color: #0c5460;">✏️ Editing Workflow</h3>
            </div>
            <div class="result-content">
                <p style="color: #0c5460;">You are now editing: <strong>${workflow.name}</strong></p>
                <p style="color: #0c5460; font-size: 13px;">Make your changes and click "Update Workflow" to save.</p>
            </div>
        `;

    } catch (error) {
        alert('Error loading workflow: ' + error.message);
    }
}

async function deleteWorkflow(workflowId, workflowName) {
    if (!confirm(`Are you sure you want to delete "${workflowName}"?\n\nThis action cannot be undone.`)) {
        return;
    }

    try {
        const response = await fetch(`/api/workflows/builder/${workflowId}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Failed to delete workflow');
        }

        alert(`✅ Workflow "${workflowName}" deleted successfully`);
        loadWorkflowList();

    } catch (error) {
        alert('❌ Error deleting workflow: ' + error.message);
    }
}

console.log('✅ Workflow Builder initialized');
