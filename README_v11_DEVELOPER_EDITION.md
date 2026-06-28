# Future Leaders AI v11 Developer Edition

這是 v11 的正式開發起始包。

原則：

- 以 `future-leaders-ai` Repository 為唯一基礎。
- 優先沿用既有 `docs/`、`knowledge/`、`companies/`、`playbooks/`、`prompts/`、`specs/`、`tests/`。
- 不新增大型平行資料夾架構。
- `stock-terminal-pro` 保持獨立，僅透過 `samantha.discovery_signal.v11` 資料契約接收 Discovery Intelligence。

## 安裝方式

將本 ZIP 解壓到 `future-leaders-ai` Repository 根目錄。

## 建立 Knowledge Index

```bash
python scripts/build_knowledge_index.py --repo .
```

輸出：

```text
.samantha/knowledge_index.json
```

## 執行 Discovery

```bash
python scripts/run_discovery.py --repo . --company NVDA --company MU --company CRDO
```

輸出：

```text
.samantha/discovery_report.json
```

## 測試

```bash
pytest
```

## v11 模組

- `future_leaders_ai/knowledge_engine.py`
- `future_leaders_ai/discovery_engine.py`
- `future_leaders_ai/ai_consensus.py`
- `specs/samantha_discovery_signal_v11.schema.json`

## 與 STS 的分工

`future-leaders-ai`：Discovery Intelligence、Knowledge Engine、AI Consensus。

`stock-terminal-pro`：Portfolio Intelligence、持股、成本、交易、Recovery AI。
