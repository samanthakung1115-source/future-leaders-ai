from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from .knowledge_engine import KnowledgeObject


@dataclass
class ConsensusResult:
    company: str
    growth_score: float
    moat_score: float
    valuation_score: float
    quality_score: float
    risk_score: float
    consensus_score: float
    evidence_count: int
    decision: str
    rationale: list[str]


class AIConsensus:
    """First executable AI Consensus core for v11.

    This is rule-based and auditable by design. Later v11.x versions can attach
    LLM or embedding models without changing the STS-compatible result shape.
    """

    def score_company(self, company: str, evidence: list[KnowledgeObject]) -> ConsensusResult:
        joined = "\n".join(obj.content.lower() for obj in evidence)
        growth = self._score_terms(joined, ["growth", "revenue", "demand", "expansion", "ai", "hbm", "datacenter"])
        moat = self._score_terms(joined, ["moat", "platform", "ecosystem", "leadership", "dominant", "switching cost"])
        valuation = self._score_terms(joined, ["undervalued", "pullback", "multiple", "valuation", "margin of safety"])
        quality = self._score_terms(joined, ["profit", "free cash flow", "margin", "execution", "management", "balance sheet"])
        risk_raw = self._score_terms(joined, ["risk", "competition", "cyclical", "regulation", "drawdown", "overvalued"])
        risk = max(1.0, 10.0 - risk_raw)
        consensus = round(mean([growth, moat, valuation, quality, risk]), 2)
        decision = self._decision(consensus, risk_raw, len(evidence))
        rationale = self._rationale(company, evidence, consensus, risk_raw)
        return ConsensusResult(
            company=company.upper(),
            growth_score=growth,
            moat_score=moat,
            valuation_score=valuation,
            quality_score=quality,
            risk_score=risk,
            consensus_score=consensus,
            evidence_count=len(evidence),
            decision=decision,
            rationale=rationale,
        )

    @staticmethod
    def _score_terms(text: str, terms: list[str]) -> float:
        hits = sum(text.count(term.lower()) for term in terms)
        return round(min(10.0, 4.0 + hits * 0.7), 2)

    @staticmethod
    def _decision(consensus: float, risk_raw: float, evidence_count: int) -> str:
        if evidence_count == 0:
            return "NO_DATA"
        if consensus >= 8.0 and risk_raw <= 5.0:
            return "HIGH_CONVICTION_DISCOVERY"
        if consensus >= 6.8:
            return "WATCHLIST"
        if risk_raw > 7.0:
            return "HIGH_RISK_REVIEW"
        return "NEEDS_MORE_RESEARCH"

    @staticmethod
    def _rationale(company: str, evidence: list[KnowledgeObject], consensus: float, risk_raw: float) -> list[str]:
        if not evidence:
            return [f"No repository evidence found for {company.upper()}."]
        sources = ", ".join(obj.source_path for obj in evidence[:5])
        notes = [f"Read {len(evidence)} repository evidence objects: {sources}."]
        notes.append(f"Consensus score is {consensus}; risk signal raw score is {round(risk_raw, 2)}.")
        return notes
