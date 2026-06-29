
# Future Leaders AI v1.1 Patch 03 - Radar Live Price Patch

## 這是 Patch，不是完整覆蓋版

請只新增：

```text
src/radar_live/__init__.py
src/radar_live/radar_live_price_patch.py
patches/APP_PY_RADAR_LIVE_PRICE_SNIPPET.md
README_PATCH03.md
```

然後依照 `patches/APP_PY_RADAR_LIVE_PRICE_SNIPPET.md` 修改你現有的 `app.py`。

## 功能

專門加到 Next DDOG / CRDO / RKLB Radar：

- Live Price 最新價
- Live % 今日%
- 52W High 前高
- Dist High % 距前高%
- Live Action 即時行動
- Price Source 報價來源

## requirements.txt 請確認有

```text
yfinance>=0.2.54
pandas
```

## Commit 建議

```text
feat: add v1.1 patch03 radar live price
```
