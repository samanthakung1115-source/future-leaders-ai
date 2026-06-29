
# Future Leaders AI v1.2 RC Integration 1 - Dashboard Integration

## Goal

Make the Dashboard page actually use the current pipeline.

## Added

```text
src/ui/dashboard_integrated.py
```

## Connects

- Unified Pipeline
- Samantha Brief
- STS Sync status
- Column Mapper status
- Live Price status
- Patch Health Check

## Required manual edit

Edit `src/main_launcher/launcher.py` so Dashboard candidate order includes:

```python
("ui.dashboard_integrated", "render_dashboard")
```

as the first candidate.

See:

```text
patches/MAIN_LAUNCHER_DASHBOARD_INTEGRATION_SNIPPET.md
```

## Suggested commit

```text
feat: add v1.2 rc integration1 dashboard
```
