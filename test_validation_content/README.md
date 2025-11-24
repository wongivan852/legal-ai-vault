# Legal Validation Test Content

## Overview

This directory contains comprehensive test content for validating the Legal AI Vault's validation agent. The test cases are designed to evaluate the system's ability to detect inconsistencies, contradictions, and compliance issues across multiple documents.

## Purpose

These test cases serve multiple purposes:

1. **Validation Agent Testing** - Test the accuracy and effectiveness of the validation agent
2. **Quality Assurance** - Ensure the system can detect known issues in documents
3. **Performance Benchmarking** - Measure validation accuracy, precision, and recall
4. **Training Examples** - Demonstrate proper validation workflows
5. **Regression Testing** - Ensure system updates don't break existing functionality

## Directory Structure

```
test_validation_content/
├── README.md (this file)
├── employment_law/              # Employment law test cases
│   ├── annual_leave_inconsistency.json
│   ├── termination_notice_inconsistency.json
│   └── working_hours_consistent.json
├── hr_policies/                 # HR policy test cases
│   ├── benefits_policy_conflicts.json
│   └── remote_work_policy.json
├── contracts/                   # Contract validation test cases
│   ├── nda_consistency_check.json
│   └── service_agreement_terms.json
├── corporate_governance/        # Corporate governance test cases
│   ├── director_duties_compliance.json
│   └── shareholder_rights_documentation.json
└── policy_inconsistencies/      # General policy inconsistency tests
    └── expense_reimbursement_conflicts.json
```

## Test Case Format

Each test case is a JSON file with the following structure:

```json
{
  "test_case_name": "Name of the test case",
  "description": "Brief description of what this test validates",
  "expected_validation_result": "passed|partial|failed",
  "expected_issues": [
    "List of specific issues the validation agent should detect"
  ],
  "task": {
    "task_type": "validation",
    "validation_type": "consistency|accuracy|completeness|comprehensive",
    "documents": [
      {
        "title": "Document title",
        "source": "Document source/author",
        "date": "Document date",
        "content": "Full document text..."
      }
    ],
    "focus": "What the validation should focus on"
  }
}
```

## Test Case Categories

### 1. Employment Law (`employment_law/`)

Test cases related to Hong Kong employment law compliance and consistency.

#### 1.1 Annual Leave Inconsistency
- **File**: `annual_leave_inconsistency.json`
- **Expected Result**: Failed
- **Key Issues**:
  - Conflicting leave entitlements (14 days vs 12 days vs 7 days)
  - Different eligibility criteria (12 months vs immediate)
  - Inconsistent carry-forward policies
  - Different pro-rata calculation methods

#### 1.2 Termination Notice Inconsistency
- **File**: `termination_notice_inconsistency.json`
- **Expected Result**: Failed
- **Key Issues**:
  - Varying notice periods (3 months vs 1 month vs 2 months)
  - Different probation periods (3 months vs 6 months)
  - Conflicting probation notice requirements (7 days vs 1 week vs 1 month)
  - Inconsistent payment in lieu provisions

#### 1.3 Working Hours Consistent (Positive Test)
- **File**: `working_hours_consistent.json`
- **Expected Result**: Passed
- **Key Features**:
  - All documents align on 40-hour workweek
  - Consistent flexible working arrangements
  - Aligned overtime policies
  - Matching rest day provisions
- **Purpose**: Test that the validation agent correctly identifies consistent documentation

### 2. HR Policies (`hr_policies/`)

Test cases for internal HR policy validation.

#### 2.1 Benefits Policy Conflicts
- **File**: `benefits_policy_conflicts.json`
- **Expected Result**: Failed
- **Key Issues**:
  - Medical insurance coverage differs (full family vs employee only vs employee + spouse)
  - MPF contribution rates don't match (10% vs 5% employer)
  - MPF calculation basis differs (total salary vs basic salary only)
  - Dental eligibility conflicts (3 months vs 6 months)
  - Life insurance coverage amounts vary (48 months vs 36 months salary)
  - Maternity coverage limits differ (HK$80,000 vs HK$100,000)

#### 2.2 Remote Work Policy
- **File**: `remote_work_policy.json`
- **Expected Result**: Partial
- **Key Issues**:
  - Equipment provision policies differ
  - Core office days don't match (Tue/Wed/Thu vs Mon/Wed/Fri)
  - Eligibility criteria conflict (3 months vs 6 months probation)
  - Mobile allowance amounts vary (HK$500 vs HK$300 vs HK$400)
  - Response time expectations differ (2 hours vs 4 hours)
  - Some alignment exists, but multiple discrepancies present

### 3. Contracts (`contracts/`)

Test cases for contract consistency validation.

#### 3.1 NDA Consistency Check
- **File**: `nda_consistency_check.json`
- **Expected Result**: Failed
- **Key Issues**:
  - Confidentiality duration varies (3 years vs 5 years vs indefinite)
  - Return of materials timelines differ (upon request vs within 3 days)
  - Trade secret treatment inconsistent
  - Different definitions of confidential information
  - Conflicting exceptions and permitted disclosures

#### 3.2 Service Agreement Terms
- **File**: `service_agreement_terms.json`
- **Expected Result**: Failed
- **Key Issues**:
  - Payment terms conflict (30 days vs 45 days vs 15 days)
  - Liability caps don't match (12 months fees vs total SOW fee vs $500K)
  - Termination notice periods vary (60 days vs 30 days)
  - Warranty periods differ (90 days vs 60 days)
  - Different late payment interest rates (1.5% vs 2%)

### 4. Corporate Governance (`corporate_governance/`)

Test cases for corporate governance compliance and consistency.

#### 4.1 Director Duties Compliance
- **File**: `director_duties_compliance.json`
- **Expected Result**: Partial
- **Key Issues**:
  - Board Charter omits certain statutory duties under Companies Ordinance Cap. 622
  - Conflict of interest disclosure timelines inconsistent (immediately vs at next meeting vs 5 days before)
  - Corporate Governance Framework references outdated ordinance (Cap. 32 instead of Cap. 622)
  - Some documents complete and accurate, others have gaps
  - Positive elements: Most core duties properly described

#### 4.2 Shareholder Rights Documentation
- **File**: `shareholder_rights_documentation.json`
- **Expected Result**: Failed
- **Key Issues**:
  - Proxy submission deadlines differ (48 hours vs 24 hours)
  - AGM notice periods conflict (21 days vs 14 days)
  - Quorum requirements don't match (2 shareholders with 25% vs 3 shareholders with 20%)
  - Dividend forfeiture period varies (6 years vs 5 years)
  - EGM requisition timelines inconsistent (21/28 days vs 30/45 days)

### 5. Policy Inconsistencies (`policy_inconsistencies/`)

General policy inconsistency test cases.

#### 5.1 Expense Reimbursement Conflicts
- **File**: `expense_reimbursement_conflicts.json`
- **Expected Result**: Failed
- **Key Issues**:
  - Meal allowances vary significantly:
    - Breakfast: HK$80 vs HK$100 vs HK$70
    - Lunch: HK$120 vs HK$150 vs HK$100
    - Dinner: HK$200 vs HK$250 vs HK$150
  - Mileage rates differ (HK$2.50 vs HK$2.00 vs HK$2.20 per km)
  - Receipt thresholds conflict (HK$100 vs HK$50 vs HK$75)
  - Approval limits don't align across documents
  - Accommodation limits vary for same locations
  - Professional dues limits differ (HK$5,000 vs HK$3,000 vs HK$4,000)

## Validation Types

The test cases cover different validation types:

### 1. Consistency Validation
Detects contradictions and conflicts between documents:
- Different values for the same item (e.g., payment terms)
- Conflicting policies or procedures
- Inconsistent definitions or terminology

### 2. Accuracy Validation
Verifies claims against authoritative sources:
- Compliance with Hong Kong Companies Ordinance
- Adherence to statutory requirements
- Correct legal citations and references

### 3. Completeness Validation
Checks if all required elements are present:
- All mandatory statutory duties listed
- Required approvals and signatures
- Necessary disclosures and notices

### 4. Comprehensive Validation
Combines all three validation types for thorough analysis.

## How to Use These Test Cases

### Method 1: Direct API Testing

Use the test payload directly with the validation agent:

```bash
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d @test_validation_content/employment_law/annual_leave_inconsistency.json
```

### Method 2: Python Script

```python
import json
import requests

# Load test case
with open('test_validation_content/employment_law/annual_leave_inconsistency.json') as f:
    test_case = json.load(f)

# Send to validation agent
response = requests.post(
    'http://localhost:8000/api/task',
    json=test_case['task']
)

# Compare results
result = response.json()
expected = test_case['expected_validation_result']
print(f"Expected: {expected}")
print(f"Actual: {result['validation_result']}")
```

### Method 3: Batch Testing Script

Create a script to run all test cases:

```python
import os
import json
import requests
from pathlib import Path

def run_validation_tests(test_dir='test_validation_content'):
    results = []

    for json_file in Path(test_dir).rglob('*.json'):
        if json_file.name == 'README.md':
            continue

        with open(json_file) as f:
            test_case = json.load(f)

        response = requests.post(
            'http://localhost:8000/api/task',
            json=test_case['task']
        )

        actual = response.json()
        expected = test_case['expected_validation_result']

        results.append({
            'test': test_case['test_case_name'],
            'expected': expected,
            'actual': actual['validation_result'],
            'passed': expected == actual['validation_result']
        })

    return results
```

## Expected Validation Results

| Test Case | Expected Result | Primary Issues |
|-----------|----------------|----------------|
| Annual Leave Inconsistency | Failed | 3+ major conflicts in leave entitlements |
| Termination Notice Inconsistency | Failed | Notice period conflicts across 3 documents |
| Working Hours Consistent | Passed | All documents properly aligned |
| Benefits Policy Conflicts | Failed | 6+ discrepancies in benefits |
| Remote Work Policy | Partial | Some alignment, multiple conflicts |
| NDA Consistency Check | Failed | Duration and scope conflicts |
| Service Agreement Terms | Failed | Payment and liability term conflicts |
| Director Duties Compliance | Partial | Outdated references, incomplete duties |
| Shareholder Rights Documentation | Failed | 5+ procedural conflicts |
| Expense Reimbursement Conflicts | Failed | 10+ limit and threshold conflicts |

## Scoring Guidelines

Based on the validation agent's scoring system:

- **80-100**: Passed - Documents are consistent and compliant
- **60-79**: Partial - Some issues detected, but generally acceptable
- **0-59**: Failed - Significant issues requiring attention

## Test Case Complexity Levels

### Level 1: Simple (2-3 documents, 1-2 issues)
- Working Hours Consistent

### Level 2: Moderate (3 documents, 3-5 issues)
- Termination Notice Inconsistency
- Remote Work Policy
- NDA Consistency Check

### Level 3: Complex (3+ documents, 6-10 issues)
- Annual Leave Inconsistency
- Benefits Policy Conflicts
- Service Agreement Terms
- Director Duties Compliance
- Shareholder Rights Documentation
- Expense Reimbursement Conflicts

## Validation Agent Testing Checklist

When testing the validation agent with these cases:

✓ **Issue Detection**
- [ ] Agent detects all expected issues
- [ ] No false positives (incorrectly flagged issues)
- [ ] Issue descriptions are clear and specific

✓ **Categorization**
- [ ] Issues properly categorized (accuracy, consistency, completeness)
- [ ] Severity levels appropriate (critical, high, medium, low)

✓ **Scoring**
- [ ] Quality scores align with expected results
- [ ] Score calculation is consistent and justified

✓ **Recommendations**
- [ ] Actionable recommendations provided
- [ ] Recommendations address root causes
- [ ] Prioritization makes sense

✓ **Performance**
- [ ] Response time acceptable (<30 seconds for simple cases)
- [ ] Memory usage reasonable
- [ ] Handles multiple documents efficiently

## Adding New Test Cases

To add new test cases:

1. **Choose appropriate directory** based on category
2. **Follow naming convention**: `descriptive_name_with_underscores.json`
3. **Use standard JSON format** (see structure above)
4. **Include all required fields**:
   - test_case_name
   - description
   - expected_validation_result
   - expected_issues (list all specific issues)
   - task (complete validation task payload)
5. **Test thoroughly** to ensure expected issues are actually present
6. **Update this README** with test case details
7. **Document complexity level** and primary issues

## Known Limitations

- Test cases focus on Hong Kong legal context
- English language only (no Chinese language test cases yet)
- Limited coverage of cross-domain validation (e.g., legal + HR combined)
- No multilingual validation test cases
- No test cases for subsection-level validation

## Future Enhancements

Potential additions to test content:

1. **Chinese Language Test Cases** - Traditional and Simplified Chinese
2. **Cross-Domain Validation** - Combined legal + HR + finance scenarios
3. **Edge Cases** - Boundary conditions, unusual scenarios
4. **Performance Test Cases** - Large documents, many documents
5. **Multilingual Validation** - Mixed language documents
6. **Real-World Examples** - Anonymized actual client documents
7. **Industry-Specific Cases** - Financial services, healthcare, technology
8. **Compliance Test Suites** - GDPR, SOX, ISO standards

## Test Results Template

Use this template to document test runs:

```markdown
## Validation Agent Test Run

**Date**: YYYY-MM-DD
**System Version**: v1.x.x
**Model**: GPT-4 / Claude / etc.

| Test Case | Expected | Actual | Issues Detected | Score | Pass/Fail |
|-----------|----------|--------|-----------------|-------|-----------|
| Annual Leave | Failed | Failed | 3/3 | 25 | ✓ Pass |
| Working Hours | Passed | Passed | 0/0 | 95 | ✓ Pass |
| ... | ... | ... | ... | ... | ... |

**Summary**:
- Total Tests: 10
- Passed: 8
- Failed: 2
- Accuracy: 80%

**Notes**:
- Test cases that didn't pass as expected
- Performance issues observed
- Recommendations for improvement
```

## Support and Questions

For questions about test cases or validation testing:

- **Technical Issues**: Check system logs and API responses
- **Test Case Issues**: Review expected_issues list carefully
- **New Test Cases**: Follow structure and naming conventions
- **Documentation**: Refer to main project documentation

## Version History

- **v1.0** (2024-11-24): Initial test content creation
  - 10 comprehensive test cases
  - 5 category directories
  - Mix of passed, partial, and failed cases
  - Covers employment law, HR, contracts, governance, and policies

---

**Last Updated**: November 24, 2024
**Content Created By**: Claude Code
**Total Test Cases**: 10
**Total Categories**: 5
