"""
HR Policy Agent
Specialized agent for HR policies, employee handbooks, and HR-related queries
Reference agent for demonstrating multi-domain capabilities
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class HRPolicyAgent(BaseAgent):
    """
    Agent specialized in HR policies and employee-related queries.

    Capabilities:
    - Search HR policies and employee handbooks
    - Answer onboarding questions
    - Provide guidance on leave policies, benefits, etc.
    - Generate HR-related documents
    - Assist with compliance questions

    This is a reference implementation showing how domain agents work.
    In production, this would connect to an HR document database.
    """

    def __init__(self, llm_service, knowledge_base: Optional[Any] = None):
        """
        Initialize HR policy agent

        Args:
            llm_service: OllamaService for LLM reasoning
            knowledge_base: Optional HR knowledge base (similar to RAG for legal)
        """
        super().__init__(
            name="hr_policy",
            llm_service=llm_service,
            description="Specialized agent for HR policies, onboarding, and employee-related queries"
        )
        self.knowledge_base = knowledge_base

        # Register available tools
        self.add_tool(
            "search_policies",
            self._search_policies,
            "Search HR policies and employee handbook"
        )
        self.add_tool(
            "get_onboarding_info",
            self._get_onboarding_info,
            "Get onboarding information for new employees"
        )
        self.add_tool(
            "answer_hr_question",
            self._answer_hr_question,
            "Answer general HR-related questions"
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute HR policy task

        Args:
            task: Task specification with the following keys:
                - question: HR-related question
                - task_type: "policy_search", "onboarding", "benefits", "general" (default: "general")
                - context: Optional additional context
                - employee_type: Optional employee type (full-time, part-time, contractor)

        Returns:
            Dict with:
                - agent: Agent name
                - status: "completed" or "failed"
                - answer: Generated answer
                - policy_references: List of relevant policies
                - confidence: Confidence level
                - execution_time: Processing time
        """
        start_time = datetime.now()

        try:
            question = task.get("question")
            if not question:
                return {
                    "agent": self.name,
                    "status": "failed",
                    "error": "No question provided"
                }

            task_type = task.get("task_type", "general")
            context = task.get("context", "")
            employee_type = task.get("employee_type", "full-time")

            logger.info(f"HR agent executing: {task_type} - {question}")

            # Route to appropriate handler
            if task_type == "policy_search":
                result = await self._handle_policy_search(question, context)
            elif task_type == "onboarding":
                result = await self._handle_onboarding(question, employee_type)
            elif task_type == "benefits":
                result = await self._handle_benefits(question, employee_type)
            else:
                result = await self._handle_general(question, context)

            # Store in memory
            self.add_to_memory({
                "timestamp": datetime.now().isoformat(),
                "type": "hr_query",
                "task_type": task_type,
                "question": question[:100]
            })

            return {
                "agent": self.name,
                "status": "completed",
                "task_type": task_type,
                "answer": result["answer"],
                "policy_references": result.get("policy_references", []),
                "confidence": result.get("confidence", "medium"),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

        except Exception as e:
            logger.error(f"HR agent execution error: {e}", exc_info=True)
            return {
                "agent": self.name,
                "status": "failed",
                "error": str(e),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

    async def _handle_policy_search(self, question: str, context: str) -> Dict[str, Any]:
        """
        Handle policy search queries

        Args:
            question: Policy-related question
            context: Additional context

        Returns:
            Dict with answer and policy references
        """
        # In production, this would query an HR document database
        # For now, use LLM knowledge + reasoning

        prompt = f"""
You are an HR policy expert. Answer the following question about HR policies.

Question: {question}
Context: {context}

Provide:
1. A clear, concise answer
2. Relevant policy references (if applicable)
3. Any important caveats or exceptions

Format your response as:
Answer: [Your answer]
Policy References: [List of relevant policies]
Notes: [Any important notes]
"""

        response = await self.think(
            prompt,
            system_prompt="You are a knowledgeable HR professional. Provide accurate, helpful guidance on HR policies and procedures.",
            temperature=0.2
        )

        # Parse response
        answer_section = self._extract_section(response, "Answer:")
        policy_refs = self._extract_section(response, "Policy References:")

        return {
            "answer": answer_section or response,
            "policy_references": [policy_refs] if policy_refs else [],
            "confidence": "high" if policy_refs else "medium"
        }

    async def _handle_onboarding(self, question: str, employee_type: str) -> Dict[str, Any]:
        """
        Handle onboarding-related queries

        Args:
            question: Onboarding question
            employee_type: Type of employee

        Returns:
            Dict with answer
        """
        prompt = f"""
You are an HR onboarding specialist. Answer the following question for a {employee_type} employee.

Question: {question}

Provide a helpful, step-by-step answer that covers:
1. What the employee needs to do
2. Timeline/deadlines (if applicable)
3. Who to contact for help
4. Any required documents

Keep your answer clear and actionable.
"""

        response = await self.think(
            prompt,
            system_prompt="You are an experienced HR onboarding specialist. Help new employees navigate their first days smoothly.",
            temperature=0.3
        )

        return {
            "answer": response,
            "policy_references": ["Employee Onboarding Guide"],
            "confidence": "high"
        }

    async def _handle_benefits(self, question: str, employee_type: str) -> Dict[str, Any]:
        """
        Handle benefits-related queries

        Args:
            question: Benefits question
            employee_type: Type of employee

        Returns:
            Dict with answer
        """
        prompt = f"""
You are an HR benefits specialist. Answer the following question for a {employee_type} employee.

Question: {question}

Provide information about:
1. What benefits are available
2. Eligibility requirements
3. How to enroll or access benefits
4. Important deadlines

Be clear about any differences based on employment type.
"""

        response = await self.think(
            prompt,
            system_prompt="You are a benefits specialist. Provide clear, accurate information about employee benefits.",
            temperature=0.2
        )

        return {
            "answer": response,
            "policy_references": ["Employee Benefits Guide", "Benefits Enrollment Policy"],
            "confidence": "high"
        }

    async def _handle_general(self, question: str, context: str) -> Dict[str, Any]:
        """
        Handle general HR queries

        Args:
            question: General HR question
            context: Additional context

        Returns:
            Dict with answer
        """
        prompt = f"""
You are an HR professional. Answer the following question.

Question: {question}
Context: {context}

Provide a helpful, professional answer. If the question involves specific policies or procedures, reference them. If you're unsure, suggest who the employee should contact.
"""

        response = await self.think(
            prompt,
            system_prompt="You are a helpful HR professional. Provide clear, professional guidance.",
            temperature=0.3
        )

        return {
            "answer": response,
            "policy_references": [],
            "confidence": "medium"
        }

    def _extract_section(self, text: str, marker: str) -> Optional[str]:
        """
        Extract section from formatted response

        Args:
            text: Response text
            marker: Section marker

        Returns:
            Section content or None
        """
        if marker not in text:
            return None

        lines = text.split('\n')
        section_lines = []
        in_section = False

        for line in lines:
            if marker in line:
                in_section = True
                # Get content after marker
                content = line.split(marker, 1)[1].strip()
                if content:
                    section_lines.append(content)
                continue

            if in_section:
                if line.strip() and not any(m in line for m in ["Answer:", "Policy References:", "Notes:"]):
                    section_lines.append(line.strip())
                elif any(m in line for m in ["Answer:", "Policy References:", "Notes:"]):
                    break

        return '\n'.join(section_lines) if section_lines else None

    async def _search_policies(
        self,
        query: str,
        policy_type: str = "all"
    ) -> List[Dict[str, str]]:
        """
        Tool: Search HR policies

        Args:
            query: Search query
            policy_type: Type of policy to search

        Returns:
            List of policy results
        """
        # In production, this would query a real HR database
        # For demonstration, return structured results
        result = await self._handle_policy_search(query, f"Policy type: {policy_type}")

        return [{
            "title": "HR Policy Search Result",
            "content": result["answer"],
            "references": result.get("policy_references", [])
        }]

    async def _get_onboarding_info(
        self,
        employee_type: str = "full-time"
    ) -> Dict[str, Any]:
        """
        Tool: Get onboarding information

        Args:
            employee_type: Type of employee

        Returns:
            Onboarding information
        """
        result = await self._handle_onboarding(
            "What are the onboarding steps?",
            employee_type
        )

        return {
            "employee_type": employee_type,
            "onboarding_guide": result["answer"],
            "references": result.get("policy_references", [])
        }

    async def _answer_hr_question(
        self,
        question: str,
        context: str = ""
    ) -> str:
        """
        Tool: Answer general HR question

        Args:
            question: Question to answer
            context: Additional context

        Returns:
            Answer text
        """
        result = await self._handle_general(question, context)
        return result["answer"]
