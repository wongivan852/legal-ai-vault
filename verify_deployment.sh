#!/bin/bash
# Deployment Verification Script for Synthesis Agent Auto-Retrieve
# Checks that all components are properly deployed and functioning

echo "========================================="
echo "Synthesis Agent Deployment Verification"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

API_BASE="http://localhost:8000"
ERRORS=0

# Function to check status
check_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}"
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((ERRORS++))
    fi
}

# Header
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}   DEPLOYMENT VERIFICATION CHECKLIST   ${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""

# 1. Check Docker is running
echo -n "1. Docker daemon running... "
if docker info > /dev/null 2>&1; then
    check_status 0
else
    check_status 1
    echo -e "${YELLOW}   → Start Docker Desktop and try again${NC}"
fi
echo ""

# 2. Check API container is up
echo -n "2. API container running... "
if docker ps | grep -q "legal-ai-vault[_-]api"; then
    check_status 0
else
    check_status 1
    echo -e "${YELLOW}   → Run: docker-compose up -d api${NC}"
fi
echo ""

# 3. Check API health
echo -n "3. API health check... "
health=$(curl -s "${API_BASE}/health" 2>/dev/null)
if echo "$health" | jq -e '.status == "healthy"' > /dev/null 2>&1; then
    check_status 0
else
    check_status 1
    echo -e "${YELLOW}   → Check: curl ${API_BASE}/health${NC}"
fi
echo ""

# 4. Check Qdrant is accessible
echo -n "4. Qdrant vector DB accessible... "
qdrant=$(curl -s "http://localhost:6333/collections/legal_documents" 2>/dev/null)
if echo "$qdrant" | jq -e '.result' > /dev/null 2>&1; then
    check_status 0
    # Show collection stats
    doc_count=$(echo "$qdrant" | jq -r '.result.points_count // 0')
    echo -e "   ${GREEN}Documents indexed: $doc_count${NC}"
else
    check_status 1
    echo -e "${YELLOW}   → Check Qdrant: curl http://localhost:6333/collections${NC}"
fi
echo ""

# 5. Check synthesis agent info endpoint
echo -n "5. Synthesis agent registered... "
agent_info=$(curl -s "${API_BASE}/api/agents/synthesis/info" 2>/dev/null)
if echo "$agent_info" | jq -e '.name' > /dev/null 2>&1; then
    check_status 0
    agent_name=$(echo "$agent_info" | jq -r '.name')
    echo -e "   ${GREEN}Agent: $agent_name${NC}"
else
    check_status 1
    echo -e "${YELLOW}   → Agent may not be initialized yet (will init on first use)${NC}"
fi
echo ""

# 6. Check frontend files exist
echo -n "6. Frontend files deployed... "
if [ -f "frontend/index.html" ] && [ -f "frontend/static/js/app.js" ]; then
    check_status 0
else
    check_status 1
    echo -e "${YELLOW}   → Check frontend directory structure${NC}"
fi
echo ""

# 7. Check backend agent file exists
echo -n "7. EnhancedSynthesisAgent file... "
if [ -f "api/agents/synthesis_agent_enhanced.py" ]; then
    check_status 0
    lines=$(wc -l < "api/agents/synthesis_agent_enhanced.py" | xargs)
    echo -e "   ${GREEN}File size: $lines lines${NC}"
else
    check_status 1
    echo -e "${YELLOW}   → File missing: api/agents/synthesis_agent_enhanced.py${NC}"
fi
echo ""

# 8. Check HTML has auto-retrieve toggle
echo -n "8. HTML auto-retrieve toggle... "
if grep -q "synthesisAutoRetrieve" frontend/index.html; then
    check_status 0
else
    check_status 1
    echo -e "${YELLOW}   → Missing auto-retrieve checkbox in HTML${NC}"
fi
echo ""

# 9. Check JavaScript has toggle function
echo -n "9. JavaScript toggle function... "
if grep -q "toggleSynthesisMode" frontend/static/js/app.js; then
    check_status 0
else
    check_status 1
    echo -e "${YELLOW}   → Missing toggleSynthesisMode in app.js${NC}"
fi
echo ""

# 10. Check routes.py has EnhancedSynthesisAgent import
echo -n "10. Backend agent initialization... "
if grep -q "EnhancedSynthesisAgent" api/routes/agents.py; then
    check_status 0
else
    check_status 1
    echo -e "${YELLOW}   → Missing EnhancedSynthesisAgent import in routes${NC}"
fi
echo ""

# Functional Tests (Optional - Quick)
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}   FUNCTIONAL TESTS (Quick Checks)     ${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""

# 11. Test manual mode (quick)
echo -n "11. Manual mode synthesis... "
manual_test=$(curl -s -X POST "${API_BASE}/api/agents/synthesis/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "task_type": "synthesis",
      "sources": [
        {"title": "Test 1", "content": "Content 1"},
        {"title": "Test 2", "content": "Content 2"}
      ]
    }
  }' 2>/dev/null)

if echo "$manual_test" | jq -e '.status == "completed"' > /dev/null 2>&1; then
    check_status 0
    exec_time=$(echo "$manual_test" | jq -r '.execution_time // 0')
    echo -e "   ${GREEN}Execution time: ${exec_time}s${NC}"
else
    check_status 1
    error=$(echo "$manual_test" | jq -r '.error // .result.error // "Unknown error"')
    echo -e "${YELLOW}   → Error: $error${NC}"
fi
echo ""

# 12. Test auto-retrieve mode (if Qdrant has data)
if [ "$doc_count" -gt 0 ]; then
    echo -n "12. Auto-retrieve mode (single query)... "
    echo -e "${YELLOW}Testing (may take 30-60 seconds)...${NC}"

    auto_test=$(timeout 120 curl -s -X POST "${API_BASE}/api/agents/synthesis/execute" \
      -H "Content-Type: application/json" \
      -d '{
        "task": {
          "task_type": "synthesis",
          "auto_retrieve": true,
          "question": "director duties Hong Kong",
          "top_k_per_query": 3,
          "min_score": 0.6
        }
      }' 2>/dev/null)

    echo -n "    "
    if echo "$auto_test" | jq -e '.status == "completed"' > /dev/null 2>&1; then
        check_status 0
        exec_time=$(echo "$auto_test" | jq -r '.execution_time // 0')
        sources=$(echo "$auto_test" | jq -r '.result.sources | length // 0')
        echo -e "   ${GREEN}Retrieved $sources sources in ${exec_time}s${NC}"
    else
        check_status 1
        error=$(echo "$auto_test" | jq -r '.error // .result.error // "Unknown error"')
        echo -e "${YELLOW}   → Error: $error${NC}"
    fi
    echo ""
else
    echo "12. Auto-retrieve mode... ${YELLOW}SKIPPED (No documents in Qdrant)${NC}"
    echo ""
fi

# Summary
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}   VERIFICATION SUMMARY                ${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED!${NC}"
    echo ""
    echo -e "${GREEN}Deployment is complete and functional.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Open frontend: http://localhost:8000"
    echo "  2. Navigate to Synthesis Agent tab"
    echo "  3. Try auto-retrieve with legal queries"
    echo ""
    echo "Test payloads available in: ./test_payloads/"
    echo "Run full test suite: ./test_synthesis_auto_retrieve.sh"
else
    echo -e "${RED}✗ $ERRORS CHECK(S) FAILED${NC}"
    echo ""
    echo -e "${YELLOW}Please fix the issues above before proceeding.${NC}"
    echo ""
    echo "Common fixes:"
    echo "  1. Start Docker Desktop"
    echo "  2. Run: docker-compose restart api"
    echo "  3. Check API logs: docker-compose logs api | tail -50"
    echo "  4. Verify Qdrant: docker-compose logs qdrant | tail -20"
fi

echo ""
echo "For detailed documentation:"
echo "  - Implementation: SYNTHESIS_AUTO_RETRIEVE_IMPLEMENTATION.md"
echo "  - Quick Start: QUICK_START_SYNTHESIS_AUTO_RETRIEVE.md"
echo "  - Test Payloads: test_payloads/README.md"
echo ""

exit $ERRORS
