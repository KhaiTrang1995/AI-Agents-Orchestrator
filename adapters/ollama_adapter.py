"""Adapter for Ollama local model."""

from typing import Any, Dict, List
import httpx
from .base import AgentCapability, AgentResponse, BaseAdapter

class OllamaAdapter(BaseAdapter):
    """Adapter for interacting with Ollama local model."""
    def __init__(self, config: Dict[str, Any]):
      """Initializes the Ollama adapter."""
      super().__init__(config)
      self.model = config.get("model", "codellama:13b")
      self.endpoint = config.get("endpoint", "http://localhost:11434")
      self.path = "api/generate"
      self._update_endpoint()
      self.stream = False
      
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
        prompt = self._build_local_llm_prompt(task,context)
        
        # set prompt to payload
        payload  = {
          "model": self.model,
          "prompt": prompt,
          "stream": self.stream
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
    
    def list_models(self) -> list[str]:
        """Return available models on the Ollama server."""
        try:
            resp = httpx.get(f"{self.endpoint}/api/tags")
            resp.raise_for_status()
            return [m["name"] for m in resp.json().get("models", [])]
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            self.logger.error(f"Failed to list Ollama models: {e}")
            return []

    def _parse_response(self, data:Dict) -> str :
        return data.get('response',"")