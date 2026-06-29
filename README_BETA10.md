
# Future Leaders AI v11 Beta 10

## Goal

STS Live Integration v1.

This version lets Samantha read an STS-exported CSV and combine portfolio context
with Future Leaders candidates.

## Added

- `src/sts_live/sts_live_reader.py`
- `src/sts_live/portfolio_brief.py`
- `src/product/samantha_daily_product.py`
- `src/ui/sts_live_page.py`
- `app_beta10.py`
- `data/samples/sts_live_sample.csv`
- `tests/test_beta10_sts_live.py`

## Run

```bash
streamlit run app_beta10.py
```

## Test

```bash
python tests/test_beta10_sts_live.py
```

Expected output:

```text
Beta 10 STS Live Integration test passed.
```

## Suggested commit

```text
feat: add beta10 STS live integration
```
