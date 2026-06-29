# Future Leaders AI v11 Beta 5 - Sprint 2

This package adds the first real parsing and indexing layer.

## Included

- `src/knowledge_engine/knowledge_parser.py`
- `src/knowledge_engine/knowledge_index.py`
- updated Knowledge Engine exports
- parser/index tests
- sample company files: NVDA, CRDO

## What works

- Load Markdown company files
- Parse title, status, summary, DNA, risks, tags, verdict, confidence
- Build company objects
- Build DNA / status / tag indexes
- Query companies by ticker and DNA

## Test

```bash
python tests/test_knowledge_parser_index.py
```

Expected output:

```text
Sprint 2 parser/index tests passed.
```

## Suggested commit message

```text
feat: add knowledge parser and index
```
