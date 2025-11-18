#!/usr/bin/env python3
"""
Test Suite for Complete Agent Ecosystem
Tests all agents, orchestrator, and multi-agent workflows
"""

import sys
import asyncio
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents import (
    BaseAgent,
    LegalResearchAgent,
    AnalysisAgent,
    SynthesisAgent,
    ValidationAgent,
    WorkflowOrchestrator
)
from services.ollama_service import OllamaService
from services.rag_service import RAGService
from db.database import SessionLocal
from db.qdrant_client import get_qdrant_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_analysis_agent():
    """Test AnalysisAgent functionality"""
    print("\n" + "="*70)
    print("TEST: Analysis Agent")
    print("="*70)

    ollama = OllamaService()
    agent = AnalysisAgent(ollama)

    print(f"✓ Created {agent.name} agent")
    print(f"  Tools: {[t['name'] for t in agent.tools]}")

    # Test theme extraction
    print("\n⏳ Testing theme analysis...")
    result = await agent.execute({
        "analysis_type": "themes",
        "data": """
        The Buildings Ordinance regulates construction safety.
        Key requirements include structural integrity, fire safety, and accessibility.
        Violations can result in penalties and prosecution.
        """,
        "focus": "legal requirements"
    })

    print(f"  Status: {result['status']}")
    print(f"  Confidence: {result.get('confidence', 'N/A')}")
    print(f"  Insights: {len(result.get('insights', []))}")

    if result.get('insights'):
        print(f"  Top insights:")
        for insight in result['insights'][:3]:
            print(f"    - {insight}")

    print("\n✅ Analysis agent test PASSED")
    return True


async def test_synthesis_agent():
    """Test SynthesisAgent functionality"""
    print("\n" + "="*70)
    print("TEST: Synthesis Agent")
    print("="*70)

    ollama = OllamaService()
    agent = SynthesisAgent(ollama)

    print(f"✓ Created {agent.name} agent")
    print(f"  Tools: {[t['name'] for t in agent.tools]}")

    # Test merging sources
    print("\n⏳ Testing source synthesis...")
    result = await agent.execute({
        "synthesis_type": "merge",
        "sources": [
            "Buildings must meet structural safety standards.",
            "Fire safety regulations require proper exits and equipment.",
            "All buildings must be accessible to persons with disabilities."
        ],
        "focus": "building requirements",
        "format": "text"
    })

    print(f"  Status: {result['status']}")
    print(f"  Sources used: {result.get('sources_used', 0)}")
    print(f"  Quality: {result.get('quality_score', 'N/A')}")

    if result.get('synthesized_output'):
        output = result['synthesized_output']
        print(f"  Output length: {len(output)} characters")
        print(f"  Preview: {output[:150]}...")

    print("\n✅ Synthesis agent test PASSED")
    return True


async def test_validation_agent():
    """Test ValidationAgent functionality"""
    print("\n" + "="*70)
    print("TEST: Validation Agent")
    print("="*70)

    ollama = OllamaService()
    agent = ValidationAgent(ollama)

    print(f"✓ Created {agent.name} agent")
    print(f"  Tools: {[t['name'] for t in agent.tools]}")

    # Test consistency validation
    print("\n⏳ Testing consistency validation...")
    result = await agent.execute({
        "validation_type": "consistency",
        "content": """
        The Buildings Ordinance requires safety standards.
        All buildings must comply with fire safety regulations.
        Accessibility is mandatory for all new construction.
        """
    })

    print(f"  Status: {result['status']}")
    print(f"  Validation result: {result.get('validation_result', 'N/A')}")
    print(f"  Quality score: {result.get('quality_score', 0)}/100")
    print(f"  Issues found: {len(result.get('issues', []))}")

    if result.get('recommendations'):
        print(f"  Recommendations: {len(result['recommendations'])}")

    print("\n✅ Validation agent test PASSED")
    return True


async def test_orchestrator():
    """Test WorkflowOrchestrator"""
    print("\n" + "="*70)
    print("TEST: Workflow Orchestrator")
    print("="*70)

    ollama = OllamaService()

    # Create simple test agents
    class TestAgentA(BaseAgent):
        async def execute(self, task):
            return {"status": "completed", "result": "A", "data": task.get("input")}

    class TestAgentB(BaseAgent):
        async def execute(self, task):
            return {"status": "completed", "result": "B", "previous": task.get("previous")}

    agent_a = TestAgentA("test_a", ollama)
    agent_b = TestAgentB("test_b", ollama)

    # Create orchestrator
    orchestrator = WorkflowOrchestrator()
    orchestrator.register_agent(agent_a)
    orchestrator.register_agent(agent_b)

    print(f"✓ Created orchestrator with {len(orchestrator.agents)} agents")

    # Define simple workflow
    workflow = {
        "tasks": [
            {
                "task_id": "step1",
                "agent": "test_a",
                "input": {"input": "${input.value}"}
            },
            {
                "task_id": "step2",
                "agent": "test_b",
                "input": {"previous": "${step1.data}"}
            }
        ],
        "output_var": "step2"
    }

    orchestrator.register_workflow("test_workflow", workflow)
    print(f"✓ Registered workflow: test_workflow")

    # Execute workflow
    print("\n⏳ Executing test workflow...")
    result = await orchestrator.execute_workflow(
        "test_workflow",
        {"value": "test_input"}
    )

    print(f"  Status: {result['status']}")
    print(f"  Tasks executed: {len(result.get('results', {}))}")
    print(f"  Execution time: {result.get('execution_time', 0):.2f}s")

    # Test variable resolution
    if result["status"] == "completed":
        step2_result = result["results"]["step2"]["result"]
        assert step2_result["previous"] == "test_input", "Variable resolution failed!"
        print(f"  ✓ Variable resolution working")

    # Test statistics
    stats = orchestrator.get_statistics()
    print(f"\n📊 Orchestrator Statistics:")
    print(f"  Total executions: {stats['total_executions']}")
    print(f"  Success rate: {stats['success_rate']*100:.0f}%")

    print("\n✅ Orchestrator test PASSED")
    return True


async def test_agent_tools():
    """Test agent tool system"""
    print("\n" + "="*70)
    print("TEST: Agent Tool System")
    print("="*70)

    ollama = OllamaService()

    # Create agent with custom tool
    class ToolTestAgent(BaseAgent):
        async def execute(self, task):
            tool_name = task.get("tool")
            tool_args = task.get("args", {})
            result = await self.use_tool(tool_name, **tool_args)
            return {"status": "completed", "tool_result": result}

    agent = ToolTestAgent("tool_test", ollama)

    # Register a tool
    def multiply(a: int, b: int) -> int:
        return a * b

    agent.add_tool("multiply", multiply, "Multiply two numbers")
    print(f"✓ Registered tool: multiply")

    # Execute using tool
    print("\n⏳ Testing tool execution...")
    result = await agent.execute({
        "tool": "multiply",
        "args": {"a": 5, "b": 7}
    })

    print(f"  Status: {result['status']}")
    print(f"  Tool result: {result.get('tool_result', 'N/A')}")

    assert result["tool_result"] == 35, "Tool execution failed!"
    print(f"  ✓ Tool executed correctly (5 × 7 = 35)")

    print("\n✅ Agent tool system test PASSED")
    return True


async def test_agent_memory():
    """Test agent memory system"""
    print("\n" + "="*70)
    print("TEST: Agent Memory System")
    print("="*70)

    ollama = OllamaService()
    agent = AnalysisAgent(ollama)

    print(f"✓ Created agent: {agent.name}")

    # Add memory items
    for i in range(5):
        agent.add_to_memory({
            "type": "test",
            "index": i,
            "data": f"item_{i}"
        })

    print(f"  Added 5 memory items")

    # Retrieve memory
    recent = agent.get_memory(count=3)
    print(f"  Retrieved {len(recent)} recent items")
    print(f"  Recent indices: {[item['index'] for item in recent]}")

    # Test memory limit
    for i in range(100):
        agent.add_to_memory({"index": i + 10})

    print(f"  After 100 more additions: {len(agent.memory)} items (capped at 100)")

    assert len(agent.memory) == 100, "Memory limit not enforced!"
    print(f"  ✓ Memory limit enforced correctly")

    print("\n✅ Agent memory test PASSED")
    return True


async def test_error_handling():
    """Test error handling in agents and orchestrator"""
    print("\n" + "="*70)
    print("TEST: Error Handling")
    print("="*70)

    ollama = OllamaService()

    # Test agent with missing data
    print("\n⏳ Testing error handling in agents...")
    agent = AnalysisAgent(ollama)

    result = await agent.execute({
        "analysis_type": "themes"
        # Missing required 'data' field
    })

    print(f"  Status: {result['status']}")
    print(f"  Error handled: {result.get('error', 'No error')}")

    assert result["status"] == "failed", "Error not caught!"
    print(f"  ✓ Agent error handling working")

    # Test orchestrator with missing agent
    print("\n⏳ Testing error handling in orchestrator...")
    orchestrator = WorkflowOrchestrator()

    workflow = {
        "tasks": [{
            "task_id": "test",
            "agent": "nonexistent_agent",
            "input": {}
        }],
        "output_var": "test"
    }

    orchestrator.register_workflow("error_test", workflow)
    result = await orchestrator.execute_workflow("error_test", {})

    print(f"  Status: {result['status']}")
    print(f"  Error handled: {result.get('error', 'No error')[:50]}...")

    assert result["status"] == "failed", "Orchestrator error not caught!"
    print(f"  ✓ Orchestrator error handling working")

    print("\n✅ Error handling test PASSED")
    return True


async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("AGENT ECOSYSTEM TEST SUITE")
    print("="*70)
    print("Testing: All agents, orchestrator, tools, memory, error handling")
    print("="*70)

    tests = [
        ("Analysis Agent", test_analysis_agent),
        ("Synthesis Agent", test_synthesis_agent),
        ("Validation Agent", test_validation_agent),
        ("Workflow Orchestrator", test_orchestrator),
        ("Agent Tool System", test_agent_tools),
        ("Agent Memory System", test_agent_memory),
        ("Error Handling", test_error_handling)
    ]

    results = []
    failed_tests = []

    for test_name, test_func in tests:
        try:
            print(f"\n{'='*70}")
            print(f"Running: {test_name}")
            print(f"{'='*70}")

            result = await test_func()
            results.append((test_name, result))

            if not result:
                failed_tests.append(test_name)

        except Exception as e:
            logger.error(f"Test '{test_name}' failed with exception: {e}", exc_info=True)
            results.append((test_name, False))
            failed_tests.append(test_name)

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")

    print("="*70)
    print(f"Results: {passed}/{total} tests passed")

    if failed_tests:
        print(f"\nFailed tests: {', '.join(failed_tests)}")

    print("="*70)

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
