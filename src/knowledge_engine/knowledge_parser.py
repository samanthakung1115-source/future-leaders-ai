
from __future__ import annotations
import re
from dataclasses import dataclass
from .knowledge_object import CompanyKnowledgeObject, KnowledgeSource

SECTION_MAP = {
    "status": "status",
    "summary": "summary",
    "why samantha selected": "why_selected",
    "why samantha is watching": "why_selected",
    "winner dna": "dna",
    "dna": "dna",
    "key signals": "key_signals",
    "risks": "risks",
    "samantha lessons": "lessons",
    "lessons learned": "lessons",
    "discovery tags": "discovery_tags",
    "why not buy": "why_not_buy",
    "similar dna": "similar_dna",
    "opposite dna": "opposite_dna",
    "samantha verdict": "verdict",
    "knowledge confidence": "confidence",
}

@dataclass
class KnowledgeParser:
    def parse_company(self, source: KnowledgeSource) -> CompanyKnowledgeObject:
        title = self._title(source.raw_text) or source.stem
        name, ticker = self._parse_title(title, source.stem)
        sections = self._sections(source.raw_text)

        company = CompanyKnowledgeObject(ticker=ticker, name=name, source_path=source.relative_path)

        for title, body in sections.items():
            field = SECTION_MAP.get(title.lower().strip())
            if not field:
                continue
            if field in {"why_selected","dna","key_signals","risks","lessons","discovery_tags","why_not_buy","similar_dna","opposite_dna"}:
                setattr(company, field, self._list(body))
            else:
                setattr(company, field, self._text(body))

        return company

    def parse_companies(self, sources: list[KnowledgeSource]) -> list[CompanyKnowledgeObject]:
        return [self.parse_company(src) for src in sources]

    def _title(self, text: str) -> str:
        for line in text.splitlines():
            if line.strip().startswith("# "):
                return line.strip()[2:].strip()
        return ""

    def _parse_title(self, title: str, fallback: str):
        match = re.search(r"\(([^)]+)\)", title)
        ticker = match.group(1).strip().upper() if match else fallback.upper()
        name = re.sub(r"\s*\([^)]+\)\s*$", "", title).strip() or ticker
        return name, ticker

    def _sections(self, text: str) -> dict[str, str]:
        sections = {}
        current = None
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("## "):
                current = s[3:].strip()
                sections[current] = []
            elif current:
                sections[current].append(line)
        return {k: "\n".join(v).strip() for k, v in sections.items()}

    def _list(self, body: str) -> list[str]:
        out = []
        for line in body.splitlines():
            s = line.strip()
            if not s or s == "---":
                continue
            if s.startswith("- "):
                s = s[2:].strip()
            out.append(s)
        return out

    def _text(self, body: str) -> str:
        return " ".join(line.strip() for line in body.splitlines() if line.strip() and line.strip() != "---")
