"""Knowledge indexes for Future Leaders AI v11."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from .knowledge_object import CompanyKnowledgeObject


def _normalize(value: str) -> str:
    return value.strip().lower()


@dataclass
class KnowledgeIndex:
    """Build lightweight indexes for company knowledge objects."""

    companies: list[CompanyKnowledgeObject]
    by_ticker: dict[str, CompanyKnowledgeObject] = field(init=False)
    by_status: dict[str, list[CompanyKnowledgeObject]] = field(init=False)
    by_dna: dict[str, list[CompanyKnowledgeObject]] = field(init=False)
    by_tag: dict[str, list[CompanyKnowledgeObject]] = field(init=False)

    def __post_init__(self) -> None:
        self.by_ticker = {company.ticker.upper(): company for company in self.companies}
        self.by_status = defaultdict(list)
        self.by_dna = defaultdict(list)
        self.by_tag = defaultdict(list)

        for company in self.companies:
            self.by_status[_normalize(company.status)].append(company)
            for dna in company.dna:
                self.by_dna[_normalize(dna)].append(company)
            for tag in company.discovery_tags:
                self.by_tag[_normalize(tag)].append(company)

        self.by_status = dict(self.by_status)
        self.by_dna = dict(self.by_dna)
        self.by_tag = dict(self.by_tag)

    def get_company(self, ticker: str) -> CompanyKnowledgeObject | None:
        return self.by_ticker.get(ticker.upper())

    def find_by_dna(self, dna: str) -> list[CompanyKnowledgeObject]:
        return self.by_dna.get(_normalize(dna), [])

    def find_by_status(self, status: str) -> list[CompanyKnowledgeObject]:
        return self.by_status.get(_normalize(status), [])

    def find_by_tag(self, tag: str) -> list[CompanyKnowledgeObject]:
        return self.by_tag.get(_normalize(tag), [])

    def summary(self) -> dict[str, int]:
        return {
            "companies": len(self.companies),
            "dna_count": len(self.by_dna),
            "status_count": len(self.by_status),
            "tag_count": len(self.by_tag),
        }
