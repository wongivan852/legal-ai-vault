"""
Agent API Routes
REST endpoints for agent execution and workflow orchestration
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import logging

from agents import (
    LegalResearchAgent,
    HRPolicyAgent,
    CSDocumentAgent,
    AnalysisAgent,
    SynthesisAgent,
    ValidationAgent,
    WorkflowOrchestrator
)
from agents.synthesis_agent_enhanced import EnhancedSynthesisAgent
from services.ollama_service import OllamaService
from services.rag_service import RAGService
from database import get_db
from qdrant_client import QdrantClient
from workflows import (
    register_reference_workflows,
    get_workflow_examples,
    get_workflow_descriptions
)
from sqlalchemy.orm import Session
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/agents", tags=["agents"])


# ============================================================================
# Request/Response Models
# ============================================================================

class AgentExecuteRequest(BaseModel):
    """Request model for agent execution"""
    task: Dict[str, Any] = Field(..., description="Task specification for the agent")


class AgentExecuteResponse(BaseModel):
    """Response model for agent execution"""
    agent: str
    status: str
    result: Dict[str, Any]
    execution_time: float


class WorkflowExecuteRequest(BaseModel):
    """Request model for workflow execution"""
    input_data: Dict[str, Any] = Field(..., description="Input data for the workflow")


class WorkflowExecuteResponse(BaseModel):
    """Response model for workflow execution"""
    workflow: str
    status: str
    results: Dict[str, Any]
    output: Any
    execution_time: float


class AgentInfo(BaseModel):
    """Information about an agent"""
    name: str
    description: str
    tools: List[Dict[str, str]]
    domain: str


class WorkflowInfo(BaseModel):
    """Information about a workflow"""
    name: str
    description: str
    tasks: List[Dict[str, Any]]


# ============================================================================
# Agent Management
# ============================================================================

# Global agent registry
_agent_registry = {}
_orchestrator = None


def get_agent_registry():
    """Get or initialize agent registry"""
    global _agent_registry, _orchestrator

    if not _agent_registry:
        # Initialize services
        ollama = OllamaService()

        # Initialize agents
        _agent_registry = {
            "legal_research": {
                "agent": None,  # Initialized on demand (needs DB)
                "class": LegalResearchAgent,
                "domain": "legal",
                "requires_db": True
            },
            "hr_policy": {
                "agent": HRPolicyAgent(ollama),
                "class": HRPolicyAgent,
                "domain": "hr"
            },
            "cs_document": {
                "agent": CSDocumentAgent(ollama),
                "class": CSDocumentAgent,
                "domain": "customer_service"
            },
            "analysis": {
                "agent": AnalysisAgent(ollama),
                "class": AnalysisAgent,
                "domain": "general"
            },
            "synthesis": {
                "agent": None,  # Initialized on demand (needs RAG for enhanced mode)
                "class": EnhancedSynthesisAgent,
                "domain": "general",
                "requires_rag": True
            },
            "validation": {
                "agent": ValidationAgent(ollama),
                "class": ValidationAgent,
                "domain": "general"
            }
        }

        # Initialize orchestrator
        _orchestrator = WorkflowOrchestrator()
        for agent_name, agent_info in _agent_registry.items():
            if agent_info["agent"]:
                _orchestrator.register_agent(agent_info["agent"])

        # Register reference workflows
        try:
            register_reference_workflows(_orchestrator)
            logger.info("Reference workflows registered successfully")
        except Exception as e:
            logger.error(f"Failed to register reference workflows: {e}", exc_info=True)

    return _agent_registry, _orchestrator


def get_agent(agent_name: str, db: Session = None):
    """Get agent instance by name"""
    registry, _ = get_agent_registry()

    if agent_name not in registry:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    agent_info = registry[agent_name]

    # Special handling for legal research agent (needs DB)
    if agent_name == "legal_research":
        if not agent_info["agent"] and db:
            ollama = OllamaService()
            qdrant_host = os.getenv("QDRANT_HOST", "localhost")
            qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
            qdrant = QdrantClient(host=qdrant_host, port=qdrant_port)
            rag = RAGService(db, qdrant, ollama)
            agent_info["agent"] = LegalResearchAgent(ollama, rag)

            # Register with orchestrator
            _, orchestrator = get_agent_registry()
            orchestrator.register_agent(agent_info["agent"])

        if not agent_info["agent"]:
            raise HTTPException(
                status_code=503,
                detail="Legal research agent requires database connection"
            )

    # Special handling for synthesis agent (needs RAG for enhanced features)
    if agent_name == "synthesis":
        if not agent_info["agent"] and db:
            ollama = OllamaService()
            qdrant_host = os.getenv("QDRANT_HOST", "localhost")
            qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
            qdrant = QdrantClient(host=qdrant_host, port=qdrant_port)
            rag = RAGService(db, qdrant, ollama)
            agent_info["agent"] = EnhancedSynthesisAgent(ollama, rag)

            # Register with orchestrator
            _, orchestrator = get_agent_registry()
            orchestrator.register_agent(agent_info["agent"])

            logger.info("Enhanced Synthesis Agent initialized with RAG capability")

        if not agent_info["agent"]:
            raise HTTPException(
                status_code=503,
                detail="Synthesis agent requires database connection for enhanced features"
            )

    return agent_info["agent"]


# ============================================================================
# API Endpoints
# ============================================================================

@router.get("/", response_model=List[AgentInfo])
async def list_agents():
    """
    List all available agents

    Returns information about all registered agents including their
    capabilities, tools, and domain specialization.
    """
    registry, _ = get_agent_registry()

    agents_info = []
    for agent_name, agent_info in registry.items():
        agent = agent_info["agent"]

        # Get agent capabilities
        if agent:
            caps = agent.get_capabilities()
            agents_info.append(AgentInfo(
                name=caps["name"],
                description=caps["description"],
                tools=caps["tools"],
                domain=agent_info["domain"]
            ))
        else:
            # Agent not yet initialized
            agents_info.append(AgentInfo(
                name=agent_name,
                description=f"{agent_info['domain'].title()} domain agent",
                tools=[],
                domain=agent_info["domain"]
            ))

    return agents_info


@router.post("/{agent_name}/execute", response_model=AgentExecuteResponse)
async def execute_agent(
    agent_name: str,
    request: AgentExecuteRequest,
    db: Session = Depends(get_db)
):
    """
    Execute a specific agent

    Args:
        agent_name: Name of the agent to execute
        request: Task specification for the agent
        db: Database session

    Returns:
        Agent execution results

    Example:
        POST /api/agents/hr_policy/execute
        {
            "task": {
                "question": "What is the vacation policy?",
                "task_type": "policy_search"
            }
        }
    """
    try:
        agent = get_agent(agent_name, db)

        logger.info(f"Executing agent: {agent_name}")
        result = await agent.execute(request.task)

        return AgentExecuteResponse(
            agent=agent_name,
            status=result.get("status", "unknown"),
            result=result,
            execution_time=result.get("execution_time", 0)
        )

    except Exception as e:
        logger.error(f"Agent execution error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{agent_name}/info", response_model=AgentInfo)
async def get_agent_info(agent_name: str, db: Session = Depends(get_db)):
    """
    Get information about a specific agent

    Args:
        agent_name: Name of the agent

    Returns:
        Agent capabilities and information
    """
    try:
        agent = get_agent(agent_name, db)
        registry, _ = get_agent_registry()

        caps = agent.get_capabilities()

        return AgentInfo(
            name=caps["name"],
            description=caps["description"],
            tools=caps["tools"],
            domain=registry[agent_name]["domain"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting agent info: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Workflow Endpoints
# ============================================================================

@router.get("/workflows", response_model=List[str])
async def list_workflows():
    """
    List all registered workflows

    Returns:
        List of workflow names
    """
    _, orchestrator = get_agent_registry()
    return orchestrator.list_workflows()


@router.post("/workflows/{workflow_name}/execute", response_model=WorkflowExecuteResponse)
async def execute_workflow(
    workflow_name: str,
    request: WorkflowExecuteRequest,
    db: Session = Depends(get_db)
):
    """
    Execute a workflow

    Args:
        workflow_name: Name of the workflow to execute
        request: Input data for the workflow
        db: Database session

    Returns:
        Workflow execution results

    Example:
        POST /api/agents/workflows/hr_onboarding/execute
        {
            "input_data": {
                "employee_name": "John Doe",
                "position": "Software Engineer"
            }
        }
    """
    try:
        # Ensure legal agent is initialized if needed
        get_agent("legal_research", db)

        _, orchestrator = get_agent_registry()

        logger.info(f"Executing workflow: {workflow_name}")
        result = await orchestrator.execute_workflow(workflow_name, request.input_data)

        return WorkflowExecuteResponse(
            workflow=workflow_name,
            status=result.get("status", "unknown"),
            results=result.get("results", {}),
            output=result.get("output"),
            execution_time=result.get("execution_time", 0)
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Workflow execution error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflows/{workflow_name}", response_model=WorkflowInfo)
async def get_workflow_info(workflow_name: str):
    """
    Get information about a specific workflow

    Args:
        workflow_name: Name of the workflow

    Returns:
        Workflow definition and information
    """
    _, orchestrator = get_agent_registry()

    workflow_def = orchestrator.get_workflow_definition(workflow_name)
    if not workflow_def:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_name}' not found")

    return WorkflowInfo(
        name=workflow_name,
        description=workflow_def.get("description", ""),
        tasks=workflow_def.get("tasks", [])
    )


@router.get("/workflows/{workflow_name}/example")
async def get_workflow_example(workflow_name: str):
    """
    Get example input data for a workflow

    Args:
        workflow_name: Name of the workflow

    Returns:
        Example input data and description

    Example:
        GET /api/agents/workflows/hr_onboarding/example
        Returns example input data that can be used to test the workflow
    """
    examples = get_workflow_examples()
    descriptions = get_workflow_descriptions()

    if workflow_name not in examples:
        raise HTTPException(
            status_code=404,
            detail=f"No example available for workflow '{workflow_name}'"
        )

    return {
        "workflow": workflow_name,
        "description": descriptions.get(workflow_name, ""),
        "example_input": examples[workflow_name],
        "usage": f"POST /api/agents/workflows/{workflow_name}/execute with this data"
    }


@router.get("/workflows/examples/all")
async def get_all_workflow_examples():
    """
    Get example input data for all workflows

    Returns:
        Dict mapping workflow names to example inputs and descriptions
    """
    examples = get_workflow_examples()
    descriptions = get_workflow_descriptions()

    return {
        "workflows": {
            name: {
                "description": descriptions.get(name, ""),
                "example_input": example,
                "endpoint": f"/api/agents/workflows/{name}/execute"
            }
            for name, example in examples.items()
        },
        "total": len(examples)
    }


@router.get("/stats")
async def get_orchestrator_stats():
    """
    Get orchestrator statistics

    Returns:
        Execution statistics and metrics
    """
    _, orchestrator = get_agent_registry()
    return orchestrator.get_statistics()


# ============================================================================
# Health Check
# ============================================================================

@router.get("/health")
async def health_check():
    """
    Check agent system health

    Returns:
        Health status of all agents and orchestrator
    """
    try:
        registry, orchestrator = get_agent_registry()

        agent_status = {}
        for agent_name, agent_info in registry.items():
            if agent_info["agent"]:
                agent_status[agent_name] = "ready"
            else:
                agent_status[agent_name] = "not_initialized"

        return {
            "status": "healthy",
            "agents": agent_status,
            "orchestrator": "ready",
            "total_agents": len(registry),
            "workflows_registered": len(orchestrator.list_workflows())
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
