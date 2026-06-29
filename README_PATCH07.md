
# Future Leaders AI v1.1 Patch 07 - Unified STS + Live Price Pipeline Patch

## 這是 Patch，不是完整覆蓋版

請只新增：

```text
src/unified_pipeline/__init__.py
src/unified_pipeline/unified_pipeline_patch.py
patches/APP_PY_UNIFIED_PIPELINE_SNIPPET.md
README_PATCH07.md
```

然後依照 `patches/APP_PY_UNIFIED_PIPELINE_SNIPPET.md` 修改你現有的 `app.py`。

## 功能

把前面 Patch 串起來：

- Patch 02：STS Live Sync
- Patch 06：STS Column Mapper
- Patch 01：Live Price
- Patch 05：Samantha Brief 可直接吃 unified_df

## 產出

```python
unified_df
pipeline_status
```

`unified_df` 會包含：

- STS 原始資料
- 標準化欄位
- Live Price
- Live %
- 52W High
- Dist High %
- Live Action

## Commit 建議

```text
feat: add v1.1 patch07 unified sts live pipeline
```
