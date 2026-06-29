
# Future Leaders AI v1.1 Patch 04 - Auto Refresh Patch

## 這是 Patch，不是完整覆蓋版

請只新增：

```text
src/auto_refresh/__init__.py
src/auto_refresh/auto_refresh_patch.py
patches/APP_PY_AUTO_REFRESH_SNIPPET.md
README_PATCH04.md
```

然後依照 `patches/APP_PY_AUTO_REFRESH_SNIPPET.md` 修改你現有的 `app.py`。

## 功能

- Sidebar 自動刷新控制
- 30 / 60 / 120 秒 / 5 分鐘
- 適合 Live Price
- 適合 Radar
- 適合 STS Sync
- 不需要額外套件

## Commit 建議

```text
feat: add v1.1 patch04 auto refresh
```
