
# Future Leaders AI v11 Beta 13

## Goal

Add one main Streamlit launcher so the app can be started from a single entry point.

## Added

- `app.py`
- `tests/test_beta13_launcher.py`

## Why this matters

Before Beta 13, each feature had its own demo app:

- `app_beta10.py`
- `app_beta11.py`
- `app_beta12.py`

Beta 13 creates the real app entry point:

```bash
streamlit run app.py
```

## Pages

The sidebar can launch:

- Samantha Daily Brief
- Samantha Unified Brief
- Samantha Action Plan
- STS Live Integration
- Project Status

## Test

```bash
python tests/test_beta13_launcher.py
```

Expected output:

```text
Beta 13 Main App Launcher test passed.
```

## Suggested commit

```text
feat: add beta13 main app launcher
```
