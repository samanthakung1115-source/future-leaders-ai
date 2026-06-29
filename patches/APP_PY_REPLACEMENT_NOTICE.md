
# v1.2 Main Launcher RC - app.py 替換說明

這次和 Patch 01～14 不一樣。

這次需要替換根目錄的：

```text
app.py
```

原因：

你目前的 app.py 只剩：

```python
from ui.sts_sync_page import render
render()
```

這會讓整個 App 只顯示 STS Sync 頁。

v1.2 Main Launcher RC 會把 app.py 改回主入口：

```text
Home
Dashboard
STS Live Sync
v1.1 Control Center
v1.1 Patch Launcher
Patch Health Check
Install Checklist
Settings / About
```

請上傳本 ZIP 裡的：

```text
app.py
src/main_launcher/
```

這次可以覆蓋 app.py。
