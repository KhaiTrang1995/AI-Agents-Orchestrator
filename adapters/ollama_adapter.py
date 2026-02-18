"""Adapter for Ollama local model."""

from typing import Any, Dict, List
import httpx
from .base import AgentCapability, AgentResponse, BaseAdapter

class OllamaAdapter(BaseAdapter):
    """Adapter for interacting with Ollama local model."""
    def __init__(self, config):
      """Initializes the Ollama adapter."""
      super().__init__(config)
      self.model = config.get("model", "codellama:13b")
      self.endpoint = config.get("endpoint", "http://localhost:11434")

    def get_capabilities(self) -> List[AgentCapability]:
          """Return the capabilities of the Ollama agent."""
          return [
              AgentCapability.IMPLEMENTATION,
              AgentCapability.CODE_REVIEW,
              AgentCapability.REFACTORING,
              AgentCapability.TESTING,
              AgentCapability.DOCUMENTATION,
          ]
    
    def execute_task(self, task: str, context: Dict[str, Any]) -> AgentResponse:
        """Execute a task using Ollama Code.
        
        Ollama is typically used for implementation and quick refinement tasks.

        """
        prompt = self._build_system_prompt(task,context)

        try:

          response = httpx.post(
              f"{self.endpoint}/api/generate",
              json={
                  "model": self.model,
                    "prompt": prompt,
                    "stream": False
              },
              timeout=self.timeout,
          )

          response.raise_for_status()
          data = response.json()

          return AgentResponse(
              success=True,
              output=data.get("response", ""),
              metadata={
                  "provider": "ollama",
                  "model": self.model,
              },
          )
        except httpx.HTTPStatusError as e:
            self.logger.error(f"Ollama returned error status: {e}", exc_info=True)
            return AgentResponse(
                success=False,
                output="",
                error=f"HTTP error: {str(e)}",
            )

        except httpx.RequestError as e:
            self.logger.error(f"Ollama request failed: {e}", exc_info=True)
            return AgentResponse(
                success=False,
                output="",
                error=f"Connection error: {str(e)}",
            )
        except Exception as e:
            self.logger.error(f"Ollama execution failed: {e}", exc_info=True)
            return AgentResponse(
                success=False,
                output="",
                error=str(e),
            )
    
    def _build_system_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """Build a detailed prompt for Ollama"""
        parts = []
        role = context.get("role", "general")
        
        if role == "implement":
            parts.append("You are an expert software engineer.")
            parts.append("Implement the following task with clean, production-ready code.")
            parts.append(f"\nTask:\n{task}")

        elif role == "review":
            parts.append("You are an expert code reviewer.")
            parts.append("Review the following implementation and provide actionable feedback.")
            parts.append(f"\nTask:\n{task}")

            if context.get("implementation"):
                parts.append("\nImplementation to Review:\n")
                parts.append("```")
                parts.append(context["implementation"])
                parts.append("```")

        elif role == "refine":
            parts.append("You are refining code based on review feedback.")
            parts.append(f"\nTask:\n{task}")

            if context.get("feedback"):
                parts.append("\nReview Feedback:\n")
                parts.append(context["feedback"])

            if context.get("implementation"):
                parts.append("\nCurrent Implementation:\n")
                parts.append("```")
                parts.append(context["implementation"])
                parts.append("```")

            parts.append("\nPlease improve the implementation while preserving functionality.")

        elif role == "test":
            parts.append("Write comprehensive tests for the following task.")
            parts.append(f"\nTask:\n{task}")

        elif role == "document":
            parts.append("Write clear documentation for the following implementation.")
            parts.append(f"\nTask:\n{task}")

        else:
            parts.append(task)

        # Common quality instructions
        parts.append("\n\nGeneral Requirements:")
        parts.append("- Follow clean code principles")
        parts.append("- Use proper error handling")
        parts.append("- Ensure readability and maintainability")
        parts.append("- Keep the solution concise but complete")

        # Include previous output if exists
        if context.get("previous_output"):
            parts.append("\n\nPrevious Output:")
            parts.append(context["previous_output"])

        return "\n".join(parts)
        
    def is_available(self) -> bool:
        try:
            resp = httpx.get(f"{self.endpoint}/api/tags", timeout=5)
            return resp.status_code == 200
        except Exception:
            return False
    
    def list_models(self) -> list[str]:
        """Return available models on the Ollama server."""
        try:
            resp = httpx.get(f"{self.endpoint}/api/tags")
            resp.raise_for_status()
            return [m["name"] for m in resp.json().get("models", [])]
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            self.logger.error(f"Failed to list Ollama models: {e}")
            return []
