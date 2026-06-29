
# Future Leaders AI v1.2 RC Sprint 4 - Logging + Error Boundary

## Goal

Add centralized logging and safe error boundaries.

## Added

- `src/app_logging/logger.py`
- `src/error_boundary/boundary.py`
- `safe_render()`
- `error_boundary()` context manager
- Streamlit demo page
- tests

## Why

When one page or patch fails, the whole Streamlit app should not crash.

## Usage

```python
from error_boundary import safe_render, error_boundary

safe_render(render_v11_control_center, title="v1.1 Control Center")

with error_boundary("Radar"):
    render_radar()
```

## Run

```bash
streamlit run app.py
```

## Test

```bash
python tests/test_v12_rc_sprint4_logging_error_boundary.py
```

Expected:

```text
Future Leaders AI v1.2 RC Sprint 4 Logging + Error Boundary test passed.
```

## Suggested commit

```text
refactor: add v1.2 rc sprint4 logging error boundary
```
