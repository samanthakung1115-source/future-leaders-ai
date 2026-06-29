
# v1.1 Patch 03 - Radar Live Price app.py 插入片段

## 目的

讓「Next DDOG / CRDO / RKLB Radar」表格加入盤中即時現價。

---

## 1. 在 app.py import 區加入

如果你的 app.py 使用 `src/` 結構：

```python
from src.radar_live import enrich_radar_with_live_price
```

如果你的 app.py 已經把 `src` 加進 `sys.path`：

```python
from radar_live import enrich_radar_with_live_price
```

---

## 2. 找到 Radar 表格產生處

你可能有類似：

```python
st.dataframe(radar_df, use_container_width=True)
```

在顯示前加入：

```python
radar_df = enrich_radar_with_live_price(
    radar_df,
    ticker_col="Ticker 股票行情",
    action_col="Tonight Action 今晚行動"
)

st.dataframe(radar_df, use_container_width=True)
```

---

## 3. 如果你的欄位名稱不同

如果股票欄叫 `Ticker`：

```python
radar_df = enrich_radar_with_live_price(radar_df, ticker_col="Ticker")
```

如果今晚行動欄叫 `Tonight Action`：

```python
radar_df = enrich_radar_with_live_price(
    radar_df,
    ticker_col="Ticker",
    action_col="Tonight Action"
)
```

---

## 4. 新增欄位

會新增：

```text
Live Price 最新價
Live % 今日%
52W High 前高
Dist High % 距前高%
Live Action 即時行動
Price Source 報價來源
```

---

## 5. 注意

`yfinance` 報價可能依交易所延遲，不一定是真正逐筆即時報價。  
但對 Radar 判斷「追不追、等不等、是否太接近高點」已經很有幫助。
