import os
import json
from unittest.mock import MagicMock
from core.triage_system import TriageSystem
from utils.llm_client import LLMClient
import colorama
from colorama import Fore, Style

colorama.init()

def mock_generate(system_prompt, user_prompt, **kwargs):
    """Mocks LLM responses for the demo if no API key is present."""
    if "Symptom Interpretation Agent" in system_prompt:
        return {
            "triage_level": "consult",
            "risk_score": 50,
            "confidence": 80,
            "red_flags": ["Severe headache", "Stiff neck"],
            "symptom_summary": "Patient reports severe headache and stiffness in neck."
        }
    elif "Risk Stratification Agent" in system_prompt:
        if "review_target" in user_prompt:
             return {"red_flags": []} # No new flags in review
        return {
            "triage_level": "urgent", # Risk agent is paranoid
            "risk_score": 85,
            "confidence": 75,
            "red_flags": ["Possible Meningitis"],
            "worst_case_analysis": "Symptoms consistent with meningitis, which is life-threatening."
        }
    elif "Evidence Quality Agent" in system_prompt:
        return {
            "confidence": 95,
            "data_quality_score": 90,
            "missing_information": []
        }
    elif "Ethics & Safety Agent" in system_prompt:
        if "review_target" in user_prompt:
            return {"veto": False}
        return {
            "triage_level": "consult",
            "veto": False
        }
    elif "Coordinator Agent" in system_prompt:
        return {
            "final_decision": "URGENT",
            "reasoning_summary": "Risk Agent identified potential Meningitis (Red Flag). Protocol requires escalation to URGENT for life-threatening possibilities.",
            "safety_notes": ["Do not wait.", "Seek immediate care."],
            "confidence_level": "High",
            "next_steps": ["Go to ER", "Monitor consciousness"]
        }
    return {}

def run_demo():
    print(Fore.YELLOW + "🚀 RUNNING AUTOMATED DEMO" + Style.RESET_ALL)
    
    api_key = os.getenv("OPENAI_API_KEY")
    use_mock = False
    
    if not api_key:
        print(Fore.YELLOW + "⚠️  No API Key found. Using MOCKED LLM responses for demonstration." + Style.RESET_ALL)
        use_mock = True
    else:
        print(Fore.GREEN + "✅ API Key found. Using REAL LLM behavior." + Style.RESET_ALL)

    system = TriageSystem(api_key="dummy" if use_mock else api_key)
    
    if use_mock:
        # Patch the client
        mock_client = MagicMock(spec=LLMClient)
        mock_client.generate.side_effect = mock_generate
        
        system.client = mock_client
        system.symptom_agent.client = mock_client
        system.risk_agent.client = mock_client
        system.evidence_agent.client = mock_client
        system.ethics_agent.client = mock_client
        system.coordinator_agent.client = mock_client

    # Sample Case
    case_inputs = {
        "symptoms": "Severe headache, stiff neck, sensitivity to light",
        "age": "25",
        "history": "None"
    }
    
    print("\n📄 Case Inputs:")
    print(json.dumps(case_inputs, indent=2))
    print("-" * 50)
    
    try:
        system.run_simulation(case_inputs)
    except Exception as e:
        print(Fore.RED + f"❌Demo failed: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    run_demo()
