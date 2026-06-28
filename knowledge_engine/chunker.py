from __future__ import annotations
import hashlib
from pathlib import Path
from .models import KnowledgeChunk

class MarkdownAwareChunker:
    def __init__(self, max_lines: int = 80, overlap: int = 8):
        self.max_lines = max_lines
        self.overlap = overlap

    def chunk(self, repo_root: Path, path: Path, text: str) -> list[KnowledgeChunk]:
        rel = path.relative_to(repo_root).as_posix()
        category = rel.split("/", 1)[0]
        lines = text.splitlines()
        if not lines:
            return []
        chunks: list[KnowledgeChunk] = []
        start = 0
        while start < len(lines):
            end = min(start + self.max_lines, len(lines))
            block = lines[start:end]
            title = self._title(block, rel)
            body = "\n".join(block).strip()
            if body:
                checksum = hashlib.sha256(f"{rel}:{start}:{end}:{body}".encode("utf-8")).hexdigest()[:16]
                chunks.append(KnowledgeChunk(rel, category, title, body, start + 1, end, checksum))
            if end == len(lines):
                break
            start = max(end - self.overlap, start + 1)
        return chunks

    def _title(self, lines: list[str], fallback: str) -> str:
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip() or fallback
        return fallback
