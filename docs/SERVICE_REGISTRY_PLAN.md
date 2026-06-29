
# Service Registry Plan

v1.2 will move from patch import style to service registry style.

Current:

```python
from unified_pipeline import build_unified_sts_live_pipeline
from samantha_brief import render_samantha_brief
```

Target:

```python
registry = get_registry()
pipeline = registry.get("unified_pipeline")
brief = registry.get("samantha_brief")
```

Benefits:
- safer imports
- easier health checks
- easier v1.2 consolidation
- fewer app.py edits
