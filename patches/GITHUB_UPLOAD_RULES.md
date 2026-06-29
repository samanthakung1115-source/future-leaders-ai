
# GitHub 上傳規則

## 正確

解壓縮 ZIP 後，進入解壓後資料夾裡面，把裡面的：

```text
src/
patches/
config/
README...
UPDATE...
requirements_add.txt
```

拖進 GitHub。

## 錯誤

不要把整個外層資料夾拖進 GitHub。

錯誤例子：

```text
future-leaders-ai-v1.1-patch09-live-price-cache/
    src/
    patches/
```

正確應該是：

```text
src/
    price_cache/
patches/
    APP_PY_PRICE_CACHE_SNIPPET.md
```

## 刪除

如果 GitHub 裡已經有：

```text
__pycache__
*.pyc
*.pyo
```

請刪掉。
