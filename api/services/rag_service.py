"""
RAG (Retrieval Augmented Generation) Service for Legal AI Vault

Combines vector search with LLM generation to provide accurate,
grounded answers based on Hong Kong legal documents.
"""

import logging
from typing import List, Dict, Optional, Any
from qdrant_client import QdrantClient
from qdrant_client.models import ScoredPoint

from services.ollama_service import OllamaService
from models.hk_legal_document import HKLegalDocument
from models.hk_legal_section import HKLegalSection
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class RAGService:
    """Service for Retrieval Augmented Generation"""

    def __init__(
        self,
        db_session: Session,
        qdrant_client: QdrantClient,
        ollama_service: OllamaService
    ):
        self.db = db_session
        self.qdrant = qdrant_client
        self.ollama = ollama_service

    async def query(
        self,
        question: str,
        top_k: int = 5,
        search_type: str = "sections",  # "documents" or "sections"
        min_score: float = 0.5,
        include_metadata: bool = True,
        max_context_length: int = 4000
    ) -> Dict[str, Any]:
        """
        Perform RAG query: retrieve relevant context and generate answer

        Args:
            question: User's question
            top_k: Number of results to retrieve
            search_type: "documents" or "sections"
            min_score: Minimum similarity score (0-1)
            include_metadata: Include source metadata in response
            max_context_length: Maximum characters for context

        Returns:
            Dict with answer, sources, and metadata
        """
        try:
            # Step 1: Generate embedding for the question
            logger.info(f"Generating embedding for question: {question[:100]}...")
            query_embedding = await self.ollama.embed(question)

            # Step 2: Search vector database
            logger.info(f"Searching {search_type} with top_k={top_k}")
            search_results = await self._search_vectors(
                query_embedding,
                search_type,
                top_k
            )

            # Step 3: Filter by score and retrieve full content
            relevant_results = [r for r in search_results if r.score >= min_score]

            if not relevant_results:
                return {
                    "success": False,
                    "answer": "I couldn't find any relevant information in the Hong Kong legal database to answer your question.",
                    "sources": [],
                    "context_used": "",
                    "retrieved_count": 0
                }

            logger.info(f"Found {len(relevant_results)} relevant results (score >= {min_score})")

            # Step 4: Retrieve full content from database
            context_items = await self._retrieve_full_content(
                relevant_results,
                search_type
            )

            # Step 5: Format context for LLM
            formatted_context = self._format_context(
                context_items,
                max_context_length
            )

            # Step 6: Generate answer using LLM
            logger.info("Generating answer with LLM...")
            answer = await self._generate_answer(
                question,
                formatted_context
            )

            # Step 7: Prepare sources metadata
            sources = self._prepare_sources(context_items) if include_metadata else []

            return {
                "success": True,
                "answer": answer,
                "sources": sources,
                "context_used": formatted_context[:500] + "..." if len(formatted_context) > 500 else formatted_context,
                "retrieved_count": len(relevant_results),
                "search_type": search_type
            }

        except Exception as e:
            logger.error(f"RAG query failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "answer": "An error occurred while processing your question.",
                "sources": []
            }

    async def _search_vectors(
        self,
        query_embedding: List[float],
        search_type: str,
        top_k: int
    ) -> List[ScoredPoint]:
        """Search Qdrant for similar vectors"""
        collection_name = (
            "hk_legal_sections" if search_type == "sections"
            else "hk_legal_documents"
        )

        # Use search method compatible with Qdrant 1.8.0
        from qdrant_client.models import SearchRequest

        search_results = self.qdrant.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=top_k
        )

        return search_results

    async def _retrieve_full_content(
        self,
        search_results: List[ScoredPoint],
        search_type: str
    ) -> List[Dict]:
        """Retrieve full content from database"""
        context_items = []

        for result in search_results:
            db_id = result.payload.get("db_id")

            if search_type == "sections":
                section = self.db.query(HKLegalSection).filter(
                    HKLegalSection.id == db_id
                ).first()

                if section:
                    # Get parent document info
                    document = section.document
                    context_items.append({
                        "type": "section",
                        "score": result.score,
                        "doc_number": document.doc_number,
                        "doc_name": document.doc_name,
                        "doc_title": document.title,
                        "section_number": section.section_number,
                        "section_heading": section.heading,
                        "content": section.content,
                        "doc_id": document.id,
                        "section_id": section.id
                    })
            else:
                document = self.db.query(HKLegalDocument).filter(
                    HKLegalDocument.id == db_id
                ).first()

                if document:
                    context_items.append({
                        "type": "document",
                        "score": result.score,
                        "doc_number": document.doc_number,
                        "doc_name": document.doc_name,
                        "doc_title": document.title,
                        "content": document.full_text,
                        "doc_id": document.id
                    })

        return context_items

    def _format_context(
        self,
        context_items: List[Dict],
        max_length: int
    ) -> str:
        """Format retrieved context for LLM prompt"""
        context_parts = []
        current_length = 0

        for item in context_items:
            if item["type"] == "section":
                part = f"""
--- {item['doc_name']}: {item['doc_title']} ---
Section {item['section_number']}: {item['section_heading']}

{item['content']}
"""
            else:
                part = f"""
--- {item['doc_name']}: {item['doc_title']} ---

{item['content'][:1000]}...
"""

            part_length = len(part)
            if current_length + part_length > max_length:
                break

            context_parts.append(part)
            current_length += part_length

        return "\n".join(context_parts)

    async def _generate_answer(
        self,
        question: str,
        context: str
    ) -> str:
        """Generate answer using LLM with retrieved context"""

        system_prompt = """You are a Hong Kong legal expert assistant. Your role is to provide accurate information based on Hong Kong legislation.

IMPORTANT INSTRUCTIONS:
1. Answer questions using ONLY the provided legal context
2. Cite specific ordinances, sections, and legal provisions
3. If the context doesn't contain enough information, clearly state this
4. Do not make up or infer legal information not in the context
5. Use clear, professional language
6. Format your response with proper structure and citations

Always reference the specific Cap. number and section when citing law."""

        user_prompt = f"""Based on the following Hong Kong legal documents, please answer this question:

QUESTION: {question}

LEGAL CONTEXT:
{context}

Please provide a comprehensive answer based on the legal context above. Cite specific ordinances and sections where applicable."""

        # Generate response
        response = await self.ollama.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=1000,
            temperature=0.3  # Lower temperature for more factual responses
        )

        return response["response"]

    def _prepare_sources(self, context_items: List[Dict]) -> List[Dict]:
        """Prepare source citations"""
        sources = []

        for item in context_items:
            source = {
                "doc_number": item["doc_number"],
                "doc_name": item["doc_name"],
                "doc_title": item["doc_title"],
                "score": round(item["score"], 3),
                "type": item["type"]
            }

            if item["type"] == "section":
                source["section_number"] = item["section_number"]
                source["section_heading"] = item["section_heading"]
                source["preview"] = item["content"][:200] + "..."
            else:
                source["preview"] = item["content"][:200] + "..."

            sources.append(source)

        return sources
