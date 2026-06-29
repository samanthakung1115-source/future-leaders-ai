
# Future Leaders AI v11 Beta 6 - Milestone 3

## Goal

Add STS Portfolio Integration v1.

This milestone allows Future Leaders AI to understand whether a candidate company
is already held in the user's portfolio and attach portfolio context to discovery analysis.

## Added

- `src/sts_integration/portfolio_context.py`
- `src/sts_integration/sts_bridge.py`
- `src/ui/portfolio_panel.py`
- `data/samples/sts_portfolio_sample.csv`
- `tests/test_sts_integration.py`

## CSV format

Required column:

- `ticker`

Optional columns:

- `shares`
- `cost_basis`
- `market_value`
- `unrealized_return_pct`
- `distance_from_high_pct`
- `status`

## Test

```bash
python tests/test_sts_integration.py
```

Expected output:

```text
Beta 6 Milestone 3 STS integration tests passed.
```

## Suggested commit

```text
feat: add STS portfolio integration beta6 milestone3
```
