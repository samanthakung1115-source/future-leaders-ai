
# v1.1 Patch 01 - app.py 插入片段

## 1. 在 app.py 最上方 import 區加入

```python
from src.live_price import enrich_with_live_price
```

如果你的 app.py 已經有 `sys.path.insert(...)`，也可以用：

```python
from live_price import enrich_with_live_price
```

## 2. 在顯示候選股表格前加入

假設你的表格 DataFrame 叫做 `df`，股票代碼欄位叫 `Ticker`：

```python
df = enrich_with_live_price(df, ticker_col="Ticker")
```

如果欄位叫 `Ticker 股票行情`，請改成：

```python
df = enrich_with_live_price(df, ticker_col="Ticker 股票行情")
```

## 3. 若要自動更新

在 app.py import 區加入：

```python
import time
```

Streamlit Cloud 原生不一定需要自動刷新；建議先用重新整理頁面更新。
之後若要 60 秒自動刷新，我們再做 Patch 02。
