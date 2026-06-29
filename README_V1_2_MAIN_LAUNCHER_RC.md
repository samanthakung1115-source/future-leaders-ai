
# Future Leaders AI v1.2 Main Launcher RC

## Goal

Fix the current app.py problem.

Current problem:

```python
from ui.sts_sync_page import render
render()
```

This makes the whole app only show STS Live Sync.

## Added

- New root `app.py`
- `src/main_launcher/launcher.py`
- Safe import page rendering
- Sidebar navigation
- Home page
- About page

## Pages

- Home
- Dashboard
- STS Live Sync
- v1.1 Control Center
- v1.1 Patch Launcher
- Patch Health Check
- Install Checklist
- Settings / About

## Important

This time you **should replace app.py**.

## Run

```bash
streamlit run app.py
```

## Suggested commit

```text
refactor: add v1.2 main launcher rc
```
