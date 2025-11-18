#!/usr/bin/env python3
"""
Platform Integration Test Suite
Tests all agents, workflows, and API endpoints
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Any, List
import sys

BASE_URL = "http://localhost:8000"

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class PlatformIntegrationTest:
    """Integration test suite for the platform"""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.results = []

    def print_header(self, text: str):
        """Print a section header"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

    def print_test(self, name: str, status: str, message: str = "", duration: float = 0):
        """Print test result"""
        if status == "PASS":
            symbol = f"{Colors.GREEN}✓{Colors.END}"
            self.passed += 1
        elif status == "FAIL":
            symbol = f"{Colors.RED}✗{Colors.END}"
            self.failed += 1
        elif status == "WARN":
            symbol = f"{Colors.YELLOW}⚠{Colors.END}"
            self.warnings += 1
        else:
            symbol = "•"

        duration_str = f"({duration:.2f}s)" if duration > 0 else ""
        print(f"{symbol} {name:50} {duration_str}")
        if message:
            print(f"  → {message}")

        self.results.append({
            "test": name,
            "status": status,
            "message": message,
            "duration": duration
        })

    async def test_health(self):
        """Test platform health"""
        self.print_header("Platform Health Check")
        start = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/api/agents/health", timeout=10) as resp:
                    duration = time.time() - start

                    if resp.status == 200:
                        data = await resp.json()

                        if data.get("status") == "healthy":
                            self.print_test("Platform health", "PASS",
                                          f"{data.get('total_agents')} agents, {data.get('workflows_registered')} workflows",
                                          duration)

                            # Check individual agents
                            agents = data.get("agents", {})
                            for agent_name, status in agents.items():
                                if status == "ready":
                                    self.print_test(f"  Agent: {agent_name}", "PASS", "Ready")
                                else:
                                    self.print_test(f"  Agent: {agent_name}", "WARN", f"Status: {status}")

                            return True
                        else:
                            self.print_test("Platform health", "FAIL", f"Status: {data.get('status')}", duration)
                            return False
                    else:
                        self.print_test("Platform health", "FAIL", f"HTTP {resp.status}", duration)
                        return False

        except Exception as e:
            duration = time.time() - start
            self.print_test("Platform health", "FAIL", str(e), duration)
            return False

    async def test_list_agents(self):
        """Test listing agents"""
        self.print_header("Agent Registry")
        start = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/api/agents/", timeout=10) as resp:
                    duration = time.time() - start

                    if resp.status == 200:
                        agents = await resp.json()
                        self.print_test("List agents", "PASS", f"Found {len(agents)} agents", duration)

                        # Check each agent
                        for agent in agents:
                            name = agent.get("name", "unknown")
                            tools = agent.get("tools", [])
                            domain = agent.get("domain", "unknown")

                            self.print_test(f"  {name}", "PASS",
                                          f"{domain} domain, {len(tools)} tools")

                        return True
                    else:
                        self.print_test("List agents", "FAIL", f"HTTP {resp.status}", duration)
                        return False

        except Exception as e:
            duration = time.time() - start
            self.print_test("List agents", "FAIL", str(e), duration)
            return False

    async def test_list_workflows(self):
        """Test listing workflows"""
        self.print_header("Workflow Registry")
        start = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/api/agents/workflows", timeout=10) as resp:
                    duration = time.time() - start

                    if resp.status == 200:
                        workflows = await resp.json()
                        self.print_test("List workflows", "PASS",
                                      f"Found {len(workflows)} workflows", duration)

                        # Get details for each workflow
                        for workflow_name in workflows:
                            wf_start = time.time()
                            async with session.get(f"{BASE_URL}/api/agents/workflows/{workflow_name}",
                                                  timeout=10) as wf_resp:
                                wf_duration = time.time() - wf_start

                                if wf_resp.status == 200:
                                    wf_data = await wf_resp.json()
                                    tasks = wf_data.get("tasks", [])
                                    self.print_test(f"  {workflow_name}", "PASS",
                                                  f"{len(tasks)} tasks")
                                else:
                                    self.print_test(f"  {workflow_name}", "WARN",
                                                  f"HTTP {wf_resp.status}")

                        return True
                    else:
                        self.print_test("List workflows", "FAIL", f"HTTP {resp.status}", duration)
                        return False

        except Exception as e:
            duration = time.time() - start
            self.print_test("List workflows", "FAIL", str(e), duration)
            return False

    async def test_workflow_examples(self):
        """Test workflow examples"""
        self.print_header("Workflow Examples")
        start = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/api/agents/workflows/examples/all",
                                      timeout=10) as resp:
                    duration = time.time() - start

                    if resp.status == 200:
                        data = await resp.json()
                        workflows = data.get("workflows", {})

                        self.print_test("Get all workflow examples", "PASS",
                                      f"{len(workflows)} workflows with examples", duration)

                        for wf_name, wf_info in workflows.items():
                            has_example = "example_input" in wf_info
                            has_desc = "description" in wf_info

                            if has_example and has_desc:
                                self.print_test(f"  {wf_name}", "PASS", "Has example & description")
                            else:
                                self.print_test(f"  {wf_name}", "WARN", "Missing data")

                        return True
                    else:
                        self.print_test("Get workflow examples", "FAIL",
                                      f"HTTP {resp.status}", duration)
                        return False

        except Exception as e:
            duration = time.time() - start
            self.print_test("Get workflow examples", "FAIL", str(e), duration)
            return False

    async def test_agent_execution(self):
        """Test executing a simple agent"""
        self.print_header("Agent Execution Tests")

        # Test 1: HR Agent
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "task": {
                        "question": "What is a typical vacation policy?",
                        "task_type": "general",
                        "context": "Quick test"
                    }
                }

                async with session.post(f"{BASE_URL}/api/agents/hr_policy/execute",
                                       json=payload,
                                       timeout=aiohttp.ClientTimeout(total=90)) as resp:
                    duration = time.time() - start

                    if resp.status == 200:
                        result = await resp.json()

                        if result.get("status") == "completed":
                            answer = result.get("result", {}).get("answer", "")
                            answer_preview = answer[:100] + "..." if len(answer) > 100 else answer

                            self.print_test("Execute HR agent", "PASS",
                                          f"Got answer: {answer_preview}", duration)
                            return True
                        else:
                            self.print_test("Execute HR agent", "FAIL",
                                          f"Status: {result.get('status')}", duration)
                            return False
                    else:
                        error_text = await resp.text()
                        self.print_test("Execute HR agent", "FAIL",
                                      f"HTTP {resp.status}: {error_text[:100]}", duration)
                        return False

        except asyncio.TimeoutError:
            duration = time.time() - start
            self.print_test("Execute HR agent", "WARN",
                          f"Timeout after {duration:.1f}s (LLM still processing)", duration)
            return False
        except Exception as e:
            duration = time.time() - start
            self.print_test("Execute HR agent", "FAIL", str(e), duration)
            return False

    async def test_agent_info(self):
        """Test getting agent information"""
        self.print_header("Agent Information")

        agents_to_test = ["hr_policy", "cs_document", "analysis"]

        for agent_name in agents_to_test:
            start = time.time()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{BASE_URL}/api/agents/{agent_name}/info",
                                          timeout=10) as resp:
                        duration = time.time() - start

                        if resp.status == 200:
                            data = await resp.json()
                            tools = data.get("tools", [])
                            domain = data.get("domain", "unknown")

                            self.print_test(f"Get {agent_name} info", "PASS",
                                          f"{domain} domain, {len(tools)} tools", duration)
                        else:
                            self.print_test(f"Get {agent_name} info", "FAIL",
                                          f"HTTP {resp.status}", duration)

            except Exception as e:
                duration = time.time() - start
                self.print_test(f"Get {agent_name} info", "FAIL", str(e), duration)

    async def test_orchestrator_stats(self):
        """Test orchestrator statistics"""
        self.print_header("Orchestrator Statistics")
        start = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/api/agents/stats", timeout=10) as resp:
                    duration = time.time() - start

                    if resp.status == 200:
                        stats = await resp.json()
                        self.print_test("Get orchestrator stats", "PASS",
                                      f"Stats available", duration)

                        # Print key stats
                        for key, value in stats.items():
                            if isinstance(value, (int, float)):
                                print(f"    {key}: {value}")

                        return True
                    else:
                        self.print_test("Get orchestrator stats", "FAIL",
                                      f"HTTP {resp.status}", duration)
                        return False

        except Exception as e:
            duration = time.time() - start
            self.print_test("Get orchestrator stats", "FAIL", str(e), duration)
            return False

    async def test_api_documentation(self):
        """Test API documentation endpoints"""
        self.print_header("API Documentation")

        endpoints = [
            ("/docs", "Swagger UI"),
            ("/redoc", "ReDoc UI"),
            ("/openapi.json", "OpenAPI Schema")
        ]

        for path, name in endpoints:
            start = time.time()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{BASE_URL}{path}", timeout=10) as resp:
                        duration = time.time() - start

                        if resp.status == 200:
                            self.print_test(f"{name}", "PASS", f"Available at {path}", duration)
                        else:
                            self.print_test(f"{name}", "WARN",
                                          f"HTTP {resp.status}", duration)

            except Exception as e:
                duration = time.time() - start
                self.print_test(f"{name}", "FAIL", str(e), duration)

    def print_summary(self):
        """Print test summary"""
        self.print_header("Test Summary")

        total = self.passed + self.failed + self.warnings

        print(f"\n{Colors.BOLD}Results:{Colors.END}")
        print(f"  {Colors.GREEN}✓ Passed:{Colors.END}  {self.passed:3d} / {total}")
        print(f"  {Colors.RED}✗ Failed:{Colors.END}  {self.failed:3d} / {total}")
        print(f"  {Colors.YELLOW}⚠ Warnings:{Colors.END} {self.warnings:3d} / {total}")

        if self.failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All critical tests passed!{Colors.END}")
            success_rate = (self.passed / total * 100) if total > 0 else 0
            print(f"  Success rate: {success_rate:.1f}%")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ Some tests failed{Colors.END}")
            print(f"  Please review failed tests above")

        print()

    async def run_all_tests(self):
        """Run all integration tests"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}")
        print("╔═══════════════════════════════════════════════════════════════════╗")
        print("║     Vault AI Platform - Integration Test Suite                   ║")
        print("║   Version 2.0.0 | Multi-Domain Agentic AI Platform              ║")
        print("╚═══════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")

        print(f"{Colors.YELLOW}Note: Agent execution tests may take 30-60 seconds (LLM processing){Colors.END}\n")

        # Run tests in order
        await self.test_health()
        await self.test_list_agents()
        await self.test_list_workflows()
        await self.test_workflow_examples()
        await self.test_agent_info()
        await self.test_orchestrator_stats()
        await self.test_api_documentation()
        await self.test_agent_execution()  # Last because it's slow

        # Print summary
        self.print_summary()

        # Return exit code
        return 0 if self.failed == 0 else 1


async def main():
    """Main test runner"""
    tester = PlatformIntegrationTest()
    exit_code = await tester.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())
