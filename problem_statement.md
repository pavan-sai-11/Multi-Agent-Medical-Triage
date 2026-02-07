##Project: Multi-Agent Medical Triage Command

##Goal:
--Build a responsible, multi-agent AI system that performs medical triage by routing patients to appropriate next steps (self-care, consultation, urgent care, or refusal) while explicitly handling uncertainty and avoiding unsafe medical advice.

##Problem Statement:
--Medical AI systems operate in a high-stakes environment where incorrect or overconfident guidance can cause serious harm. Most existing systems attempt to provide definitive medical answers even when patient information is incomplete, ambiguous, or unreliable, and they often fail to communicate uncertainty or refuse unsafe decisions.
--This project addresses the need for a non-diagnostic, safety-first medical triage system that can reason under uncertainty. By using a multi-agent architecture, the system enables structured debate, risk assessment, evidence quality evaluation, and ethical oversight, allowing it to escalate, caution, or refuse to decide when confidence is low or risk is high.

##Key Features:
--Multi-agent deliberation with explicit debate and dissent
--Safety-first triage without diagnosis or treatment recommendations
--Confidence scoring and uncertainty-aware refusal logic
--Ethics agent with veto power to prevent unsafe outputs
--Transparent reasoning through structured agent outputs

##Technical Stack:
--Frontend: Command-center styled web interface (React-based)
--Backend: Agent orchestration and decision logic
--AI Layer: Multi-agent reasoning with confidence and risk thresholds
--UI Enhancements: Live medical-themed background and deliberation logs

