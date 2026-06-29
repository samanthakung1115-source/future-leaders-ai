
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from .knowledge_object import KnowledgeSource

@dataclass
class KnowledgeLoader:
    repo_root: Path | str = "."
    company_dir: str = "knowledge/companies"

    def __post_init__(self):
        self.repo_root = Path(self.repo_root).resolve()

    def load_company_sources(self) -> list[KnowledgeSource]:
        root = self.repo_root / self.company_dir
        if not root.exists():
            return []
        sources = []
        for path in sorted(root.rglob("*.md")):
            sources.append(
                KnowledgeSource(
                    path=path,
                    relative_path=path.relative_to(self.repo_root).as_posix(),
                    category="company",
                    raw_text=path.read_text(encoding="utf-8"),
                )
            )
        return sources
