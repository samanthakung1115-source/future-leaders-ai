
# v1.2 RC Integration 1 - Dashboard 接回 Main Launcher

## 目的

讓左側選單的 Dashboard 優先載入新的整合 Dashboard：

```python
ui.dashboard_integrated.render_dashboard
```

---

## 1. 上傳新增檔案

```text
src/ui/dashboard_integrated.py
```

---

## 2. 修改 src/main_launcher/launcher.py

找到 Dashboard 這一段：

```python
candidates = [
    ("ui.dashboard", "render_dashboard"),
    ("ui.release_dashboard", "render_release_dashboard"),
    ("ui.main_dashboard", "render"),
]
```

改成：

```python
candidates = [
    ("ui.dashboard_integrated", "render_dashboard"),
    ("ui.dashboard", "render_dashboard"),
    ("ui.release_dashboard", "render_release_dashboard"),
    ("ui.main_dashboard", "render"),
]
```

---

## 3. 效果

左側點 Dashboard 時，會顯示：

- Samantha 今日 AI 摘要
- STS Sync 狀態
- Column Mapper 狀態
- Live Price 狀態
- Unified DataFrame 預覽
- Patch Health Check

---

## 4. 不要覆蓋 app.py

這次不需要覆蓋 app.py。
