#!/bin/bash
# Quick Start Script for HK Legal Data Integration
# This script automates the complete setup process

set -e  # Exit on error

echo "================================"
echo "HK Legal Data Quick Start"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Verify download.zip exists
echo -e "${YELLOW}Step 1: Verifying data files...${NC}"
DATA_ZIP="$HOME/Downloads/download.zip"

if [ ! -f "$DATA_ZIP" ]; then
    echo -e "${RED}Error: download.zip not found in ~/Downloads${NC}"
    echo "Please ensure download.zip is in your Downloads folder"
    exit 1
fi
echo -e "${GREEN}✓ Found download.zip${NC}"

# Step 2: Extract data
echo ""
echo -e "${YELLOW}Step 2: Extracting HK legal data...${NC}"
EXTRACT_DIR="$HOME/Downloads/hkel_data"

if [ -d "$EXTRACT_DIR" ]; then
    echo "Data directory already exists: $EXTRACT_DIR"
    read -p "Delete and re-extract? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$EXTRACT_DIR"
        mkdir -p "$EXTRACT_DIR"
    fi
else
    mkdir -p "$EXTRACT_DIR"
fi

cd "$HOME/Downloads"
echo "Extracting download.zip..."
unzip -q download.zip

cd "$EXTRACT_DIR"
echo "Extracting English instruments..."
unzip -q ../hkel_c_instruments_en.zip

echo "Extracting English legislation (Cap 1-300)..."
unzip -q ../hkel_c_leg_cap_1_cap_300_en.zip

echo "Extracting English legislation (Cap 301-600)..."
unzip -q ../hkel_c_leg_cap_301_cap_600_en.zip

echo "Extracting English legislation (Cap 601+)..."
unzip -q ../hkel_c_leg_cap_601_cap_end_en.zip

echo -e "${GREEN}✓ Data extracted to $EXTRACT_DIR${NC}"

# Count XML files
XML_COUNT=$(find "$EXTRACT_DIR" -name "*.xml" -type f | wc -l)
echo "Found $XML_COUNT XML files"

# Step 3: Initialize database
echo ""
echo -e "${YELLOW}Step 3: Initializing database...${NC}"
cd "$HOME/legal_financial_ai_vault"

python3 scripts/ingest_hk_legal_data.py "$EXTRACT_DIR" --init-db --language en <<EOF
y
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database initialized${NC}"
else
    echo -e "${RED}✗ Database initialization failed${NC}"
    exit 1
fi

# Step 4: Display summary
echo ""
echo "================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Start the Legal AI Vault services:"
echo "   cd $HOME/legal_financial_ai_vault"
echo "   docker-compose up -d"
echo ""
echo "2. Access the API:"
echo "   http://localhost:8000/api/docs"
echo ""
echo "3. Test HK legal search:"
echo "   curl -X GET 'http://localhost:8000/api/hk-legal/stats'"
echo ""
echo "4. View documentation:"
echo "   cat HK_LEGAL_DATA_INTEGRATION.md"
echo ""
echo "================================"
