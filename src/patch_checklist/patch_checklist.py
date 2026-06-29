
from __future__ import annotations

import streamlit as st


def render_patch_install_checklist():
    """Render a safe patch install checklist inside Streamlit."""
    st.subheader("✅ Patch 安裝檢查清單")

    st.markdown("""
### 1. 不要覆蓋整個專案

Patch 只上傳新增檔案，不要重新上傳整包專案。

---

### 2. 正確資料夾位置

GitHub 應該看到：

```text
src/live_price/
src/sts_sync/
src/radar_live/
src/auto_refresh/
src/samantha_brief/
src/sts_mapper/
src/unified_pipeline/
src/patch_health/
src/price_cache/
```

而不是：

```text
future-leaders-ai-v1.1-patch01-live-price/src/live_price/
```

如果看到多一層 patch 資料夾，代表上傳錯層。

---

### 3. 不要上傳 Python 快取

請刪掉：

```text
__pycache__/
*.pyc
*.pyo
```

---

### 4. app.py 只手動加 snippet

每個 Patch 裡的 `patches/*.md` 只告訴你要加哪幾行。

不要整個覆蓋 app.py。

---

### 5. requirements.txt

如果 Patch 有 `requirements_add.txt`，只把裡面的套件加到原本 requirements.txt。

---

### 6. 建議 Commit 順序

```text
feat: add v1.1 patch01 live price support
feat: add v1.1 patch02 sts live sync
feat: add v1.1 patch03 radar live price
feat: add v1.1 patch04 auto refresh
feat: add v1.1 patch05 samantha brief
feat: add v1.1 patch06 sts column mapper
feat: add v1.1 patch07 unified pipeline
chore: add v1.1 patch08 patch health check
feat: add v1.1 patch09 live price cache
chore: add v1.1 patch10 install checklist
```
""")
