
# v1.1 Patch 08 - Patch Health Check app.py 插入片段

## 目的

檢查目前已安裝的 Patch 01～07：

- 是否 import 成功
- 是否有多餘 `__pycache__`
- 是否有 `.pyc`
- 是否需要清理 GitHub

---

## 1. 在 app.py import 區加入

如果你的 app.py 使用 `src/` 結構：

```python
from src.patch_health import render_patch_health_check
```

如果你的 app.py 已經把 `src` 加進 `sys.path`：

```python
from patch_health import render_patch_health_check
```

---

## 2. 在 sidebar 或設定頁加入

```python
with st.sidebar.expander("🧩 Patch Health Check"):
    if st.button("Run Patch Health Check"):
        render_patch_health_check(".")
```

---

## 3. 或建立一個 Debug / Health Check 頁面

```python
if page == "Patch Health":
    render_patch_health_check(".")
```

---

## 4. 如果看到 __pycache__ / .pyc

請從 GitHub 刪掉：

```text
__pycache__/
*.pyc
*.pyo
```

並建議新增 `.gitignore`：

```text
__pycache__/
*.pyc
*.pyo
.env
.venv/
```
