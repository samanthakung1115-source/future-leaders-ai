"""Knowledge object models for Future Leaders AI v11."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class KnowledgeSource:
    """Represents a file-based knowledge source inside the repository."""

    path: Path
    relative_path: str
    category: str
    raw_text: str

    @property
    def filename(self) -> str:
        return self.path.name

    @property
    def stem(self) -> str:
        return self.path.stem

    def is_empty(self) -> bool:
        return not self.raw_text.strip()


@dataclass
class CompanyKnowledgeObject:
    """Structured company object used by the Knowledge Engine."""

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
        target = dna_name.strip().lower()
        return any(item.strip().lower() == target for item in self.dna)

    def to_dict(self) -> dict[str, Any]:
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
