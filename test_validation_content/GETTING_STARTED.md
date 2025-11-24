# Getting Started with Legal Validation Test Content

## Quick Start Guide

This guide will help you start using the legal validation test content immediately.

## What You Have

✅ **10 comprehensive test cases** covering:
- Employment law (3 cases)
- HR policies (2 cases)
- Contracts (2 cases)
- Corporate governance (2 cases)
- Policy inconsistencies (1 case)

✅ **31 realistic documents** with:
- Known inconsistencies and conflicts
- Real-world scenarios
- Hong Kong legal context
- Mix of passed, partial, and failed cases

✅ **Complete documentation**:
- README.md - Full documentation
- TEST_CASE_INDEX.md - Quick reference
- GETTING_STARTED.md - This guide

✅ **Test runners**:
- run_sample_test.sh - Bash script
- run_validation_tests.py - Python script

## 5-Minute Quick Test

### Step 1: Choose Your First Test

Start with the simplest test case to verify your setup:

```bash
cd test_validation_content
```

**Recommended first test**: `employment_law/working_hours_consistent.json`
- This is a **positive test** (should pass)
- Has only 3 documents
- No conflicts present
- Good for verifying the system works

### Step 2: View the Test Case

```bash
cat employment_law/working_hours_consistent.json | jq '.'
```

Or just open it in your editor to see the structure.

### Step 3: Run the Test

**Using curl directly**:
```bash
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d @employment_law/working_hours_consistent.json
```

**Using the Python runner**:
```bash
python run_validation_tests.py employment_law/working_hours_consistent.json
```

**Using the shell script**:
```bash
./run_sample_test.sh employment_law/working_hours_consistent.json
```

### Step 4: Check the Results

The response should show:
- `validation_result`: "passed"
- `quality_score`: 85-100
- `issues`: [] (empty list - no issues)

✅ **If you see this, your validation system is working!**

## Next Steps: Try a Failed Case

### Step 5: Test Failure Detection

Now try a test that **should fail**:

```bash
python run_validation_tests.py employment_law/annual_leave_inconsistency.json
```

Expected results:
- `validation_result`: "failed"
- `quality_score`: 20-40 (low score)
- `issues`: List of 3+ conflicts
- Should detect:
  - 14 days vs 12 days vs 7 days leave
  - Eligibility conflicts (12 months vs immediate)
  - Carry-forward policy differences

✅ **If you see multiple issues detected, failure detection is working!**

## Understanding Test Results

### Validation Results

Tests return one of three results:

1. **"passed"** (Quality Score 80-100)
   - Documents are consistent
   - No significant issues found
   - Example: working_hours_consistent.json

2. **"partial"** (Quality Score 60-79)
   - Some issues detected
   - Generally acceptable with minor fixes
   - Examples: remote_work_policy.json, director_duties_compliance.json

3. **"failed"** (Quality Score 0-59)
   - Significant inconsistencies found
   - Requires attention and correction
   - Examples: Most test cases

### Key Metrics

Each test result includes:

```json
{
  "validation_result": "failed|partial|passed",
  "quality_score": 0-100,
  "issues": [
    "Specific issue description 1",
    "Specific issue description 2"
  ],
  "recommendations": [
    "How to fix the issues"
  ],
  "details": {
    "contradictions": [...],
    "unsupported_claims": [...],
    "missing_elements": [...]
  }
}
```

## Test Case Difficulty Levels

### ⭐ Level 1: Simple (Start Here)
- **working_hours_consistent.json** - Positive test, should pass

### ⭐⭐ Level 2: Moderate
- **termination_notice_inconsistency.json** - 3-4 clear conflicts
- **nda_consistency_check.json** - Contract terms conflicts

### ⭐⭐⭐ Level 3: Advanced
- **annual_leave_inconsistency.json** - Multiple interrelated conflicts
- **benefits_policy_conflicts.json** - 6+ different conflicts
- **remote_work_policy.json** - Partial result expected

### ⭐⭐⭐⭐ Level 4: Complex
- **service_agreement_terms.json** - Multi-document hierarchy
- **shareholder_rights_documentation.json** - Legal compliance
- **expense_reimbursement_conflicts.json** - 10+ small conflicts

### ⭐⭐⭐⭐⭐ Level 5: Expert
- **director_duties_compliance.json** - Comprehensive validation
  - Tests accuracy (legal compliance)
  - Tests completeness (all duties listed)
  - Tests consistency (cross-document)

## Running Multiple Tests

### Test All Cases in a Category

```bash
# Test all employment law cases
python run_validation_tests.py --category employment_law

# Test all HR policy cases
python run_validation_tests.py --category hr_policies

# Test all contract cases
python run_validation_tests.py --category contracts
```

### Test Everything

```bash
# Run all test cases
python run_validation_tests.py

# Generate detailed report
python run_validation_tests.py --report all --output full_test_report

# This creates:
# - full_test_report.json (detailed results)
# - full_test_report.md (readable report)
```

### Batch Testing with Shell Script

```bash
# Interactive mode - press Enter between tests
./run_sample_test.sh
```

## Interpreting Test Results

### Success Criteria

A validation system is working well if:

✅ **Detection Rate**: 90%+ of expected issues are found
- Check `expected_issues` in test case
- Compare with `issues` in response

✅ **Correct Classification**: Issues properly categorized
- Consistency issues vs accuracy issues
- Appropriate severity levels

✅ **Accurate Results**: Expected result matches actual
- "passed" test should return "passed"
- "failed" test should return "failed"
- "partial" test should return "partial"

✅ **Low False Positives**: <10% incorrect issues flagged
- Issues should be real conflicts
- Not normal variations in wording

### Example Analysis

For `annual_leave_inconsistency.json`:

**Expected Issues** (from test case):
1. Inconsistent annual leave days (14 vs 12 vs 7)
2. Conflicting eligibility criteria (12 months vs immediate)
3. Different calculation methods

**Good Response**:
```json
{
  "validation_result": "failed",
  "quality_score": 35,
  "issues": [
    "Annual leave entitlement varies: Handbook states 14 days, Portal states 12 days, Contract states 7 days in first year",
    "Eligibility requirements conflict: Handbook requires 12 months service, Contract provides immediate eligibility",
    "Carry-forward policy differs: Handbook allows 5 days carry forward, Portal prohibits carry forward"
  ]
}
```

**Poor Response**:
```json
{
  "validation_result": "passed",
  "quality_score": 95,
  "issues": []
}
```
❌ This indicates the validation system isn't detecting the conflicts

## Common Issues and Solutions

### Issue: API Not Responding

**Symptoms**:
- Connection refused
- Timeout errors

**Solutions**:
1. Check API is running: `curl http://localhost:8000/health`
2. Verify port: Check if 8000 is correct
3. Update API URL: `--api-url http://your-server:port/api/task`

### Issue: Test Always Passes

**Symptoms**:
- All tests return "passed"
- Even clearly conflicting documents

**Solutions**:
1. Check validation logic in validation_agent.py
2. Verify documents are being read correctly
3. Check focus/instructions are clear
4. Review model temperature settings

### Issue: Too Many False Positives

**Symptoms**:
- Issues flagged that aren't real conflicts
- "passed" test failing incorrectly

**Solutions**:
1. Improve validation prompts
2. Add context about acceptable variations
3. Adjust sensitivity thresholds
4. Review scoring algorithm

### Issue: Slow Performance

**Symptoms**:
- Tests take >60 seconds
- Timeouts on complex cases

**Solutions**:
1. Check document length (may need chunking)
2. Review LLM model choice
3. Consider caching repeated queries
4. Optimize prompts for efficiency

## Tips for Effective Testing

### 1. Test Progressively

Don't jump to the hardest test first:
1. Start with `working_hours_consistent.json` (should pass)
2. Try `annual_leave_inconsistency.json` (should fail with 3 issues)
3. Move to complex cases like `expense_reimbursement_conflicts.json`

### 2. Compare Expected vs Actual

Always check:
- Expected result vs actual result
- Expected issues vs detected issues
- Quality score appropriateness

### 3. Review False Negatives

If expected issues aren't detected:
- Are documents being read fully?
- Is the focus clear enough?
- Does the model have enough context?

### 4. Review False Positives

If unexpected issues are flagged:
- Are they legitimate issues we missed?
- Are they stylistic vs substantive differences?
- Should we adjust sensitivity?

### 5. Track Performance Over Time

Keep test result history:
```bash
# Save results with timestamp
python run_validation_tests.py --report all --output results_$(date +%Y%m%d)
```

Compare accuracy across versions to ensure improvements.

## Advanced Usage

### Custom API Configuration

```bash
# Use different endpoint
export API_URL=https://production-server.com/api/task
python run_validation_tests.py

# Or specify directly
python run_validation_tests.py --api-url https://staging.company.com/api/task
```

### Automated Testing in CI/CD

```yaml
# .github/workflows/validation-tests.yml
name: Validation Agent Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run validation tests
        run: |
          python test_validation_content/run_validation_tests.py --report all
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: test_results_*.json
```

### Integration with Test Framework

```python
# pytest example
import pytest
from run_validation_tests import ValidationTestRunner

def test_all_validation_cases():
    """Test that validation system works correctly on all test cases"""
    runner = ValidationTestRunner()
    results = runner.run_all_tests()

    # Check overall accuracy
    passed = sum(1 for r in results if r.passed)
    accuracy = passed / len(results) if results else 0

    assert accuracy >= 0.90, f"Validation accuracy {accuracy:.1%} below threshold"

def test_passed_case_detection():
    """Ensure system correctly identifies consistent documents"""
    runner = ValidationTestRunner()
    result = runner.run_single_test(
        Path("test_validation_content/employment_law/working_hours_consistent.json")
    )

    assert result.actual_result == "passed"
    assert result.quality_score >= 80
    assert result.issues_detected == 0
```

## Next Steps

Now that you've run some tests:

1. **Review Results**: Check if the validation system is working as expected

2. **Tune Settings**: Adjust prompts, thresholds, or scoring if needed

3. **Add Test Cases**: Create your own test cases for specific scenarios

4. **Integrate**: Use these tests in your CI/CD pipeline

5. **Monitor**: Track validation accuracy over time

## Resources

- **Full Documentation**: See README.md
- **Test Index**: See TEST_CASE_INDEX.md
- **Test Files**: Browse the category directories
- **API Documentation**: Check your main project docs

## Need Help?

- Review the example test cases
- Check the detailed documentation in README.md
- Examine the test case structure
- Look at expected vs actual results

---

**Ready to start testing?**

```bash
# Run your first test now!
python run_validation_tests.py employment_law/working_hours_consistent.json
```

Good luck with your legal validation testing! 🚀
