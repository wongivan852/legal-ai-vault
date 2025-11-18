#!/usr/bin/env python3
"""
Import Hong Kong Legal Ordinances from XML files
Parses XML files and imports into PostgreSQL + Qdrant vector database
"""

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import logging
from typing import Dict, List, Optional
import asyncio

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from database import get_db, init_db
from models.hk_legal_document import HKLegalDocument
from models.hk_legal_section import HKLegalSection
from services.ollama_service import OllamaService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HKOrdinanceImporter:
    """Importer for Hong Kong legal ordinances from XML"""

    def __init__(self, db: Session, qdrant: QdrantClient, ollama: OllamaService):
        self.db = db
        self.qdrant = qdrant
        self.ollama = ollama
        self.namespace = "{http://www.xml.gov.hk/schemas/hklm/1.0}"

    def parse_xml_file(self, xml_path: Path) -> Optional[Dict]:
        """Parse XML file and extract ordinance data"""
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Extract metadata
            meta = root.find(f"{self.namespace}meta")
            if meta is None:
                logger.warning(f"No metadata found in {xml_path}")
                return None

            doc_name_elem = meta.find(f"{self.namespace}docName")
            doc_number_elem = meta.find(f"{self.namespace}docNumber")

            if doc_name_elem is None or doc_number_elem is None:
                logger.warning(f"Missing required metadata in {xml_path}")
                return None

            doc_name = doc_name_elem.text
            doc_number = doc_number_elem.text

            # Extract title from longTitle
            main = root.find(f"{self.namespace}main")
            title = ""
            if main is not None:
                long_title = main.find(f"{self.namespace}longTitle")
                if long_title is not None:
                    title = ET.tostring(long_title, encoding='unicode', method='text').strip()

            # Extract sections
            sections = []
            if main is not None:
                for section in main.findall(f"{self.namespace}section"):
                    section_num = section.find(f"{self.namespace}num")
                    if section_num is not None:
                        section_number = section_num.get('value', section_num.text or '')

                        # Extract section heading
                        heading_elem = section.find(f"{self.namespace}heading")
                        heading = heading_elem.text if heading_elem is not None else ""

                        # Extract section content (all text)
                        content = ET.tostring(section, encoding='unicode', method='text').strip()

                        if content:  # Only add if there's actual content
                            sections.append({
                                'section_number': section_number,
                                'heading': heading,
                                'content': content
                            })

            return {
                'doc_name': doc_name,
                'doc_number': doc_number,
                'title': title,
                'sections': sections,
                'full_text': ET.tostring(root, encoding='unicode', method='text').strip()
            }

        except Exception as e:
            logger.error(f"Error parsing {xml_path}: {e}")
            return None

    async def import_ordinance(self, xml_path: Path, batch_embeddings: bool = True) -> bool:
        """Import a single ordinance"""
        try:
            data = self.parse_xml_file(xml_path)
            if not data:
                return False

            # Check if document already exists
            existing = self.db.query(HKLegalDocument).filter(
                HKLegalDocument.doc_number == data['doc_number']
            ).first()

            if existing:
                logger.info(f"Document {data['doc_name']} already exists, skipping")
                return False

            # Determine category based on doc_name
            category = "subsidiary_legislation" if "sub. leg." in data['doc_name'] else "ordinance"

            # Create document
            document = HKLegalDocument(
                doc_name=data['doc_name'],
                doc_number=data['doc_number'],
                category=category,
                doc_type="cap",
                doc_status="active",
                language="en",
                title=data['title'][:500] if data['title'] else "",  # Limit title length
                full_text=data['full_text']
            )

            self.db.add(document)
            self.db.flush()  # Get document ID

            # Generate document embedding
            logger.info(f"Generating embedding for document {data['doc_name']}")
            doc_embedding = await self.ollama.embed(
                f"{data['doc_name']}: {data['title'][:200]}"
            )

            # Store document in Qdrant
            self.qdrant.upsert(
                collection_name="hk_legal_documents",
                points=[PointStruct(
                    id=document.id,
                    vector=doc_embedding,
                    payload={
                        "db_id": document.id,
                        "doc_number": data['doc_number'],
                        "doc_name": data['doc_name']
                    }
                )]
            )

            # Import sections
            section_count = 0
            for section_data in data['sections']:
                section = HKLegalSection(
                    document_id=document.id,
                    section_number=section_data['section_number'],
                    heading=section_data['heading'][:200] if section_data['heading'] else "",
                    content=section_data['content']
                )

                self.db.add(section)
                self.db.flush()  # Get section ID

                # Generate section embedding
                section_text = f"Section {section_data['section_number']}: {section_data['heading']} {section_data['content'][:500]}"
                section_embedding = await self.ollama.embed(section_text)

                # Store section in Qdrant
                self.qdrant.upsert(
                    collection_name="hk_legal_sections",
                    points=[PointStruct(
                        id=section.id,
                        vector=section_embedding,
                        payload={
                            "db_id": section.id,
                            "section_number": section_data['section_number'],
                            "doc_id": document.id
                        }
                    )]
                )

                section_count += 1

            self.db.commit()
            logger.info(f"✓ Imported {data['doc_name']} with {section_count} sections")
            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error importing {xml_path}: {e}", exc_info=True)
            return False


async def main():
    """Main import function"""
    import_dir = Path("/app/data/hkel_legal_import")

    if not import_dir.exists():
        logger.error(f"Import directory not found: {import_dir}")
        return

    # Initialize database
    init_db()

    # Get database session
    db = next(get_db())

    # Initialize Qdrant
    qdrant = QdrantClient(
        host=os.getenv("QDRANT_HOST", "localhost"),
        port=int(os.getenv("QDRANT_PORT", "6333"))
    )

    # Ensure collections exist
    try:
        qdrant.get_collection("hk_legal_documents")
    except:
        logger.info("Creating hk_legal_documents collection")
        qdrant.create_collection(
            collection_name="hk_legal_documents",
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )

    try:
        qdrant.get_collection("hk_legal_sections")
    except:
        logger.info("Creating hk_legal_sections collection")
        qdrant.create_collection(
            collection_name="hk_legal_sections",
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )

    # Initialize Ollama
    ollama = OllamaService()

    # Create importer
    importer = HKOrdinanceImporter(db, qdrant, ollama)

    # Find all XML files
    xml_files = []
    for cap_dir in sorted(import_dir.iterdir()):
        if cap_dir.is_dir() and cap_dir.name.startswith("cap_"):
            for xml_file in cap_dir.glob("*.xml"):
                xml_files.append(xml_file)

    logger.info(f"Found {len(xml_files)} XML files to import")

    # Import ordinances
    imported_count = 0
    failed_count = 0

    for i, xml_file in enumerate(xml_files, 1):
        logger.info(f"Processing {i}/{len(xml_files)}: {xml_file.name}")

        success = await importer.import_ordinance(xml_file)
        if success:
            imported_count += 1
        else:
            failed_count += 1

        # Log progress every 50 files
        if i % 50 == 0:
            logger.info(f"Progress: {i}/{len(xml_files)} - Imported: {imported_count}, Failed: {failed_count}")

    logger.info(f"Import complete! Imported: {imported_count}, Failed: {failed_count}")
    db.close()


if __name__ == "__main__":
    asyncio.run(main())
