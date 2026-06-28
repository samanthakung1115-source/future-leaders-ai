# Future Leaders AI v11 — Knowledge Engine 開發起點

v11 的方向：停止大量新增 Markdown，開始讓 AI 讀取 `knowledge/`、`docs/`、`tests/`、`specs/`、`prompts/`、`playbooks/`、`companies/`，建立可查詢的 Knowledge Index。

## 安裝到 repo

把以下資料夾放到 `future-leaders-ai` 根目錄：

- `knowledge_engine/`
- `scripts/build_knowledge_index.py`
- `tests/test_knowledge_engine.py`

## 建立索引

```bash
python scripts/build_knowledge_index.py --repo .
```

輸出：

```text
.samantha/knowledge_index.json
```

## v11 原則

- Future Leaders AI = Discovery Intelligence
- STS stock-terminal-pro = Portfolio Intelligence
- Samantha AI Platform = Discovery + Portfolio
- v11 不再以文件為主，而是以可執行 Knowledge Engine 為主
