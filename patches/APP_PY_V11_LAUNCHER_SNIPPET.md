
# v1.1 Patch 13 - Launcher Menu app.py 插入片段

## 目的

新增一個 v1.1 Patch Launcher Menu，讓你不用到處找功能。

---

## 1. 在 app.py import 區加入

如果你的 app.py 使用 `src/` 結構：

```python
from src.v11_launcher import render_v11_launcher_menu
```

如果你的 app.py 已經把 `src` 加進 `sys.path`：

```python
from v11_launcher import render_v11_launcher_menu
```

---

## 2. 加到你的 sidebar page 選單

如果你有：

```python
page = st.sidebar.radio("功能", [...])
```

請加入：

```python
"v1.1 Patch Launcher"
```

然後下面加入：

```python
if page == "v1.1 Patch Launcher":
    render_v11_launcher_menu()
```

---

## 3. 或直接放在首頁下方

```python
with st.expander("🧩 v1.1 Patch Launcher"):
    render_v11_launcher_menu()
```

---

## 4. 這個 Launcher 會提供

- Unified Pipeline
- Samantha Brief
- Patch Health
- Install Checklist
- About v1.1
