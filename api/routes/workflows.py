"""
Workflow API Routes

Endpoints for executing and managing multi-agent workflows.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from workflows import WorkflowRegistry, get_all_workflows
from sqlalchemy.orm import Session
from database import get_db
from services.workflow_service import WorkflowService

router = APIRouter(prefix="/api/workflows", tags=["workflows"])

# Global workflow registry
workflow_registry = WorkflowRegistry()


def load_all_workflows():
    """
    Load both system workflows and custom database workflows
    This function is called on module load and can be called to refresh workflows
    """
    # Load system workflows (hardcoded in workflow_definitions.py)
    for workflow_id, workflow in get_all_workflows().items():
        workflow_registry.register(workflow_id, workflow)

    # Load custom workflows from database
    try:
        from database import SessionLocal
        db = SessionLocal()
        try:
            custom_workflows = WorkflowService.list_workflows(
                db=db,
                is_active=True,
                include_system=False
            )

            for custom_wf in custom_workflows:
                runtime_workflow = WorkflowService.json_to_workflow(custom_wf)
                workflow_registry.register(custom_wf.workflow_id, runtime_workflow)

            print(f"✓ Loaded {len(custom_workflows)} custom workflows from database")

        finally:
            db.close()

    except Exception as e:
        print(f"⚠ Warning: Could not load custom workflows from database: {e}")
        print("  This is normal on first startup before database tables are created.")


# Initialize workflows on module load
load_all_workflows()


class WorkflowExecuteRequest(BaseModel):
    """Request model for workflow execution"""
    input: Dict[str, Any]


class WorkflowStepDefinition(BaseModel):
    """Definition of a single workflow step"""
    name: str = Field(..., description="Step name (e.g., 'legal_research')")
    agent_name: str = Field(..., description="Agent to use (e.g., 'legal_research')")
    description: str = Field("", description="Human-readable description")
    task_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Task configuration with input_mappings and static_fields"
    )


class WorkflowCreateRequest(BaseModel):
    """Request model for creating a new workflow"""
    workflow_id: str = Field(..., description="Unique workflow ID (lowercase, underscores)")
    name: str = Field(..., description="Display name")
    description: str = Field("", description="Workflow description")
    steps: List[WorkflowStepDefinition] = Field(..., description="List of workflow steps")
    input_schema: Optional[Dict[str, Any]] = Field(None, description="Input field definitions")
    category: Optional[str] = Field("general", description="Workflow category")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for categorization")


class WorkflowUpdateRequest(BaseModel):
    """Request model for updating a workflow"""
    name: Optional[str] = Field(None, description="New display name")
    description: Optional[str] = Field(None, description="New description")
    steps: Optional[List[WorkflowStepDefinition]] = Field(None, description="New step definitions")
    input_schema: Optional[Dict[str, Any]] = Field(None, description="New input schema")
    category: Optional[str] = Field(None, description="New category")
    tags: Optional[List[str]] = Field(None, description="New tags")
    is_active: Optional[bool] = Field(None, description="Enable/disable workflow")


@router.get("/")
async def list_workflows():
    """List all available workflows"""
    return {
        "workflows": workflow_registry.list_all(),
        "total": len(workflow_registry.workflows)
    }


@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get details about a specific workflow"""
    workflow = workflow_registry.get(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")

    return {
        "id": workflow_id,
        **workflow.to_dict()
    }


@router.post("/{workflow_id}/execute")
async def execute_workflow(workflow_id: str, request: WorkflowExecuteRequest):
    """
    Execute a workflow

    This endpoint runs a multi-agent workflow with the provided input.
    The workflow orchestrates multiple agents in sequence and returns
    aggregated results with progress tracking.
    """
    # Get agents registry (avoid circular imports by importing inside function)
    from routes.agents import get_agent_registry, get_agent
    from database import get_db

    # Get database session
    db = next(get_db())

    # Initialize agents that need database (legal_research, synthesis)
    get_agent("legal_research", db)
    get_agent("synthesis", db)

    # Get the fully initialized registry
    agents_registry, _ = get_agent_registry()

    try:
        result = await workflow_registry.execute_workflow(
            workflow_id=workflow_id,
            agents_registry=agents_registry,
            user_input=request.input
        )
        return result

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")


@router.get("/{workflow_id}/schema")
async def get_workflow_schema(workflow_id: str):
    """Get input schema for a workflow (describes expected input fields)"""
    schemas = {
        "hr_onboarding": {
            "employee_question": {
                "type": "string",
                "required": False,
                "description": "Specific question about onboarding (optional, defaults to general onboarding)",
                "example": "What are the key onboarding steps for a new employee?"
            },
            "employee_name": {
                "type": "string",
                "required": False,
                "description": "Name of the employee being onboarded",
                "example": "John Doe"
            },
            "role": {
                "type": "string",
                "required": False,
                "description": "Role/position of the new employee",
                "example": "Software Engineer"
            },
            "hr_policies": {
                "type": "string",
                "required": False,
                "description": "HR policy documents (optional, for context)",
                "example": "Employee Handbook content..."
            }
        },
        "cs_ticket": {
            "customer_query": {
                "type": "string",
                "required": True,
                "description": "The customer's support question or issue",
                "example": "How do I reset my password?"
            },
            "customer_name": {
                "type": "string",
                "required": False,
                "description": "Customer's name",
                "example": "Jane Smith"
            },
            "support_docs": {
                "type": "string",
                "required": False,
                "description": "Support documentation or FAQs",
                "example": "Password Reset Guide: Step 1..."
            }
        },
        "legal_hr_compliance": {
            "compliance_area": {
                "type": "string",
                "required": True,
                "description": "Area of compliance to check",
                "example": "What are the legal requirements for employee leave policies in Hong Kong?"
            },
            "policy_name": {
                "type": "string",
                "required": True,
                "description": "Name of the HR policy being validated",
                "example": "Annual Leave Policy"
            },
            "policy_content": {
                "type": "string",
                "required": True,
                "description": "Full text of the HR policy to validate",
                "example": "Employees receive 7 days annual leave after 12 months..."
            }
        },
        "simple_qa": {
            "question": {
                "type": "string",
                "required": True,
                "description": "Legal question to answer and validate",
                "example": "What are director duties under Companies Ordinance?"
            }
        },
        "multi_agent_research": {
            "research_topic": {
                "type": "string",
                "required": True,
                "description": "Topic to research from multiple perspectives",
                "example": "Remote work policies and their legal implications"
            },
            "hr_context": {
                "type": "string",
                "required": False,
                "description": "HR-specific context (optional)",
                "example": "Current remote work policy..."
            },
            "cs_context": {
                "type": "string",
                "required": False,
                "description": "Customer service context (optional)",
                "example": "Customer feedback on remote support..."
            }
        }
    }

    schema = schemas.get(workflow_id)
    if not schema:
        raise HTTPException(status_code=404, detail=f"Schema for workflow '{workflow_id}' not found")

    return {
        "workflow_id": workflow_id,
        "input_schema": schema
    }


# ============================================================================
# Workflow Builder CRUD Endpoints
# ============================================================================

@router.post("/builder/create")
async def create_custom_workflow(
    request: WorkflowCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new custom workflow

    This endpoint allows users to create workflows through the UI without coding.
    The workflow is stored in the database and can be executed like system workflows.
    """
    try:
        # Convert Pydantic models to dict
        steps_dict = [step.dict() for step in request.steps]

        # Create workflow in database
        workflow = WorkflowService.create_workflow(
            db=db,
            workflow_id=request.workflow_id,
            name=request.name,
            description=request.description,
            steps=steps_dict,
            input_schema=request.input_schema,
            category=request.category,
            tags=request.tags
        )

        # Convert to runtime Workflow and register
        runtime_workflow = WorkflowService.json_to_workflow(workflow)
        workflow_registry.register(request.workflow_id, runtime_workflow)

        return {
            "success": True,
            "message": f"Workflow '{request.name}' created successfully",
            "workflow": workflow.to_dict()
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create workflow: {str(e)}")


@router.put("/builder/{workflow_id}")
async def update_custom_workflow(
    workflow_id: str,
    request: WorkflowUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Update an existing custom workflow

    System workflows (pre-built) cannot be modified through this endpoint.
    """
    try:
        # Convert step models to dict if provided
        steps_dict = None
        if request.steps:
            steps_dict = [step.dict() for step in request.steps]

        # Update workflow in database
        workflow = WorkflowService.update_workflow(
            db=db,
            workflow_id=workflow_id,
            name=request.name,
            description=request.description,
            steps=steps_dict,
            input_schema=request.input_schema,
            category=request.category,
            tags=request.tags,
            is_active=request.is_active
        )

        # Update in registry if active
        if workflow.is_active:
            runtime_workflow = WorkflowService.json_to_workflow(workflow)
            workflow_registry.register(workflow_id, runtime_workflow)
        else:
            # Remove from registry if deactivated
            if workflow_id in workflow_registry.workflows:
                del workflow_registry.workflows[workflow_id]

        return {
            "success": True,
            "message": f"Workflow '{workflow.name}' updated successfully",
            "workflow": workflow.to_dict()
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update workflow: {str(e)}")


@router.delete("/builder/{workflow_id}")
async def delete_custom_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a custom workflow

    System workflows (pre-built) cannot be deleted through this endpoint.
    """
    try:
        # Delete from database
        WorkflowService.delete_workflow(db, workflow_id)

        # Remove from registry
        if workflow_id in workflow_registry.workflows:
            del workflow_registry.workflows[workflow_id]

        return {
            "success": True,
            "message": f"Workflow '{workflow_id}' deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete workflow: {str(e)}")


@router.get("/builder/list")
async def list_custom_workflows(
    category: Optional[str] = None,
    include_system: bool = True,
    db: Session = Depends(get_db)
):
    """
    List all custom workflows

    Query Parameters:
    - category: Filter by category (legal, hr, cs, general)
    - include_system: Include pre-built system workflows (default: true)
    """
    try:
        workflows = WorkflowService.list_workflows(
            db=db,
            category=category,
            is_active=True,
            include_system=include_system
        )

        return {
            "workflows": [w.to_workflow_summary() for w in workflows],
            "total": len(workflows)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list workflows: {str(e)}")


@router.get("/builder/{workflow_id}")
async def get_custom_workflow_detail(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a custom workflow

    This endpoint returns the full workflow definition including all steps
    and configuration, suitable for editing in the workflow builder UI.
    """
    try:
        workflow = WorkflowService.get_workflow(db, workflow_id)

        if not workflow:
            raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")

        return {
            "success": True,
            "workflow": workflow.to_dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get workflow: {str(e)}")
