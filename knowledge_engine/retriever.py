from __future__ import annotations
import math
import re
from collections import Counter
from .models import KnowledgeChunk, QueryResult

TOKEN_RE = re.compile(r"[A-Za-z0-9_.$-]+|[\u4e00-\u9fff]+")

def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]

class KeywordRetriever:
    def __init__(self, chunks: list[KnowledgeChunk]):
        self.chunks = chunks
        self.chunk_tokens = [Counter(tokenize(c.title + "\n" + c.text)) for c in chunks]
        self.df = Counter()
        for toks in self.chunk_tokens:
            self.df.update(toks.keys())
        self.n = max(len(chunks), 1)

    def search(self, query: str, top_k: int = 8, category: str | None = None) -> list[QueryResult]:
        q_tokens = Counter(tokenize(query))
        results: list[QueryResult] = []
        for chunk, toks in zip(self.chunks, self.chunk_tokens):
            if category and chunk.category != category:
                continue
            score = 0.0
            matched = []
            for term, qtf in q_tokens.items():
                if term not in toks:
                    continue
                idf = math.log((self.n + 1) / (self.df[term] + 1)) + 1
                score += (1 + math.log(toks[term])) * idf * qtf
                matched.append(term)
            if score > 0:
                results.append(QueryResult(chunk, round(score, 4), "matched: " + ", ".join(matched[:8])))
        return sorted(results, key=lambda r: r.score, reverse=True)[:top_k]
