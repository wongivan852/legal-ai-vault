"""
Agentic AI Framework
Base classes and specialized agents for workflow automation
Multi-domain support: Legal, HR, Customer Service, and more
"""

from agents.base_agent import BaseAgent
from agents.legal_agent import LegalResearchAgent
from agents.hr_policy_agent import HRPolicyAgent
from agents.cs_document_agent import CSDocumentAgent
from agents.analysis_agent import AnalysisAgent
from agents.synthesis_agent import SynthesisAgent
from agents.validation_agent import ValidationAgent
from agents.orchestrator import WorkflowOrchestrator

__all__ = [
    "BaseAgent",
    "LegalResearchAgent",
    "HRPolicyAgent",
    "CSDocumentAgent",
    "AnalysisAgent",
    "SynthesisAgent",
    "ValidationAgent",
    "WorkflowOrchestrator"
]
