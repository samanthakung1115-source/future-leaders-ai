from __future__ import annotations
from pathlib import Path

DEFAULT_INCLUDE_DIRS = ["knowledge", "docs", "tests", "specs", "prompts", "playbooks", "companies"]
DEFAULT_EXTENSIONS = {".md", ".txt", ".yaml", ".yml", ".json", ".py"}

class RepositoryLoader:
    def __init__(self, repo_root: str | Path, include_dirs: list[str] | None = None):
        self.repo_root = Path(repo_root).resolve()
        self.include_dirs = include_dirs or DEFAULT_INCLUDE_DIRS

    def iter_files(self):
        for dirname in self.include_dirs:
            base = self.repo_root / dirname
            if not base.exists():
                continue
            for path in sorted(base.rglob("*")):
                if path.is_file() and path.suffix.lower() in DEFAULT_EXTENSIONS:
                    yield path

    def read_text(self, path: Path) -> str:
        return path.read_text(encoding="utf-8", errors="replace")
