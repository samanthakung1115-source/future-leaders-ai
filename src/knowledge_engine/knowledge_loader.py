"""Repository knowledge loader for Future Leaders AI v11."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from .knowledge_object import KnowledgeSource


DEFAULT_KNOWLEDGE_DIRS = (
    "knowledge/companies",
    "knowledge/decision_patterns",
    "knowledge/investment_rules",
    "knowledge/themes",
    "docs",
    "tests",
)


@dataclass
class KnowledgeLoader:
    """Load Markdown knowledge files from a Future Leaders AI repository."""

    repo_root: Path | str = "."
    knowledge_dirs: Iterable[str] = field(default_factory=lambda: DEFAULT_KNOWLEDGE_DIRS)

    def __post_init__(self) -> None:
        self.repo_root = Path(self.repo_root).resolve()

    def discover_markdown_files(self) -> list[Path]:
        files: list[Path] = []
        for directory in self.knowledge_dirs:
            root = self.repo_root / directory
            if not root.exists():
                continue
            for path in root.rglob("*.md"):
                if path.is_file():
                    files.append(path)
        return sorted(files)

    def load_sources(self) -> list[KnowledgeSource]:
        sources: list[KnowledgeSource] = []
        for path in self.discover_markdown_files():
            raw_text = path.read_text(encoding="utf-8")
            relative_path = path.relative_to(self.repo_root).as_posix()
            sources.append(
                KnowledgeSource(
                    path=path,
                    relative_path=relative_path,
                    category=self._infer_category(relative_path),
                    raw_text=raw_text,
                )
            )
        return sources

    def load_company_sources(self) -> list[KnowledgeSource]:
        return [source for source in self.load_sources() if source.category == "company"]

    def _infer_category(self, relative_path: str) -> str:
        if relative_path.startswith("knowledge/companies/"):
            return "company"
        if relative_path.startswith("knowledge/decision_patterns/"):
            return "decision_pattern"
        if relative_path.startswith("knowledge/investment_rules/"):
            return "investment_rule"
        if relative_path.startswith("knowledge/themes/"):
            return "theme"
        if relative_path.startswith("docs/"):
            return "doc"
        if relative_path.startswith("tests/"):
            return "test"
        return "unknown"
