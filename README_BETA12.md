
# Future Leaders AI v11 Beta 12

## Goal

Add Action Plan v1.

This version converts Samantha Unified Brief into actionable next steps.

## Added

- `src/action_plan/action_plan_engine.py`
- `src/ui/action_plan_page.py`
- `app_beta12.py`
- sample candidate CSV
- sample STS CSV
- Beta 12 test

## Run

```bash
streamlit run app_beta12.py
```

## Test

```bash
python tests/test_beta12_action_plan.py
```

Expected output:

```text
Beta 12 Action Plan test passed.
```

## Suggested commit

```text
feat: add beta12 action plan engine
```
