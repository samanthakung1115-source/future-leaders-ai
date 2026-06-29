
# v1.2 RC Sprint 4 - app.py 使用片段

## Import

```python
from error_boundary import safe_render, error_boundary
from app_logging import log_event, log_error
```

## Safe Page Render

原本：

```python
render_v11_control_center()
```

改成：

```python
safe_render(render_v11_control_center, title="v1.1 Control Center")
```

## Section Boundary

```python
with error_boundary("Radar"):
    render_radar()
```
