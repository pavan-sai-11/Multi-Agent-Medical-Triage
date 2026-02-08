# 4-Bots(epochon hackathon)

Multi-Agent Medical Triage System

Overview

This project implements an ethics-first, multi-agent AI system designed to perform medical triage under uncertainty.
The system does not diagnose diseases or provide treatment, but instead routes users into safe triage outcomes based on symptom information, data completeness, and risk assessment.

The core idea of the system is that refusal under uncertainty is safer than incorrect medical advice.

⸻

Problem Statement

Medical decision-making is a high-stakes domain where overconfident or incomplete AI responses can cause serious harm.
Most AI systems attempt to provide answers even when data is insufficient, hiding uncertainty and forcing unsafe decisions.

This project addresses that problem by explicitly modeling uncertainty, disagreement, and ethical constraints within the decision pipeline.

⸻

What the System Does
	•	Performs triage only
	•	Routes users into one of four outcomes:
	•	Self-Care
	•	Monitor / Consult
	•	Seek Urgent Attention
	•	Refuse Due to Uncertainty

What the System Does NOT Do
	•	No diagnosis
	•	No disease naming
	•	No treatment recommendations

⸻

System Architecture

The system is composed of multiple specialized agents, each with a distinct role:
	•	Symptom Interpretation Agent
Extracts structured symptoms and potential red flags from user input.
	•	Risk Stratification Agent (Skeptic)
Evaluates worst-case plausible scenarios and assigns risk scores.
	•	Evidence Quality Agent
Assesses data completeness, ambiguity, and reliability.
	•	Ethics & Safety Agent (Veto)
Enforces safety rules and blocks unsafe or out-of-scope decisions.
	•	Coordinator Agent
Aggregates agent outputs and applies collective decision rules.

No single agent is allowed to make a decision independently.

⸻

Decision Logic

The system applies explicit, rule-based safety thresholds:
	•	Any life-threatening red flag → URGENT
	•	Any agent confidence < 40% → REFUSE
	•	Agent disagreement > 50% → REFUSE
	•	Average risk score > 70% → CONSULT
	•	Otherwise → SELF-CARE (with warnings)

Refusal is treated as a designed safety feature, not a failure.

⸻

Key Features
	•	Multi-agent reasoning and disagreement handling
	•	Explicit uncertainty modeling
	•	Ethics-first design with veto authority
	•	Structured, auditable agent outputs
	•	Robust refusal logic in high-risk scenarios

⸻

Technologies Used
	•	Python
	•	Multi-Agent System Design
	•	Large Language Model (LLM) Integration
	•	Modular Utilities and Testing
	•	Git and Collaborative Development

⸻

Intended Use
	•	Academic research and experimentation
	•	Hackathon and demonstration purposes
	•	Exploration of safe AI decision-making under uncertainty

This system is not intended for real-world medical deployment.

⸻

Design Philosophy

Responsible autonomy means knowing when not to act.

The system prioritizes safety, transparency, and ethical responsibility over confident but potentially harmful outputs.

⸻

Team

Developed as part of EpochOn 2.0 Hackathon
Collective Intelligence × Ethics × Safety
