#!/bin/bash
# Test script for Synthesis Agent Auto-Retrieve Enhancement
# Usage: ./test_synthesis_auto_retrieve.sh

echo "========================================="
echo "Synthesis Agent Auto-Retrieve Test Suite"
echo "========================================="
echo ""

API_BASE="http://localhost:8000"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo -e "${YELLOW}Test 1: API Health Check${NC}"
health_response=$(curl -s "${API_BASE}/health")
echo "$health_response" | jq .
echo ""
sleep 2

# Test 2: Synthesis Agent Info
echo -e "${YELLOW}Test 2: Synthesis Agent Info${NC}"
agent_info=$(curl -s "${API_BASE}/api/agents/synthesis/info")
echo "$agent_info" | jq .
echo ""
sleep 2

# Test 3: Manual Mode (Traditional Synthesis)
echo -e "${YELLOW}Test 3: Manual Mode - Traditional Synthesis${NC}"
manual_payload='{
  "task": {
    "task_type": "synthesis",
    "sources": [
      {
        "title": "Document 1",
        "content": "Hong Kong company law requires directors to act in good faith and exercise reasonable care, skill and diligence."
      },
      {
        "title": "Document 2",
        "content": "Directors must avoid conflicts of interest and must not make secret profits from their position."
      }
    ],
    "focus": "Summarize director duties"
  }
}'

echo "Sending request..."
manual_response=$(curl -s -X POST "${API_BASE}/api/agents/synthesis/execute" \
  -H "Content-Type: application/json" \
  -d "$manual_payload")

status=$(echo "$manual_response" | jq -r '.status')
if [ "$status" == "completed" ]; then
  echo -e "${GREEN}✅ Manual mode test passed${NC}"
  echo "$manual_response" | jq '.result.synthesized_output' -r | head -15
else
  echo -e "${RED}❌ Manual mode test failed${NC}"
  echo "$manual_response" | jq .
fi
echo ""
sleep 3

# Test 4: Auto-Retrieve Mode (Single Query)
echo -e "${YELLOW}Test 4: Auto-Retrieve Mode - Single Query${NC}"
auto_single_payload='{
  "task": {
    "task_type": "synthesis",
    "auto_retrieve": true,
    "question": "What are the director duties under the Companies Ordinance?",
    "top_k_per_query": 3,
    "min_score": 0.65,
    "focus": "Create brief summary"
  }
}'

echo "Sending request (this may take 30-60 seconds)..."
auto_single_response=$(curl -s -X POST "${API_BASE}/api/agents/synthesis/execute" \
  -H "Content-Type: application/json" \
  -d "$auto_single_payload")

status=$(echo "$auto_single_response" | jq -r '.status')
if [ "$status" == "completed" ]; then
  echo -e "${GREEN}✅ Auto-retrieve single query test passed${NC}"
  echo "$auto_single_response" | jq '.result.synthesized_output' -r | head -20
  echo ""
  sources=$(echo "$auto_single_response" | jq '.result.sources | length')
  echo -e "${GREEN}📚 Retrieved $sources sources${NC}"
else
  echo -e "${RED}❌ Auto-retrieve single query test failed${NC}"
  echo "$auto_single_response" | jq .
fi
echo ""
sleep 3

# Test 5: Auto-Retrieve Mode (Multiple Queries)
echo -e "${YELLOW}Test 5: Auto-Retrieve Mode - Multiple Queries${NC}"
auto_multi_payload='{
  "task": {
    "task_type": "synthesis",
    "auto_retrieve": true,
    "document_queries": [
      "director duties Hong Kong",
      "company secretary responsibilities",
      "corporate governance requirements"
    ],
    "top_k_per_query": 4,
    "min_score": 0.6,
    "focus": "Create comprehensive corporate compliance guide"
  }
}'

echo "Sending request (this may take 60-90 seconds)..."
auto_multi_response=$(curl -s -X POST "${API_BASE}/api/agents/synthesis/execute" \
  -H "Content-Type: application/json" \
  -d "$auto_multi_payload")

status=$(echo "$auto_multi_response" | jq -r '.status')
if [ "$status" == "completed" ]; then
  echo -e "${GREEN}✅ Auto-retrieve multiple queries test passed${NC}"
  echo "$auto_multi_response" | jq '.result.synthesized_output' -r | head -25
  echo ""
  sources=$(echo "$auto_multi_response" | jq '.result.sources | length')
  echo -e "${GREEN}📚 Retrieved $sources unique sources from 3 queries${NC}"

  # Show source breakdown
  echo ""
  echo -e "${GREEN}Source Citations:${NC}"
  echo "$auto_multi_response" | jq -r '.result.sources[] | "- \(.source) (\(.score | tonumber * 100 | floor)% relevance)"' | head -10
else
  echo -e "${RED}❌ Auto-retrieve multiple queries test failed${NC}"
  echo "$auto_multi_response" | jq .
fi
echo ""

# Summary
echo "========================================="
echo -e "${GREEN}Test Suite Complete${NC}"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Check frontend UI at: http://localhost:8000"
echo "2. Try auto-retrieve toggle in Synthesis Agent tab"
echo "3. Test with your own legal queries"
echo ""
echo "For detailed documentation, see:"
echo "  - SYNTHESIS_AUTO_RETRIEVE_IMPLEMENTATION.md"
echo "  - SYNTHESIS_DOCUMENT_EMBEDDING_GUIDE.md"
echo ""
