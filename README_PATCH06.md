
# Future Leaders AI v1.1 Patch 06 - STS Column Mapper Patch

## 這是 Patch，不是完整覆蓋版

請只新增：

```text
src/sts_mapper/__init__.py
src/sts_mapper/sts_column_mapper_patch.py
patches/APP_PY_STS_COLUMN_MAPPER_SNIPPET.md
README_PATCH06.md
```

然後依照 `patches/APP_PY_STS_COLUMN_MAPPER_SNIPPET.md` 修改你現有的 `app.py`。

## 功能

把 STS / Google Sheet 欄位標準化：

- ticker
- shares
- cost
- market_value
- return_pct
- distance_from_high_pct
- ai_score
- tonight_action
- category

## 為什麼重要？

因為你的 STS 可能有中文欄位，Radar / Portfolio / Samantha Brief / Live Price 需要穩定欄位才能自動分析。

## Commit 建議

```text
feat: add v1.1 patch06 sts column mapper
```
