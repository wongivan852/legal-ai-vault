"""
Analysis Agent
Specialized agent for data analysis, pattern recognition, and insights extraction
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import json

from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class AnalysisAgent(BaseAgent):
    """
    Agent specialized in analyzing data, identifying patterns, and extracting insights.

    Capabilities:
    - Analyze text data for patterns and themes
    - Compare multiple data sources
    - Extract key insights and summaries
    - Identify risks and opportunities
    - Generate structured analysis reports
    """

    def __init__(self, llm_service):
        """
        Initialize analysis agent

        Args:
            llm_service: OllamaService for LLM reasoning
        """
        super().__init__(
            name="analysis",
            llm_service=llm_service,
            description="Specialized agent for data analysis, pattern recognition, and insights extraction"
        )

        # Register available tools
        self.add_tool(
            "extract_themes",
            self._extract_themes,
            "Extract key themes from text data"
        )
        self.add_tool(
            "compare_sources",
            self._compare_sources,
            "Compare multiple data sources and identify differences"
        )
        self.add_tool(
            "identify_risks",
            self._identify_risks,
            "Identify potential risks in provided data"
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute analysis task

        Args:
            task: Task specification with the following keys:
                - analysis_type: Type of analysis ("themes", "comparison", "risk", "summary", "structured")
                - data: Data to analyze (text, list of texts, or structured data)
                - focus: Optional focus area for analysis
                - output_format: "text" or "structured" (default: "structured")

        Returns:
            Dict with:
                - agent: Agent name
                - status: "completed" or "failed"
                - analysis: Analysis results
                - insights: Key insights extracted
                - confidence: Confidence level
                - execution_time: Processing time
        """
        start_time = datetime.now()

        try:
            analysis_type = task.get("analysis_type", "summary")
            data = task.get("data")
            focus = task.get("focus", "general")
            output_format = task.get("output_format", "structured")

            if not data:
                return {
                    "agent": self.name,
                    "status": "failed",
                    "error": "No data provided for analysis"
                }

            logger.info(f"Analysis agent executing: {analysis_type}")

            # Route to appropriate analysis method
            if analysis_type == "themes":
                result = await self._analyze_themes(data, focus)
            elif analysis_type == "comparison":
                result = await self._analyze_comparison(data, focus)
            elif analysis_type == "risk":
                result = await self._analyze_risks(data, focus)
            elif analysis_type == "summary":
                result = await self._analyze_summary(data, focus)
            elif analysis_type == "structured":
                result = await self._analyze_structured(data, focus)
            else:
                return {
                    "agent": self.name,
                    "status": "failed",
                    "error": f"Unknown analysis type: {analysis_type}"
                }

            # Store in memory
            self.add_to_memory({
                "timestamp": datetime.now().isoformat(),
                "type": "analysis",
                "analysis_type": analysis_type,
                "data_length": len(str(data))
            })

            return {
                "agent": self.name,
                "status": "completed",
                "analysis_type": analysis_type,
                "analysis": result["analysis"],
                "insights": result.get("insights", []),
                "confidence": result.get("confidence", "medium"),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

        except Exception as e:
            logger.error(f"Analysis agent execution error: {e}", exc_info=True)
            return {
                "agent": self.name,
                "status": "failed",
                "error": str(e),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

    async def _analyze_themes(self, data: Any, focus: str) -> Dict[str, Any]:
        """
        Analyze data to extract key themes

        Args:
            data: Data to analyze
            focus: Focus area

        Returns:
            Dict with themes and insights
        """
        data_text = self._prepare_data_text(data)

        prompt = f"""
Analyze the following data and extract the key themes and patterns.

Focus Area: {focus}

Data:
{data_text[:3000]}

Please identify:
1. Main themes (3-5 key themes)
2. Supporting evidence for each theme
3. Frequency/prominence of each theme

Respond in JSON format:
{{
    "themes": [
        {{"theme": "theme name", "evidence": "supporting evidence", "prominence": "high|medium|low"}},
        ...
    ],
    "overall_pattern": "description of overall pattern"
}}
"""

        response = await self.think(
            prompt,
            system_prompt="You are a data analysis expert. Extract themes and patterns objectively."
        )

        try:
            # Try to parse JSON response
            parsed = json.loads(response)
            themes = parsed.get("themes", [])
            insights = [t["theme"] for t in themes]

            return {
                "analysis": parsed,
                "insights": insights,
                "confidence": "high" if len(themes) >= 3 else "medium"
            }
        except json.JSONDecodeError:
            # Fallback to text response
            return {
                "analysis": {"themes": [], "raw_response": response},
                "insights": [],
                "confidence": "low"
            }

    async def _analyze_comparison(self, data: Any, focus: str) -> Dict[str, Any]:
        """
        Compare multiple data sources

        Args:
            data: List of data sources or dict with sources
            focus: Focus area

        Returns:
            Dict with comparison results
        """
        if not isinstance(data, (list, dict)):
            data = [data]

        data_text = self._prepare_data_text(data)

        prompt = f"""
Compare and contrast the following data sources.

Focus: {focus}

Data:
{data_text[:3000]}

Please identify:
1. Key similarities across sources
2. Key differences between sources
3. Contradictions or conflicts
4. Overall assessment

Respond in JSON format:
{{
    "similarities": ["similarity 1", "similarity 2", ...],
    "differences": ["difference 1", "difference 2", ...],
    "conflicts": ["conflict 1", ...],
    "assessment": "overall assessment"
}}
"""

        response = await self.think(
            prompt,
            system_prompt="You are a comparative analysis expert. Compare sources objectively."
        )

        try:
            parsed = json.loads(response)
            insights = parsed.get("similarities", []) + parsed.get("differences", [])

            return {
                "analysis": parsed,
                "insights": insights[:5],  # Top 5 insights
                "confidence": "high"
            }
        except json.JSONDecodeError:
            return {
                "analysis": {"raw_response": response},
                "insights": [],
                "confidence": "low"
            }

    async def _analyze_risks(self, data: Any, focus: str) -> Dict[str, Any]:
        """
        Identify risks in data

        Args:
            data: Data to analyze for risks
            focus: Focus area

        Returns:
            Dict with risk assessment
        """
        data_text = self._prepare_data_text(data)

        prompt = f"""
Analyze the following data and identify potential risks, issues, or concerns.

Focus: {focus}

Data:
{data_text[:3000]}

Please identify:
1. High-priority risks (critical issues)
2. Medium-priority risks (important concerns)
3. Low-priority risks (minor issues)
4. Recommended actions for each risk

Respond in JSON format:
{{
    "high_priority": [
        {{"risk": "description", "impact": "impact", "action": "recommended action"}},
        ...
    ],
    "medium_priority": [...],
    "low_priority": [...],
    "overall_risk_level": "high|medium|low"
}}
"""

        response = await self.think(
            prompt,
            system_prompt="You are a risk assessment expert. Identify risks objectively and provide actionable recommendations."
        )

        try:
            parsed = json.loads(response)
            all_risks = (
                parsed.get("high_priority", []) +
                parsed.get("medium_priority", []) +
                parsed.get("low_priority", [])
            )
            insights = [r.get("risk", "") for r in all_risks if r.get("risk")]

            return {
                "analysis": parsed,
                "insights": insights[:5],
                "confidence": "high"
            }
        except json.JSONDecodeError:
            return {
                "analysis": {"raw_response": response},
                "insights": [],
                "confidence": "low"
            }

    async def _analyze_summary(self, data: Any, focus: str) -> Dict[str, Any]:
        """
        Generate comprehensive summary of data

        Args:
            data: Data to summarize
            focus: Focus area

        Returns:
            Dict with summary
        """
        data_text = self._prepare_data_text(data)

        prompt = f"""
Provide a comprehensive summary and analysis of the following data.

Focus: {focus}

Data:
{data_text[:3000]}

Please provide:
1. Executive summary (2-3 sentences)
2. Key points (3-5 main points)
3. Important details
4. Conclusions and implications

Keep your response clear and concise.
"""

        response = await self.think(
            prompt,
            system_prompt="You are an expert analyst. Provide clear, concise summaries."
        )

        # Extract key points as insights
        lines = response.split('\n')
        insights = [line.strip('- ').strip() for line in lines if line.strip().startswith('-')][:5]

        return {
            "analysis": {
                "summary": response,
                "type": "summary"
            },
            "insights": insights,
            "confidence": "medium"
        }

    async def _analyze_structured(self, data: Any, focus: str) -> Dict[str, Any]:
        """
        Perform structured analysis with multiple dimensions

        Args:
            data: Data to analyze
            focus: Focus area

        Returns:
            Dict with structured analysis
        """
        data_text = self._prepare_data_text(data)

        prompt = f"""
Perform a structured multi-dimensional analysis of the following data.

Focus: {focus}

Data:
{data_text[:3000]}

Analyze across these dimensions:
1. Content Analysis: What is being communicated?
2. Context Analysis: What is the broader context?
3. Quality Assessment: How reliable/accurate is this?
4. Implications: What are the implications?
5. Actionable Insights: What should be done?

Respond in JSON format:
{{
    "content": "content analysis",
    "context": "context analysis",
    "quality": "quality assessment",
    "implications": ["implication 1", ...],
    "actions": ["action 1", ...]
}}
"""

        response = await self.think(
            prompt,
            system_prompt="You are a comprehensive analyst. Provide structured, multi-dimensional analysis.",
            temperature=0.2  # Lower temperature for more structured output
        )

        try:
            parsed = json.loads(response)
            insights = parsed.get("implications", []) + parsed.get("actions", [])

            return {
                "analysis": parsed,
                "insights": insights[:5],
                "confidence": "high"
            }
        except json.JSONDecodeError:
            return {
                "analysis": {"raw_response": response},
                "insights": [],
                "confidence": "low"
            }

    def _prepare_data_text(self, data: Any) -> str:
        """
        Convert data to text for analysis

        Args:
            data: Data in any format

        Returns:
            Text representation
        """
        if isinstance(data, str):
            return data
        elif isinstance(data, list):
            return "\n\n---\n\n".join(str(item) for item in data)
        elif isinstance(data, dict):
            return json.dumps(data, indent=2)
        else:
            return str(data)

    async def _extract_themes(self, text: str, num_themes: int = 5) -> List[str]:
        """
        Tool: Extract themes from text

        Args:
            text: Text to analyze
            num_themes: Number of themes to extract

        Returns:
            List of themes
        """
        result = await self._analyze_themes(text, "general")
        themes = result.get("analysis", {}).get("themes", [])
        return [t.get("theme", "") for t in themes[:num_themes]]

    async def _compare_sources(self, sources: List[str]) -> Dict[str, Any]:
        """
        Tool: Compare multiple sources

        Args:
            sources: List of text sources

        Returns:
            Comparison results
        """
        result = await self._analyze_comparison(sources, "general")
        return result.get("analysis", {})

    async def _identify_risks(self, text: str) -> List[Dict[str, str]]:
        """
        Tool: Identify risks in text

        Args:
            text: Text to analyze for risks

        Returns:
            List of risk items
        """
        result = await self._analyze_risks(text, "general")
        analysis = result.get("analysis", {})
        return (
            analysis.get("high_priority", []) +
            analysis.get("medium_priority", [])
        )
