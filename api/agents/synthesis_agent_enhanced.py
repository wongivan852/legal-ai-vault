"""
Enhanced Synthesis Agent with Document Embedding Integration

This agent extends the standard Synthesis Agent with the ability to
automatically retrieve relevant documents from the Qdrant vector database.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from agents.synthesis_agent import SynthesisAgent

logger = logging.getLogger(__name__)


class EnhancedSynthesisAgent(SynthesisAgent):
    """
    Synthesis Agent with automatic document retrieval from Qdrant

    Features:
    - Automatic document retrieval via RAG service
    - Semantic search for relevant legal documents
    - Backward compatible with manual source input
    - Duplicate detection across retrieved documents
    """

    def __init__(self, llm_service, rag_service=None):
        """
        Initialize enhanced synthesis agent

        Args:
            llm_service: OllamaService for LLM reasoning
            rag_service: Optional RAGService for document retrieval
        """
        super().__init__(llm_service)
        self.rag_service = rag_service

        # Update description
        self.description = "Synthesis agent with automatic document retrieval from legal database"

        logger.info("Enhanced Synthesis Agent initialized with RAG capability")

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute synthesis task with optional auto-retrieval

        Args:
            task: Task specification with:
                - auto_retrieve: bool - Enable automatic document retrieval
                - document_queries: List[str] - Queries for document retrieval
                - top_k_per_query: int - Number of docs to retrieve per query
                - min_score: float - Minimum similarity score (0-1)
                - question: str - Original user question (for context)
                - sources: List[Dict] - Manual sources (if auto_retrieve=False)
                - synthesis_type: str - Type of synthesis
                - focus: str - Focus area

        Returns:
            Dict with synthesis results
        """
        start_time = datetime.now()

        try:
            auto_retrieve = task.get("auto_retrieve", False)

            # Check if RAG service is available
            if auto_retrieve and not self.rag_service:
                logger.warning("Auto-retrieve requested but RAG service not available")
                return {
                    "agent": self.name,
                    "status": "failed",
                    "error": "Document auto-retrieval not available. RAG service not initialized."
                }

            if auto_retrieve:
                # Auto-retrieve documents from Qdrant
                logger.info("Auto-retrieving documents from Qdrant vector database...")
                sources = await self._retrieve_documents(task)

                if not sources:
                    return {
                        "agent": self.name,
                        "status": "failed",
                        "error": "No relevant documents found in database. Try adjusting your query or lowering min_score."
                    }

                # Update task with retrieved sources
                task["sources"] = sources
                logger.info(f"Successfully retrieved {len(sources)} unique documents for synthesis")

                # Add metadata about retrieval
                task["_retrieval_metadata"] = {
                    "retrieved_count": len(sources),
                    "auto_retrieved": True
                }

            # Execute standard synthesis with retrieved or manual sources
            return await super().execute(task)

        except Exception as e:
            logger.error(f"Enhanced synthesis execution error: {e}", exc_info=True)
            return {
                "agent": self.name,
                "status": "failed",
                "error": f"Synthesis failed: {str(e)}",
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

    async def _retrieve_documents(
        self,
        task: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Retrieve documents from Qdrant based on queries

        Args:
            task: Task containing document_queries and retrieval params

        Returns:
            List of retrieved documents formatted for synthesis
        """
        document_queries = task.get("document_queries", [])
        question = task.get("question", "")
        top_k_per_query = task.get("top_k_per_query", 5)
        min_score = task.get("min_score", 0.6)

        # If no document queries provided, use the main question
        if not document_queries:
            if question:
                document_queries = [question]
                logger.info(f"Using main question as document query: {question}")
            else:
                logger.error("No document queries or question provided")
                return []

        all_sources = []
        seen_docs = set()  # Prevent duplicates

        for idx, query in enumerate(document_queries, 1):
            logger.info(f"Query {idx}/{len(document_queries)}: Retrieving documents for '{query[:50]}...'")

            try:
                # Use RAG service to retrieve relevant documents
                result = await self.rag_service.query(
                    question=query,
                    top_k=top_k_per_query,
                    search_type="sections",  # Search at section level for more granular results
                    min_score=min_score,
                    include_metadata=True,
                    max_context_length=8000  # Allow more context
                )

                if result.get("success") and result.get("sources"):
                    logger.info(f"Query {idx}: Found {len(result['sources'])} relevant documents")

                    # Format sources for synthesis
                    for source in result["sources"]:
                        # Create unique identifier to prevent duplicates
                        doc_id = self._generate_doc_id(source)

                        if doc_id not in seen_docs:
                            seen_docs.add(doc_id)

                            # Format as synthesis source
                            formatted_source = self._format_source(source, query)
                            all_sources.append(formatted_source)
                        else:
                            logger.debug(f"Skipping duplicate document: {doc_id}")
                else:
                    logger.warning(f"Query {idx}: No results found or search failed")

            except Exception as e:
                logger.error(f"Error retrieving documents for query '{query}': {e}")
                # Continue with other queries

        logger.info(f"Total unique documents retrieved: {len(all_sources)} (from {len(document_queries)} queries)")

        # Sort by relevance score
        all_sources.sort(key=lambda x: x.get("score", 0), reverse=True)

        return all_sources

    def _generate_doc_id(self, source: Dict[str, Any]) -> str:
        """
        Generate unique identifier for a document to prevent duplicates

        Args:
            source: Source document from RAG service

        Returns:
            Unique identifier string
        """
        doc_number = source.get("doc_number", "")
        section_number = source.get("section_number", "")

        if section_number:
            return f"{doc_number}_{section_number}"
        else:
            return f"{doc_number}"

    def _format_source(
        self,
        source: Dict[str, Any],
        query: str
    ) -> Dict[str, Any]:
        """
        Format RAG source for synthesis

        Args:
            source: Source document from RAG service
            query: Query that retrieved this source

        Returns:
            Formatted source dict
        """
        # Extract content (prefer preview, fallback to content)
        content = source.get("preview", "")
        if not content:
            content = source.get("content", "")

        # Build descriptive title
        doc_name = source.get("doc_name", "Unknown Document")
        section_heading = source.get("section_heading", "")
        doc_title = source.get("doc_title", "")

        if section_heading:
            title = f"{doc_name} - {section_heading}"
        else:
            title = f"{doc_name} - {doc_title}"

        # Build source citation
        doc_number = source.get("doc_number", "N/A")
        section_number = source.get("section_number", "")

        if section_number:
            citation = f"Cap. {doc_number}, Section {section_number}"
        else:
            citation = f"Cap. {doc_number}"

        # Create formatted source
        formatted = {
            "title": title,
            "content": content,
            "source": citation,
            "score": round(source.get("score", 0), 3),
            "query": query,  # Track which query found this
            "metadata": {
                "doc_number": doc_number,
                "doc_name": doc_name,
                "doc_title": doc_title,
                "section_number": section_number,
                "type": source.get("type", "section"),
                "retrieved_by_query": query
            }
        }

        return formatted

    async def _synthesize_merge(
        self,
        sources: List[Any],
        focus: str,
        output_format: str
    ) -> Dict[str, Any]:
        """
        Override to handle enhanced source format with metadata

        Args:
            sources: List of sources (may include retrieval metadata)
            focus: Focus area
            output_format: Desired output format

        Returns:
            Dict with merged output
        """
        # Check if sources have metadata (from auto-retrieval)
        has_metadata = any(
            isinstance(s, dict) and "metadata" in s
            for s in sources
        )

        if has_metadata:
            # Enhanced formatting with citations
            sources_text = self._prepare_sources_with_citations(sources)
        else:
            # Standard formatting
            sources_text = self._prepare_sources_text(sources)

        prompt = f"""
Merge the following sources into a unified, coherent output.

Focus: {focus}
Output Format: {output_format}

Sources:
{sources_text[:5000]}

Instructions:
1. Combine all relevant information from sources
2. Remove redundancy and duplication
3. Maintain important details from each source
4. Create a logical, coherent structure
5. Cite sources properly (e.g., "According to Cap. 344, Section 12...")
6. Highlight any conflicts or variations between sources

Provide the merged output with proper citations:
"""

        response = await self.think(
            prompt,
            system_prompt="You are an expert at synthesizing legal information from multiple sources. Create coherent, comprehensive outputs with proper citations.",
            temperature=0.3
        )

        return {
            "output": response,
            "quality_score": self._assess_quality(response, len(sources)),
            "sources_with_citations": has_metadata
        }

    def _prepare_sources_with_citations(
        self,
        sources: List[Dict[str, Any]]
    ) -> str:
        """
        Prepare sources with enhanced citation information

        Args:
            sources: List of sources with metadata

        Returns:
            Formatted text with citations
        """
        formatted_sources = []

        for i, source in enumerate(sources, 1):
            title = source.get("title", f"Source {i}")
            content = source.get("content", "")
            citation = source.get("source", "N/A")
            score = source.get("score", 0)

            formatted = f"""
## Source {i}: {title}
**Citation**: {citation}
**Relevance Score**: {score:.2f}

{content}
"""
            formatted_sources.append(formatted)

        return "\n\n---\n\n".join(formatted_sources)
