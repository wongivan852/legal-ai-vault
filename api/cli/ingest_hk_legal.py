#!/usr/bin/env python3
"""
CLI tool for ingesting HK legal documents
Usage: python cli/ingest_hk_legal.py [--limit N] [--directory PATH]
"""

import sys
import os
import asyncio
import argparse
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, init_db
from services.hk_legal_ingestion import HKLegalIngestionService
from services.ollama_service import OllamaService
from qdrant_client import QdrantClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main ingestion function"""
    parser = argparse.ArgumentParser(description='Ingest HK legal documents')
    parser.add_argument(
        '--directory',
        default='/app/data/hkel_data',
        help='Directory containing XML files (default: /app/data/hkel_data)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of files to process (default: all)'
    )
    parser.add_argument(
        '--stats-only',
        action='store_true',
        help='Only show statistics, do not ingest'
    )

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("HK Legal Document Ingestion")
    logger.info("=" * 60)

    # Initialize database
    logger.info("Initializing database...")
    init_db()

    # Create clients
    db = SessionLocal()
    qdrant = QdrantClient(
        host=os.getenv("QDRANT_HOST", "qdrant"),
        port=int(os.getenv("QDRANT_PORT", 6333))
    )
    ollama = OllamaService()

    # Create ingestion service
    ingestion_service = HKLegalIngestionService(db, qdrant, ollama)

    # Show current stats
    stats = ingestion_service.get_stats()
    logger.info("\nCurrent Database Status:")
    logger.info(f"  Documents in PostgreSQL: {stats['documents']}")
    logger.info(f"  Sections in PostgreSQL: {stats['sections']}")
    logger.info(f"  Vectors in Qdrant (documents): {stats['qdrant_documents']}")
    logger.info(f"  Vectors in Qdrant (sections): {stats['qdrant_sections']}")

    if args.stats_only:
        logger.info("\nStats-only mode. Exiting.")
        return

    # Check if directory exists
    if not os.path.exists(args.directory):
        logger.error(f"Directory not found: {args.directory}")
        return

    # Run ingestion
    logger.info(f"\nStarting ingestion from: {args.directory}")
    if args.limit:
        logger.info(f"Limiting to {args.limit} files")

    result = await ingestion_service.ingest_directory(
        args.directory,
        limit=args.limit
    )

    # Show results
    logger.info("\n" + "=" * 60)
    logger.info("Ingestion Results:")
    logger.info("=" * 60)
    logger.info(f"Total files processed: {result['total_files']}")
    logger.info(f"Successful: {result['successful']}")
    logger.info(f"Skipped (already exists): {result['skipped']}")
    logger.info(f"Failed: {result['failed']}")

    if result['errors']:
        logger.info("\nErrors:")
        for error in result['errors'][:10]:  # Show first 10 errors
            logger.error(f"  {error['file']}: {error['error']}")
        if len(result['errors']) > 10:
            logger.info(f"  ... and {len(result['errors']) - 10} more errors")

    # Final stats
    final_stats = ingestion_service.get_stats()
    logger.info("\nFinal Database Status:")
    logger.info(f"  Documents in PostgreSQL: {final_stats['documents']}")
    logger.info(f"  Sections in PostgreSQL: {final_stats['sections']}")
    logger.info(f"  Vectors in Qdrant (documents): {final_stats['qdrant_documents']}")
    logger.info(f"  Vectors in Qdrant (sections): {final_stats['qdrant_sections']}")

    logger.info("\n✓ Ingestion complete!")

    db.close()


if __name__ == "__main__":
    asyncio.run(main())
