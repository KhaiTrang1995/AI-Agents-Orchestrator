"""Adapter for LlamaCpp local model."""

from typing import Any, Dict, List
import httpx
from .base import AgentCapability, AgentResponse, BaseAdapter

class LlamaCppAdapter(BaseAdapter):
    """Adapter for interacting with LlamaCpp local model."""
    def __init__(self, config: Dict[str, Any]):
        """Initializes the LlamaCpp adapter."""
        super().__init__(config)
        self.endpoint = config.get("endpoint", "http://localhost:8080")
        self.model_path = config.get("model_path", None)
        self.path = "v1/completions"
        self._update_endpoint()
        self.max_tokens = 4096
        self.temperature = 0.7

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
        """Execute a task using LlamaCpp Code.
        
        LlamaCpp is typically used for larger-context implementation and code review tasks.
        """
        prompt = self._build_local_llm_prompt(task,context)
        
        # set prompt to payload
        payload  = {
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stop": ["```\n\n", "Human:", "User:"],
            "prompt":prompt
        }

        # run the prompt with http call
        response = self._run_http_with_prompt(payload)

        if response.success:
            response.output = self._parse_response(response.output)

        return response

    def is_available(self) -> bool:
        try:
            resp = httpx.get(self.endpoint, timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    def _parse_response(self, data:Dict) -> str :
        choices = data.get("choices", [])
        return choices[0].get("text", "") if choices else ""
