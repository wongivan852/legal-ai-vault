"""
Workflow Orchestration Engine

Handles multi-agent workflow execution with progress tracking and result aggregation.
"""

import asyncio
import time
from typing import Dict, List, Any, Callable
from datetime import datetime


class WorkflowStep:
    """Represents a single step in a workflow"""

    def __init__(self, name: str, agent_name: str, task_builder: Callable, description: str = ""):
        self.name = name
        self.agent_name = agent_name
        self.task_builder = task_builder  # Function that builds the task dict
        self.description = description
        self.result = None
        self.error = None
        self.status = "pending"  # pending, running, completed, failed
        self.start_time = None
        self.end_time = None

    def to_dict(self):
        """Convert step to dictionary for API response"""
        return {
            "name": self.name,
            "agent": self.agent_name,
            "description": self.description,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "execution_time": self.execution_time if self.end_time else None
        }

    @property
    def execution_time(self):
        """Calculate execution time in seconds"""
        if self.start_time and self.end_time:
            return round(self.end_time - self.start_time, 2)
        return None


class Workflow:
    """Base class for multi-agent workflows"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.steps: List[WorkflowStep] = []
        self.status = "pending"
        self.start_time = None
        self.end_time = None
        self.context = {}  # Shared context between steps

    def add_step(self, step: WorkflowStep):
        """Add a step to the workflow"""
        self.steps.append(step)

    async def execute(self, agents_registry: Dict, initial_input: Dict) -> Dict:
        """
        Execute the workflow

        Args:
            agents_registry: Dictionary of initialized agents
            initial_input: User input for the workflow

        Returns:
            Dictionary with workflow results and metadata
        """
        self.status = "running"
        self.start_time = time.time()
        self.context["input"] = initial_input

        results = {
            "workflow": self.name,
            "status": "running",
            "steps": [],
            "final_result": None,
            "execution_time": None,
            "timestamp": datetime.now().isoformat()
        }

        try:
            for i, step in enumerate(self.steps):
                step.status = "running"
                step.start_time = time.time()

                # Update progress
                results["current_step"] = i + 1
                results["total_steps"] = len(self.steps)
                results["steps"] = [s.to_dict() for s in self.steps]

                # Get the agent
                agent_info = agents_registry.get(step.agent_name)
                if not agent_info or not agent_info.get("agent"):
                    raise ValueError(f"Agent '{step.agent_name}' not found or not initialized")

                agent = agent_info["agent"]

                # Build task using the task_builder function
                task = step.task_builder(self.context, initial_input)

                # Execute the agent
                result = await agent.execute(task)

                # Store result
                step.result = result
                step.status = "completed"
                step.end_time = time.time()

                # Update context with this step's result
                self.context[f"step_{i + 1}_result"] = result
                self.context[step.name] = result

            # Workflow completed successfully
            self.status = "completed"
            self.end_time = time.time()

            results["status"] = "completed"
            results["steps"] = [s.to_dict() for s in self.steps]
            results["final_result"] = self.steps[-1].result if self.steps else None
            results["execution_time"] = round(self.end_time - self.start_time, 2)
            results["context"] = {k: v for k, v in self.context.items() if k != "input"}

        except Exception as e:
            self.status = "failed"
            self.end_time = time.time()

            results["status"] = "failed"
            results["error"] = str(e)
            results["steps"] = [s.to_dict() for s in self.steps]

            # Mark current step as failed
            for step in self.steps:
                if step.status == "running":
                    step.status = "failed"
                    step.error = str(e)
                    step.end_time = time.time()

        return results

    def to_dict(self):
        """Convert workflow to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "steps": [
                {
                    "name": step.name,
                    "agent": step.agent_name,
                    "description": step.description
                }
                for step in self.steps
            ],
            "status": self.status
        }


class WorkflowRegistry:
    """Registry for managing available workflows"""

    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}

    def register(self, workflow_id: str, workflow: Workflow):
        """Register a workflow"""
        self.workflows[workflow_id] = workflow

    def get(self, workflow_id: str) -> Workflow:
        """Get a workflow by ID"""
        return self.workflows.get(workflow_id)

    def list_all(self) -> List[Dict]:
        """List all available workflows"""
        return [
            {
                "id": wf_id,
                **workflow.to_dict()
            }
            for wf_id, workflow in self.workflows.items()
        ]

    async def execute_workflow(self, workflow_id: str, agents_registry: Dict, user_input: Dict) -> Dict:
        """Execute a workflow by ID"""
        workflow = self.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow '{workflow_id}' not found")

        # Create a fresh instance to avoid state conflicts
        workflow_class = type(workflow)
        fresh_workflow = workflow_class.__new__(workflow_class)
        fresh_workflow.__dict__.update(workflow.__dict__.copy())
        fresh_workflow.steps = [
            WorkflowStep(s.name, s.agent_name, s.task_builder, s.description)
            for s in workflow.steps
        ]
        fresh_workflow.status = "pending"
        fresh_workflow.context = {}

        return await fresh_workflow.execute(agents_registry, user_input)
