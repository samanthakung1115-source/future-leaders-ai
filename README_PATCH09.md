
# Future Leaders AI v1.1 Patch 09 - Live Price Cache & Rate Limit Patch

## 這是 Patch，不是完整覆蓋版

請只新增：

```text
src/price_cache/__init__.py
src/price_cache/price_cache_patch.py
patches/APP_PY_PRICE_CACHE_SNIPPET.md
README_PATCH09.md
```

然後依照 `patches/APP_PY_PRICE_CACHE_SNIPPET.md` 修改你現有的 `app.py`。

## 功能

- Live Price JSON cache
- TTL 快取
- 避免每次刷新都打 yfinance
- 保留上次成功價格
- 適合 Patch 04 Auto Refresh

## Commit 建議

```text
feat: add v1.1 patch09 live price cache
```
