
# v1.1 Patch 05 - Samantha One-Line Brief app.py 插入片段

## 目的

在首頁最上方加入：

```text
🧠 Samantha 今日一句話
```

它會把 Radar、Portfolio、Decision Coach 的資訊濃縮成今天最重要的提醒。

---

## 1. 在 app.py import 區加入

如果你的 app.py 使用 `src/` 結構：

```python
from src.samantha_brief import render_samantha_brief
```

如果你的 app.py 已經把 `src` 加進 `sys.path`：

```python
from samantha_brief import render_samantha_brief
```

---

## 2. 在首頁最上方加入

如果你已經有：

```python
radar_df
portfolio_df
coach_notes
```

請在 Dashboard 標題下面加入：

```python
render_samantha_brief(
    radar_df=radar_df,
    portfolio_df=portfolio_df,
    coach_notes=coach_notes
)
```

---

## 3. 如果你目前只有 Radar 表格

```python
render_samantha_brief(radar_df=radar_df)
```

---

## 4. 如果你目前只有 Portfolio 表格

```python
render_samantha_brief(portfolio_df=portfolio_df)
```

---

## 5. 如果你的變數名稱不同

例如你的 Radar 表格叫：

```python
next_winners_df
```

就用：

```python
render_samantha_brief(radar_df=next_winners_df)
```

例如你的持股表格叫：

```python
holdings_df
```

就用：

```python
render_samantha_brief(portfolio_df=holdings_df)
```

---

## 6. 這版會自動辨識常見欄位

Ticker 欄位：

```text
Ticker 股票行情
Ticker
ticker
股票
代碼
Symbol
symbol
```

行動欄位：

```text
Live Action 即時行動
Live Action
Tonight Action 今晚行動
Tonight Action
```

報酬欄位：

```text
cost_return_pct
距成本%
距成本
Return %
報酬率%
損益%
```
