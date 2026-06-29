
# Future Leaders AI v1.0 RC1 - Milestone 4

## Goal

Add Future Leaders Ranking + Research Cards.

This milestone makes every ranked candidate more explainable.

## Added

- `ResearchCard` model
- `ResearchCardEngine`
- Candidate theme and DNA fields
- Research Cards section in dashboard
- Explainable confidence
- Coach notes inside research cards
- RC1 Milestone 4 test

## Candidate CSV

New optional columns:

- `theme`
- `dna`

## Run

```bash
streamlit run app.py
```

## Test

```bash
python tests/test_rc1_milestone4.py
```

Expected output:

```text
Future Leaders AI v1.0 RC1 Milestone 4 test passed.
```

## Suggested commit

```text
feat: add rc1 milestone4 research cards
```
