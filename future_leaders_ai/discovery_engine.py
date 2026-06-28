from __future__ import annotations

from dataclasses import asdict, dataclass

from .ai_consensus import AIConsensus, ConsensusResult
from .knowledge_engine import KnowledgeEngine, KnowledgeObject


@dataclass
class DiscoveryReport:
    company: str
    consensus: ConsensusResult
    evidence: list[dict[str, str]]
    sts_compatible_payload: dict


class DiscoveryEngine:
    """Discovery Intelligence for Future Leaders AI v11.

    It does not manage positions, trades, costs or recovery logic. Those remain
    in stock-terminal-pro. Output is intentionally shaped for STS compatibility.
    """

    def __init__(self, knowledge_engine: KnowledgeEngine | None = None) -> None:
        self.knowledge_engine = knowledge_engine or KnowledgeEngine(".")
        self.consensus = AIConsensus()

    def analyze_company(self, company: str, top_k: int = 10) -> DiscoveryReport:
        evidence = self.knowledge_engine.search(company, top_k=top_k)
        result = self.consensus.score_company(company, evidence)
        evidence_payload = [
            {
                "id": obj.id,
                "title": obj.title,
                "source_path": obj.source_path,
                "source_dir": obj.source_dir,
                "themes": ",".join(obj.themes),
            }
            for obj in evidence
        ]
        sts_payload = {
            "schema": "samantha.discovery_signal.v11",
            "producer": "future-leaders-ai",
            "consumer": "stock-terminal-pro",
            "company": result.company,
            "consensus_score": result.consensus_score,
            "decision": result.decision,
            "evidence_count": result.evidence_count,
            "scores": {
                "growth": result.growth_score,
                "moat": result.moat_score,
                "valuation": result.valuation_score,
                "quality": result.quality_score,
                "risk": result.risk_score,
            },
            "rationale": result.rationale,
        }
        return DiscoveryReport(
            company=result.company,
            consensus=result,
            evidence=evidence_payload,
            sts_compatible_payload=sts_payload,
        )

    def analyze_universe(self, companies: list[str], top_k: int = 8) -> list[DiscoveryReport]:
        reports = [self.analyze_company(company, top_k=top_k) for company in companies]
        return sorted(reports, key=lambda report: report.consensus.consensus_score, reverse=True)

    @staticmethod
    def to_dict(report: DiscoveryReport) -> dict:
        return asdict(report)
