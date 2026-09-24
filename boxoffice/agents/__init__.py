"""Agentic AI workflows over SeatGeek spend — categorization, policy, dispute, fraud, tieout.

Each single-shot agent is *backend-agnostic* and satisfies
:class:`~boxoffice.llm.base.AgentProtocol`, so it runs identically on the analytical
engine, a simulated model, or live Claude — which is what makes the eval harness a
real multi-model leaderboard. The multi-step :class:`BoxOfficeOrchestrator` and
:class:`FraudInvestigator` chain these into autonomous workflows.
"""
from .base import BaseAgent
from .categorization import CategorizationAgent
from .policy import PolicyAuditAgent
from .dispute import DisputeAgent
from .fraud_triage import FraudTriageAgent
from .tieout import TieoutAgent
from .investigator import FraudInvestigator, InvestigationReport
from .orchestrator import BoxOfficeOrchestrator, OrchestratorDecision

EVAL_AGENTS = {
    "categorization": CategorizationAgent,
    "policy_audit": PolicyAuditAgent,
    "dispute": DisputeAgent,
    "fraud_triage": FraudTriageAgent,
    "tieout": TieoutAgent,
}

__all__ = [
    "BaseAgent",
    "CategorizationAgent",
    "PolicyAuditAgent",
    "DisputeAgent",
    "FraudTriageAgent",
    "TieoutAgent",
    "FraudInvestigator",
    "InvestigationReport",
    "BoxOfficeOrchestrator",
    "OrchestratorDecision",
    "EVAL_AGENTS",
]
