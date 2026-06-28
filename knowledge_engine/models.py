from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

@dataclass(frozen=True)
class KnowledgeChunk:
    source_path: str
    category: str
    title: str
    text: str
    start_line: int
    end_line: int
    checksum: str

@dataclass(frozen=True)
class QueryResult:
    chunk: KnowledgeChunk
    score: float
    reason: str

@dataclass
class KnowledgeIndex:
    root: str
    chunks: list[KnowledgeChunk]
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "chunks": [asdict(c) for c in self.chunks],
            "metadata": self.metadata,
        }
