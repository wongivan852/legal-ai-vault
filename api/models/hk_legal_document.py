"""
Database models for Hong Kong legal documents
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class HKLegalDocument(Base):
    """Model for HK legal documents (ordinances and subsidiary legislation)"""

    __tablename__ = "hk_legal_documents"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Document identification
    doc_number = Column(String(50), nullable=False, index=True)  # e.g., "109D", "Cap. 1"
    doc_name = Column(String(500), nullable=False)  # e.g., "Cap. 109 sub. leg. D"
    identifier = Column(String(200), unique=True, index=True)  # e.g., "/hk/cap109D!en"

    # Document categorization
    category = Column(String(50), nullable=False, index=True)  # 'ordinance' or 'subsidiary_legislation'
    doc_type = Column(String(100))  # e.g., "cap", "regulation"
    doc_status = Column(String(50), index=True)  # e.g., "In Force", "Repealed"

    # Metadata
    effective_date = Column(DateTime, index=True)  # When document came into effect
    language = Column(String(10), default='en', index=True)  # 'en', 'zh-Hans', 'zh-Hant'

    # Content
    title = Column(Text)  # Short title
    long_title = Column(Text)  # Full official title
    preamble = Column(Text)  # Preamble text
    full_text = Column(Text, nullable=False)  # Complete document text

    # Statistics
    total_sections = Column(Integer, default=0)  # Number of sections
    word_count = Column(Integer)  # Approximate word count

    # Vector embedding reference
    qdrant_id = Column(String(100), index=True)  # UUID in Qdrant vector database

    # Source and processing
    source_file = Column(String(500))  # Path to source XML file
    metadata_json = Column(JSON)  # Additional metadata as JSON

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    imported_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sections = relationship("HKLegalSection", back_populates="document", cascade="all, delete-orphan")

    # Indexes for common queries
    __table_args__ = (
        Index('idx_doc_category_status', 'category', 'doc_status'),
        Index('idx_effective_date', 'effective_date'),
        Index('idx_language_category', 'language', 'category'),
    )

    def __repr__(self):
        return f"<HKLegalDocument(doc_number='{self.doc_number}', doc_name='{self.doc_name}')>"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'doc_number': self.doc_number,
            'doc_name': self.doc_name,
            'identifier': self.identifier,
            'category': self.category,
            'doc_type': self.doc_type,
            'doc_status': self.doc_status,
            'effective_date': self.effective_date.isoformat() if self.effective_date else None,
            'language': self.language,
            'title': self.title,
            'long_title': self.long_title,
            'total_sections': self.total_sections,
            'word_count': self.word_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
