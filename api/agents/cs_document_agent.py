"""
Customer Service Document Agent
Specialized agent for customer service knowledge base and ticket handling
Reference agent for demonstrating CS domain capabilities
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import json

from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class CSDocumentAgent(BaseAgent):
    """
    Agent specialized in customer service documentation and support.

    Capabilities:
    - Search help documentation and FAQs
    - Generate customer responses
    - Route tickets to appropriate teams
    - Suggest solutions to common problems
    - Escalate complex issues

    This is a reference implementation showing CS domain capabilities.
    In production, this would connect to a CS knowledge base and ticketing system.
    """

    def __init__(self, llm_service, knowledge_base: Optional[Any] = None):
        """
        Initialize CS document agent

        Args:
            llm_service: OllamaService for LLM reasoning
            knowledge_base: Optional CS knowledge base
        """
        super().__init__(
            name="cs_document",
            llm_service=llm_service,
            description="Specialized agent for customer service documentation and ticket handling"
        )
        self.knowledge_base = knowledge_base

        # Register available tools
        self.add_tool(
            "search_help_docs",
            self._search_help_docs,
            "Search help documentation and FAQs"
        )
        self.add_tool(
            "generate_ticket_response",
            self._generate_ticket_response,
            "Generate response for customer ticket"
        )
        self.add_tool(
            "route_ticket",
            self._route_ticket,
            "Route ticket to appropriate team"
        )
        self.add_tool(
            "escalate_to_human",
            self._escalate_to_human,
            "Escalate ticket to human agent"
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute CS task

        Args:
            task: Task specification with the following keys:
                - task_type: "search", "respond", "route", "escalate" (default: "respond")
                - ticket: Customer ticket/question
                - customer_info: Optional customer information
                - priority: Optional priority level (low, medium, high, urgent)
                - category: Optional ticket category

        Returns:
            Dict with:
                - agent: Agent name
                - status: "completed" or "failed"
                - response: Generated response or action result
                - routing: Routing recommendation (if applicable)
                - escalation_needed: Boolean indicating if escalation needed
                - confidence: Confidence level
                - execution_time: Processing time
        """
        start_time = datetime.now()

        try:
            task_type = task.get("task_type", "respond")
            ticket = task.get("ticket")

            if not ticket:
                return {
                    "agent": self.name,
                    "status": "failed",
                    "error": "No ticket or question provided"
                }

            customer_info = task.get("customer_info", {})
            priority = task.get("priority", "medium")
            category = task.get("category", "general")

            logger.info(f"CS agent executing: {task_type} - priority: {priority}")

            # Route to appropriate handler
            if task_type == "search":
                result = await self._handle_search(ticket, category)
            elif task_type == "respond":
                result = await self._handle_respond(ticket, customer_info, category)
            elif task_type == "route":
                result = await self._handle_route(ticket, priority, category)
            elif task_type == "escalate":
                result = await self._handle_escalate(ticket, priority, customer_info)
            else:
                return {
                    "agent": self.name,
                    "status": "failed",
                    "error": f"Unknown task type: {task_type}"
                }

            # Store in memory
            self.add_to_memory({
                "timestamp": datetime.now().isoformat(),
                "type": "cs_task",
                "task_type": task_type,
                "category": category,
                "priority": priority
            })

            return {
                "agent": self.name,
                "status": "completed",
                "task_type": task_type,
                "response": result["response"],
                "routing": result.get("routing"),
                "escalation_needed": result.get("escalation_needed", False),
                "confidence": result.get("confidence", "medium"),
                "suggested_actions": result.get("suggested_actions", []),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

        except Exception as e:
            logger.error(f"CS agent execution error: {e}", exc_info=True)
            return {
                "agent": self.name,
                "status": "failed",
                "error": str(e),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

    async def _handle_search(self, query: str, category: str) -> Dict[str, Any]:
        """
        Handle help documentation search

        Args:
            query: Search query
            category: Ticket category

        Returns:
            Dict with search results
        """
        # In production, this would search a CS knowledge base

        prompt = f"""
You are a customer service knowledge base search system. Find relevant help articles for this query.

Query: {query}
Category: {category}

Provide:
1. List of 3-5 most relevant help articles (with titles and summaries)
2. Key information from those articles
3. Quick answer if possible

Format as JSON:
{{
    "quick_answer": "Brief answer if applicable",
    "articles": [
        {{"title": "Article title", "summary": "Article summary", "relevance": "high/medium/low"}},
        ...
    ],
    "additional_info": "Any additional helpful information"
}}
"""

        response = await self.think(
            prompt,
            system_prompt="You are a customer service knowledge base. Provide accurate, helpful information.",
            temperature=0.2
        )

        try:
            parsed = json.loads(response)
            return {
                "response": parsed.get("quick_answer", "See articles below"),
                "articles": parsed.get("articles", []),
                "confidence": "high" if parsed.get("quick_answer") else "medium"
            }
        except json.JSONDecodeError:
            return {
                "response": response,
                "confidence": "low"
            }

    async def _handle_respond(
        self,
        ticket: str,
        customer_info: Dict[str, Any],
        category: str
    ) -> Dict[str, Any]:
        """
        Handle ticket response generation

        Args:
            ticket: Customer ticket/question
            customer_info: Customer information
            category: Ticket category

        Returns:
            Dict with response
        """
        customer_context = f"Customer type: {customer_info.get('type', 'standard')}" if customer_info else ""

        prompt = f"""
You are a professional customer service agent. Generate a helpful, empathetic response to this customer ticket.

Ticket: {ticket}
Category: {category}
{customer_context}

Your response should:
1. Acknowledge the customer's concern
2. Provide a clear, helpful answer or solution
3. Offer next steps if needed
4. Be professional but warm in tone
5. Include a call-to-action or offer for further help

Generate the response:
"""

        response = await self.think(
            prompt,
            system_prompt="You are an experienced customer service professional. Help customers effectively and empathetically.",
            temperature=0.4
        )

        # Determine if escalation is needed
        escalation_keywords = ["urgent", "escalate", "manager", "refund", "cancel", "complaint", "legal"]
        needs_escalation = any(keyword in ticket.lower() for keyword in escalation_keywords)

        return {
            "response": response,
            "escalation_needed": needs_escalation,
            "confidence": "high",
            "suggested_actions": ["Send response", "Escalate to supervisor"] if needs_escalation else ["Send response"]
        }

    async def _handle_route(
        self,
        ticket: str,
        priority: str,
        category: str
    ) -> Dict[str, Any]:
        """
        Handle ticket routing

        Args:
            ticket: Customer ticket
            priority: Priority level
            category: Ticket category

        Returns:
            Dict with routing recommendation
        """
        prompt = f"""
You are a ticket routing system. Analyze this ticket and recommend the best team to handle it.

Ticket: {ticket}
Priority: {priority}
Category: {category}

Available teams:
- Technical Support: Technical issues, bugs, errors
- Billing: Payment, invoices, subscriptions
- Account Management: Account access, settings, profile
- Product Support: Product questions, how-to, features
- Escalations: Urgent issues, complaints, legal

Respond in JSON:
{{
    "recommended_team": "Team name",
    "reasoning": "Why this team",
    "priority_adjustment": "Should priority be adjusted? (same/higher/lower)",
    "estimated_response_time": "Estimated time to first response"
}}
"""

        response = await self.think(
            prompt,
            system_prompt="You are a ticket routing expert. Route tickets efficiently.",
            temperature=0.1
        )

        try:
            parsed = json.loads(response)
            return {
                "response": f"Route to {parsed.get('recommended_team', 'General Support')}",
                "routing": parsed,
                "confidence": "high"
            }
        except json.JSONDecodeError:
            return {
                "response": response,
                "routing": {"recommended_team": "General Support"},
                "confidence": "medium"
            }

    async def _handle_escalate(
        self,
        ticket: str,
        priority: str,
        customer_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle ticket escalation

        Args:
            ticket: Customer ticket
            priority: Priority level
            customer_info: Customer information

        Returns:
            Dict with escalation details
        """
        prompt = f"""
You are a customer service escalation specialist. Prepare an escalation summary for this ticket.

Ticket: {ticket}
Current Priority: {priority}
Customer Info: {customer_info}

Provide:
1. Escalation summary (for supervisor)
2. Key issues to address
3. Recommended actions
4. Suggested priority level

Be concise but comprehensive.
"""

        response = await self.think(
            prompt,
            system_prompt="You are an escalation specialist. Prepare clear, actionable escalation summaries.",
            temperature=0.2
        )

        return {
            "response": response,
            "escalation_needed": True,
            "routing": {"recommended_team": "Escalations"},
            "confidence": "high",
            "suggested_actions": [
                "Notify supervisor",
                "Update priority to urgent",
                "Assign to senior agent"
            ]
        }

    async def _search_help_docs(
        self,
        query: str,
        category: str = "all",
        max_results: int = 5
    ) -> List[Dict[str, str]]:
        """
        Tool: Search help documentation

        Args:
            query: Search query
            category: Category filter
            max_results: Maximum number of results

        Returns:
            List of help articles
        """
        result = await self._handle_search(query, category)
        return result.get("articles", [])[:max_results]

    async def _generate_ticket_response(
        self,
        ticket: str,
        customer_type: str = "standard"
    ) -> str:
        """
        Tool: Generate ticket response

        Args:
            ticket: Customer ticket
            customer_type: Type of customer

        Returns:
            Response text
        """
        result = await self._handle_respond(
            ticket,
            {"type": customer_type},
            "general"
        )
        return result["response"]

    async def _route_ticket(
        self,
        ticket: str,
        priority: str = "medium"
    ) -> Dict[str, str]:
        """
        Tool: Route ticket to team

        Args:
            ticket: Customer ticket
            priority: Priority level

        Returns:
            Routing recommendation
        """
        result = await self._handle_route(ticket, priority, "general")
        return result.get("routing", {"recommended_team": "General Support"})

    async def _escalate_to_human(
        self,
        ticket: str,
        reason: str = "Complex issue requiring human review"
    ) -> Dict[str, Any]:
        """
        Tool: Escalate to human agent

        Args:
            ticket: Customer ticket
            reason: Escalation reason

        Returns:
            Escalation details
        """
        result = await self._handle_escalate(
            ticket,
            "high",
            {"escalation_reason": reason}
        )

        return {
            "escalated": True,
            "summary": result["response"],
            "actions": result.get("suggested_actions", [])
        }
