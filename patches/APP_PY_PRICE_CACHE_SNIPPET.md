
# v1.1 Patch 09 - Live Price Cache app.py 插入片段

## 目的

避免每次 Auto Refresh 都重新抓全部 yfinance 報價。

這會讓 Live Price / Radar / Unified Pipeline：

- 更快
- 更穩
- 比較不容易被 API 限制
- 失敗時仍可保留上次成功價格

---

## 1. 在 app.py import 區加入

如果你的 app.py 使用 `src/` 結構：

```python
from src.price_cache import enrich_with_cached_live_price
```

如果你的 app.py 已經把 `src` 加進 `sys.path`：

```python
from price_cache import enrich_with_cached_live_price
```

---

## 2. 用在 Radar / Portfolio 表格

```python
df = enrich_with_cached_live_price(
    df,
    ticker_col="ticker",
    action_col="tonight_action",
    ttl_seconds=60
)
```

如果欄位叫 `Ticker 股票行情`：

```python
df = enrich_with_cached_live_price(
    df,
    ticker_col="Ticker 股票行情",
    action_col="Tonight Action 今晚行動",
    ttl_seconds=60
)
```

---

## 3. 建議取代 Patch 01 / Patch 03 的即時抓價

原本：

```python
df = enrich_with_live_price(df, ticker_col="ticker")
```

可以改成：

```python
df = enrich_with_cached_live_price(df, ticker_col="ticker", ttl_seconds=60)
```

---

## 4. Cache 位置

預設會產生：

```text
data/cache/live_price_cache.json
```

建議 `.gitignore` 加入：

```text
data/cache/*.json
data/cache/*.csv
```

---

## 5. TTL 建議

盤中看盤：

```text
ttl_seconds=60
```

比較保守：

```text
ttl_seconds=120
```
