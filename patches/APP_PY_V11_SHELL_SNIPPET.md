
# v1.1 Patch 12 - App Integration Shell app.py 插入片段

## 目的

把 Patch 01～11 的功能集中成一個 Panel：

```python
render_v11_patch_panel()
```

這樣你不用在 `app.py` 到處插很多段。

---

## 1. 在 app.py import 區加入

如果你的 app.py 使用 `src/` 結構：

```python
from src.v11_shell import render_v11_patch_panel
```

如果你的 app.py 已經把 `src` 加進 `sys.path`：

```python
from v11_shell import render_v11_patch_panel
```

---

## 2. 在側邊欄或頁面選單加入

如果你有：

```python
page = st.sidebar.radio(...)
```

可以加一個頁面：

```python
if page == "v1.1 Patch Panel":
    render_v11_patch_panel()
```

---

## 3. 或直接放在首頁下方

```python
with st.expander("🧠 v1.1 Patch Panel"):
    render_v11_patch_panel()
```

---

## 4. 這個 Shell 會安全呼叫

- Unified Pipeline
- Samantha Brief
- Patch Health Check

若某個 Patch 沒裝好，它會顯示 warning，不會讓整個 App 掛掉。
