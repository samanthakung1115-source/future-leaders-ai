
# Future Leaders AI v1.1 Sprint 1 - Live Price Engine

## Goal

Add intraday / delayed live price support.

## Added

- `LivePriceEngine`
- `PriceSnapshot`
- `LiveActionEngine`
- `CandidatePriceEnricher`
- Streamlit live price page
- Sample candidate CSV
- Tests

## Columns created

- latest price
- day change %
- 52-week high
- distance from high %
- live action

## Run

```bash
streamlit run app.py
```

## Test

```bash
python tests/test_v11_sprint1_live_price.py
```

Expected:

```text
Future Leaders AI v1.1 Sprint 1 Live Price Engine test passed.
```

## Suggested commit

```text
feat: add v1.1 sprint1 live price engine
```
