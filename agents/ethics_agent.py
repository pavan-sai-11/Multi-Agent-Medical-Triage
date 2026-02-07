import json
from typing import Dict, Any
from agents.base_agent import BaseAgent

class EthicsSafetyAgent(BaseAgent):
    def __init__(self, client: Any):
        super().__init__("Ethics & Safety Agent", client)

    def analyze(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes the inputs for ethical and safety violations.
        Can be used in Round 1 (initial check) or Round 2 (reviewing other agents).
        """
        system_prompt = """
        You are the Ethics & Safety Agent.
        Your Goal: strict safety enforcement.
        Powers: Veto diagnosis, unsafe reassurance, or scope creep.
        
        Constraints:
        - FORCE REFUSAL if uncertain or unsafe.
        - Output JSON only.

        Output Format:
        {
            "triage_level": "self-care | consult | urgent | unknown",
            "risk_score": 0-100,
            "confidence": 0-100,
            "red_flags": ["safety violations"],
            "veto": true | false,
            "refusal_reason": "why we must refuse (if applicable)"
        }
        """

        user_prompt = f"""
        Review the following case for safety:
        {json.dumps(inputs, indent=2)}
        """

        return self.client.generate(system_prompt, user_prompt)
