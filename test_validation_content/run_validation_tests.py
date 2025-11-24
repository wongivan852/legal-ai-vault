#!/usr/bin/env python3
"""
Legal Validation Test Runner

This script runs validation test cases against the Legal AI Vault API
and generates detailed test reports.

Usage:
    # Run all tests
    python run_validation_tests.py

    # Run specific test
    python run_validation_tests.py employment_law/annual_leave_inconsistency.json

    # Run tests in specific category
    python run_validation_tests.py --category employment_law

    # Generate detailed report
    python run_validation_tests.py --report detailed
"""

import json
import sys
import os
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict


@dataclass
class TestResult:
    """Test result data structure"""
    test_name: str
    category: str
    file_path: str
    expected_result: str
    actual_result: str
    quality_score: float
    issues_detected: int
    expected_issues: int
    passed: bool
    response_time: float
    timestamp: str
    full_response: dict


class ValidationTestRunner:
    """Runs validation test cases and generates reports"""

    def __init__(self, api_url: str = "http://localhost:8000/api/task"):
        self.api_url = api_url
        self.results: List[TestResult] = []
        self.test_dir = Path(__file__).parent

    def load_test_case(self, test_file: Path) -> Dict:
        """Load a test case from JSON file"""
        try:
            with open(test_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading test case {test_file}: {e}")
            return None

    def run_single_test(self, test_file: Path) -> TestResult:
        """Run a single test case"""
        print(f"\n{'='*70}")
        print(f"Running: {test_file.name}")
        print(f"Category: {test_file.parent.name}")
        print(f"{'='*70}")

        test_case = self.load_test_case(test_file)
        if not test_case:
            return None

        test_name = test_case.get('test_case_name', test_file.stem)
        expected_result = test_case.get('expected_validation_result', 'unknown')
        expected_issues = len(test_case.get('expected_issues', []))

        print(f"Test: {test_name}")
        print(f"Expected Result: {expected_result}")
        print(f"Expected Issues: {expected_issues}")

        # Send request to API
        task_payload = test_case.get('task', {})
        print(f"\nSending request to {self.api_url}...")

        start_time = datetime.now()
        try:
            response = requests.post(
                self.api_url,
                json=task_payload,
                timeout=120
            )
            response.raise_for_status()
            result_data = response.json()
            response_time = (datetime.now() - start_time).total_seconds()

            # Extract results
            actual_result = result_data.get('validation_result', 'error')
            quality_score = result_data.get('quality_score', 0)
            issues = result_data.get('issues', [])
            issues_count = len(issues)

            print(f"\nActual Result: {actual_result}")
            print(f"Quality Score: {quality_score}")
            print(f"Issues Detected: {issues_count}")
            print(f"Response Time: {response_time:.2f}s")

            # Determine if test passed
            passed = (expected_result.lower() == actual_result.lower())

            if passed:
                print(f"✓ TEST PASSED")
            else:
                print(f"✗ TEST FAILED (Expected: {expected_result}, Got: {actual_result})")

            # Create result object
            result = TestResult(
                test_name=test_name,
                category=test_file.parent.name,
                file_path=str(test_file),
                expected_result=expected_result,
                actual_result=actual_result,
                quality_score=quality_score,
                issues_detected=issues_count,
                expected_issues=expected_issues,
                passed=passed,
                response_time=response_time,
                timestamp=datetime.now().isoformat(),
                full_response=result_data
            )

            return result

        except requests.exceptions.Timeout:
            print(f"✗ TEST ERROR: Request timeout")
            return TestResult(
                test_name=test_name,
                category=test_file.parent.name,
                file_path=str(test_file),
                expected_result=expected_result,
                actual_result="timeout",
                quality_score=0,
                issues_detected=0,
                expected_issues=expected_issues,
                passed=False,
                response_time=120,
                timestamp=datetime.now().isoformat(),
                full_response={}
            )

        except Exception as e:
            print(f"✗ TEST ERROR: {str(e)}")
            return TestResult(
                test_name=test_name,
                category=test_file.parent.name,
                file_path=str(test_file),
                expected_result=expected_result,
                actual_result="error",
                quality_score=0,
                issues_detected=0,
                expected_issues=expected_issues,
                passed=False,
                response_time=0,
                timestamp=datetime.now().isoformat(),
                full_response={"error": str(e)}
            )

    def run_all_tests(self, category: str = None) -> List[TestResult]:
        """Run all test cases, optionally filtered by category"""
        test_files = []

        if category:
            category_dir = self.test_dir / category
            if category_dir.exists():
                test_files = list(category_dir.glob("*.json"))
            else:
                print(f"Category directory not found: {category}")
                return []
        else:
            test_files = list(self.test_dir.rglob("*.json"))

        # Sort test files
        test_files.sort()

        print(f"\nFound {len(test_files)} test case(s)")

        results = []
        for test_file in test_files:
            result = self.run_single_test(test_file)
            if result:
                results.append(result)
                self.results.append(result)

        return results

    def generate_summary(self, results: List[TestResult] = None):
        """Generate test summary"""
        if results is None:
            results = self.results

        if not results:
            print("\nNo test results to summarize")
            return

        total = len(results)
        passed = sum(1 for r in results if r.passed)
        failed = total - passed
        accuracy = (passed / total * 100) if total > 0 else 0

        print(f"\n{'='*70}")
        print(f"TEST SUMMARY")
        print(f"{'='*70}")
        print(f"Total Tests:      {total}")
        print(f"Passed:           {passed} ({passed/total*100:.1f}%)" if total > 0 else "Passed: 0")
        print(f"Failed:           {failed} ({failed/total*100:.1f}%)" if total > 0 else "Failed: 0")
        print(f"Accuracy:         {accuracy:.1f}%")

        # Average metrics
        avg_score = sum(r.quality_score for r in results) / total if total > 0 else 0
        avg_time = sum(r.response_time for r in results) / total if total > 0 else 0

        print(f"\nAverage Quality Score: {avg_score:.1f}")
        print(f"Average Response Time: {avg_time:.2f}s")

        # Category breakdown
        categories = {}
        for result in results:
            if result.category not in categories:
                categories[result.category] = {'passed': 0, 'failed': 0}

            if result.passed:
                categories[result.category]['passed'] += 1
            else:
                categories[result.category]['failed'] += 1

        print(f"\nResults by Category:")
        for category, stats in sorted(categories.items()):
            total_cat = stats['passed'] + stats['failed']
            pass_rate = (stats['passed'] / total_cat * 100) if total_cat > 0 else 0
            print(f"  {category:30s} {stats['passed']}/{total_cat} ({pass_rate:.0f}%)")

    def generate_detailed_report(self, output_file: str = None):
        """Generate detailed JSON report"""
        if not self.results:
            print("No results to report")
            return

        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"test_results_{timestamp}.json"

        report = {
            "test_run": {
                "timestamp": datetime.now().isoformat(),
                "total_tests": len(self.results),
                "passed": sum(1 for r in self.results if r.passed),
                "failed": sum(1 for r in self.results if not r.passed),
                "api_url": self.api_url
            },
            "results": [asdict(r) for r in self.results]
        }

        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\nDetailed report saved to: {output_path}")

    def generate_markdown_report(self, output_file: str = None):
        """Generate Markdown test report"""
        if not self.results:
            print("No results to report")
            return

        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"test_report_{timestamp}.md"

        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed

        md = []
        md.append("# Legal Validation Test Report\n")
        md.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md.append(f"**API URL**: {self.api_url}\n")
        md.append("")
        md.append("## Summary\n")
        md.append(f"- **Total Tests**: {total}")
        md.append(f"- **Passed**: {passed} ({passed/total*100:.1f}%)" if total > 0 else "- **Passed**: 0")
        md.append(f"- **Failed**: {failed} ({failed/total*100:.1f}%)" if total > 0 else "- **Failed**: 0")
        md.append("")
        md.append("## Test Results\n")
        md.append("| # | Test Name | Category | Expected | Actual | Score | Issues | Status |")
        md.append("|---|-----------|----------|----------|--------|-------|--------|--------|")

        for i, result in enumerate(self.results, 1):
            status = "✅ Pass" if result.passed else "❌ Fail"
            md.append(
                f"| {i} | {result.test_name} | {result.category} | "
                f"{result.expected_result} | {result.actual_result} | "
                f"{result.quality_score:.0f} | {result.issues_detected} | {status} |"
            )

        md.append("")
        md.append("## Detailed Results\n")

        for i, result in enumerate(self.results, 1):
            md.append(f"### {i}. {result.test_name}\n")
            md.append(f"- **Category**: {result.category}")
            md.append(f"- **File**: `{result.file_path}`")
            md.append(f"- **Expected Result**: {result.expected_result}")
            md.append(f"- **Actual Result**: {result.actual_result}")
            md.append(f"- **Quality Score**: {result.quality_score}")
            md.append(f"- **Issues Detected**: {result.issues_detected} (expected: {result.expected_issues})")
            md.append(f"- **Response Time**: {result.response_time:.2f}s")
            md.append(f"- **Status**: {'✅ PASSED' if result.passed else '❌ FAILED'}")
            md.append("")

        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            f.write('\n'.join(md))

        print(f"Markdown report saved to: {output_path}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Run legal validation test cases")
    parser.add_argument(
        'test_file',
        nargs='?',
        help='Specific test file to run'
    )
    parser.add_argument(
        '--category',
        help='Run all tests in a specific category'
    )
    parser.add_argument(
        '--api-url',
        default='http://localhost:8000/api/task',
        help='API endpoint URL'
    )
    parser.add_argument(
        '--report',
        choices=['summary', 'detailed', 'markdown', 'all'],
        default='summary',
        help='Report type to generate'
    )
    parser.add_argument(
        '--output',
        help='Output file for detailed/markdown report'
    )

    args = parser.parse_args()

    # Create test runner
    runner = ValidationTestRunner(api_url=args.api_url)

    # Run tests
    if args.test_file:
        # Run single test
        test_path = Path(args.test_file)
        if not test_path.exists():
            print(f"Test file not found: {args.test_file}")
            sys.exit(1)

        result = runner.run_single_test(test_path)
        if result:
            runner.results.append(result)
    else:
        # Run all tests or category
        runner.run_all_tests(category=args.category)

    # Generate reports
    runner.generate_summary()

    if args.report in ['detailed', 'all']:
        runner.generate_detailed_report(args.output)

    if args.report in ['markdown', 'all']:
        output = args.output.replace('.json', '.md') if args.output else None
        runner.generate_markdown_report(output)

    # Exit with appropriate code
    if runner.results:
        failed = sum(1 for r in runner.results if not r.passed)
        sys.exit(0 if failed == 0 else 1)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
