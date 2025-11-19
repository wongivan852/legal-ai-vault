"""
Database model for sections within HK legal documents
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index, JSON, event
from sqlalchemy.orm import relationship, validates
from database import Base


class HKLegalSection(Base):
    """Model for sections within HK legal documents"""

    __tablename__ = "hk_legal_sections"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to parent document
    document_id = Column(Integer, ForeignKey('hk_legal_documents.id', ondelete='CASCADE'), nullable=False, index=True)

    # Section identification
    section_id = Column(String(100), index=True)  # XML ID attribute
    section_name = Column(String(100))  # Name attribute (e.g., "s1", "s2")
    section_number = Column(String(50))  # Display number (e.g., "1", "2A")

    # Content
    heading = Column(Text)  # Section heading/title
    content = Column(Text, nullable=False)  # Full section text

    # Hierarchy
    has_subsections = Column(Integer, default=0)  # Boolean flag stored as Integer (0 or 1)
    subsections_json = Column(JSON)  # Array of subsection data

    # Vector embedding reference
    qdrant_id = Column(String(100), index=True)  # UUID in Qdrant for this section

    # Relationship
    document = relationship("HKLegalDocument", back_populates="sections")

    @validates('has_subsections')
    def validate_has_subsections(self, key, value):
        """Convert boolean to integer for has_subsections field"""
        if isinstance(value, bool):
            return 1 if value else 0
        return int(value) if value is not None else 0

    # Indexes
    __table_args__ = (
        Index('idx_document_section', 'document_id', 'section_number'),
    )

    def __repr__(self):
        return f"<HKLegalSection(document_id={self.document_id}, section_number='{self.section_number}')>"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'document_id': self.document_id,
            'section_id': self.section_id,
            'section_name': self.section_name,
            'section_number': self.section_number,
            'heading': self.heading,
            'content': self.content,
            'has_subsections': bool(self.has_subsections),
            'subsections': self.subsections_json
        }
