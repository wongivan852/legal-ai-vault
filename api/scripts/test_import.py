#!/usr/bin/env python3
"""
Test import of HK ordinances with fixed model
"""
import asyncio
import sys
import os
from pathlib import Path

sys.path.insert(0, '/app')

from database import get_db, init_db
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from services.ollama_service import OllamaService
from scripts.import_hk_ordinances import HKOrdinanceImporter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_import():
    """Test import with first 3 files"""
    init_db()
    db = next(get_db())

    qdrant = QdrantClient(host='qdrant', port=6333)

    # Create collections
    try:
        qdrant.create_collection(
            collection_name='hk_legal_documents',
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )
        logger.info("Created hk_legal_documents collection")
    except Exception as e:
        logger.info(f"Collection exists: {e}")

    try:
        qdrant.create_collection(
            collection_name='hk_legal_sections',
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )
        logger.info("Created hk_legal_sections collection")
    except Exception as e:
        logger.info(f"Collection exists: {e}")

    ollama = OllamaService()
    importer = HKOrdinanceImporter(db, qdrant, ollama)

    # Test with first 3 files
    import_dir = Path('/app/data/hkel_legal_import')
    test_files = []

    cap_dirs = sorted([d for d in import_dir.iterdir() if d.is_dir() and d.name.startswith('cap_')])[:3]

    for cap_dir in cap_dirs:
        for xml_file in cap_dir.glob('*.xml'):
            test_files.append(xml_file)
            break  # Only first XML from each dir

    logger.info(f"Testing with {len(test_files)} files")

    success_count = 0
    failed_count = 0

    for i, xml_file in enumerate(test_files, 1):
        logger.info(f"\n{'='*70}")
        logger.info(f"Test {i}/{len(test_files)}: {xml_file.name}")
        logger.info(f"{'='*70}")

        success = await importer.import_ordinance(xml_file)

        if success:
            success_count += 1
            logger.info("✓ SUCCESS")
        else:
            failed_count += 1
            logger.error("✗ FAILED")

    logger.info(f"\n{'='*70}")
    logger.info(f"Test Results: {success_count} succeeded, {failed_count} failed")
    logger.info(f"{'='*70}")

    db.close()

if __name__ == "__main__":
    asyncio.run(test_import())
