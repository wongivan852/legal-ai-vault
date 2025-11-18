"""
Service for ingesting HK legal documents into database and vector store
"""

import logging
import uuid
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from parsers.hk_legal_xml_parser import HKLegalXMLParser
from models.hk_legal_document import HKLegalDocument
from models.hk_legal_section import HKLegalSection
from services.ollama_service import OllamaService

logger = logging.getLogger(__name__)


def clean_metadata_for_json(metadata: Dict) -> Dict:
    """Convert datetime objects to ISO strings for JSON serialization"""
    cleaned = {}
    for key, value in metadata.items():
        if isinstance(value, datetime):
            cleaned[key] = value.isoformat()
        else:
            cleaned[key] = value
    return cleaned


class HKLegalIngestionService:
    """Service for ingesting HK legal documents"""

    COLLECTION_DOCUMENTS = "hk_legal_documents"
    COLLECTION_SECTIONS = "hk_legal_sections"
    VECTOR_SIZE = 768  # nomic-embed-text dimension

    def __init__(
        self,
        db_session: Session,
        qdrant_client: QdrantClient,
        ollama_service: OllamaService
    ):
        self.db = db_session
        self.qdrant = qdrant_client
        self.ollama = ollama_service
        self.parser = HKLegalXMLParser()

        # Initialize Qdrant collections
        self._init_collections()

    def _init_collections(self):
        """Create Qdrant collections if they don't exist"""
        try:
            # Check if collections exist
            collections = self.qdrant.get_collections().collections
            collection_names = [c.name for c in collections]

            # Create documents collection
            if self.COLLECTION_DOCUMENTS not in collection_names:
                self.qdrant.create_collection(
                    collection_name=self.COLLECTION_DOCUMENTS,
                    vectors_config=VectorParams(
                        size=self.VECTOR_SIZE,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created Qdrant collection: {self.COLLECTION_DOCUMENTS}")

            # Create sections collection
            if self.COLLECTION_SECTIONS not in collection_names:
                self.qdrant.create_collection(
                    collection_name=self.COLLECTION_SECTIONS,
                    vectors_config=VectorParams(
                        size=self.VECTOR_SIZE,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created Qdrant collection: {self.COLLECTION_SECTIONS}")

        except Exception as e:
            logger.error(f"Failed to initialize Qdrant collections: {e}")
            raise

    async def ingest_xml_file(self, xml_path: str) -> Optional[HKLegalDocument]:
        """
        Ingest a single XML file

        Args:
            xml_path: Path to XML file

        Returns:
            HKLegalDocument instance if successful, None otherwise
        """
        try:
            # Parse XML
            doc_data = self.parser.parse_file(xml_path)
            if not doc_data:
                logger.warning(f"Failed to parse {xml_path}")
                return None

            # Check if document already exists
            existing = self.db.query(HKLegalDocument).filter(
                HKLegalDocument.identifier == doc_data['identifier']
            ).first()

            if existing:
                logger.info(f"Document already exists: {doc_data['identifier']}")
                return existing

            # Create document record
            document = HKLegalDocument(
                doc_number=doc_data['doc_number'],
                doc_name=doc_data['doc_name'],
                identifier=doc_data['identifier'],
                category=doc_data['category'],
                doc_type=doc_data['doc_type'],
                doc_status=doc_data['doc_status'],
                effective_date=doc_data['effective_date'],
                language=doc_data['language'],
                title=doc_data['title'],
                long_title=doc_data['long_title'],
                preamble=doc_data['preamble'],
                full_text=doc_data['full_text'],
                total_sections=doc_data['total_sections'],
                word_count=len(doc_data['full_text'].split()) if doc_data['full_text'] else 0,
                source_file=xml_path,
                metadata_json=clean_metadata_for_json(doc_data['metadata'])
            )

            # Add to database
            self.db.add(document)
            self.db.flush()  # Get the ID

            # Generate and store embedding for full document
            if doc_data['full_text']:
                embedding_text = f"{doc_data['title']} {doc_data['long_title']} {doc_data['full_text'][:5000]}"
                doc_embedding = await self.ollama.embed(embedding_text)

                # Store in Qdrant
                qdrant_id = str(uuid.uuid4())
                self.qdrant.upsert(
                    collection_name=self.COLLECTION_DOCUMENTS,
                    points=[
                        PointStruct(
                            id=qdrant_id,
                            vector=doc_embedding,
                            payload={
                                "db_id": document.id,
                                "doc_number": document.doc_number,
                                "doc_name": document.doc_name,
                                "title": document.title,
                                "category": document.category,
                                "doc_status": document.doc_status,
                                "language": document.language
                            }
                        )
                    ]
                )
                document.qdrant_id = qdrant_id

            # Process sections
            for section_data in doc_data['sections']:
                section = HKLegalSection(
                    document_id=document.id,
                    section_id=section_data['section_id'],
                    section_name=section_data['section_name'],
                    section_number=section_data['section_number'],
                    heading=section_data['heading'],
                    content=section_data['content'],
                    has_subsections=1 if section_data['has_subsections'] else 0,
                    subsections_json=section_data['subsections']
                )

                self.db.add(section)
                self.db.flush()

                # Generate embedding for section
                if section_data['content']:
                    section_text = f"{section_data['heading']} {section_data['content']}"
                    section_embedding = await self.ollama.embed(section_text)

                    # Store in Qdrant
                    section_qdrant_id = str(uuid.uuid4())
                    self.qdrant.upsert(
                        collection_name=self.COLLECTION_SECTIONS,
                        points=[
                            PointStruct(
                                id=section_qdrant_id,
                                vector=section_embedding,
                                payload={
                                    "db_id": section.id,
                                    "document_id": document.id,
                                    "doc_number": document.doc_number,
                                    "section_number": section.section_number,
                                    "heading": section.heading,
                                    "content": section.content[:500]  # Preview
                                }
                            )
                        ]
                    )
                    section.qdrant_id = section_qdrant_id

            # Commit transaction
            self.db.commit()
            logger.info(f"Ingested document: {doc_data['doc_name']} with {len(doc_data['sections'])} sections")

            return document

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to ingest {xml_path}: {e}", exc_info=True)
            return None

    async def ingest_directory(self, directory: str, limit: Optional[int] = None) -> Dict:
        """
        Ingest all XML files in a directory

        Args:
            directory: Path to directory containing XML files
            limit: Optional limit on number of files to process

        Returns:
            Dict with statistics
        """
        from pathlib import Path

        xml_files = list(Path(directory).rglob('*.xml'))
        total_files = len(xml_files)

        if limit:
            xml_files = xml_files[:limit]
            logger.info(f"Processing {limit} of {total_files} files (limit applied)")
        else:
            logger.info(f"Processing all {total_files} files")

        stats = {
            'total_files': len(xml_files),
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'documents': [],
            'errors': []
        }

        for i, xml_file in enumerate(xml_files, 1):
            if i % 50 == 0:
                logger.info(f"Progress: {i}/{len(xml_files)} files processed")

            try:
                document = await self.ingest_xml_file(str(xml_file))
                if document:
                    stats['successful'] += 1
                    stats['documents'].append(document.identifier)
                else:
                    stats['skipped'] += 1

            except Exception as e:
                stats['failed'] += 1
                stats['errors'].append({
                    'file': str(xml_file),
                    'error': str(e)
                })
                logger.error(f"Error processing {xml_file}: {e}")

        logger.info(f"Ingestion complete: {stats['successful']} successful, "
                   f"{stats['failed']} failed, {stats['skipped']} skipped")

        return stats

    def get_document_count(self) -> int:
        """Get total number of documents in database"""
        return self.db.query(HKLegalDocument).count()

    def get_section_count(self) -> int:
        """Get total number of sections in database"""
        return self.db.query(HKLegalSection).count()

    def get_stats(self) -> Dict:
        """Get ingestion statistics"""
        return {
            'documents': self.get_document_count(),
            'sections': self.get_section_count(),
            'qdrant_documents': self.qdrant.count(self.COLLECTION_DOCUMENTS).count,
            'qdrant_sections': self.qdrant.count(self.COLLECTION_SECTIONS).count
        }
