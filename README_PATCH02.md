# Future Leaders AI v1.1 Patch 02 - STS Live Sync Patch

## 這是 Patch，不是完整覆蓋版

請只新增：

```text
config/sync_config.json
src/sts_sync/__init__.py
src/sts_sync/sts_live_sync_patch.py
patches/APP_PY_STS_SYNC_INSERT_SNIPPET.md
```

然後依照 `patches/APP_PY_STS_SYNC_INSERT_SNIPPET.md` 修改你現有的 `app.py`。

## 已內建你的 Google Sheet CSV URL

```text
https://docs.google.com/spreadsheets/d/1KnMA2MxX58ZpmM8zZ6_eJ7fcdB47lF1m4oBpdIcWebE/export?format=csv&gid=1389414286
```

## 功能

- 不再需要下載 Excel 再上傳
- 直接從 Google Sheet CSV 同步 STS
- 同步失敗時使用 cache
- 回傳同步狀態、資料列數、欄位

## requirements.txt 請確認有

```text
pandas
requests
openpyxl
```

## Commit 建議

```text
feat: add v1.1 patch02 sts live sync
```
