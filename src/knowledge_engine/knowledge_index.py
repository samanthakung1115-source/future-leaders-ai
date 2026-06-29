
from collections import defaultdict
from dataclasses import dataclass, field
from .knowledge_object import CompanyKnowledgeObject

def norm(x: str) -> str:
    return x.strip().lower()

@dataclass
class KnowledgeIndex:
    companies: list[CompanyKnowledgeObject]
    by_ticker: dict[str, CompanyKnowledgeObject] = field(init=False)
    by_dna: dict[str, list[CompanyKnowledgeObject]] = field(init=False)

    def __post_init__(self):
        self.by_ticker = {c.ticker.upper(): c for c in self.companies}
        by_dna = defaultdict(list)
        for c in self.companies:
            for dna in c.dna:
                by_dna[norm(dna)].append(c)
        self.by_dna = dict(by_dna)

    def get_company(self, ticker: str):
        return self.by_ticker.get(ticker.upper())

    def find_by_dna(self, dna: str):
        return self.by_dna.get(norm(dna), [])
