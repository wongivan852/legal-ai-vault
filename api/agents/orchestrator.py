"""
Workflow Orchestrator
Coordinates multiple agents to execute complex multi-step workflows
"""

from typing import Dict, List, Any, Optional
import logging
import asyncio
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """
    Orchestrates multi-agent workflows for complex task execution.

    Manages agent lifecycle, workflow state, and task execution order.
    Supports sequential and parallel execution patterns.
    """

    def __init__(self):
        """Initialize the orchestrator"""
        self.agents = {}
        self.workflows = {}
        self.execution_history = []

    def register_agent(self, agent):
        """
        Register an agent for use in workflows

        Args:
            agent: BaseAgent instance
        """
        self.agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")

    def register_workflow(self, workflow_name: str, workflow_definition: Dict[str, Any]):
        """
        Register a workflow definition

        Args:
            workflow_name: Unique workflow identifier
            workflow_definition: Workflow specification with tasks and dependencies
        """
        self.workflows[workflow_name] = workflow_definition
        logger.info(f"Registered workflow: {workflow_name}")

    async def execute_workflow(
        self,
        workflow_name: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a registered workflow

        Args:
            workflow_name: Name of workflow to execute
            input_data: Initial input data for workflow

        Returns:
            Dict with workflow results and metadata
        """
        start_time = datetime.now()

        try:
            workflow = self.workflows.get(workflow_name)
            if not workflow:
                raise ValueError(f"Workflow '{workflow_name}' not found")

            logger.info(f"Starting workflow: {workflow_name}")

            # Initialize context with input
            context = {
                "input": input_data,
                "workflow_name": workflow_name,
                "start_time": start_time.isoformat()
            }

            results = {}

            # Execute tasks in order
            for task in workflow["tasks"]:
                task_id = task["task_id"]
                agent_name = task["agent"]

                logger.info(f"Executing task: {task_id} with agent: {agent_name}")

                # Get agent
                agent = self.agents.get(agent_name)
                if not agent:
                    raise ValueError(f"Agent '{agent_name}' not found")

                # Prepare task input by resolving variables
                task_input = self._resolve_variables(task["input"], context)

                # Execute agent
                task_start = datetime.now()
                result = await agent.execute(task_input)
                task_duration = (datetime.now() - task_start).total_seconds()

                # Store result in context and results
                results[task_id] = {
                    "agent": agent_name,
                    "result": result,
                    "duration": task_duration,
                    "timestamp": datetime.now().isoformat()
                }
                context[task_id] = result

                # Check if task failed
                if result.get("status") == "failed":
                    logger.error(f"Task {task_id} failed: {result.get('error')}")
                    if not task.get("continue_on_failure", False):
                        break

            # Get final output
            output_var = workflow.get("output_var")
            final_output = context.get(output_var) if output_var else results

            execution_time = (datetime.now() - start_time).total_seconds()

            workflow_result = {
                "workflow": workflow_name,
                "status": "completed",
                "results": results,
                "output": final_output,
                "execution_time": execution_time,
                "completed_at": datetime.now().isoformat()
            }

            # Store in history
            self.execution_history.append({
                "workflow": workflow_name,
                "timestamp": start_time.isoformat(),
                "duration": execution_time,
                "status": "completed"
            })

            logger.info(f"Workflow {workflow_name} completed in {execution_time:.1f}s")
            return workflow_result

        except Exception as e:
            logger.error(f"Workflow execution error: {e}", exc_info=True)
            return {
                "workflow": workflow_name,
                "status": "failed",
                "error": str(e),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

    async def execute_parallel_tasks(
        self,
        tasks: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute multiple tasks in parallel

        Args:
            tasks: List of task definitions
            context: Shared context for variable resolution

        Returns:
            Dict mapping task_id to results
        """
        async def execute_task(task):
            task_id = task["task_id"]
            agent_name = task["agent"]
            agent = self.agents.get(agent_name)

            if not agent:
                return task_id, {"status": "failed", "error": f"Agent {agent_name} not found"}

            task_input = self._resolve_variables(task["input"], context)
            result = await agent.execute(task_input)
            return task_id, result

        # Execute all tasks concurrently
        logger.info(f"Executing {len(tasks)} tasks in parallel")
        results = await asyncio.gather(*[execute_task(task) for task in tasks])

        # Convert to dict
        return {task_id: result for task_id, result in results}

    def _resolve_variables(self, input_template: Any, context: Dict[str, Any]) -> Any:
        """
        Resolve variable references in input template

        Supports ${variable.path} syntax to reference context values

        Args:
            input_template: Template with variable references
            context: Context dict with values

        Returns:
            Resolved input with variables substituted
        """
        if isinstance(input_template, str):
            # Find all ${variable} patterns
            pattern = r'\$\{([^}]+)\}'
            matches = re.findall(pattern, input_template)

            for match in matches:
                value = self._get_nested_value(context, match)
                if value is not None:
                    input_template = input_template.replace(f"${{{match}}}", str(value))

            return input_template

        elif isinstance(input_template, dict):
            # Recursively resolve dict values
            return {
                key: self._resolve_variables(value, context)
                for key, value in input_template.items()
            }

        elif isinstance(input_template, list):
            # Recursively resolve list items
            return [self._resolve_variables(item, context) for item in input_template]

        else:
            return input_template

    def _get_nested_value(self, data: Dict, path: str) -> Any:
        """
        Get nested value from dict using dot notation

        Args:
            data: Dict to search
            path: Dot-separated path (e.g., "result.answer")

        Returns:
            Value at path or None
        """
        keys = path.split('.')
        value = data

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None

            if value is None:
                return None

        return value

    def list_agents(self) -> List[Dict[str, Any]]:
        """
        List all registered agents

        Returns:
            List of agent capability descriptions
        """
        return [agent.get_capabilities() for agent in self.agents.values()]

    def list_workflows(self) -> List[str]:
        """
        List all registered workflows

        Returns:
            List of workflow names
        """
        return list(self.workflows.keys())

    def get_workflow_definition(self, workflow_name: str) -> Optional[Dict[str, Any]]:
        """
        Get workflow definition

        Args:
            workflow_name: Name of workflow

        Returns:
            Workflow definition or None
        """
        return self.workflows.get(workflow_name)

    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent workflow execution history

        Args:
            limit: Number of recent executions to return

        Returns:
            List of execution records
        """
        return self.execution_history[-limit:]

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get orchestrator statistics

        Returns:
            Dict with statistics
        """
        if not self.execution_history:
            return {
                "total_executions": 0,
                "avg_duration": 0,
                "success_rate": 0
            }

        total = len(self.execution_history)
        successful = sum(1 for e in self.execution_history if e.get("status") == "completed")
        durations = [e.get("duration", 0) for e in self.execution_history]

        return {
            "total_executions": total,
            "successful_executions": successful,
            "failed_executions": total - successful,
            "success_rate": (successful / total) if total > 0 else 0,
            "avg_duration": sum(durations) / len(durations) if durations else 0,
            "registered_agents": len(self.agents),
            "registered_workflows": len(self.workflows)
        }

    def __repr__(self):
        return f"<WorkflowOrchestrator agents={len(self.agents)} workflows={len(self.workflows)}>"
