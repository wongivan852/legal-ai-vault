#!/usr/bin/env python3
"""
Test script for agent framework
Tests BaseAgent and LegalResearchAgent
"""

import sys
import asyncio
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents import BaseAgent, LegalResearchAgent
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


async def test_base_agent():
    """Test base agent functionality"""
    print("\n" + "="*70)
    print("TEST 1: Base Agent Functionality")
    print("="*70)

    ollama = OllamaService()

    # Create a simple test agent
    class TestAgent(BaseAgent):
        async def execute(self, task):
            question = task.get("question")
            answer = await self.think(question)
            return {
                "agent": self.name,
                "status": "completed",
                "answer": answer
            }

    # Initialize test agent
    agent = TestAgent(
        name="test_agent",
        llm_service=ollama,
        description="Simple test agent"
    )

    print(f"✓ Created agent: {agent.name}")
    print(f"  Description: {agent.description}")

    # Test tool registration
    def sample_tool(text: str) -> str:
        return f"Processed: {text}"

    agent.add_tool("sample_tool", sample_tool, "A sample tool")
    print(f"✓ Registered tool: sample_tool")

    # Test capabilities
    capabilities = agent.get_capabilities()
    print(f"✓ Agent capabilities: {capabilities}")

    # Test memory
    agent.add_to_memory({
        "type": "test",
        "content": "Sample memory item"
    })
    memory = agent.get_memory()
    print(f"✓ Agent memory items: {len(memory)}")

    print("\n✅ Base agent test PASSED\n")
    return True


async def test_legal_research_agent():
    """Test legal research agent"""
    print("\n" + "="*70)
    print("TEST 2: Legal Research Agent")
    print("="*70)

    # Initialize services
    db = SessionLocal()
    qdrant = get_qdrant_client()
    ollama = OllamaService()
    rag = RAGService(db, qdrant, ollama)

    # Initialize legal agent
    legal_agent = LegalResearchAgent(ollama, rag)
    print(f"✓ Created legal research agent: {legal_agent.name}")

    # Check capabilities
    capabilities = legal_agent.get_capabilities()
    print(f"✓ Agent tools: {[t['name'] for t in capabilities['tools']]}")

    # Test simple execution
    print("\n⏳ Testing agent execution (this may take 3-5 minutes)...")
    print("   Question: 'What is the Buildings Ordinance?'")

    task = {
        "question": "What is the Buildings Ordinance?",
        "top_k": 3,
        "search_type": "sections",
        "include_reasoning": False
    }

    result = await legal_agent.execute(task)

    print("\n" + "="*70)
    print("AGENT EXECUTION RESULT")
    print("="*70)
    print(f"Status: {result.get('status')}")
    print(f"Confidence: {result.get('confidence')}")
    print(f"Execution Time: {result.get('execution_time', 0):.1f}s")
    print(f"Sources Retrieved: {len(result.get('sources', []))}")

    if result.get('status') == 'completed':
        print(f"\n📝 Answer Preview:")
        answer = result.get('answer', '')
        print(f"   {answer[:300]}..." if len(answer) > 300 else f"   {answer}")

        if result.get('sources'):
            print(f"\n📚 Top Sources:")
            for i, src in enumerate(result['sources'][:3], 1):
                print(f"   {i}. {src.get('doc_name', 'Unknown')} (score: {src.get('score', 0):.1%})")

        print("\n✅ Legal research agent test PASSED\n")
    else:
        print(f"\n❌ Agent execution failed: {result.get('error')}")
        return False

    # Test statistics
    stats = legal_agent.get_statistics()
    print(f"📊 Agent Statistics:")
    print(f"   Total queries: {stats['total_queries']}")
    print(f"   Confidence distribution: {stats.get('confidence_distribution', {})}")

    db.close()
    return True


async def test_agent_memory():
    """Test agent memory system"""
    print("\n" + "="*70)
    print("TEST 3: Agent Memory System")
    print("="*70)

    ollama = OllamaService()

    class MemoryTestAgent(BaseAgent):
        async def execute(self, task):
            return {"status": "completed"}

    agent = MemoryTestAgent("memory_test", ollama)

    # Add multiple memory items
    for i in range(5):
        agent.add_to_memory({
            "type": "test_item",
            "index": i,
            "data": f"Item {i}"
        })

    print(f"✓ Added 5 items to memory")

    # Retrieve memory
    recent = agent.get_memory(count=3)
    print(f"✓ Retrieved {len(recent)} recent items")
    print(f"  Recent items: {[item['index'] for item in recent]}")

    # Test memory limit
    for i in range(100):
        agent.add_to_memory({"index": i + 5})

    print(f"✓ Memory size after 100 additions: {len(agent.memory)} (should be capped at 100)")

    print("\n✅ Agent memory test PASSED\n")
    return True


async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("AGENT FRAMEWORK TEST SUITE")
    print("="*70)
    print("Testing: BaseAgent, LegalResearchAgent, Memory System")
    print("="*70)

    tests = [
        ("Base Agent", test_base_agent),
        ("Legal Research Agent", test_legal_research_agent),
        ("Agent Memory", test_agent_memory)
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test '{test_name}' failed with exception: {e}", exc_info=True)
            results.append((test_name, False))

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
    print("="*70)

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
