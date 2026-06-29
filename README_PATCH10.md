
# Future Leaders AI v1.1 Patch 10 - Install Checklist Patch

## 這是 Patch，不是完整覆蓋版

請只新增：

```text
src/patch_checklist/__init__.py
src/patch_checklist/patch_checklist.py
patches/APP_PY_PATCH_CHECKLIST_SNIPPET.md
patches/PATCH_INSTALL_ORDER.md
patches/GITHUB_UPLOAD_RULES.md
README_PATCH10.md
```

## 功能

新增 Patch 安裝檢查清單，避免：

- 上傳錯層
- 覆蓋 app.py
- 忘記加 requirements
- 把 __pycache__ 放進 GitHub
- Patch 安裝順序混亂

## Commit 建議

```text
chore: add v1.1 patch10 install checklist
```
