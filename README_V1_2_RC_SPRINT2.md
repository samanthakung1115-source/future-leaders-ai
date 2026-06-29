
# Future Leaders AI v1.2 RC Sprint 2 - Service Registry

## Goal

Create a central service registry.

## Why

Before this sprint, `app.py` and pages may import many patch modules directly.

This sprint introduces:

```python
registry = get_registry()
registry.get("unified_pipeline")
registry.call("samantha_brief", ...)
```

## Registered services

- sts_sync
- sts_mapper
- live_price
- price_cache
- unified_pipeline
- pipeline_status
- samantha_brief
- patch_health
- install_checklist
- v11_control_center
- v11_launcher

## Run

```bash
streamlit run app.py
```

## Test

```bash
python tests/test_v12_rc_sprint2_service_registry.py
```

Expected:

```text
Future Leaders AI v1.2 RC Sprint 2 Service Registry test passed.
```

## Suggested commit

```text
refactor: add v1.2 rc sprint2 service registry
```
