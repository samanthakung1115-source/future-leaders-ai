
# v1.1 Patch 11 - Safe Import Guard app.py 插入片段

## 目的

避免某個 Patch 還沒安裝好時，整個 app.py 因 import 失敗而不能開。

---

## 1. 在 app.py import 區加入

如果你的 app.py 使用 `src/` 結構：

```python
from src.safe_imports import safe_import, render_missing_patch_warning, load_patch_modules
```

如果你的 app.py 已經把 `src` 加進 `sys.path`：

```python
from safe_imports import safe_import, render_missing_patch_warning, load_patch_modules
```

---

## 2. 安全載入所有 Patch

放在主程式開始處：

```python
patches = load_patch_modules()
```

---

## 3. 使用範例：安全使用 Unified Pipeline

```python
if patches["unified_pipeline"]["ok"]:
    build_unified_sts_live_pipeline = patches["unified_pipeline"]["object"]
    unified_df, pipeline_status = build_unified_sts_live_pipeline(enable_live_price=True)
else:
    render_missing_patch_warning("Unified Pipeline Patch", patches["unified_pipeline"]["error"])
    unified_df = None
```

---

## 4. 使用範例：安全使用 Samantha Brief

```python
if patches["samantha_brief"]["ok"] and unified_df is not None:
    render_samantha_brief = patches["samantha_brief"]["object"]
    render_samantha_brief(radar_df=unified_df, portfolio_df=unified_df)
```

---

## 5. 建議

未來你 app.py 不要直接寫：

```python
from unified_pipeline import build_unified_sts_live_pipeline
```

改用 Patch 11 的 safe import。  
這樣即使某個 Patch 上傳錯，也不會整個 App 掛掉。
