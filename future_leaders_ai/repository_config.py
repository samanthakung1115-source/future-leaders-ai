from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class RepositoryConfig:
    """Repository-aware configuration for Future Leaders AI v11.

    The default source directories match the existing repository architecture.
    Do not add a new top-level knowledge structure unless the repository itself
    already contains it.
    """

    root: Path
    source_dirs: tuple[str, ...] = (
        "knowledge",
        "docs",
        "tests",
        "companies",
        "playbooks",
        "prompts",
        "specs",
    )
    file_extensions: tuple[str, ...] = (
        ".md",
        ".txt",
        ".json",
        ".yaml",
        ".yml",
        ".py",
    )
    index_path: Path = field(default_factory=lambda: Path(".samantha/knowledge_index.json"))

    def existing_source_paths(self) -> list[Path]:
        return [self.root / name for name in self.source_dirs if (self.root / name).exists()]

    def should_read(self, path: Path) -> bool:
        return path.is_file() and path.suffix.lower() in self.file_extensions

    def iter_source_files(self) -> Iterable[Path]:
        for folder in self.existing_source_paths():
            for path in folder.rglob("*"):
                if self.should_read(path):
                    yield path

    def resolved_index_path(self) -> Path:
        return self.root / self.index_path
