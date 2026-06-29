
# Future Leaders AI v1.1 Patch 01 - Live Price Patch

## 這是 Patch，不是完整覆蓋版

請只上傳這些新增檔案：

```text
src/live_price/__init__.py
src/live_price/live_price_patch.py
patches/APP_PY_INSERT_SNIPPET.md
```

然後依照 `APP_PY_INSERT_SNIPPET.md` 手動把 1~2 行程式加到你現有的 `app.py`。

## 功能

新增欄位：

- Live Price
- Live %
- 52W High
- Dist High %
- Live Action
- Price Source

## requirements.txt 請確認有

```text
yfinance>=0.2.54
```

## Commit 建議

```text
feat: add v1.1 patch01 live price support
```
