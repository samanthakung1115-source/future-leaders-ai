
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

@dataclass(frozen=True)
class KnowledgeSource:
    path: Path
    relative_path: str
    category: str
    raw_text: str

    @property
    def stem(self) -> str:
        return self.path.stem

@dataclass
class CompanyKnowledgeObject:
    ticker: str
    name: str = ""
    status: str = "Unknown"
    summary: str = ""
    why_selected: list[str] = field(default_factory=list)
    dna: list[str] = field(default_factory=list)
    key_signals: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    lessons: list[str] = field(default_factory=list)
    discovery_tags: list[str] = field(default_factory=list)
    why_not_buy: list[str] = field(default_factory=list)
    similar_dna: list[str] = field(default_factory=list)
    opposite_dna: list[str] = field(default_factory=list)
    verdict: str = ""
    confidence: str = "Unknown"
    source_path: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def has_dna(self, dna_name: str) -> bool:
        return dna_name.strip().lower() in {item.strip().lower() for item in self.dna}

    def to_dict(self) -> dict:
        return {
            "ticker": self.ticker,
            "name": self.name,
            "status": self.status,
            "summary": self.summary,
            "why_selected": self.why_selected,
            "dna": self.dna,
            "key_signals": self.key_signals,
            "risks": self.risks,
            "lessons": self.lessons,
            "discovery_tags": self.discovery_tags,
            "why_not_buy": self.why_not_buy,
            "similar_dna": self.similar_dna,
            "opposite_dna": self.opposite_dna,
            "verdict": self.verdict,
            "confidence": self.confidence,
            "source_path": self.source_path,
            "metadata": self.metadata,
        }
