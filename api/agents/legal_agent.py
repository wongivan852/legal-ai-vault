"""
Legal Research Agent
Specialized agent for legal document search and analysis using RAG
"""

from typing import Dict, Any, Optional
import logging
from datetime import datetime

from agents.base_agent import BaseAgent
from services.rag_service import RAGService

logger = logging.getLogger(__name__)


class LegalResearchAgent(BaseAgent):
    """
    Agent specialized in legal research using the existing RAG system.

    Capabilities:
    - Search Hong Kong legal ordinances
    - Retrieve relevant legal sections
    - Provide citations and sources
    - Answer legal questions with grounded responses
    """

    def __init__(self, llm_service, rag_service: RAGService):
        """
        Initialize legal research agent

        Args:
            llm_service: OllamaService for LLM reasoning
            rag_service: RAGService for legal document search
        """
        super().__init__(
            name="legal_research",
            llm_service=llm_service,
            description="Specialized agent for Hong Kong legal ordinance research and analysis"
        )
        self.rag = rag_service

        # Register available tools
        self.add_tool(
            "search_ordinances",
            self._search_ordinances,
            "Search Hong Kong legal ordinances by keyword or question"
        )
        self.add_tool(
            "get_document",
            self._get_document,
            "Retrieve full legal document by name or number"
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute legal research task

        Args:
            task: Task specification with the following keys:
                - question: Legal question to answer
                - top_k: Number of results to retrieve (default: 5)
                - search_type: "documents" or "sections" (default: "sections")
                - min_score: Minimum similarity score (default: 0.3)
                - include_reasoning: Whether to include reasoning (default: False)

        Returns:
            Dict with:
                - agent: Agent name
                - status: "completed" or "failed"
                - answer: Generated answer
                - sources: List of source documents/sections
                - confidence: "high", "medium", or "low"
                - reasoning: Optional reasoning trace
                - execution_time: Processing time in seconds
        """
        start_time = datetime.now()

        try:
            # Extract task parameters
            question = task.get("question")
            if not question:
                return {
                    "agent": self.name,
                    "status": "failed",
                    "error": "No question provided"
                }

            top_k = task.get("top_k", 5)
            search_type = task.get("search_type", "sections")
            min_score = task.get("min_score", 0.3)
            include_reasoning = task.get("include_reasoning", False)

            logger.info(f"Legal agent executing: {question}")

            # Use RAG to search legal documents
            result = await self.rag.query(
                question=question,
                top_k=top_k,
                search_type=search_type,
                min_score=min_score
            )

            # Determine confidence based on retrieval quality
            confidence = self._calculate_confidence(result)

            # Store in memory
            self.add_to_memory({
                "timestamp": datetime.now().isoformat(),
                "type": "task_execution",
                "question": question,
                "confidence": confidence,
                "sources_count": len(result.get("sources", []))
            })

            # Build response
            response = {
                "agent": self.name,
                "status": "completed",
                "answer": result.get("answer", ""),
                "sources": result.get("sources", []),
                "confidence": confidence,
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

            # Add reasoning if requested
            if include_reasoning:
                response["reasoning"] = await self._generate_reasoning(question, result)

            return response

        except Exception as e:
            logger.error(f"Legal agent execution error: {e}", exc_info=True)
            return {
                "agent": self.name,
                "status": "failed",
                "error": str(e),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

    def _calculate_confidence(self, result: Dict[str, Any]) -> str:
        """
        Calculate confidence level based on RAG results

        Args:
            result: RAG query result

        Returns:
            "high", "medium", or "low"
        """
        retrieved_count = result.get("retrieved_count", 0)
        sources = result.get("sources", [])

        # Check if we have high-scoring sources
        if sources:
            avg_score = sum(s.get("score", 0) for s in sources) / len(sources)

            if retrieved_count >= 3 and avg_score >= 0.7:
                return "high"
            elif retrieved_count >= 2 and avg_score >= 0.5:
                return "medium"

        return "low" if retrieved_count == 0 else "medium"

    async def _generate_reasoning(self, question: str, result: Dict[str, Any]) -> str:
        """
        Generate reasoning about the answer

        Args:
            question: Original question
            result: RAG result

        Returns:
            Reasoning text
        """
        reasoning_prompt = f"""
You are analyzing a legal research query and its results.

Question: {question}

Number of sources found: {result.get('retrieved_count', 0)}
Answer quality: {len(result.get('answer', ''))} characters

Please briefly explain:
1. Why these sources are relevant
2. The confidence level of the answer
3. Any limitations or gaps

Keep it concise (2-3 sentences).
"""

        try:
            reasoning = await self.think(
                reasoning_prompt,
                system_prompt="You are a legal research analyst."
            )
            return reasoning
        except Exception as e:
            logger.error(f"Reasoning generation failed: {e}")
            return "Reasoning unavailable"

    async def _search_ordinances(
        self,
        query: str,
        top_k: int = 5,
        search_type: str = "sections"
    ) -> Dict[str, Any]:
        """
        Tool: Search ordinances directly

        Args:
            query: Search query
            top_k: Number of results
            search_type: "documents" or "sections"

        Returns:
            Search results
        """
        return await self.rag.query(
            question=query,
            top_k=top_k,
            search_type=search_type
        )

    async def _get_document(self, doc_name: str) -> Optional[Dict[str, Any]]:
        """
        Tool: Get full document by name

        Args:
            doc_name: Document name or number

        Returns:
            Document data or None
        """
        # This would integrate with the database service
        # For now, return placeholder
        logger.info(f"Getting document: {doc_name}")
        return {
            "doc_name": doc_name,
            "status": "not_implemented",
            "message": "Direct document retrieval to be implemented"
        }

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get agent statistics and performance metrics

        Returns:
            Dict with statistics
        """
        executions = [m for m in self.memory if m.get("type") == "task_execution"]

        if not executions:
            return {
                "total_queries": 0,
                "avg_confidence": "N/A",
                "total_sources": 0
            }

        confidences = [e.get("confidence") for e in executions]
        confidence_counts = {
            "high": confidences.count("high"),
            "medium": confidences.count("medium"),
            "low": confidences.count("low")
        }

        return {
            "total_queries": len(executions),
            "confidence_distribution": confidence_counts,
            "total_sources": sum(e.get("sources_count", 0) for e in executions),
            "avg_sources_per_query": sum(e.get("sources_count", 0) for e in executions) / len(executions)
        }
