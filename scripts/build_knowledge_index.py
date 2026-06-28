from __future__ import annotations
import argparse
from knowledge_engine import KnowledgeEngine

def main() -> None:
    parser = argparse.ArgumentParser(description="Build Samantha Future Leaders AI v11 Knowledge Index")
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--out", default=".samantha/knowledge_index.json", help="Output path inside repo")
    args = parser.parse_args()
    engine = KnowledgeEngine(args.repo)
    index = engine.build()
    out = engine.save(args.out)
    print(f"Knowledge index built: {index.metadata['file_count']} files, {index.metadata['chunk_count']} chunks")
    print(f"Saved to: {out}")

if __name__ == "__main__":
    main()
