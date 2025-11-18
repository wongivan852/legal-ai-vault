"""
Hong Kong Legal Data API Endpoints
Provides access to HK legislation and instruments
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from database import get_db
from models.hk_legal_document import HKLegalDocument, HKLegalSection
from services.hk_legal_ingestion import HKLegalIngestionService
from security.auth import get_current_user
from models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/search")
async def search_legislation(
    query: str = Query(..., description="Search query"),
    language: str = Query("en", description="Language filter"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search Hong Kong legal documents using vector similarity

    This endpoint uses AI-powered semantic search to find relevant
    legislation based on natural language queries.
    """
    try:
        service = HKLegalIngestionService()
        results = await service.search_documents(
            query=query,
            language=language,
            limit=limit
        )

        return {
            "query": query,
            "language": language,
            "count": len(results),
            "results": results
        }

    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/documents")
async def list_documents(
    doc_type: Optional[str] = Query(None, description="Document type filter"),
    language: str = Query("en", description="Language filter"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List Hong Kong legal documents with filtering and pagination
    """
    try:
        query = db.query(HKLegalDocument)

        # Apply filters
        if doc_type:
            query = query.filter(HKLegalDocument.doc_type == doc_type)

        query = query.filter(HKLegalDocument.language == language)

        # Get total count
        total = query.count()

        # Apply pagination
        documents = query.offset(skip).limit(limit).all()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "documents": [doc.to_dict() for doc in documents]
        }

    except Exception as e:
        logger.error(f"List documents error: {e}")
        raise HTTPException(status_code=500, detail="Failed to list documents")


@router.get("/documents/{doc_id}")
async def get_document(
    doc_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get full details of a specific legal document
    """
    document = db.query(HKLegalDocument).filter(
        HKLegalDocument.id == doc_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        **document.to_dict(),
        "preamble": document.preamble,
        "structure": document.structure,
        "chapters": document.chapters
    }


@router.get("/documents/{doc_id}/full_text")
async def get_document_text(
    doc_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get full text content of a legal document
    """
    document = db.query(HKLegalDocument).filter(
        HKLegalDocument.id == doc_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "id": document.id,
        "doc_number": document.doc_number,
        "title": document.title,
        "full_text": document.full_text,
        "word_count": document.word_count
    }


@router.get("/documents/{doc_id}/sections")
async def get_document_sections(
    doc_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all sections of a legal document
    """
    # Verify document exists
    document = db.query(HKLegalDocument).filter(
        HKLegalDocument.id == doc_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Get sections
    sections = db.query(HKLegalSection).filter(
        HKLegalSection.document_id == doc_id
    ).all()

    return {
        "document_id": doc_id,
        "doc_number": document.doc_number,
        "total_sections": len(sections),
        "sections": [section.to_dict() for section in sections]
    }


@router.get("/sections/{section_id}")
async def get_section(
    section_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific section
    """
    section = db.query(HKLegalSection).filter(
        HKLegalSection.id == section_id
    ).first()

    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    return {
        **section.to_dict(),
        'subsections': section.subsections
    }


@router.get("/by_number/{doc_number}")
async def get_by_doc_number(
    doc_number: str,
    language: str = Query("en", description="Language"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get document by its official number (e.g., A101, Cap. 1)
    """
    document = db.query(HKLegalDocument).filter(
        HKLegalDocument.doc_number == doc_number,
        HKLegalDocument.language == language
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document {doc_number} not found in {language}"
        )

    return {
        **document.to_dict(),
        "preamble": document.preamble,
        "structure": document.structure,
        "chapters": document.chapters
    }


@router.get("/stats")
async def get_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get statistics about the HK legal document collection
    """
    try:
        total_docs = db.query(HKLegalDocument).count()
        total_sections = db.query(HKLegalSection).count()

        # Count by type
        instruments = db.query(HKLegalDocument).filter(
            HKLegalDocument.doc_type == 'instrument'
        ).count()

        ordinances = db.query(HKLegalDocument).filter(
            HKLegalDocument.doc_type == 'ordinance'
        ).count()

        # Count by language
        english = db.query(HKLegalDocument).filter(
            HKLegalDocument.language == 'en'
        ).count()

        trad_chinese = db.query(HKLegalDocument).filter(
            HKLegalDocument.language == 'zh-Hant'
        ).count()

        simp_chinese = db.query(HKLegalDocument).filter(
            HKLegalDocument.language == 'zh-Hans'
        ).count()

        # Vectorization status
        vectorized = db.query(HKLegalDocument).filter(
            HKLegalDocument.vectorized == True
        ).count()

        return {
            "total_documents": total_docs,
            "total_sections": total_sections,
            "by_type": {
                "instruments": instruments,
                "ordinances": ordinances
            },
            "by_language": {
                "english": english,
                "traditional_chinese": trad_chinese,
                "simplified_chinese": simp_chinese
            },
            "vectorization": {
                "vectorized": vectorized,
                "not_vectorized": total_docs - vectorized,
                "percentage": round((vectorized / total_docs * 100), 2) if total_docs > 0 else 0
            }
        }

    except Exception as e:
        logger.error(f"Statistics error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")
