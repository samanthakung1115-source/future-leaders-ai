
# v1.1 Patch 07 - Unified STS + Live Price Pipeline app.py 插入片段

## 目的

把前面的 Patch 串起來：

```text
STS Google Sheet
    ↓
Column Mapper
    ↓
Live Price
    ↓
Portfolio / Radar / Samantha Brief
```

---

## 1. 在 app.py import 區加入

如果你的 app.py 使用 `src/` 結構：

```python
from src.unified_pipeline import build_unified_sts_live_pipeline, render_unified_pipeline_status
```

如果你的 app.py 已經把 `src` 加進 `sys.path`：

```python
from unified_pipeline import build_unified_sts_live_pipeline, render_unified_pipeline_status
```

---

## 2. 在 Portfolio Center 或 Dashboard 開始處加入

```python
unified_df, pipeline_status = build_unified_sts_live_pipeline(
    enable_live_price=True,
    ticker_col="ticker"
)

render_unified_pipeline_status(pipeline_status)

if not unified_df.empty:
    st.dataframe(unified_df, use_container_width=True)
```

---

## 3. 如果你想把原本 Excel Upload 當 fallback

假設你原本的 DataFrame 叫 `uploaded_df`：

```python
unified_df, pipeline_status = build_unified_sts_live_pipeline(
    fallback_df=uploaded_df,
    enable_live_price=True,
    ticker_col="ticker"
)
```

---

## 4. 給 Samantha Brief 使用

如果你已安裝 Patch 05：

```python
render_samantha_brief(
    radar_df=unified_df,
    portfolio_df=unified_df
)
```

---

## 5. 給 Radar 使用

如果你有原本的 radar_df，也可以先用 unified_df：

```python
radar_df = unified_df
```

或把你的 radar_df 另外跑 Patch 03：

```python
radar_df = enrich_radar_with_live_price(
    radar_df,
    ticker_col="ticker",
    action_col="tonight_action"
)
```

---

## 6. 建議放置順序

在 app.py 中建議順序：

```python
refresh_config = render_auto_refresh_controls(default_seconds=60)
apply_auto_refresh(refresh_config)

unified_df, pipeline_status = build_unified_sts_live_pipeline(enable_live_price=True)
render_unified_pipeline_status(pipeline_status)

render_samantha_brief(
    radar_df=unified_df,
    portfolio_df=unified_df
)
```
