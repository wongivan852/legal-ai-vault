"""
Synthesis Agent
Specialized agent for combining multiple sources and generating cohesive outputs
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import json

from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class SynthesisAgent(BaseAgent):
    """
    Agent specialized in synthesizing information from multiple sources.

    Capabilities:
    - Combine multiple data sources into unified output
    - Reconcile conflicting information
    - Generate comprehensive reports
    - Create executive summaries
    - Merge and deduplicate content
    """

    def __init__(self, llm_service):
        """
        Initialize synthesis agent

        Args:
            llm_service: OllamaService for LLM reasoning
        """
        super().__init__(
            name="synthesis",
            llm_service=llm_service,
            description="Specialized agent for synthesizing information from multiple sources"
        )

        # Register available tools
        self.add_tool(
            "merge_sources",
            self._merge_sources,
            "Merge multiple sources into unified content"
        )
        self.add_tool(
            "reconcile_conflicts",
            self._reconcile_conflicts,
            "Reconcile conflicting information from sources"
        )
        self.add_tool(
            "generate_report",
            self._generate_report,
            "Generate comprehensive report from multiple inputs"
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute synthesis task

        Args:
            task: Task specification with the following keys:
                - synthesis_type: Type of synthesis ("merge", "reconcile", "report", "summary")
                - sources: List of source data/results to synthesize
                - focus: Optional focus for synthesis
                - format: Output format ("text", "structured", "markdown")
                - question: Original question/goal (for context)

        Returns:
            Dict with:
                - agent: Agent name
                - status: "completed" or "failed"
                - synthesized_output: Combined/synthesized result
                - sources_used: Number of sources processed
                - conflicts_resolved: Number of conflicts handled
                - execution_time: Processing time
        """
        start_time = datetime.now()

        try:
            synthesis_type = task.get("synthesis_type", "merge")
            sources = task.get("sources", [])
            focus = task.get("focus", "comprehensive")
            output_format = task.get("format", "text")
            question = task.get("question", "")

            if not sources:
                return {
                    "agent": self.name,
                    "status": "failed",
                    "error": "No sources provided for synthesis"
                }

            logger.info(f"Synthesis agent executing: {synthesis_type} on {len(sources)} sources")

            # Route to appropriate synthesis method
            if synthesis_type == "merge":
                result = await self._synthesize_merge(sources, focus, output_format)
            elif synthesis_type == "reconcile":
                result = await self._synthesize_reconcile(sources, focus, output_format)
            elif synthesis_type == "report":
                result = await self._synthesize_report(sources, question, focus, output_format)
            elif synthesis_type == "summary":
                result = await self._synthesize_summary(sources, question, focus)
            else:
                return {
                    "agent": self.name,
                    "status": "failed",
                    "error": f"Unknown synthesis type: {synthesis_type}"
                }

            # Store in memory
            self.add_to_memory({
                "timestamp": datetime.now().isoformat(),
                "type": "synthesis",
                "synthesis_type": synthesis_type,
                "sources_count": len(sources)
            })

            return {
                "agent": self.name,
                "status": "completed",
                "synthesis_type": synthesis_type,
                "synthesized_output": result["output"],
                "sources_used": len(sources),
                "conflicts_resolved": result.get("conflicts_resolved", 0),
                "quality_score": result.get("quality_score", "N/A"),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

        except Exception as e:
            logger.error(f"Synthesis agent execution error: {e}", exc_info=True)
            return {
                "agent": self.name,
                "status": "failed",
                "error": str(e),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

    async def _synthesize_merge(
        self,
        sources: List[Any],
        focus: str,
        output_format: str
    ) -> Dict[str, Any]:
        """
        Merge multiple sources into unified content

        Args:
            sources: List of sources to merge
            focus: Focus area
            output_format: Desired output format

        Returns:
            Dict with merged output
        """
        sources_text = self._prepare_sources_text(sources)

        prompt = f"""
Merge the following sources into a unified, coherent output.

Focus: {focus}
Output Format: {output_format}

Sources:
{sources_text[:4000]}

Instructions:
1. Combine all relevant information from sources
2. Remove redundancy and duplication
3. Maintain important details from each source
4. Create a logical, coherent structure
5. Cite sources where appropriate

Provide the merged output:
"""

        response = await self.think(
            prompt,
            system_prompt="You are an expert at synthesizing information from multiple sources. Create coherent, comprehensive outputs.",
            temperature=0.3
        )

        return {
            "output": response,
            "quality_score": self._assess_quality(response, len(sources))
        }

    async def _synthesize_reconcile(
        self,
        sources: List[Any],
        focus: str,
        output_format: str
    ) -> Dict[str, Any]:
        """
        Reconcile conflicting information from sources

        Args:
            sources: List of sources (may contain conflicts)
            focus: Focus area
            output_format: Desired output format

        Returns:
            Dict with reconciled output
        """
        sources_text = self._prepare_sources_text(sources)

        prompt = f"""
Analyze the following sources and reconcile any conflicting information.

Focus: {focus}

Sources:
{sources_text[:4000]}

Instructions:
1. Identify conflicts and contradictions between sources
2. Evaluate reliability and credibility of each source
3. Provide reconciled information with reasoning
4. Note where conflicts cannot be resolved
5. Present a balanced, objective synthesis

Respond in JSON format:
{{
    "conflicts_identified": [
        {{"conflict": "description", "sources": ["source 1", "source 2"], "resolution": "how it was resolved"}},
        ...
    ],
    "reconciled_output": "the reconciled comprehensive answer",
    "unresolved_conflicts": ["conflict 1", ...]
}}
"""

        response = await self.think(
            prompt,
            system_prompt="You are an expert at reconciling conflicting information objectively.",
            temperature=0.2
        )

        try:
            parsed = json.loads(response)
            conflicts_resolved = len(parsed.get("conflicts_identified", []))
            output_text = parsed.get("reconciled_output", response)

            return {
                "output": output_text,
                "conflicts_resolved": conflicts_resolved,
                "conflicts_detail": parsed.get("conflicts_identified", []),
                "unresolved": parsed.get("unresolved_conflicts", []),
                "quality_score": "high" if conflicts_resolved > 0 else "medium"
            }
        except json.JSONDecodeError:
            return {
                "output": response,
                "conflicts_resolved": 0,
                "quality_score": "medium"
            }

    async def _synthesize_report(
        self,
        sources: List[Any],
        question: str,
        focus: str,
        output_format: str
    ) -> Dict[str, Any]:
        """
        Generate comprehensive report from multiple sources

        Args:
            sources: List of source data
            question: Original question/goal
            focus: Focus area
            output_format: Desired format

        Returns:
            Dict with report
        """
        sources_text = self._prepare_sources_text(sources)

        prompt = f"""
Generate a comprehensive report based on the following sources.

Original Question: {question}
Focus: {focus}
Output Format: {output_format}

Sources:
{sources_text[:4000]}

Create a report with:
1. Executive Summary (2-3 sentences)
2. Key Findings (bullet points)
3. Detailed Analysis (main body)
4. Conclusions and Recommendations
5. Sources Referenced

Structure the report clearly and professionally:
"""

        response = await self.think(
            prompt,
            system_prompt="You are an expert report writer. Create clear, comprehensive, well-structured reports.",
            temperature=0.3
        )

        # Assess report quality based on structure
        has_sections = all(
            marker in response.lower()
            for marker in ["summary", "findings", "conclusion"]
        )

        return {
            "output": response,
            "quality_score": "high" if has_sections else "medium"
        }

    async def _synthesize_summary(
        self,
        sources: List[Any],
        question: str,
        focus: str
    ) -> Dict[str, Any]:
        """
        Generate executive summary from multiple sources

        Args:
            sources: List of source data
            question: Original question
            focus: Focus area

        Returns:
            Dict with summary
        """
        sources_text = self._prepare_sources_text(sources)

        prompt = f"""
Create an executive summary based on the following sources.

Question: {question}
Focus: {focus}

Sources:
{sources_text[:4000]}

Provide:
1. Executive Summary (3-5 sentences capturing the essence)
2. Top 3 Key Insights
3. Main Recommendation (if applicable)

Keep it concise and actionable:
"""

        response = await self.think(
            prompt,
            system_prompt="You are an expert at creating concise, actionable executive summaries.",
            temperature=0.3
        )

        return {
            "output": response,
            "quality_score": "high" if len(response) < 1000 else "medium"
        }

    def _prepare_sources_text(self, sources: List[Any]) -> str:
        """
        Prepare sources for synthesis

        Args:
            sources: List of sources

        Returns:
            Formatted text of all sources
        """
        formatted_sources = []

        for i, source in enumerate(sources, 1):
            if isinstance(source, dict):
                # Extract relevant fields from dict
                if "answer" in source:
                    text = source["answer"]
                elif "result" in source:
                    text = str(source["result"])
                elif "analysis" in source:
                    text = str(source["analysis"])
                else:
                    text = json.dumps(source, indent=2)

                # Add source metadata if available
                source_name = source.get("agent", source.get("source", f"Source {i}"))
                formatted_sources.append(f"## {source_name}\n\n{text}")
            else:
                formatted_sources.append(f"## Source {i}\n\n{str(source)}")

        return "\n\n---\n\n".join(formatted_sources)

    def _assess_quality(self, output: str, num_sources: int) -> str:
        """
        Assess quality of synthesized output

        Args:
            output: Synthesized text
            num_sources: Number of sources used

        Returns:
            Quality score: "high", "medium", or "low"
        """
        # Simple heuristic-based quality assessment
        if len(output) < 100:
            return "low"

        # Check if output references multiple sources
        has_integration = num_sources > 1 and (
            "both" in output.lower() or
            "multiple" in output.lower() or
            "sources" in output.lower()
        )

        # Check for structure
        has_structure = output.count('\n') > 3

        if has_integration and has_structure:
            return "high"
        elif has_integration or has_structure:
            return "medium"
        else:
            return "low"

    async def _merge_sources(
        self,
        sources: List[str],
        remove_duplicates: bool = True
    ) -> str:
        """
        Tool: Merge multiple text sources

        Args:
            sources: List of text sources
            remove_duplicates: Whether to deduplicate content

        Returns:
            Merged text
        """
        result = await self._synthesize_merge(sources, "comprehensive", "text")
        return result["output"]

    async def _reconcile_conflicts(
        self,
        conflicting_sources: List[str]
    ) -> Dict[str, Any]:
        """
        Tool: Reconcile conflicting information

        Args:
            conflicting_sources: List of sources with potential conflicts

        Returns:
            Reconciliation result
        """
        result = await self._synthesize_reconcile(
            conflicting_sources,
            "conflict_resolution",
            "structured"
        )
        return {
            "reconciled": result["output"],
            "conflicts_resolved": result.get("conflicts_resolved", 0)
        }

    async def _generate_report(
        self,
        sources: List[Any],
        title: str
    ) -> str:
        """
        Tool: Generate report from sources

        Args:
            sources: Data sources
            title: Report title

        Returns:
            Report text
        """
        result = await self._synthesize_report(
            sources,
            title,
            "comprehensive",
            "markdown"
        )
        return result["output"]
