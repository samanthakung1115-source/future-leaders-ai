
# Future Leaders AI v11 Beta 11

## Goal

Create a unified Samantha Brief that combines:

- Future Leaders candidates
- STS portfolio context
- Portfolio warnings
- Discovery reasoning

## Added

- `src/product/unified_brief_service.py`
- `src/ui/unified_brief_page.py`
- `app_beta11.py`
- sample Future Leaders CSV
- sample STS CSV
- test for unified brief

## Run

```bash
streamlit run app_beta11.py
```

## Test

```bash
python tests/test_beta11_unified_brief.py
```

Expected output:

```text
Beta 11 Unified Brief test passed.
```

## Suggested commit

```text
feat: add beta11 unified Samantha brief
```
