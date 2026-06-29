
# Future Leaders AI v1.0 Release - Sprint 2

## Goal

Add Future Leaders Ranking Engine v1.

## Added

- Multi-factor ranking model
- Ranking candidate CSV loader
- Weighted score calculation
- Verdict classification
- Rank change indicator
- Streamlit ranking dashboard
- Sprint 2 tests

## Candidate CSV columns

Required:

- `ticker`

Optional:

- `ai_score`
- `growth_score`
- `quality_score`
- `risk_score`
- `previous_rank`
- `theme`
- `dna`
- `why_selected`
- `risks`

## Run

```bash
streamlit run app.py
```

## Test

```bash
python tests/test_release_sprint2.py
```

Expected output:

```text
Future Leaders AI v1.0 Release Sprint 2 test passed.
```

## Suggested commit

```text
feat: add v1 release sprint2 ranking engine
```
