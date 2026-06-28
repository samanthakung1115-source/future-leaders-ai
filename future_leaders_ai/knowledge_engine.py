from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

from .repository_config import RepositoryConfig

_TOKEN_RE = re.compile(r"[A-Za-z0-9_.$-]+|[\u4e00-\u9fff]+")
_TICKER_RE = re.compile(r"\b[A-Z]{2,6}\b")


@dataclass
class KnowledgeObject:
    id: str
    source_path: str
    source_dir: str
    title: str
    content: str
    content_hash: str
    companies: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    tokens: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)


class KnowledgeEngine:
    """Reads existing repository knowledge and builds a lightweight local index.

    v11 goal: AI must read knowledge/, docs/, tests/, playbooks/, companies/ and
    specs/ before reasoning. This engine keeps the source of truth in GitHub and
    writes only a generated index under .samantha/.
    """

    def __init__(self, repo_root: str | Path = ".") -> None:
        self.config = RepositoryConfig(root=Path(repo_root).resolve())
        self.objects: list[KnowledgeObject] = []

    def build_index(self) -> list[KnowledgeObject]:
        self.objects = [self._to_object(path) for path in self.config.iter_source_files()]
        return self.objects

    def save_index(self, path: str | Path | None = None) -> Path:
        if not self.objects:
            self.build_index()
        output_path = Path(path) if path else self.config.resolved_index_path()
        if not output_path.is_absolute():
            output_path = self.config.root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": "v11.0.0",
            "platform": "Samantha AI Platform",
            "repository": "future-leaders-ai",
            "sts_repository": "stock-terminal-pro",
            "object_count": len(self.objects),
            "objects": [asdict(obj) for obj in self.objects],
        }
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return output_path

    def load_index(self, path: str | Path | None = None) -> list[KnowledgeObject]:
        index_path = Path(path) if path else self.config.resolved_index_path()
        if not index_path.is_absolute():
            index_path = self.config.root / index_path
        data = json.loads(index_path.read_text(encoding="utf-8"))
        self.objects = [KnowledgeObject(**item) for item in data.get("objects", [])]
        return self.objects

    def search(self, query: str, top_k: int = 8, source_dirs: Iterable[str] | None = None) -> list[KnowledgeObject]:
        if not self.objects:
            self.build_index()
        allowed = set(source_dirs or [])
        query_tokens = self._tokenize(query)
        scored: list[tuple[float, KnowledgeObject]] = []
        for obj in self.objects:
            if allowed and obj.source_dir not in allowed:
                continue
            score = self._score(query_tokens, obj)
            if score > 0:
                scored.append((score, obj))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [obj for _, obj in scored[:top_k]]

    def _to_object(self, path: Path) -> KnowledgeObject:
        rel = path.relative_to(self.config.root).as_posix()
        raw = path.read_text(encoding="utf-8", errors="ignore")
        title = self._extract_title(raw, path)
        tokens = self._tokenize(raw)
        companies = sorted(set(t for t in _TICKER_RE.findall(raw) if len(t) <= 6))[:30]
        themes = self._extract_themes(raw)
        content_hash = hashlib.sha256(raw.encode("utf-8", errors="ignore")).hexdigest()[:16]
        return KnowledgeObject(
            id=f"ko_{hashlib.sha1(rel.encode()).hexdigest()[:12]}",
            source_path=rel,
            source_dir=rel.split("/", 1)[0],
            title=title,
            content=raw[:12000],
            content_hash=content_hash,
            companies=companies,
            themes=themes,
            tokens=tokens[:3000],
            metadata={"extension": path.suffix.lower()},
        )

    @staticmethod
    def _extract_title(text: str, path: Path) -> str:
        for line in text.splitlines()[:20]:
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip() or path.stem
        return path.stem.replace("_", " ").replace("-", " ").strip()

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return [m.group(0).lower() for m in _TOKEN_RE.finditer(text)]

    @staticmethod
    def _extract_themes(text: str) -> list[str]:
        theme_keywords = {
            "ai_infrastructure": ["AI", "GPU", "data center", "inference", "training", "accelerator"],
            "semiconductor": ["semiconductor", "chip", "DRAM", "HBM", "wafer", "foundry"],
            "cloud": ["cloud", "SaaS", "platform", "observability", "cybersecurity"],
            "networking": ["network", "ethernet", "switch", "optical", "interconnect"],
            "defense_space": ["defense", "space", "satellite", "rocket", "aerospace"],
        }
        lowered = text.lower()
        found = []
        for theme, keywords in theme_keywords.items():
            if any(keyword.lower() in lowered for keyword in keywords):
                found.append(theme)
        return found

    @staticmethod
    def _score(query_tokens: list[str], obj: KnowledgeObject) -> float:
        if not query_tokens:
            return 0.0
        counts = Counter(obj.tokens)
        score = sum(counts[token] for token in query_tokens)
        title_bonus = sum(3 for token in query_tokens if token in obj.title.lower())
        company_bonus = sum(5 for token in query_tokens if token.upper() in obj.companies)
        return float(score + title_bonus + company_bonus)
