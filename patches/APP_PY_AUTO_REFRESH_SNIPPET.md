
# v1.1 Patch 04 - Auto Refresh app.py 插入片段

## 目的

讓你的 Dashboard / Radar / STS Sync / Live Price 可以每 30、60、120 秒自動刷新。

---

## 1. 在 app.py import 區加入

如果你的 app.py 使用 `src/` 結構：

```python
from src.auto_refresh import render_auto_refresh_controls, apply_auto_refresh
```

如果你的 app.py 已經把 `src` 加進 `sys.path`：

```python
from auto_refresh import render_auto_refresh_controls, apply_auto_refresh
```

---

## 2. 在 app.py 主畫面開始處加入

建議放在 `st.set_page_config(...)` 後面，或主函數一開始：

```python
refresh_config = render_auto_refresh_controls(default_seconds=60)
apply_auto_refresh(refresh_config)
```

---

## 3. 使用效果

左側 sidebar 會多一個：

```text
🔄 Auto Refresh 自動刷新
```

可選：

```text
30 秒
60 秒
120 秒
5 分鐘
```

---

## 4. 建議用法

如果你正在看盤中價格：

```text
60 秒
```

如果你怕 API 抓太頻繁：

```text
120 秒 或 5 分鐘
```

---

## 5. 注意

這個 Patch 不需要額外安裝 `streamlit-autorefresh`，使用 Streamlit 內建 rerun。
