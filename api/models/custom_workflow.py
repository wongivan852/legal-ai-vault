"""
Database model for custom user-created workflows
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Index
from datetime import datetime
from database import Base


class CustomWorkflow(Base):
    """Model for user-created multi-agent workflows"""

    __tablename__ = "custom_workflows"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Workflow identification
    workflow_id = Column(String(100), unique=True, nullable=False, index=True)  # e.g., "legal_compliance_check"
    name = Column(String(200), nullable=False)  # Display name: "Legal Compliance Check"
    description = Column(Text)  # Human-readable description

    # Workflow definition (stored as JSON)
    steps = Column(JSON, nullable=False)  # Array of step definitions
    # Example step structure:
    # {
    #     "name": "legal_research",
    #     "agent_name": "legal_research",
    #     "description": "Research legal requirements",
    #     "task_config": {
    #         "input_mappings": {
    #             "question": {"source": "input", "field": "compliance_question"}
    #         }
    #     }
    # }

    # Input schema (defines what fields the workflow expects)
    input_schema = Column(JSON)  # JSON schema for form validation
    # Example:
    # {
    #     "fields": [
    #         {"name": "compliance_question", "type": "text", "required": true, "label": "Compliance Question"},
    #         {"name": "policy_text", "type": "textarea", "required": false, "label": "Policy Text"}
    #     ]
    # }

    # Workflow metadata
    category = Column(String(50), index=True)  # e.g., "legal", "hr", "cs", "general"
    tags = Column(JSON)  # Array of tags: ["compliance", "legal", "hr"]
    is_active = Column(Boolean, default=True, index=True)  # Enable/disable workflow
    is_system = Column(Boolean, default=False, index=True)  # True for pre-built workflows

    # Usage statistics
    execution_count = Column(Integer, default=0)  # Number of times executed
    last_executed = Column(DateTime)  # Last execution timestamp

    # Creator information
    created_by = Column(String(100))  # User ID or username

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Indexes for common queries
    __table_args__ = (
        Index('idx_active_category', 'is_active', 'category'),
        Index('idx_created_at', 'created_at'),
    )

    def __repr__(self):
        return f"<CustomWorkflow(workflow_id='{self.workflow_id}', name='{self.name}')>"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'name': self.name,
            'description': self.description,
            'steps': self.steps,
            'input_schema': self.input_schema,
            'category': self.category,
            'tags': self.tags,
            'is_active': self.is_active,
            'is_system': self.is_system,
            'execution_count': self.execution_count,
            'last_executed': self.last_executed.isoformat() if self.last_executed else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def to_workflow_summary(self):
        """Convert to summary format for workflow listings"""
        return {
            'id': self.workflow_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'tags': self.tags,
            'step_count': len(self.steps) if self.steps else 0,
            'is_system': self.is_system,
            'execution_count': self.execution_count,
            'last_executed': self.last_executed.isoformat() if self.last_executed else None
        }
