#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from future_leaders_ai import DiscoveryEngine, KnowledgeEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Future Leaders AI v11 discovery analysis.")
    parser.add_argument("--repo", default=".", help="Path to future-leaders-ai repository root.")
    parser.add_argument("--company", action="append", required=True, help="Ticker/company symbol. Can be repeated.")
    parser.add_argument("--out", default=".samantha/discovery_report.json", help="Output JSON path.")
    args = parser.parse_args()

    knowledge = KnowledgeEngine(args.repo)
    knowledge.build_index()
    discovery = DiscoveryEngine(knowledge)
    reports = discovery.analyze_universe(args.company)
    payload = [DiscoveryEngine.to_dict(report) for report in reports]

    out = Path(args.out)
    if not out.is_absolute():
        out = Path(args.repo) / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Discovery report written: {out}")


if __name__ == "__main__":
    main()
