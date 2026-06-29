
# v1.1 Patch 安裝順序

建議順序：

```text
Patch 01 Live Price
Patch 02 STS Live Sync
Patch 06 STS Column Mapper
Patch 09 Live Price Cache
Patch 07 Unified Pipeline
Patch 05 Samantha Brief
Patch 04 Auto Refresh
Patch 03 Radar Live Price
Patch 08 Patch Health Check
Patch 10 Install Checklist
```

## 為什麼這樣排？

核心資料流要先建立：

```text
STS Sync
    ↓
Column Mapper
    ↓
Live Price Cache
    ↓
Unified Pipeline
    ↓
Samantha Brief / Radar / Dashboard
```

## 如果你只想先做最小可用

只裝：

```text
Patch 02
Patch 06
Patch 09
Patch 07
```

就可以先做到：

```text
Google Sheet → 標準欄位 → 現價 → 統一資料表
```
