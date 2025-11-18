"""
Workflows Package
Pre-built multi-agent workflows and workflow utilities
"""

from workflows.reference_workflows import (
    register_reference_workflows,
    get_workflow_examples,
    get_workflow_descriptions
)

__all__ = [
    "register_reference_workflows",
    "get_workflow_examples",
    "get_workflow_descriptions"
]
