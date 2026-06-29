
# v1.1 Patch 06 - STS Column Mapper app.py 插入片段

## 目的

Google Sheet 同步後，欄位可能是中文、英文、或 STS 自訂名稱。

這個 Patch 會把欄位標準化成：

```text
ticker
shares
cost
market_value
return_pct
distance_from_high_pct
ai_score
tonight_action
category
```

這樣 Portfolio、Radar、Samantha Brief、Live Price 都可以用同一套欄位。

---

## 1. 在 app.py import 區加入

如果你的 app.py 使用 `src/` 結構：

```python
from src.sts_mapper import normalize_sts_columns, detect_sts_columns
```

如果你的 app.py 已經把 `src` 加進 `sys.path`：

```python
from sts_mapper import normalize_sts_columns, detect_sts_columns
```

---

## 2. 在 STS Google Sheet 同步後加入

如果你有：

```python
df, sync_status = STSLiveSyncPatch().read()
```

請在下一行加入：

```python
df = normalize_sts_columns(df)
```

完整例子：

```python
df, sync_status = STSLiveSyncPatch().read()
df = normalize_sts_columns(df)

st.caption(f"同步時間：{sync_status.synced_at}｜資料列數：{sync_status.rows}")
st.dataframe(df, use_container_width=True)
```

---

## 3. 如果你想檢查欄位對應

```python
mapping = detect_sts_columns(df)
st.json(mapping)
```

---

## 4. 之後 Live Price 可直接用標準欄位

例如：

```python
df = enrich_with_live_price(df, ticker_col="ticker")
```

Radar 也可以用：

```python
radar_df = enrich_radar_with_live_price(
    radar_df,
    ticker_col="ticker",
    action_col="tonight_action"
)
```

---

## 5. 常見對應

```text
Ticker 股票行情 / 股票 / 代碼 / Ticker -> ticker
股數 / 持股數 -> shares
成本 / 平均成本 -> cost
市值 / 現值 -> market_value
距成本% / 報酬率% / 損益% -> return_pct
距前高% -> distance_from_high_pct
AI Score / AI分數 -> ai_score
Tonight Action / 今晚行動 / 建議動作 -> tonight_action
類別 / 產業 / Theme -> category
```
