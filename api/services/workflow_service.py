"""
Workflow Service Layer

Handles persistence and conversion of custom workflows.
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from models.custom_workflow import CustomWorkflow
from workflows.workflow_engine import Workflow, WorkflowStep
from datetime import datetime
import json


class WorkflowService:
    """Service for managing custom workflows in database"""

    @staticmethod
    def create_workflow(
        db: Session,
        workflow_id: str,
        name: str,
        description: str,
        steps: List[Dict[str, Any]],
        input_schema: Optional[Dict[str, Any]] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        created_by: Optional[str] = "system"
    ) -> CustomWorkflow:
        """
        Create a new custom workflow

        Args:
            db: Database session
            workflow_id: Unique workflow identifier (e.g., "my_legal_check")
            name: Display name (e.g., "My Legal Compliance Check")
            description: Human-readable description
            steps: List of workflow step definitions
            input_schema: JSON schema for input fields
            category: Workflow category (legal, hr, cs, general)
            tags: List of tags for categorization
            created_by: User ID or username

        Returns:
            Created CustomWorkflow instance

        Raises:
            ValueError: If workflow_id already exists
        """
        # Check if workflow_id already exists
        existing = db.query(CustomWorkflow).filter(
            CustomWorkflow.workflow_id == workflow_id
        ).first()

        if existing:
            raise ValueError(f"Workflow with ID '{workflow_id}' already exists")

        # Validate workflow_id format (lowercase, underscores only)
        if not workflow_id.replace('_', '').replace('-', '').isalnum():
            raise ValueError(
                "Workflow ID must contain only letters, numbers, underscores, and hyphens"
            )

        # Create new workflow
        workflow = CustomWorkflow(
            workflow_id=workflow_id,
            name=name,
            description=description,
            steps=steps,
            input_schema=input_schema or {},
            category=category or "general",
            tags=tags or [],
            created_by=created_by,
            is_system=False,
            is_active=True
        )

        db.add(workflow)
        db.commit()
        db.refresh(workflow)

        return workflow

    @staticmethod
    def update_workflow(
        db: Session,
        workflow_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        steps: Optional[List[Dict[str, Any]]] = None,
        input_schema: Optional[Dict[str, Any]] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        is_active: Optional[bool] = None
    ) -> CustomWorkflow:
        """
        Update an existing workflow

        Args:
            db: Database session
            workflow_id: Workflow to update
            name: New display name (optional)
            description: New description (optional)
            steps: New step definitions (optional)
            input_schema: New input schema (optional)
            category: New category (optional)
            tags: New tags (optional)
            is_active: New active status (optional)

        Returns:
            Updated CustomWorkflow instance

        Raises:
            ValueError: If workflow not found or is system workflow
        """
        workflow = db.query(CustomWorkflow).filter(
            CustomWorkflow.workflow_id == workflow_id
        ).first()

        if not workflow:
            raise ValueError(f"Workflow '{workflow_id}' not found")

        if workflow.is_system:
            raise ValueError(f"Cannot modify system workflow '{workflow_id}'")

        # Update fields if provided
        if name is not None:
            workflow.name = name
        if description is not None:
            workflow.description = description
        if steps is not None:
            workflow.steps = steps
        if input_schema is not None:
            workflow.input_schema = input_schema
        if category is not None:
            workflow.category = category
        if tags is not None:
            workflow.tags = tags
        if is_active is not None:
            workflow.is_active = is_active

        db.commit()
        db.refresh(workflow)

        return workflow

    @staticmethod
    def delete_workflow(db: Session, workflow_id: str) -> bool:
        """
        Delete a workflow

        Args:
            db: Database session
            workflow_id: Workflow to delete

        Returns:
            True if deleted successfully

        Raises:
            ValueError: If workflow not found or is system workflow
        """
        workflow = db.query(CustomWorkflow).filter(
            CustomWorkflow.workflow_id == workflow_id
        ).first()

        if not workflow:
            raise ValueError(f"Workflow '{workflow_id}' not found")

        if workflow.is_system:
            raise ValueError(f"Cannot delete system workflow '{workflow_id}'")

        db.delete(workflow)
        db.commit()

        return True

    @staticmethod
    def get_workflow(db: Session, workflow_id: str) -> Optional[CustomWorkflow]:
        """Get a workflow by ID"""
        return db.query(CustomWorkflow).filter(
            CustomWorkflow.workflow_id == workflow_id
        ).first()

    @staticmethod
    def list_workflows(
        db: Session,
        category: Optional[str] = None,
        is_active: Optional[bool] = True,
        include_system: bool = True
    ) -> List[CustomWorkflow]:
        """
        List workflows with optional filters

        Args:
            db: Database session
            category: Filter by category (optional)
            is_active: Filter by active status (optional)
            include_system: Include system workflows (default True)

        Returns:
            List of CustomWorkflow instances
        """
        query = db.query(CustomWorkflow)

        if category:
            query = query.filter(CustomWorkflow.category == category)

        if is_active is not None:
            query = query.filter(CustomWorkflow.is_active == is_active)

        if not include_system:
            query = query.filter(CustomWorkflow.is_system == False)

        return query.order_by(CustomWorkflow.created_at.desc()).all()

    @staticmethod
    def increment_execution_count(db: Session, workflow_id: str):
        """Increment execution count and update last_executed timestamp"""
        workflow = db.query(CustomWorkflow).filter(
            CustomWorkflow.workflow_id == workflow_id
        ).first()

        if workflow:
            workflow.execution_count = (workflow.execution_count or 0) + 1
            workflow.last_executed = datetime.utcnow()
            db.commit()

    @staticmethod
    def json_to_workflow(workflow_data: CustomWorkflow) -> Workflow:
        """
        Convert database CustomWorkflow to runtime Workflow object

        Args:
            workflow_data: CustomWorkflow database instance

        Returns:
            Workflow runtime object
        """
        workflow = Workflow(
            name=workflow_data.name,
            description=workflow_data.description or ""
        )

        # Build workflow steps from JSON definition
        for step_def in workflow_data.steps:
            step = WorkflowService._build_step_from_json(step_def)
            workflow.add_step(step)

        return workflow

    @staticmethod
    def _build_step_from_json(step_def: Dict[str, Any]) -> WorkflowStep:
        """
        Build a WorkflowStep from JSON definition

        Step definition format:
        {
            "name": "legal_research",
            "agent_name": "legal_research",
            "description": "Research legal requirements",
            "task_config": {
                "input_mappings": {
                    "question": {"source": "input", "field": "compliance_question"},
                    "context": {"source": "step", "step_name": "previous_step", "field": "answer"}
                },
                "static_fields": {
                    "task_type": "compliance"
                }
            }
        }
        """
        task_config = step_def.get("task_config", {})
        input_mappings = task_config.get("input_mappings", {})
        static_fields = task_config.get("static_fields", {})

        def task_builder(ctx: Dict[str, Any], inp: Dict[str, Any]) -> Dict[str, Any]:
            """Dynamically build task from mappings"""
            task = {}

            # Add static fields
            task.update(static_fields)

            # Add mapped fields
            for task_field, mapping in input_mappings.items():
                source = mapping.get("source")

                if source == "input":
                    # Get from user input
                    field_name = mapping.get("field")
                    default = mapping.get("default", "")
                    task[task_field] = inp.get(field_name, default)

                elif source == "step":
                    # Get from previous step
                    step_name = mapping.get("step_name")
                    field_name = mapping.get("field", "answer")
                    default = mapping.get("default", "")

                    if step_name in ctx:
                        task[task_field] = ctx[step_name].get(field_name, default)
                    else:
                        task[task_field] = default

                elif source == "static":
                    # Static value
                    task[task_field] = mapping.get("value", "")

            return task

        return WorkflowStep(
            name=step_def["name"],
            agent_name=step_def["agent_name"],
            task_builder=task_builder,
            description=step_def.get("description", "")
        )
