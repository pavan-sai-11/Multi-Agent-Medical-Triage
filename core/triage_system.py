import json
from typing import Dict, Any, List
from agents.symptom_agent import SymptomInterpretationAgent
from agents.risk_agent import RiskStratificationAgent
from agents.evidence_agent import EvidenceQualityAgent
from agents.ethics_agent import EthicsSafetyAgent
from agents.coordinator_agent import CoordinatorAgent
from utils.llm_client import LLMClient
import colorama
from colorama import Fore, Style

colorama.init()

from core.doctors_data import DOCTOR_DATABASE
import random

class TriageSystem:
    def __init__(self, api_key: str):
        self.client = LLMClient(api_key=api_key)
        self.symptom_agent = SymptomInterpretationAgent(self.client)
        self.risk_agent = RiskStratificationAgent(self.client)
        self.evidence_agent = EvidenceQualityAgent(self.client)
        self.ethics_agent = EthicsSafetyAgent(self.client)
        self.coordinator = CoordinatorAgent(self.client)
        
        # For iteration if needed, though mostly used individually
        self.agents = [
            self.symptom_agent, 
            self.risk_agent, 
            self.evidence_agent, 
            self.ethics_agent
        ]

    def _get_doctor_recommendations(self, decision: str, symptoms: str):
        """Simple keyword matching to recommend relevant specialists."""
        recommendations = []
        symptoms_lower = symptoms.lower()
        
        # Keyword mapping
        keywords = {
            "heart": "Cardiology",
            "chest": "Cardiology",
            "palpitation": "Cardiology",
            "headache": "Neurology",
            "dizzy": "Neurology",
            "numb": "Neurology",
            "breath": "Pulmonology",
            "cough": "Pulmonology",
            "lung": "Pulmonology",
            "sugar": "Endocrinology",
            "thirst": "Endocrinology"
        }

        # Find relevant specialties
        relevant_specialties = set()
        for key, specialty in keywords.items():
            if key in symptoms_lower:
                relevant_specialties.add(specialty)
        
        # Always add General Practice if nothing specific found or if Consult
        if not relevant_specialties or "CONSULT" in decision:
            relevant_specialties.add("General Practice / Internal Medicine")

        # Filter doctors
        for doc in DOCTOR_DATABASE:
            if doc["specialty"] in relevant_specialties:
                recommendations.append(doc)
        
        # If still empty or few, add random ones to ensure user sees something
        if len(recommendations) < 2:
            remaining = [d for d in DOCTOR_DATABASE if d not in recommendations]
            recommendations.extend(remaining[:2])

        return recommendations[:3]

    def run_simulation(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        print(Fore.CYAN + "🌀 ROUND 1: Independent Analysis" + Style.RESET_ALL)
        
        # Round 1: Parallel Analysis
        symptom_analysis = self.symptom_agent.analyze(inputs)
        print(f"Symptom Agent: {symptom_analysis.get('triage_level', 'Unknown')}")
        
        risk_analysis = self.risk_agent.analyze(inputs)
        print(f"Risk Agent: {risk_analysis.get('triage_level', 'Unknown')}")
        
        evidence_analysis = self.evidence_agent.analyze(inputs)
        print(f"Evidence Agent: Confidence {evidence_analysis.get('confidence', 0)}%")
        
        ethics_analysis = self.ethics_agent.analyze(inputs)
        print(f"Ethics Agent: {ethics_analysis.get('triage_level', 'Unknown')}")

        round1_outputs = {
            "symptom": symptom_analysis,
            "risk": risk_analysis,
            "evidence": evidence_analysis,
            "ethics": ethics_analysis
        }

        print(Fore.CYAN + "\n🌀 ROUND 2: Challenge & Dissent" + Style.RESET_ALL)
        # Simplified Round 2: Agents review the aggregated state (conceptually). 
        # For this implementation, we will do a second pass if disagreement is high or risk is borderline.
        # But per the prompt, Risk/Evidence/Ethics should challenge.
        # We can simulate this by passing R1 outputs to Ethics/Risk for a "review".
        
        # Risk Review
        risk_review_prompt = f"Review these outputs: {json.dumps(round1_outputs)}. Identify missed risks."
        risk_review = self.risk_agent.analyze({"review_target": round1_outputs})
        print(f"Risk Agent Review: {risk_review.get('red_flags', [])}")
        
        # Ethics Review
        ethics_review_prompt = f"Review these outputs: {json.dumps(round1_outputs)}. Veto if unsafe."
        ethics_review = self.ethics_agent.analyze({"review_target": round1_outputs})
        print(f"Ethics Agent Review: Veto? {ethics_review.get('veto', False)}")

        round2_outputs = {
           "risk_review": risk_review,
           "ethics_review": ethics_review
        }

        print(Fore.CYAN + "\n🌀 ROUND 3: Decision Gate" + Style.RESET_ALL)
        
        # Combine everything for Coordinator
        final_context = {
            "initial_inputs": inputs,
            "round1": round1_outputs,
            "round2": round2_outputs
        }
        
        # System Rules Hard Checks (Pre-computation for Coordinator context)
        # 1. Red Flags
        all_red_flags = []
        for key, val in round1_outputs.items():
            if isinstance(val, dict):
                all_red_flags.extend(val.get('red_flags', []))
        
        if ethics_review.get('veto', False):
             print(Fore.RED + "ETHICS VETO TRIGGERED" + Style.RESET_ALL)
        # Round 3: Decision
        # The original `final_context` is used here to maintain consistency with the coordinator's expected input.
        final_decision = self.coordinator.analyze(final_context)
        
        # [NEW] Append Doctor Recommendations
        recommended_doctors = []
        decision_str = final_decision.get("final_decision", "UNKNOWN")
        if "CONSULT" in decision_str or "URGENT" in decision_str:
             recommended_doctors = self._get_doctor_recommendations(decision_str, inputs.get("symptoms", ""))

        final_decision["recommended_doctors"] = recommended_doctors

        print(f"\n{Fore.GREEN}🏆 FINAL DECISION: {final_decision}{Style.RESET_ALL}")
        return final_decision
