#!/usr/bin/env python3
"""
Multi-Agent Workflow Examples
Demonstrates orchestrator coordinating multiple agents for complex tasks
"""

import sys
import asyncio
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents import (
    WorkflowOrchestrator,
    LegalResearchAgent,
    AnalysisAgent,
    SynthesisAgent,
    ValidationAgent
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


async def example_1_comprehensive_legal_research():
    """
    Example 1: Comprehensive Legal Research Workflow

    Flow: Research → Analysis → Synthesis → Validation

    This workflow demonstrates a complete legal research process:
    1. Legal agent searches for relevant ordinances
    2. Analysis agent extracts key themes and risks
    3. Synthesis agent creates comprehensive report
    4. Validation agent verifies accuracy and completeness
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Comprehensive Legal Research Workflow")
    print("="*70)

    # Initialize services
    db = SessionLocal()
    qdrant = get_qdrant_client()
    ollama = OllamaService()
    rag = RAGService(db, qdrant, ollama)

    # Initialize agents
    legal_agent = LegalResearchAgent(ollama, rag)
    analysis_agent = AnalysisAgent(ollama)
    synthesis_agent = SynthesisAgent(ollama)
    validation_agent = ValidationAgent(ollama)

    # Create orchestrator
    orchestrator = WorkflowOrchestrator()

    # Register agents
    orchestrator.register_agent(legal_agent)
    orchestrator.register_agent(analysis_agent)
    orchestrator.register_agent(synthesis_agent)
    orchestrator.register_agent(validation_agent)

    # Define workflow
    workflow_definition = {
        "tasks": [
            {
                "task_id": "research",
                "agent": "legal_research",
                "input": {
                    "question": "${input.question}",
                    "top_k": 5
                }
            },
            {
                "task_id": "analyze",
                "agent": "analysis",
                "input": {
                    "analysis_type": "risk",
                    "data": "${research.answer}",
                    "focus": "legal compliance"
                }
            },
            {
                "task_id": "synthesize",
                "agent": "synthesis",
                "input": {
                    "synthesis_type": "report",
                    "sources": [
                        {"source": "legal_research", "content": "${research.answer}"},
                        {"source": "risk_analysis", "content": "${analyze.analysis}"}
                    ],
                    "question": "${input.question}",
                    "format": "markdown"
                }
            },
            {
                "task_id": "validate",
                "agent": "validation",
                "input": {
                    "validation_type": "comprehensive",
                    "content": "${synthesize.synthesized_output}",
                    "sources": "${research.sources}",
                    "question": "${input.question}"
                }
            }
        ],
        "output_var": "validate"
    }

    orchestrator.register_workflow("comprehensive_legal_research", workflow_definition)

    # Execute workflow
    print("\n⏳ Executing comprehensive legal research workflow...")
    print("   Question: 'What are the key building safety requirements?'")
    print("   This will take 10-15 minutes with llama3.3:70b\n")

    result = await orchestrator.execute_workflow(
        "comprehensive_legal_research",
        {"question": "What are the key building safety requirements?"}
    )

    # Display results
    print("\n" + "="*70)
    print("WORKFLOW RESULTS")
    print("="*70)
    print(f"Status: {result['status']}")
    print(f"Total Time: {result['execution_time']:.1f}s ({result['execution_time']/60:.1f} minutes)")

    if result["status"] == "completed":
        print("\n📊 Task Results:")
        for task_id, task_result in result["results"].items():
            print(f"\n  {task_id.upper()}:")
            print(f"    Agent: {task_result['agent']}")
            print(f"    Duration: {task_result['duration']:.1f}s")
            print(f"    Status: {task_result['result'].get('status', 'N/A')}")

        # Show validation results
        validation = result["results"]["validate"]["result"]
        print(f"\n✅ Validation Results:")
        print(f"    Result: {validation.get('validation_result', 'N/A')}")
        print(f"    Quality Score: {validation.get('quality_score', 0)}/100")
        print(f"    Issues Found: {len(validation.get('issues', []))}")

        if validation.get('issues'):
            print(f"\n    Issues:")
            for issue in validation['issues'][:3]:
                print(f"      - {issue}")

    db.close()
    print("\n✅ Example 1 complete!\n")


async def example_2_multi_source_comparison():
    """
    Example 2: Multi-Source Comparison Workflow

    Flow: Research (parallel) → Analysis → Synthesis

    This workflow demonstrates parallel execution:
    1. Multiple research queries executed simultaneously
    2. Analysis agent compares results
    3. Synthesis agent creates unified answer
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Multi-Source Comparison Workflow")
    print("="*70)

    # Initialize services
    db = SessionLocal()
    qdrant = get_qdrant_client()
    ollama = OllamaService()
    rag = RAGService(db, qdrant, ollama)

    # Initialize agents
    legal_agent = LegalResearchAgent(ollama, rag)
    analysis_agent = AnalysisAgent(ollama)
    synthesis_agent = SynthesisAgent(ollama)

    # Create orchestrator
    orchestrator = WorkflowOrchestrator()
    orchestrator.register_agent(legal_agent)
    orchestrator.register_agent(analysis_agent)
    orchestrator.register_agent(synthesis_agent)

    # Define workflow with parallel tasks
    workflow_definition = {
        "tasks": [
            # Note: In a real implementation, you'd use orchestrator.execute_parallel_tasks()
            # For this example, we show sequential but conceptually parallel queries
            {
                "task_id": "research1",
                "agent": "legal_research",
                "input": {
                    "question": "What is the Buildings Ordinance?",
                    "top_k": 3
                }
            },
            {
                "task_id": "research2",
                "agent": "legal_research",
                "input": {
                    "question": "What are building safety regulations?",
                    "top_k": 3
                }
            },
            {
                "task_id": "compare",
                "agent": "analysis",
                "input": {
                    "analysis_type": "comparison",
                    "data": [
                        "${research1.answer}",
                        "${research2.answer}"
                    ],
                    "focus": "building regulations"
                }
            },
            {
                "task_id": "synthesize",
                "agent": "synthesis",
                "input": {
                    "synthesis_type": "merge",
                    "sources": [
                        "${research1}",
                        "${research2}",
                        "${compare}"
                    ],
                    "focus": "comprehensive building regulations"
                }
            }
        ],
        "output_var": "synthesize"
    }

    orchestrator.register_workflow("multi_source_comparison", workflow_definition)

    # Execute workflow
    print("\n⏳ Executing multi-source comparison workflow...")
    print("   This will take 15-20 minutes with llama3.3:70b\n")

    result = await orchestrator.execute_workflow(
        "multi_source_comparison",
        {"question": "Tell me about building regulations"}
    )

    # Display results
    print("\n" + "="*70)
    print("WORKFLOW RESULTS")
    print("="*70)
    print(f"Status: {result['status']}")
    print(f"Total Time: {result['execution_time']:.1f}s")

    if result["status"] == "completed":
        synthesis_result = result["results"]["synthesize"]["result"]
        print(f"\n📝 Synthesized Output Preview:")
        output = synthesis_result.get("synthesized_output", "")
        print(f"   {output[:300]}...")

    db.close()
    print("\n✅ Example 2 complete!\n")


async def example_3_simple_orchestration():
    """
    Example 3: Simple 2-Agent Orchestration

    Flow: Research → Validation

    Simplest workflow to test orchestration basics.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Simple Research + Validation")
    print("="*70)

    # Initialize services
    db = SessionLocal()
    qdrant = get_qdrant_client()
    ollama = OllamaService()
    rag = RAGService(db, qdrant, ollama)

    # Initialize agents
    legal_agent = LegalResearchAgent(ollama, rag)
    validation_agent = ValidationAgent(ollama)

    # Create orchestrator
    orchestrator = WorkflowOrchestrator()
    orchestrator.register_agent(legal_agent)
    orchestrator.register_agent(validation_agent)

    # Define simple workflow
    workflow_definition = {
        "tasks": [
            {
                "task_id": "research",
                "agent": "legal_research",
                "input": {
                    "question": "${input.question}",
                    "top_k": 3
                }
            },
            {
                "task_id": "validate",
                "agent": "validation",
                "input": {
                    "validation_type": "completeness",
                    "content": "${research.answer}",
                    "question": "${input.question}"
                }
            }
        ],
        "output_var": "validate"
    }

    orchestrator.register_workflow("simple_research_validation", workflow_definition)

    # Execute workflow
    print("\n⏳ Executing simple workflow...")
    print("   Question: 'What is Cap. 123?'\n")

    result = await orchestrator.execute_workflow(
        "simple_research_validation",
        {"question": "What is Cap. 123?"}
    )

    # Display results
    print("\n" + "="*70)
    print("WORKFLOW RESULTS")
    print("="*70)
    print(f"Status: {result['status']}")
    print(f"Total Time: {result['execution_time']:.1f}s")

    if result["status"] == "completed":
        validation = result["results"]["validate"]["result"]
        print(f"\n✅ Validation:")
        print(f"    Result: {validation.get('validation_result')}")
        print(f"    Quality: {validation.get('quality_score')}/100")

    # Show orchestrator statistics
    stats = orchestrator.get_statistics()
    print(f"\n📊 Orchestrator Statistics:")
    print(f"    Total Executions: {stats['total_executions']}")
    print(f"    Success Rate: {stats['success_rate']*100:.1f}%")
    print(f"    Avg Duration: {stats['avg_duration']:.1f}s")

    db.close()
    print("\n✅ Example 3 complete!\n")


async def main():
    """Run workflow examples"""
    print("\n" + "="*70)
    print("MULTI-AGENT WORKFLOW EXAMPLES")
    print("="*70)
    print("Demonstrating orchestration of multiple specialized agents")
    print("="*70)

    examples = [
        ("Simple Research + Validation", example_3_simple_orchestration),
        ("Multi-Source Comparison", example_2_multi_source_comparison),
        ("Comprehensive Legal Research", example_1_comprehensive_legal_research)
    ]

    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\n" + "="*70)
    print("Note: Each example takes 5-20 minutes with llama3.3:70b")
    print("Choose an example to run or run all sequentially")
    print("="*70)

    # For now, run example 3 (simplest) as demonstration
    print("\nRunning Example 3 (simplest) as demonstration...")

    try:
        await example_3_simple_orchestration()
    except Exception as e:
        logger.error(f"Example failed: {e}", exc_info=True)

    print("\n" + "="*70)
    print("EXAMPLES COMPLETE")
    print("="*70)
    print("\nTo run other examples:")
    print("  - Uncomment the desired example in main()")
    print("  - Or call the example function directly")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())
