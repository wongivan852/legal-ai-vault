#!/usr/bin/env python3
"""
Hong Kong Legal Data Ingestion Script
Imports HK legislation XML files into the Legal AI Vault
"""

import sys
import os
import asyncio
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from services.hk_legal_ingestion import HKLegalIngestionService
from database import engine, Base

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'hk_legal_ingestion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


async def main():
    """Main ingestion function"""

    parser = argparse.ArgumentParser(description='Ingest Hong Kong Legal Data')
    parser.add_argument(
        'data_path',
        help='Path to directory containing HK legal XML files'
    )
    parser.add_argument(
        '--init-db',
        action='store_true',
        help='Initialize database tables before ingestion'
    )
    parser.add_argument(
        '--language',
        choices=['en', 'zh-Hant', 'zh-Hans', 'all'],
        default='all',
        help='Filter by language (default: all)'
    )

    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("Hong Kong Legal Data Ingestion")
    logger.info("=" * 80)

    # Validate data path
    if not os.path.exists(args.data_path):
        logger.error(f"Data path does not exist: {args.data_path}")
        return 1

    # Initialize database if requested
    if args.init_db:
        logger.info("Initializing database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized")

    # Initialize ingestion service
    logger.info("Initializing ingestion service...")
    service = HKLegalIngestionService()

    # Start ingestion
    start_time = datetime.now()
    logger.info(f"Starting ingestion from: {args.data_path}")
    logger.info(f"Language filter: {args.language}")

    stats = await service.ingest_directory(args.data_path)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Print summary
    logger.info("=" * 80)
    logger.info("INGESTION SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total files found:      {stats['total_files']}")
    logger.info(f"Successfully processed: {stats['processed']}")
    logger.info(f"Failed:                 {stats['failed']}")
    logger.info(f"Skipped (duplicates):   {stats['skipped']}")
    logger.info(f"Documents created:      {stats['documents_created']}")
    logger.info(f"Sections created:       {stats['sections_created']}")
    logger.info(f"Vectors created:        {stats['vectors_created']}")
    logger.info(f"Duration:               {duration:.2f} seconds")
    logger.info("=" * 80)

    # Print errors if any
    if stats['errors']:
        logger.warning(f"\nErrors encountered: {len(stats['errors'])}")
        for error in stats['errors'][:10]:  # Show first 10 errors
            logger.warning(f"  {error['file']}: {error['error']}")
        if len(stats['errors']) > 10:
            logger.warning(f"  ... and {len(stats['errors']) - 10} more errors")

    logger.info("\nIngestion complete!")
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
