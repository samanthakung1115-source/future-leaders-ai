from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from .chunker import MarkdownAwareChunker
from .loader import RepositoryLoader
from .models import KnowledgeIndex, QueryResult
from .retriever import KeywordRetriever

class KnowledgeEngine:
    def __init__(self, repo_root: str | Path):
        self.repo_root = Path(repo_root).resolve()
        self.index: KnowledgeIndex | None = None
        self.retriever: KeywordRetriever | None = None

    def build(self) -> KnowledgeIndex:
        loader = RepositoryLoader(self.repo_root)
        chunker = MarkdownAwareChunker()
        chunks = []
        files = []
        for path in loader.iter_files():
            files.append(path.relative_to(self.repo_root).as_posix())
            chunks.extend(chunker.chunk(self.repo_root, path, loader.read_text(path)))
        self.index = KnowledgeIndex(
            root=str(self.repo_root),
            chunks=chunks,
            metadata={
                "version": "v11.0.0",
                "built_at": datetime.now(timezone.utc).isoformat(),
                "file_count": len(files),
                "chunk_count": len(chunks),
                "source_dirs": ["knowledge", "docs", "tests", "specs", "prompts", "playbooks", "companies"],
            },
        )
        self.retriever = KeywordRetriever(chunks)
        return self.index

    def save(self, output_path: str | Path = ".samantha/knowledge_index.json") -> Path:
        if self.index is None:
            self.build()
        out = (self.repo_root / output_path).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(self.index.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return out

    def query(self, question: str, top_k: int = 8, category: str | None = None) -> list[QueryResult]:
        if self.retriever is None:
            self.build()
        assert self.retriever is not None
        return self.retriever.search(question, top_k=top_k, category=category)
