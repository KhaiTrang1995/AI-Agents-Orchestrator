"""Adapter for LlamaCpp local modal."""

from typing import Any, Dict, List
import httpx
from .base import AgentCapability, AgentResponse, BaseAdapter

class LlamaCppAdapter(BaseAdapter):
    """Adapter for interacting with LlamaCpp local modal."""
    def __init__(self, config):
      """Initializes the LlamaCpp adapter."""
      super().__init__(config)
      self.endpoint = config.get("endpoint", "http://localhost:8080")
      self.model_path = config.get("model_path", None)

    def get_capabilities(self) -> List[AgentCapability]:
          """Return the capabilities of the LlamaCpp local agent."""
          return [
              AgentCapability.IMPLEMENTATION,
              AgentCapability.CODE_REVIEW,
              AgentCapability.REFACTORING,
              AgentCapability.TESTING,
              AgentCapability.DOCUMENTATION,
          ]

    def execute_task(self, task: str, context: Dict[str, Any]) -> AgentResponse:
        """Execute a task using LlamaCpp Code."""
        prompt = self._build_system_prompt(task,context)

        try:
            response = httpx.post(
                f"{self.endpoint}/v1/completions",
                json={
                    "prompt": prompt,
                    "max_tokens": 4096,
                    "temperature": 0.7,
                    "stop": ["```\n\n", "Human:", "User:"]
                },
                timeout=self.timeout,
            )

            response.raise_for_status()
            data = response.json()

            choices = data.get("choices", [])
            text = choices[0].get("text", "") if choices else ""

            return AgentResponse(
                success=True,
                output=text,
                metadata={
                    "provider": "llama.cpp",
                    "endpoint": self.endpoint,
                },
            )

        except Exception as e:
            self.logger.error(f"llama.cpp execution failed: {e}", exc_info=True)
            return AgentResponse(
                success=False,
                output="",
                error=str(e),
            )

    def _build_system_prompt(self, task: str, context: Dict[str, Any]) -> str:
        parts = []

        role = context.get("role", "general")

        if role == "implement":
            parts.append("You are an expert software engineer.")
            parts.append(f"Implement the following task:\n{task}")

        elif role == "review":
            parts.append("You are an expert code reviewer.")
            parts.append(f"Review the following task:\n{task}")

        elif role == "refine":
            parts.append("Improve the implementation based on feedback.")
            parts.append(f"Task:\n{task}")

        elif role == "test":
            parts.append(f"Write tests for:\n{task}")

        elif role == "document":
            parts.append(f"Write documentation for:\n{task}")

        else:
            parts.append(task)

        if context.get("previous_output"):
            parts.append("\nPrevious Output:")
            parts.append(context["previous_output"])

        return "\n\n".join(parts)
