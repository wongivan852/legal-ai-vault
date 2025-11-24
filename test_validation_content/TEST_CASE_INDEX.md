# Test Case Index - Quick Reference

## Summary Statistics

- **Total Test Cases**: 10
- **Total Documents**: 31 documents across all test cases
- **Categories**: 5
- **Expected Pass**: 1
- **Expected Partial**: 2
- **Expected Fail**: 7

## Quick Reference Table

| # | Test Case | Category | Result | Issues | Docs | Complexity |
|---|-----------|----------|--------|--------|------|------------|
| 1 | Annual Leave Inconsistency | Employment Law | ❌ Failed | 3+ | 3 | ●●●○○ High |
| 2 | Termination Notice Inconsistency | Employment Law | ❌ Failed | 3+ | 3 | ●●●○○ High |
| 3 | Working Hours Consistent | Employment Law | ✅ Passed | 0 | 3 | ●●○○○ Medium |
| 4 | Benefits Policy Conflicts | HR Policies | ❌ Failed | 6+ | 3 | ●●●●○ Very High |
| 5 | Remote Work Policy | HR Policies | ⚠️ Partial | 5+ | 3 | ●●●○○ High |
| 6 | NDA Consistency Check | Contracts | ❌ Failed | 4+ | 3 | ●●●○○ High |
| 7 | Service Agreement Terms | Contracts | ❌ Failed | 5+ | 3 | ●●●●○ Very High |
| 8 | Director Duties Compliance | Corporate Governance | ⚠️ Partial | 3+ | 3 | ●●●●● Extreme |
| 9 | Shareholder Rights Documentation | Corporate Governance | ❌ Failed | 5+ | 3 | ●●●●○ Very High |
| 10 | Expense Reimbursement Conflicts | Policy Inconsistencies | ❌ Failed | 10+ | 3 | ●●●●○ Very High |

## By Category

### 📋 Employment Law (3 test cases)
```
employment_law/
├── annual_leave_inconsistency.json         ❌ Failed   | Leave entitlements conflict
├── termination_notice_inconsistency.json   ❌ Failed   | Notice period conflicts
└── working_hours_consistent.json           ✅ Passed   | Positive test case
```

### 👥 HR Policies (2 test cases)
```
hr_policies/
├── benefits_policy_conflicts.json          ❌ Failed   | Medical, MPF, dental conflicts
└── remote_work_policy.json                 ⚠️ Partial  | Equipment, attendance issues
```

### 📄 Contracts (2 test cases)
```
contracts/
├── nda_consistency_check.json              ❌ Failed   | Confidentiality duration varies
└── service_agreement_terms.json            ❌ Failed   | Payment, liability conflicts
```

### 🏛️ Corporate Governance (2 test cases)
```
corporate_governance/
├── director_duties_compliance.json         ⚠️ Partial  | Outdated references, gaps
└── shareholder_rights_documentation.json   ❌ Failed   | Proxy, quorum, notice conflicts
```

### ⚙️ Policy Inconsistencies (1 test case)
```
policy_inconsistencies/
└── expense_reimbursement_conflicts.json    ❌ Failed   | Meal, travel, receipt conflicts
```

## Detailed Test Case Reference

### 1. Annual Leave Inconsistency
**File**: `employment_law/annual_leave_inconsistency.json`
**Validation Type**: Consistency
**Expected Result**: Failed (Quality Score: 20-40)

**Documents**:
1. Employee Handbook - Leave Policy (2024-01-15)
2. HR Portal - Annual Leave Information (2024-03-20)
3. Standard Employment Contract - Section 5 (2023-11-08)

**Key Conflicts**:
- Leave days: 14 vs 12 vs 7 days
- Eligibility: 12 months vs immediate
- Carry forward: 5 days vs none vs payment in lieu
- Calculation: Monthly accrual vs pro-rata vs statutory scale

**Testing Focus**: Multi-way conflicts, calculation methodology differences

---

### 2. Termination Notice Inconsistency
**File**: `employment_law/termination_notice_inconsistency.json`
**Validation Type**: Consistency
**Expected Result**: Failed (Quality Score: 25-45)

**Documents**:
1. Company Policy Manual - Termination Procedures (2024-02-01)
2. Offer Letter - Manager Position (2023-12-15)
3. Employment Contract - Article 8 (2024-01-10)

**Key Conflicts**:
- Management notice: 3 months vs 1 month vs 2 months
- Probation period: 3 months vs 6 months
- Probation notice: 7 days vs 1 week vs 1 month
- Garden leave: Mentioned vs not mentioned

**Testing Focus**: Hierarchical document conflicts, probation vs regular employment

---

### 3. Working Hours Consistent ✓
**File**: `employment_law/working_hours_consistent.json`
**Validation Type**: Consistency
**Expected Result**: Passed (Quality Score: 85-100)

**Documents**:
1. Employee Handbook - Working Hours Policy (2024-01-01)
2. Employment Contract - Schedule of Terms (2024-01-01)
3. HR Policy Guide - Attendance and Hours (2024-01-01)

**Key Alignments**:
- 40 hours/week consistently stated
- 9 AM - 6 PM hours match
- Core hours 10 AM - 4 PM aligned
- Overtime at 1.5x consistent
- Rest day provisions match

**Testing Focus**: Positive validation, consistency verification

---

### 4. Benefits Policy Conflicts
**File**: `hr_policies/benefits_policy_conflicts.json`
**Validation Type**: Consistency
**Expected Result**: Failed (Quality Score: 30-50)

**Documents**:
1. Employee Benefits Guide 2024 (2024-01-01)
2. Company Website - Careers Page: Benefits (2024-02-15)
3. Standard Employment Contract - Benefits Schedule (2023-12-01)

**Key Conflicts**:
- Medical coverage: Full family vs employee only vs employee + spouse
- MPF employer rate: 10% vs 5%
- MPF calculation: Total salary vs basic salary only
- Dental eligibility: 3 months vs 6 months
- Life insurance: 48 months vs 36 months salary
- Maternity: HK$80K vs HK$100K

**Testing Focus**: Multiple conflict types, benefits quantification

---

### 5. Remote Work Policy
**File**: `hr_policies/remote_work_policy.json`
**Validation Type**: Consistency
**Expected Result**: Partial (Quality Score: 60-75)

**Documents**:
1. Remote Work Policy - Updated Guidelines (2024-03-01)
2. Manager's Guide - Hybrid Work Implementation (2024-03-15)
3. IT Department Email - Remote Work Technology Setup (2024-03-20)

**Key Issues**:
- Core office days: Tue/Wed/Thu vs Mon/Wed/Fri
- Probation requirement: 3 months vs 6 months
- Mobile allowance: HK$500 vs HK$300 vs HK$400
- Response time: 2 hours vs 4 hours
- Equipment: Monitor mentioned vs basic package

**Positive Aspects**:
- VPN requirements consistent
- Laptop provision aligned
- Security requirements match

**Testing Focus**: Partial validation, mixed results

---

### 6. NDA Consistency Check
**File**: `contracts/nda_consistency_check.json`
**Validation Type**: Consistency
**Expected Result**: Failed (Quality Score: 35-55)

**Documents**:
1. Standard Non-Disclosure Agreement Template (2023-08-15)
2. Company Confidentiality and Information Security Policy (2024-01-10)
3. Employment Contract - Confidentiality Clause (2024-01-05)

**Key Conflicts**:
- Duration: 5 years vs 5 years vs indefinite
- Agreement duration: 2 years + 3 years vs not specified
- Return materials: Upon request vs within 3 days
- Trade secrets: Special treatment vs general confidentiality
- Scope: Broad vs narrow definitions

**Testing Focus**: Legal document consistency, term alignment

---

### 7. Service Agreement Terms
**File**: `contracts/service_agreement_terms.json`
**Validation Type**: Consistency
**Expected Result**: Failed (Quality Score: 30-50)

**Documents**:
1. Master Service Agreement (2023-06-01)
2. Statement of Work #007 - Mobile App Development (2024-01-15)
3. Invoice #2024-0342 - Milestone 2 Payment (2024-04-10)

**Key Conflicts**:
- Payment terms: 30 days vs 45 days vs 15 days
- Liability cap: 12 months fees vs total SOW fee (USD $280K) vs $500K max
- Termination notice: 60 days vs 30 days
- Warranty: 90 days vs 60 days
- Late payment: 1.5% vs 2% monthly

**Testing Focus**: Master agreement vs SOW vs invoice consistency

---

### 8. Director Duties Compliance
**File**: `corporate_governance/director_duties_compliance.json`
**Validation Type**: Comprehensive (Accuracy + Consistency + Completeness)
**Expected Result**: Partial (Quality Score: 65-75)

**Documents**:
1. Board of Directors Charter (2023-05-20)
2. Director Handbook - Guide for Directors (2024-02-01)
3. Corporate Governance Framework Document (2022-11-30)

**Key Issues**:
- Legal references: Cap. 32 (old) vs Cap. 622 (current)
- Disclosure timing: Immediately vs at next meeting vs 5 days before
- Statutory duties: Some omissions in Charter
- Independence criteria: Generally consistent

**Positive Aspects**:
- Core fiduciary duties well described
- Meeting procedures aligned
- Committee structures consistent

**Testing Focus**: Legal accuracy, statutory compliance, completeness

---

### 9. Shareholder Rights Documentation
**File**: `corporate_governance/shareholder_rights_documentation.json`
**Validation Type**: Accuracy
**Expected Result**: Failed (Quality Score: 40-60)

**Documents**:
1. Articles of Association - Extract: Shareholder Rights (2020-03-15)
2. Shareholder Information Guide 2024 (2024-01-15)
3. Notice of Annual General Meeting 2024 (2024-04-30)

**Key Conflicts**:
- Proxy deadline: 48 hours vs 24 hours
- AGM notice: 21 days vs 14 days
- Quorum: 2 shareholders with 25% vs 3 shareholders with 20%
- Dividend forfeiture: 6 years vs 5 years
- EGM requisition: 21 days convene, 28 days hold vs 30/45 days

**Testing Focus**: Legal document vs guidance vs actual notice consistency

---

### 10. Expense Reimbursement Conflicts
**File**: `policy_inconsistencies/expense_reimbursement_conflicts.json`
**Validation Type**: Consistency
**Expected Result**: Failed (Quality Score: 25-45)

**Documents**:
1. Corporate Expense Reimbursement Policy (2024-01-01)
2. Employee Handbook - Travel and Expenses Section (2023-11-15)
3. Finance Department Quick Reference Guide (2024-03-01)

**Key Conflicts** (10+ total):

**Meals**:
- Breakfast: HK$80 vs HK$100 vs HK$70
- Lunch: HK$120 vs HK$150 vs HK$100
- Dinner: HK$200 vs HK$250 vs HK$150
- Daily max: HK$400 vs HK$500 vs HK$320

**Transportation**:
- Mileage: HK$2.50 vs HK$2.00 vs HK$2.20/km

**Documentation**:
- Receipt threshold: HK$100 vs HK$50 vs HK$75
- Non-receipt max: HK$500 vs none specified vs HK$300/month

**Approvals**:
- Manager limit: HK$5,000 vs HK$10,000 vs HK$3,000
- Department head: HK$20,000 vs HK$30,000 vs HK$15,000

**Other**:
- HK accommodation: HK$1,800 vs HK$1,500 vs HK$1,600
- Professional dues: HK$5,000 vs HK$3,000 vs HK$4,000/year
- Roaming: HK$500 vs HK$300 vs HK$400/trip

**Testing Focus**: Many small inconsistencies, numerical conflicts

---

## Testing Strategies

### Progressive Testing
Start with simpler cases and progress to complex:
1. **Level 1**: Working Hours Consistent (passed case)
2. **Level 2**: Termination Notice, NDA Consistency
3. **Level 3**: Benefits, Service Agreement, Shareholder Rights
4. **Level 4**: Director Duties (comprehensive validation)

### Focused Testing
Test specific validation capabilities:
- **Consistency Only**: Cases 1, 2, 4, 5, 6, 7, 10
- **Accuracy Focus**: Cases 8, 9
- **Positive Validation**: Case 3
- **Partial Results**: Cases 5, 8

### Performance Testing
Test with varying document counts and sizes:
- All cases have 3 documents (controlled)
- Document lengths vary: 1,000 - 5,000+ words
- Total text per case: 3,000 - 15,000+ words

## Expected Detection Rates

| Test Case | Total Issues | Critical | High | Medium | Low |
|-----------|--------------|----------|------|--------|-----|
| Annual Leave | 3-4 | 2 | 1 | 1 | 0 |
| Termination Notice | 3-4 | 2 | 1 | 1 | 0 |
| Working Hours | 0 | 0 | 0 | 0 | 0 |
| Benefits Conflicts | 6-8 | 3 | 2 | 2 | 1 |
| Remote Work | 5-6 | 1 | 2 | 2 | 1 |
| NDA Consistency | 4-5 | 2 | 2 | 1 | 0 |
| Service Agreement | 5-6 | 3 | 2 | 1 | 0 |
| Director Duties | 3-4 | 1 | 1 | 1 | 1 |
| Shareholder Rights | 5-6 | 2 | 2 | 2 | 0 |
| Expense Reimbursement | 10-12 | 2 | 4 | 4 | 2 |

## Success Metrics

For a successful validation run:

✓ **Detection Accuracy**: 90%+ of expected issues detected
✓ **False Positive Rate**: <10% (issues flagged that don't exist)
✓ **Classification Accuracy**: Issues correctly categorized
✓ **Severity Assignment**: Appropriate severity levels
✓ **Result Consistency**: Same input = same output
✓ **Response Time**: <60 seconds per test case
✓ **Quality Scoring**: Scores align with issue counts and severity

---

**Quick Start**: Run test case #3 (Working Hours) first to verify passed validation works, then test case #10 (Expense Reimbursement) for complex failure detection.

**Last Updated**: November 24, 2024
