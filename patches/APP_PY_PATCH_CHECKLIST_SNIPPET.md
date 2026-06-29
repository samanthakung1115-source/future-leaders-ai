
# v1.1 Patch 10 - Install Checklist app.py 插入片段

## 1. 在 app.py import 區加入

如果你的 app.py 使用 `src/` 結構：

```python
from src.patch_checklist import render_patch_install_checklist
```

如果你的 app.py 已經把 `src` 加進 `sys.path`：

```python
from patch_checklist import render_patch_install_checklist
```

## 2. 在 Debug / Settings 頁加入

```python
if page == "Patch Install Checklist":
    render_patch_install_checklist()
```

## 3. 或放到 sidebar

```python
with st.sidebar.expander("✅ Patch 安裝檢查"):
    render_patch_install_checklist()
```
