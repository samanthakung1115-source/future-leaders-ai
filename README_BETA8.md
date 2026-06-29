
# Future Leaders AI v11 Beta 8

## Goal

Make Samantha Daily Brief usable with uploaded candidate CSV files.

## Added

- `src/product/candidate_loader.py`
- Updated `src/product/daily_brief_service.py`
- Updated `src/ui/samantha_daily_brief_page.py`
- `app_beta8.py`
- `data/samples/beta8_candidates.csv`
- `tests/test_beta8_candidate_csv.py`

## CSV format

Required columns:

- `ticker`
- `score`

Optional columns:

- `why_selected`
- `risks`

Use semicolon-separated text for multiple reasons or risks.

## Run locally

```bash
streamlit run app_beta8.py
```

## Test

```bash
python tests/test_beta8_candidate_csv.py
```

Expected output:

```text
Beta 8 Candidate CSV + Daily Brief test passed.
```

## Suggested commit

```text
feat: add beta8 candidate csv daily brief
```
