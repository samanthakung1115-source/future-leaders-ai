
# v1.1 Patch 02 - STS Live Sync app.py 插入片段

## 1. 在 app.py 的 import 區加入

如果你的 app.py 使用 `src/` 結構：

```python
from src.sts_sync import STSLiveSyncPatch
```

如果你的 app.py 已經把 `src` 加進 `sys.path`，用：

```python
from sts_sync import STSLiveSyncPatch
```

## 2. 在 Portfolio Center 區塊中，取代 Excel Upload

找到類似這段：

```python
uploaded = st.file_uploader("上傳 STS Excel")
df, sheet = read_sts_excel(uploaded, hide_sold=hide_sold)
```

改成：

```python
if st.button("🔄 從 Google Sheet 同步 STS"):
    df, sync_status = STSLiveSyncPatch().read()

    if sync_status.ok:
        st.success(sync_status.message)
    else:
        st.warning(sync_status.message)

    st.caption(f"同步時間：{sync_status.synced_at}｜資料列數：{sync_status.rows}")
else:
    df = None
```

## 3. 若要保留 Excel Upload 當備用

```python
sync_mode = st.radio("資料來源", ["Google Sheet", "Excel Upload"])

if sync_mode == "Google Sheet":
    df, sync_status = STSLiveSyncPatch().read()
    st.caption(f"同步時間：{sync_status.synced_at}｜資料列數：{sync_status.rows}")
else:
    uploaded = st.file_uploader("上傳 STS Excel")
    if uploaded:
        df, sheet = read_sts_excel(uploaded, hide_sold=hide_sold)
    else:
        df = None
```

## 4. 正確檔案位置

```text
config/sync_config.json
src/sts_sync/__init__.py
src/sts_sync/sts_live_sync_patch.py
```

GitHub 顯示時應該是資料夾，不是檔名含 `/`。
