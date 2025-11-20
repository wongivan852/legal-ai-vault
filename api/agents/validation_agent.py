"""
Validation Agent
Specialized agent for validating results, checking accuracy, and ensuring quality
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import json
import re

from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ValidationAgent(BaseAgent):
    """
    Agent specialized in validating results and ensuring quality.

    Capabilities:
    - Verify accuracy of information
    - Check completeness of responses
    - Validate against requirements
    - Identify errors and inconsistencies
    - Provide quality scores and feedback
    """

    def __init__(self, llm_service):
        """
        Initialize validation agent

        Args:
            llm_service: OllamaService for LLM reasoning
        """
        super().__init__(
            name="validation",
            llm_service=llm_service,
            description="Specialized agent for validating results and ensuring quality"
        )

        # Register available tools
        self.add_tool(
            "check_accuracy",
            self._check_accuracy,
            "Verify accuracy of information against sources"
        )
        self.add_tool(
            "check_completeness",
            self._check_completeness,
            "Check if response is complete"
        )
        self.add_tool(
            "check_consistency",
            self._check_consistency,
            "Check for internal consistency"
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute validation task

        Args:
            task: Task specification with the following keys:
                - validation_type: Type of validation ("accuracy", "completeness", "consistency", "comprehensive")
                - content: Content to validate
                - sources: Optional source data for verification
                - requirements: Optional requirements to validate against
                - question: Original question/goal for context

        Returns:
            Dict with:
                - agent: Agent name
                - status: "completed" or "failed"
                - validation_result: "passed", "failed", or "partial"
                - issues: List of issues found
                - quality_score: 0-100 score
                - recommendations: Suggested improvements
                - execution_time: Processing time
        """
        start_time = datetime.now()

        try:
            validation_type = task.get("validation_type", "comprehensive")
            content = task.get("content")
            sources = task.get("sources", [])
            requirements = task.get("requirements", [])
            question = task.get("question", "")

            if not content:
                return {
                    "agent": self.name,
                    "status": "failed",
                    "error": "No content provided for validation"
                }

            logger.info(f"Validation agent executing: {validation_type}")

            # Route to appropriate validation method
            if validation_type == "accuracy":
                result = await self._validate_accuracy(content, sources, question)
            elif validation_type == "completeness":
                result = await self._validate_completeness(content, question, requirements)
            elif validation_type == "consistency":
                result = await self._validate_consistency(content)
            elif validation_type == "comprehensive":
                result = await self._validate_comprehensive(content, sources, question, requirements)
            else:
                return {
                    "agent": self.name,
                    "status": "failed",
                    "error": f"Unknown validation type: {validation_type}"
                }

            # Store in memory
            self.add_to_memory({
                "timestamp": datetime.now().isoformat(),
                "type": "validation",
                "validation_type": validation_type,
                "result": result["validation_result"]
            })

            return {
                "agent": self.name,
                "status": "completed",
                "validation_type": validation_type,
                "validation_result": result["validation_result"],
                "issues": result["issues"],
                "quality_score": result["quality_score"],
                "recommendations": result.get("recommendations", []),
                "details": result.get("details", {}),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

        except Exception as e:
            logger.error(f"Validation agent execution error: {e}", exc_info=True)
            return {
                "agent": self.name,
                "status": "failed",
                "error": str(e),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

    async def _validate_accuracy(
        self,
        content: Any,
        sources: List[Any],
        question: str
    ) -> Dict[str, Any]:
        """
        Validate accuracy against sources

        Args:
            content: Content to validate
            sources: Source data for verification
            question: Original question

        Returns:
            Dict with validation results
        """
        content_text = self._prepare_content_text(content)
        sources_text = self._prepare_sources_text(sources)

        prompt = f"""
Validate the accuracy of the following content against the provided sources.

Original Question: {question}

Content to Validate:
{content_text[:2000]}

Sources for Verification:
{sources_text[:2000]}

Please check:
1. Are all claims supported by the sources?
2. Are there any factual errors?
3. Are there any misleading statements?
4. Are citations accurate?

Respond in JSON format:
{{
    "is_accurate": true/false,
    "unsupported_claims": ["claim 1", ...],
    "factual_errors": ["error 1", ...],
    "misleading_statements": ["statement 1", ...],
    "accuracy_score": 0-100,
    "recommendations": ["recommendation 1", ...]
}}
"""

        response = await self.think(
            prompt,
            system_prompt="You are a fact-checker. Verify accuracy objectively and thoroughly. You MUST respond with valid JSON only, no additional text.",
            temperature=0.1
        )

        try:
            # Try to extract JSON from markdown code blocks if present
            json_text = self._extract_json(response)
            parsed = json.loads(json_text)

            issues = (
                parsed.get("unsupported_claims", []) +
                parsed.get("factual_errors", []) +
                parsed.get("misleading_statements", [])
            )

            accuracy_score = parsed.get("accuracy_score", 50)

            validation_result = (
                "passed" if accuracy_score >= 80 else
                "partial" if accuracy_score >= 60 else
                "failed"
            )

            return {
                "validation_result": validation_result,
                "issues": issues,
                "quality_score": accuracy_score,
                "recommendations": parsed.get("recommendations", []),
                "details": parsed
            }
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to parse accuracy validation JSON: {e}")
            # Use fallback extraction to get useful information anyway
            return self._extract_fallback_validation(response, "accuracy")

    async def _validate_completeness(
        self,
        content: Any,
        question: str,
        requirements: List[str]
    ) -> Dict[str, Any]:
        """
        Validate completeness of response

        Args:
            content: Content to validate
            question: Original question
            requirements: List of requirements to check

        Returns:
            Dict with validation results
        """
        content_text = self._prepare_content_text(content)
        requirements_text = "\n".join(f"- {req}" for req in requirements) if requirements else "N/A"

        prompt = f"""
Evaluate the completeness of the following content.

Original Question: {question}

Requirements:
{requirements_text}

Content to Validate:
{content_text[:2500]}

Please check:
1. Does it fully answer the question?
2. Are all requirements addressed?
3. Are there significant gaps or missing information?
4. Is the level of detail appropriate?

Respond in JSON format:
{{
    "is_complete": true/false,
    "missing_elements": ["element 1", ...],
    "unaddressed_requirements": ["requirement 1", ...],
    "completeness_score": 0-100,
    "recommendations": ["recommendation 1", ...]
}}
"""

        response = await self.think(
            prompt,
            system_prompt="You are a quality assurance expert. Evaluate completeness objectively. You MUST respond with valid JSON only, no additional text.",
            temperature=0.1
        )

        try:
            # Try to extract JSON from markdown code blocks if present
            json_text = self._extract_json(response)
            parsed = json.loads(json_text)

            issues = (
                parsed.get("missing_elements", []) +
                parsed.get("unaddressed_requirements", [])
            )

            completeness_score = parsed.get("completeness_score", 50)

            validation_result = (
                "passed" if completeness_score >= 80 else
                "partial" if completeness_score >= 60 else
                "failed"
            )

            return {
                "validation_result": validation_result,
                "issues": issues,
                "quality_score": completeness_score,
                "recommendations": parsed.get("recommendations", []),
                "details": parsed
            }
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to parse completeness validation JSON: {e}")
            # Use fallback extraction to get useful information anyway
            return self._extract_fallback_validation(response, "completeness")

    async def _validate_consistency(self, content: Any) -> Dict[str, Any]:
        """
        Validate internal consistency

        Args:
            content: Content to validate

        Returns:
            Dict with validation results
        """
        content_text = self._prepare_content_text(content)

        prompt = f"""
Check the following content for internal consistency.

Content:
{content_text[:2500]}

Please check for:
1. Contradictions or conflicting statements
2. Logical inconsistencies
3. Inconsistent terminology or naming
4. Inconsistent formatting or structure

Respond in JSON format:
{{
    "is_consistent": true/false,
    "contradictions": ["contradiction 1", ...],
    "logical_issues": ["issue 1", ...],
    "terminology_issues": ["issue 1", ...],
    "consistency_score": 0-100,
    "recommendations": ["recommendation 1", ...]
}}
"""

        response = await self.think(
            prompt,
            system_prompt="You are a logic and consistency checker. Identify inconsistencies precisely. You MUST respond with valid JSON only, no additional text.",
            temperature=0.1
        )

        try:
            # Try to extract JSON from markdown code blocks if present
            json_text = self._extract_json(response)
            parsed = json.loads(json_text)

            issues = (
                parsed.get("contradictions", []) +
                parsed.get("logical_issues", []) +
                parsed.get("terminology_issues", [])
            )

            consistency_score = parsed.get("consistency_score", 50)

            validation_result = (
                "passed" if consistency_score >= 80 else
                "partial" if consistency_score >= 60 else
                "failed"
            )

            return {
                "validation_result": validation_result,
                "issues": issues,
                "quality_score": consistency_score,
                "recommendations": parsed.get("recommendations", []),
                "details": parsed
            }
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to parse consistency validation JSON: {e}")
            # Use fallback extraction to get useful information anyway
            return self._extract_fallback_validation(response, "consistency")

    async def _validate_comprehensive(
        self,
        content: Any,
        sources: List[Any],
        question: str,
        requirements: List[str]
    ) -> Dict[str, Any]:
        """
        Perform comprehensive validation across all dimensions

        Args:
            content: Content to validate
            sources: Source data
            question: Original question
            requirements: Requirements list

        Returns:
            Dict with comprehensive validation results
        """
        # Run all validation types
        accuracy_result = await self._validate_accuracy(content, sources, question)
        completeness_result = await self._validate_completeness(content, question, requirements)
        consistency_result = await self._validate_consistency(content)

        # Combine results
        all_issues = (
            accuracy_result["issues"] +
            completeness_result["issues"] +
            consistency_result["issues"]
        )

        # Calculate overall score (weighted average)
        overall_score = (
            accuracy_result["quality_score"] * 0.4 +
            completeness_result["quality_score"] * 0.3 +
            consistency_result["quality_score"] * 0.3
        )

        # Combine recommendations
        all_recommendations = list(set(
            accuracy_result.get("recommendations", []) +
            completeness_result.get("recommendations", []) +
            consistency_result.get("recommendations", [])
        ))

        validation_result = (
            "passed" if overall_score >= 80 else
            "partial" if overall_score >= 60 else
            "failed"
        )

        return {
            "validation_result": validation_result,
            "issues": all_issues,
            "quality_score": int(overall_score),
            "recommendations": all_recommendations[:5],  # Top 5
            "details": {
                "accuracy": accuracy_result,
                "completeness": completeness_result,
                "consistency": consistency_result
            }
        }

    def _extract_json(self, text: str) -> str:
        """
        Extract JSON from response text, handling markdown code blocks and various formats

        Args:
            text: Response text that may contain JSON

        Returns:
            Extracted JSON string
        """
        if not text or not text.strip():
            return "{}"

        # Strategy 1: Try to extract from markdown code blocks (```json or ```)
        json_match = re.search(r'```(?:json)?\s*(\{[^`]*?\})\s*```', text, re.DOTALL)
        if json_match:
            logger.debug("Extracted JSON from markdown code block")
            return json_match.group(1)

        # Strategy 2: Try to find the largest valid JSON object
        # This handles cases where JSON is embedded in narrative text
        json_objects = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if json_objects:
            # Return the longest JSON string (most likely to be complete)
            longest = max(json_objects, key=len)
            logger.debug(f"Extracted JSON object (length: {len(longest)})")
            return longest

        # Strategy 3: Try to find JSON with nested braces
        brace_match = re.search(r'\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}', text, re.DOTALL)
        if brace_match:
            logger.debug("Extracted nested JSON structure")
            return brace_match.group(0)

        # Strategy 4: Extract from "JSON:" or "Result:" prefixes
        prefix_match = re.search(r'(?:JSON|Result|Output):\s*(\{.*?\})', text, re.DOTALL | re.IGNORECASE)
        if prefix_match:
            logger.debug("Extracted JSON after label prefix")
            return prefix_match.group(1)

        logger.warning("Could not extract JSON structure, returning original text")
        return text

    def _extract_fallback_validation(self, response_text: str, validation_type: str) -> Dict[str, Any]:
        """
        Extract validation information from non-JSON responses as a fallback

        Args:
            response_text: The raw response text
            validation_type: Type of validation (accuracy, completeness, consistency)

        Returns:
            Dict with extracted validation information
        """
        logger.warning(f"Using fallback extraction for {validation_type} validation")

        issues = []
        recommendations = []
        score = 50  # Default neutral score

        # Try to extract score from text
        score_match = re.search(r'(?:score|rating)[:\s]*(\d+)', response_text, re.IGNORECASE)
        if score_match:
            score = min(100, max(0, int(score_match.group(1))))

        # Extract bullet points or numbered lists as issues
        issue_patterns = [
            r'(?:issue|problem|error|concern)[s]?[:\s]*\n((?:[-•*]\s*.+\n?)+)',
            r'(?:found|identified)[:\s]*\n((?:\d+[.)]\s*.+\n?)+)',
        ]

        for pattern in issue_patterns:
            matches = re.finditer(pattern, response_text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                items = re.findall(r'[-•*\d+.)]\s*(.+)', match.group(1))
                issues.extend([item.strip() for item in items if item.strip()])

        # Extract recommendations
        rec_patterns = [
            r'(?:recommend|suggest|should|improve)[:\s]*\n((?:[-•*]\s*.+\n?)+)',
            r'recommendations?[:\s]*\n((?:\d+[.)]\s*.+\n?)+)',
        ]

        for pattern in rec_patterns:
            matches = re.finditer(pattern, response_text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                items = re.findall(r'[-•*\d+.)]\s*(.+)', match.group(1))
                recommendations.extend([item.strip() for item in items if item.strip()])

        # If no issues found but response mentions problems, extract sentences
        if not issues and any(word in response_text.lower() for word in ['error', 'issue', 'problem', 'incorrect', 'missing']):
            sentences = re.split(r'[.!?]\s+', response_text)
            issues = [s.strip() for s in sentences[:3] if len(s.strip()) > 20][:3]

        # Determine result based on extracted info
        if not issues:
            validation_result = "passed"
            score = max(score, 80)
        elif len(issues) <= 2:
            validation_result = "partial"
            score = max(score, 60) if score < 60 else min(score, 79)
        else:
            validation_result = "failed"
            score = min(score, 59)

        return {
            "validation_result": validation_result,
            "issues": issues if issues else [f"Unable to parse {validation_type} validation fully - review may be incomplete"],
            "quality_score": score,
            "recommendations": recommendations[:5],  # Limit to top 5
            "details": {
                "raw_response_preview": response_text[:500] + "..." if len(response_text) > 500 else response_text,
                "extraction_method": "fallback"
            }
        }

    def _prepare_content_text(self, content: Any) -> str:
        """
        Prepare content for validation

        Args:
            content: Content in any format

        Returns:
            Text representation
        """
        if isinstance(content, str):
            return content
        elif isinstance(content, dict):
            if "answer" in content:
                return content["answer"]
            elif "result" in content:
                return str(content["result"])
            else:
                return json.dumps(content, indent=2)
        else:
            return str(content)

    def _prepare_sources_text(self, sources: List[Any]) -> str:
        """
        Prepare sources for validation

        Args:
            sources: List of sources

        Returns:
            Formatted text
        """
        if not sources:
            return "No sources provided"

        formatted = []
        for i, source in enumerate(sources, 1):
            if isinstance(source, dict):
                text = source.get("content", source.get("answer", str(source)))
            else:
                text = str(source)
            formatted.append(f"Source {i}: {text[:500]}...")

        return "\n\n".join(formatted)

    async def _check_accuracy(self, content: str, sources: List[str]) -> Dict[str, Any]:
        """
        Tool: Check accuracy

        Args:
            content: Content to check
            sources: Sources for verification

        Returns:
            Accuracy check result
        """
        result = await self._validate_accuracy(content, sources, "")
        return {
            "accurate": result["validation_result"] == "passed",
            "score": result["quality_score"],
            "issues": result["issues"]
        }

    async def _check_completeness(
        self,
        content: str,
        question: str,
        requirements: List[str] = None
    ) -> Dict[str, Any]:
        """
        Tool: Check completeness

        Args:
            content: Content to check
            question: Original question
            requirements: Optional requirements

        Returns:
            Completeness check result
        """
        result = await self._validate_completeness(
            content,
            question,
            requirements or []
        )
        return {
            "complete": result["validation_result"] == "passed",
            "score": result["quality_score"],
            "missing": result["issues"]
        }

    async def _check_consistency(self, content: str) -> Dict[str, Any]:
        """
        Tool: Check consistency

        Args:
            content: Content to check

        Returns:
            Consistency check result
        """
        result = await self._validate_consistency(content)
        return {
            "consistent": result["validation_result"] == "passed",
            "score": result["quality_score"],
            "issues": result["issues"]
        }
