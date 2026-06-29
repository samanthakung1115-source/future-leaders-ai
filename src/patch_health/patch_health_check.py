
from __future__ import annotations

from pathlib import Path
import importlib
import streamlit as st


PATCH_MODULES = {
    "Patch 01 Live Price": "live_price",
    "Patch 02 STS Sync": "sts_sync",
    "Patch 03 Radar Live": "radar_live",
    "Patch 04 Auto Refresh": "auto_refresh",
    "Patch 05 Samantha Brief": "samantha_brief",
    "Patch 06 STS Mapper": "sts_mapper",
    "Patch 07 Unified Pipeline": "unified_pipeline",
}


BAD_PATTERNS = [
    "__pycache__",
    ".pyc",
    ".pyo",
]


def _can_import(module_name: str) -> tuple[bool, str]:
    try:
        importlib.import_module(module_name)
        return True, "OK"
    except Exception as exc:
        return False, str(exc)


def _find_bad_files(project_root: str | Path = ".") -> list[str]:
    root = Path(project_root)
    bad = []
    for path in root.rglob("*"):
        text = str(path)
        if any(pattern in text for pattern in BAD_PATTERNS):
            bad.append(text)
    return bad


def check_patch_health(project_root: str | Path = ".") -> dict:
    """Check installed v1.1 patches and cleanup risks."""
    imports = []
    for label, module_name in PATCH_MODULES.items():
        ok, msg = _can_import(module_name)
        imports.append({
            "patch": label,
            "module": module_name,
            "ok": ok,
            "message": msg,
        })

    bad_files = _find_bad_files(project_root)

    return {
        "imports": imports,
        "bad_files": bad_files,
        "summary": {
            "patches_ok": sum(1 for x in imports if x["ok"]),
            "patches_total": len(imports),
            "bad_files_count": len(bad_files),
            "ok": all(x["ok"] for x in imports) and not bad_files,
        }
    }


def render_patch_health_check(project_root: str | Path = "."):
    """Render patch health check in Streamlit."""
    result = check_patch_health(project_root)

    st.subheader("🧩 Patch Health Check")
    s = result["summary"]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Patches OK", f"{s['patches_ok']} / {s['patches_total']}")
    with c2:
        st.metric("Bad Files", s["bad_files_count"])
    with c3:
        st.metric("Overall", "OK" if s["ok"] else "Check")

    st.markdown("### Installed Patch Modules")
    for item in result["imports"]:
        if item["ok"]:
            st.success(f"{item['patch']} — {item['module']} import OK")
        else:
            st.warning(f"{item['patch']} — {item['module']} import failed: {item['message']}")

    if result["bad_files"]:
        st.markdown("### Cleanup Needed")
        st.warning("以下檔案不建議放在 GitHub：")
        for path in result["bad_files"][:100]:
            st.write(f"- {path}")
        if len(result["bad_files"]) > 100:
            st.caption(f"Only showing first 100 of {len(result['bad_files'])} files.")
    else:
        st.success("No __pycache__ / .pyc cleanup issues found.")

    with st.expander("Raw Health Result"):
        st.json(result)
