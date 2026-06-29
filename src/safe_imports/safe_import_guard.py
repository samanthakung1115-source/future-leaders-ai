
from __future__ import annotations

import importlib
import streamlit as st


def safe_import(module_name: str, attr_name: str | None = None):
    """Safely import a module or attribute.

    Returns:
        (object_or_none, error_message_or_empty)
    """
    try:
        module = importlib.import_module(module_name)
        if attr_name:
            return getattr(module, attr_name), ""
        return module, ""
    except Exception as exc:
        return None, str(exc)


def render_missing_patch_warning(patch_name: str, error: str):
    st.warning(f"{patch_name} 尚未正確安裝或 import 失敗：{error}")


def load_patch_modules() -> dict:
    """Load common v1.1 patch modules safely."""
    specs = {
        "live_price": ("live_price", "enrich_with_live_price"),
        "sts_sync": ("sts_sync", "STSLiveSyncPatch"),
        "radar_live": ("radar_live", "enrich_radar_with_live_price"),
        "auto_refresh": ("auto_refresh", "render_auto_refresh_controls"),
        "samantha_brief": ("samantha_brief", "render_samantha_brief"),
        "sts_mapper": ("sts_mapper", "normalize_sts_columns"),
        "unified_pipeline": ("unified_pipeline", "build_unified_sts_live_pipeline"),
        "price_cache": ("price_cache", "enrich_with_cached_live_price"),
    }

    loaded = {}
    for key, (module_name, attr_name) in specs.items():
        obj, err = safe_import(module_name, attr_name)
        loaded[key] = {
            "ok": obj is not None,
            "object": obj,
            "error": err,
            "module": module_name,
            "attribute": attr_name,
        }
    return loaded
