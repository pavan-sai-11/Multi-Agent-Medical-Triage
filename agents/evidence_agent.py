import json
from typing import Dict, Any
from agents.base_agent import BaseAgent

class EvidenceQualityAgent(BaseAgent):
    def __init__(self, client: Any):
        super().__init__("Evidence Quality Agent", client)

    def analyze(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = """
        You are the Evidence Quality Agent.
        Your Goal: Score completeness of inputs. identify missing vitals or unclear descriptions.
        Constraints:
        - Low evidence -> Low confidence.
        - Missing inputs -> INCREASE uncertainty.
        - Output JSON only.

        Output Format:
        {
            "triage_level": "unknown", 
            "risk_score": 0,
            "confidence": 0-100,
            "red_flags": ["list missing critical info"],
            "data_quality_score": 0-100,
            "missing_information": ["list what is needed"]
        }
        """
        # Note: triage_level might not be relevant for this agent directly, but keeping schema consistent is good.
        # Although the prompt asks for specific fields, the Base Agent might expect a unified schema?
        # The user prompt specified a common JSON format for Round 1:
        # { "triage_level": ..., "risk_score": ..., "confidence": ..., "red_flags": ... }

        user_prompt = f"""
        Assess the quality of the following data:
        {json.dumps(inputs, indent=2)}
        """

        return self.client.generate(system_prompt, user_prompt)
