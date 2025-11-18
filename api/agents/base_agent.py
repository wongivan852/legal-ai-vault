"""
Base Agent Class for Agentic AI Platform
Provides foundation for all specialized agents
"""

from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the platform.

    All specialized agents (Legal, Research, Analysis, etc.) inherit from this class
    and implement the execute() method for their specific functionality.
    """

    def __init__(self, name: str, llm_service, description: str = ""):
        """
        Initialize base agent

        Args:
            name: Unique identifier for this agent
            llm_service: OllamaService instance for LLM reasoning
            description: Human-readable description of agent capabilities
        """
        self.name = name
        self.llm = llm_service
        self.description = description
        self.tools = []
        self.memory = []

        logger.info(f"Initialized agent: {name}")

    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent task (must be implemented by subclass)

        Args:
            task: Task specification with inputs and parameters

        Returns:
            Dict with execution results, status, and metadata
        """
        pass

    def add_tool(self, tool_name: str, tool_func, description: str = ""):
        """
        Register a tool that this agent can use

        Args:
            tool_name: Unique name for the tool
            tool_func: Callable function or coroutine
            description: What the tool does
        """
        self.tools.append({
            "name": tool_name,
            "func": tool_func,
            "description": description
        })
        logger.info(f"Agent {self.name} registered tool: {tool_name}")

    async def think(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3
    ) -> str:
        """
        Use LLM to reason about a problem

        Args:
            prompt: The question or problem to reason about
            system_prompt: Optional system instruction for the LLM
            temperature: Sampling temperature (0.0-1.0)

        Returns:
            LLM's response text
        """
        try:
            result = await self.llm.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature
            )
            return result["response"]
        except Exception as e:
            logger.error(f"Agent {self.name} thinking error: {e}")
            raise

    async def use_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Execute a registered tool

        Args:
            tool_name: Name of tool to execute
            **kwargs: Tool parameters

        Returns:
            Tool execution result
        """
        tool = next((t for t in self.tools if t["name"] == tool_name), None)
        if not tool:
            raise ValueError(f"Tool {tool_name} not found in agent {self.name}")

        try:
            # Handle both sync and async tools
            import asyncio
            if asyncio.iscoroutinefunction(tool["func"]):
                return await tool["func"](**kwargs)
            else:
                return tool["func"](**kwargs)
        except Exception as e:
            logger.error(f"Tool {tool_name} execution error: {e}")
            raise

    def add_to_memory(self, item: Dict[str, Any]):
        """
        Add item to agent's short-term memory

        Args:
            item: Memory item (should include timestamp, type, content)
        """
        self.memory.append(item)

        # Keep memory limited (last 100 items)
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]

    def get_memory(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve recent memory items

        Args:
            count: Number of recent items to retrieve

        Returns:
            List of memory items (most recent first)
        """
        return list(reversed(self.memory[-count:]))

    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get agent's capabilities and tools

        Returns:
            Dict describing agent capabilities
        """
        return {
            "name": self.name,
            "description": self.description,
            "tools": [
                {"name": t["name"], "description": t["description"]}
                for t in self.tools
            ],
            "memory_items": len(self.memory)
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name} tools={len(self.tools)}>"
