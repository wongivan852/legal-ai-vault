"""
Database models for Legal AI Vault
"""

from .hk_legal_document import HKLegalDocument
from .hk_legal_section import HKLegalSection
from .custom_workflow import CustomWorkflow

__all__ = [
    'HKLegalDocument',
    'HKLegalSection',
    'CustomWorkflow'
]
