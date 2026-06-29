
# v1.1 Patch 14 - Control Center app.py 插入片段

## 目的

新增一個完整 v1.1 控制中心：

```python
render_v11_control_center()
```

包含：

- Live Pipeline
- Samantha Brief
- Patch Health
- Install Checklist

---

## 1. 在 app.py import 區加入

如果你的 app.py 使用 `src/` 結構：

```python
from src.v11_control_center import render_v11_control_center
```

如果你的 app.py 已經把 `src` 加進 `sys.path`：

```python
from v11_control_center import render_v11_control_center
```

---

## 2. 加到你的 sidebar page 選單

如果你有：

```python
page = st.sidebar.radio("功能", [...])
```

請加入：

```python
"v1.1 Control Center"
```

然後下面加入：

```python
if page == "v1.1 Control Center":
    render_v11_control_center()
```

---

## 3. 或直接放在首頁下方

```python
with st.expander("🧠 v1.1 Control Center"):
    render_v11_control_center()
```

---

## 4. 建議

這個 Patch 可以取代 Patch 13 Launcher 的日常使用。

Patch 13 是選單。  
Patch 14 是真正控制中心。
