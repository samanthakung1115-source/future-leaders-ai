# Future Leaders AI v1.1 Sprint 2 - STS Live Sync Engine

## Goal

Read STS directly from Google Sheets CSV export URL.

## Your STS CSV URL

```text
https://docs.google.com/spreadsheets/d/1KnMA2MxX58ZpmM8zZ6_eJ7fcdB47lF1m4oBpdIcWebE/export?format=csv&gid=1389414286
```

## Added

- `SyncConfig`
- `STSLiveSyncEngine`
- Google Sheets CSV sync
- Local cache fallback
- Streamlit STS sync page
- Sync test

## Run

```bash
streamlit run app.py
```

## Test

```bash
python tests/test_v11_sprint2_sts_sync.py
```

Expected:

```text
Future Leaders AI v1.1 Sprint 2 STS Live Sync Engine test passed.
```

## Suggested commit

```text
feat: add v1.1 sprint2 sts live sync engine
```
