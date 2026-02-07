from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseAgent(ABC):
    def __init__(self, name: str, client: Any):
        self.name = name
        self.client = client

    @abstractmethod
    def analyze(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes the inputs and returns a structured dictionary.
        """
        pass

    def format_prompt(self, template: str, **kwargs) -> str:
        """
        Helper to format prompts.
        """
        return template.format(**kwargs)
