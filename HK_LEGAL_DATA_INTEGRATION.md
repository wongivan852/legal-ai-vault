# Hong Kong Legal Data Integration

## Overview

This integration adds comprehensive Hong Kong legal document support to the Legal AI Vault, including:

- **Hong Kong Legislation Chapters** (Cap. 1 to Cap. 600+)
- **Legal Instruments** (A-series instruments)
- **Multilingual Support** (English, Traditional Chinese, Simplified Chinese)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              HK LEGAL DATA INTEGRATION                       │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  XML Files       │
│  (Download.zip)  │
│  - Instruments   │
│  - Legislation   │
│  - 3 Languages   │
└────────┬─────────┘
         │
         ▼
┌────────────────────────┐
│  XML Parser            │
│  hk_legal_xml_parser.py│
│  - Extracts metadata   │
│  - Parses structure    │
│  - Extracts content    │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│  Ingestion Service     │
│  hk_legal_ingestion.py │
│  - Creates DB records  │
│  - Generates embeddings│
│  - Stores in Qdrant    │
└────────┬───────────────┘
         │
         ├──────────────────────┬──────────────────────┐
         ▼                      ▼                      ▼
┌────────────────┐    ┌────────────────┐    ┌────────────────┐
│  PostgreSQL    │    │  Qdrant Vector │    │  API Endpoints │
│  - Documents   │    │  - Embeddings  │    │  /api/hk-legal │
│  - Sections    │    │  - RAG Search  │    │  - Search      │
│  - Metadata    │    │  - Similarity  │    │  - Browse      │
└────────────────┘    └────────────────┘    └────────┬───────┘
                                                      │
                                                      ▼
                                            ┌────────────────┐
                                            │  AI Agents     │
                                            │  - Contract    │
                                            │  - Compliance  │
                                            │  - Research    │
                                            └────────────────┘
```

## Components Created

### 1. XML Parser (`api/parsers/hk_legal_xml_parser.py`)

Parses Hong Kong e-Legislation XML format:

```python
parser = HKLegalXMLParser()
parsed_data = parser.parse_document("path/to/A101_en_c.xml")

# Returns:
{
    'metadata': {
        'doc_number': 'A101',
        'doc_type': 'instrument',
        'doc_status': 'In effect',
        'language': 'en',
        'effective_date': '1997-07-01'
    },
    'content': {
        'title': 'The Basic Law of Hong Kong...',
        'full_text': '...',
        'sections': [...],
        'chapters': [...]
    },
    'structure': [...]
}
```

### 2. Database Models (`api/models/hk_legal_document.py`)

Two main models:

- **HKLegalDocument**: Stores complete legal documents
- **HKLegalSection**: Stores individual sections for granular search

Schema:
```sql
CREATE TABLE hk_legal_documents (
    id VARCHAR PRIMARY KEY,
    doc_number VARCHAR NOT NULL,  -- 'A101', 'Cap. 1'
    doc_name VARCHAR NOT NULL,
    doc_type VARCHAR NOT NULL,    -- 'instrument', 'ordinance'
    language VARCHAR NOT NULL,    -- 'en', 'zh-Hant', 'zh-Hans'
    title TEXT,
    full_text TEXT NOT NULL,
    word_count INTEGER,
    vector_ids JSON,              -- References to Qdrant vectors
    imported_at TIMESTAMP,
    vectorized BOOLEAN
);

CREATE TABLE hk_legal_sections (
    id VARCHAR PRIMARY KEY,
    document_id VARCHAR NOT NULL,
    section_number VARCHAR,
    section_heading VARCHAR,
    content TEXT NOT NULL,
    vector_id VARCHAR
);
```

### 3. Ingestion Service (`api/services/hk_legal_ingestion.py`)

Handles the complete ingestion pipeline:

1. **Parse XML** - Extract structured data
2. **Store in PostgreSQL** - Document metadata and content
3. **Generate Embeddings** - Using bge-large-en-v1.5 model
4. **Store in Qdrant** - Vector embeddings for RAG
5. **Chunk Long Documents** - Split into searchable chunks

Features:
- Batch processing
- Duplicate detection
- Progress tracking
- Error handling
- Automatic vectorization

### 4. CLI Ingestion Script (`scripts/ingest_hk_legal_data.py`)

Command-line tool for data import:

```bash
# Basic usage
python scripts/ingest_hk_legal_data.py /path/to/hkel_data

# With database initialization
python scripts/ingest_hk_legal_data.py /path/to/hkel_data --init-db

# Filter by language
python scripts/ingest_hk_legal_data.py /path/to/hkel_data --language en
```

### 5. API Endpoints (`api/routers/hk_legal.py`)

RESTful API for accessing HK legal data:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/hk-legal/search` | GET | AI-powered semantic search |
| `/api/hk-legal/documents` | GET | List documents with filters |
| `/api/hk-legal/documents/{id}` | GET | Get full document details |
| `/api/hk-legal/documents/{id}/full_text` | GET | Get document text |
| `/api/hk-legal/documents/{id}/sections` | GET | Get document sections |
| `/api/hk-legal/by_number/{doc_number}` | GET | Get by official number |
| `/api/hk-legal/stats` | GET | Collection statistics |

## Installation & Setup

### Step 1: Extract Data

```bash
cd ~/Downloads
unzip download.zip

# Extract all language versions
mkdir hkel_data
cd hkel_data

unzip ../hkel_c_instruments_en.zip
unzip ../hkel_c_instruments_zh-Hant.zip
unzip ../hkel_c_instruments_zh-Hans.zip

unzip ../hkel_c_leg_cap_1_cap_300_en.zip
unzip ../hkel_c_leg_cap_301_cap_600_en.zip
unzip ../hkel_c_leg_cap_601_cap_end_en.zip

# Optional: Extract Chinese versions
# unzip ../hkel_c_leg_cap_1_cap_300_zh-Hant.zip
# ... etc
```

### Step 2: Initialize Database

```bash
cd ~/legal_financial_ai_vault

# Create database tables
python scripts/ingest_hk_legal_data.py ~/Downloads/hkel_data --init-db
```

### Step 3: Ingest Data

```bash
# Ingest English documents
python scripts/ingest_hk_legal_data.py ~/Downloads/hkel_data --language en

# This will:
# 1. Parse all XML files
# 2. Create database records
# 3. Generate embeddings
# 4. Store vectors in Qdrant
```

### Step 4: Verify Import

Check the logs:
```bash
tail -f hk_legal_ingestion_*.log
```

Expected output:
```
INFO - Starting ingestion from directory: /Users/wongivan/Downloads/hkel_data
INFO - Found 1234 XML files
INFO - Processing file: /Users/wongivan/Downloads/hkel_data/A101_en_c/A101_--------------_en_c.xml
INFO - Successfully imported: A101 (en)
INFO - Created 45 vectors for document A101
...
INFO - INGESTION SUMMARY
INFO - Total files found:      1234
INFO - Successfully processed: 1200
INFO - Failed:                 5
INFO - Skipped (duplicates):   29
INFO - Documents created:      1200
INFO - Sections created:       15678
INFO - Vectors created:        45000
```

### Step 5: Update Main API

Add HK Legal router to main API:

```python
# api/main.py

from routers import auth, documents, agents, admin, hk_legal

# Include HK Legal router
app.include_router(hk_legal.router, prefix="/api/hk-legal", tags=["HK Legal"])
```

### Step 6: Test API

Start the server and test endpoints:

```bash
# Start FastAPI server
cd api
uvicorn main:app --reload

# Test search endpoint
curl -X GET "http://localhost:8000/api/hk-legal/search?query=employment%20rights&language=en" \
     -H "Authorization: Bearer YOUR_TOKEN"

# Get statistics
curl -X GET "http://localhost:8000/api/hk-legal/stats" \
     -H "Authorization: Bearer YOUR_TOKEN"

# Get document by number
curl -X GET "http://localhost:8000/api/hk-legal/by_number/A101?language=en" \
     -H "Authorization: Bearer YOUR_TOKEN"
```

## Usage Examples

### Example 1: Semantic Search

```python
from services.hk_legal_ingestion import HKLegalIngestionService

service = HKLegalIngestionService()

# Search for relevant legislation
results = await service.search_documents(
    query="What are the employment rights for workers in Hong Kong?",
    language='en',
    limit=5
)

for result in results:
    print(f"Document: {result['doc_number']} - {result['doc_name']}")
    print(f"Relevance Score: {result['score']}")
    print(f"Excerpt: {result['text'][:200]}...")
```

### Example 2: Browse Legislation

```python
from models.hk_legal_document import HKLegalDocument
from database import SessionLocal

db = SessionLocal()

# Get all ordinances
ordinances = db.query(HKLegalDocument).filter(
    HKLegalDocument.doc_type == 'ordinance',
    HKLegalDocument.language == 'en'
).all()

for doc in ordinances:
    print(f"{doc.doc_number}: {doc.doc_name}")
    print(f"  Status: {doc.doc_status}")
    print(f"  Effective: {doc.effective_date}")
    print(f"  Word Count: {doc.word_count}")
```

### Example 3: AI Agent Integration

```python
from agents.contract_review import ContractReviewAgent

agent = ContractReviewAgent()

# Analyze a contract against HK law
result = await agent.analyze_with_hk_law(
    contract_text=contract_content,
    relevant_ordinances=['Employment Ordinance', 'Companies Ordinance']
)

print(f"Compliance Issues: {result['compliance_issues']}")
print(f"Relevant Sections: {result['relevant_law_sections']}")
```

## Data Statistics

Expected document counts after ingestion:

| Category | English | 繁體中文 | 简体中文 | Total |
|----------|---------|----------|----------|-------|
| Instruments | ~500 | ~500 | ~500 | ~1,500 |
| Cap. 1-300 | ~300 | ~300 | ~300 | ~900 |
| Cap. 301-600 | ~300 | ~300 | ~300 | ~900 |
| Cap. 601+ | ~50 | ~50 | ~50 | ~150 |
| **Total** | ~1,150 | ~1,150 | ~1,150 | **~3,450** |

Estimated storage:
- **PostgreSQL**: ~5-10 GB
- **Qdrant Vectors**: ~20-30 GB
- **Total**: ~25-40 GB

## Performance Considerations

### Ingestion Speed

- **XML Parsing**: ~100-200 files/minute
- **Embedding Generation**: ~10-20 files/minute (GPU-accelerated)
- **Total Time**:
  - English only: ~1-2 hours
  - All languages: ~3-6 hours

### Query Performance

- **Vector Search**: < 100ms (with GPU acceleration)
- **Database Queries**: < 50ms
- **Full Pipeline**: < 200ms per query

### Optimization Tips

1. **Batch Size**: Process 10 documents at a time for optimal GPU utilization
2. **Caching**: Enable Qdrant query caching for common searches
3. **Indexing**: Create indexes on `doc_number`, `language`, `doc_type`
4. **Chunking**: Use 500-word chunks for optimal retrieval accuracy

## Troubleshooting

### Common Issues

**Issue**: Import fails with "Database connection error"
```
Solution: Ensure PostgreSQL is running and DATABASE_URL is configured
```

**Issue**: Embedding service timeout
```
Solution: Increase INFERENCE_TIMEOUT_SECONDS in config.py
Check GPU availability with nvidia-smi
```

**Issue**: Duplicate documents
```
Solution: The system automatically skips duplicates based on identifier
Check logs for "already_exists" messages
```

**Issue**: Out of memory during ingestion
```
Solution: Process one language at a time
Reduce batch size in ingestion script
```

## Future Enhancements

- [ ] Bilingual search (cross-language retrieval)
- [ ] Citation extraction and linking
- [ ] Amendment tracking
- [ ] Legal precedent integration
- [ ] Advanced filtering (by date, status, category)
- [ ] Export to PDF/DOCX with formatting
- [ ] Comparison tool for different language versions
- [ ] Integration with case law databases

## References

- [Hong Kong e-Legislation](https://www.elegislation.gov.hk)
- [Department of Justice - Hong Kong](https://www.doj.gov.hk)
- [Basic Law of Hong Kong](https://www.basiclaw.gov.hk)

## Support

For issues or questions:
1. Check the logs: `hk_legal_ingestion_*.log`
2. Review API documentation: `http://localhost:8000/api/docs`
3. Contact: wongivan852@github
