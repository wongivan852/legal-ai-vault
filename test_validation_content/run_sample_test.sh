#!/bin/bash

# Sample Test Runner for Legal Validation Test Cases
# This script demonstrates how to run validation test cases against the API

# Configuration
API_URL="${API_URL:-http://localhost:8000/api/task}"
TEST_DIR="$(dirname "$0")"
RESULTS_DIR="${TEST_DIR}/test_results"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create results directory
mkdir -p "${RESULTS_DIR}"

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Legal Validation Test Case Runner                 ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to run a single test case
run_test() {
    local test_file=$1
    local test_name=$(basename "$test_file" .json)
    local category=$(basename "$(dirname "$test_file")")

    echo -e "${YELLOW}Testing:${NC} ${category}/${test_name}"
    echo -e "File: ${test_file}"

    # Extract expected result from test file
    local expected_result=$(jq -r '.expected_validation_result' "$test_file")
    echo -e "Expected Result: ${expected_result}"

    # Extract the task payload
    local task_payload=$(jq '.task' "$test_file")

    # Send to API
    echo -e "${BLUE}Sending request to API...${NC}"
    local response=$(echo "$task_payload" | curl -s -X POST "${API_URL}" \
        -H "Content-Type: application/json" \
        -d @-)

    # Save full response
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local result_file="${RESULTS_DIR}/${category}_${test_name}_${timestamp}.json"
    echo "$response" | jq '.' > "$result_file"

    # Extract actual result
    local actual_result=$(echo "$response" | jq -r '.validation_result // "error"')
    local quality_score=$(echo "$response" | jq -r '.quality_score // "N/A"')
    local issue_count=$(echo "$response" | jq -r '.issues | length // 0')

    echo -e "Actual Result: ${actual_result}"
    echo -e "Quality Score: ${quality_score}"
    echo -e "Issues Found: ${issue_count}"

    # Compare results
    if [ "$expected_result" == "$actual_result" ]; then
        echo -e "${GREEN}✓ TEST PASSED${NC} - Result matches expectation"
        return 0
    else
        echo -e "${RED}✗ TEST FAILED${NC} - Expected: ${expected_result}, Got: ${actual_result}"
        return 1
    fi
}

# Function to print test summary
print_summary() {
    local total=$1
    local passed=$2
    local failed=$3

    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                  TEST SUMMARY                          ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Total Tests Run:     ${total}"
    echo -e "${GREEN}Tests Passed:        ${passed}${NC}"
    echo -e "${RED}Tests Failed:        ${failed}${NC}"

    if [ $total -gt 0 ]; then
        local accuracy=$(awk "BEGIN {printf \"%.1f\", ($passed/$total)*100}")
        echo -e "Accuracy:            ${accuracy}%"
    fi

    echo ""
    echo -e "Detailed results saved to: ${RESULTS_DIR}"
    echo ""
}

# Main execution
main() {
    local total_tests=0
    local passed_tests=0
    local failed_tests=0

    # Check if specific test file provided
    if [ $# -eq 1 ] && [ -f "$1" ]; then
        echo "Running single test: $1"
        echo ""
        run_test "$1"
        exit_code=$?
        echo ""

        if [ $exit_code -eq 0 ]; then
            echo -e "${GREEN}✓ Test passed${NC}"
        else
            echo -e "${RED}✗ Test failed${NC}"
        fi
        exit $exit_code
    fi

    # Run all tests in test_validation_content
    echo "Running all test cases..."
    echo ""

    # Find all JSON test files (excluding README)
    while IFS= read -r test_file; do
        total_tests=$((total_tests + 1))
        echo ""
        echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
        echo -e "${BLUE}Test #${total_tests}${NC}"
        echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"

        if run_test "$test_file"; then
            passed_tests=$((passed_tests + 1))
        else
            failed_tests=$((failed_tests + 1))
        fi

        echo ""
        echo -e "${BLUE}Press Enter to continue to next test...${NC}"
        read -r
    done < <(find "${TEST_DIR}" -name "*.json" -type f | sort)

    # Print summary
    print_summary $total_tests $passed_tests $failed_tests

    # Exit with appropriate code
    if [ $failed_tests -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Run main function
main "$@"
