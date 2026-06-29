"""Markdown parser for Future Leaders AI v11 Knowledge Engine."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .knowledge_object import CompanyKnowledgeObject, KnowledgeSource


SECTION_ALIASES = {
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
    "samantha ai tags": "discovery_tags",
    "why not buy": "why_not_buy",
    "similar dna": "similar_dna",
    "opposite dna": "opposite_dna",
    "samantha verdict": "verdict",
    "knowledge confidence": "confidence",
}


@dataclass
class KnowledgeParser:
    """Parse company Markdown files into CompanyKnowledgeObject."""

    def parse_company(self, source: KnowledgeSource) -> CompanyKnowledgeObject:
        if source.category != "company":
            raise ValueError(f"Expected company source, got {source.category!r}")

        title = self._extract_title(source.raw_text) or source.stem
        name, ticker = self._parse_title(title, fallback_ticker=source.stem)
        sections = self._split_sections(source.raw_text)

        company = CompanyKnowledgeObject(
            ticker=ticker,
            name=name,
            source_path=source.relative_path,
        )

        for raw_title, body in sections.items():
            field_name = SECTION_ALIASES.get(raw_title.strip().lower())
            if not field_name:
                continue

            if field_name in {
                "why_selected",
                "dna",
                "key_signals",
                "risks",
                "lessons",
                "discovery_tags",
                "why_not_buy",
                "similar_dna",
                "opposite_dna",
            }:
                setattr(company, field_name, self._parse_list_or_lines(body))
            else:
                setattr(company, field_name, self._parse_text(body))

        if company.status == "Unknown":
            company.status = "Unknown"
        if not company.summary:
            company.summary = self._first_paragraph_after_title(source.raw_text)

        return company

    def parse_companies(self, sources: list[KnowledgeSource]) -> list[CompanyKnowledgeObject]:
        return [self.parse_company(source) for source in sources if source.category == "company"]

    def _extract_title(self, text: str) -> str:
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        return ""

    def _parse_title(self, title: str, fallback_ticker: str) -> tuple[str, str]:
        match = re.search(r"\(([^)]+)\)", title)
        ticker = match.group(1).strip().upper() if match else fallback_ticker.upper()
        name = re.sub(r"\s*\([^)]+\)\s*$", "", title).strip()
        return name or ticker, ticker

    def _split_sections(self, text: str) -> dict[str, str]:
        sections: dict[str, list[str]] = {}
        current: str | None = None

        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("## "):
                current = stripped[3:].strip()
                sections[current] = []
            elif current:
                sections[current].append(line)

        return {title: "\n".join(lines).strip() for title, lines in sections.items()}

    def _parse_list_or_lines(self, body: str) -> list[str]:
        items: list[str] = []
        for line in body.splitlines():
            stripped = line.strip()
            if not stripped or stripped == "---":
                continue
            if stripped.startswith("- "):
                stripped = stripped[2:].strip()
            if stripped:
                items.append(stripped)
        return items

    def _parse_text(self, body: str) -> str:
        lines = [line.strip() for line in body.splitlines() if line.strip() and line.strip() != "---"]
        return " ".join(lines).strip()

    def _first_paragraph_after_title(self, text: str) -> str:
        lines = []
        seen_title = False
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                seen_title = True
                continue
            if not seen_title:
                continue
            if stripped.startswith("## "):
                break
            if stripped:
                lines.append(stripped)
        return " ".join(lines)
