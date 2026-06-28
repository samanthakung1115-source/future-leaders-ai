#!/usr/bin/env python3
from __future__ import annotations

import argparse

from future_leaders_ai import KnowledgeEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Future Leaders AI v11 knowledge index.")
    parser.add_argument("--repo", default=".", help="Path to future-leaders-ai repository root.")
    parser.add_argument("--out", default=None, help="Optional output path. Default: .samantha/knowledge_index.json")
    args = parser.parse_args()

    engine = KnowledgeEngine(args.repo)
    objects = engine.build_index()
    output = engine.save_index(args.out)
    print(f"Future Leaders AI v11 index built: {len(objects)} objects -> {output}")


if __name__ == "__main__":
    main()
