
from __future__ import annotations

import pandas as pd
import streamlit as st


def _safe_imports():
    """Import optional patch modules only when available."""
    imports = {}

    try:
        from sts_sync import STSLiveSyncPatch
        imports["STSLiveSyncPatch"] = STSLiveSyncPatch
    except Exception:
        imports["STSLiveSyncPatch"] = None

    try:
        from sts_mapper import normalize_sts_columns, detect_sts_columns
        imports["normalize_sts_columns"] = normalize_sts_columns
        imports["detect_sts_columns"] = detect_sts_columns
    except Exception:
        imports["normalize_sts_columns"] = None
        imports["detect_sts_columns"] = None

    try:
        from live_price import enrich_with_live_price
        imports["enrich_with_live_price"] = enrich_with_live_price
    except Exception:
        imports["enrich_with_live_price"] = None

    try:
        from samantha_brief import build_samantha_brief
        imports["build_samantha_brief"] = build_samantha_brief
    except Exception:
        imports["build_samantha_brief"] = None

    return imports


def build_unified_sts_live_pipeline(
    fallback_df: pd.DataFrame | None = None,
    enable_live_price: bool = True,
    ticker_col: str = "ticker",
) -> tuple[pd.DataFrame, dict]:
    """Build unified data from STS Google Sheet + Column Mapper + Live Price.

    Pipeline:
    1. Read STS from Google Sheet if Patch 02 exists.
    2. Normalize STS columns if Patch 06 exists.
    3. Enrich live price if Patch 01 exists.
    4. Return df + status.

    This patch does not replace your app.py. It creates one function you can call
    inside Portfolio Center, Radar, or Dashboard.
    """
    modules = _safe_imports()
    status = {
        "sync_ok": False,
        "mapper_ok": False,
        "live_price_ok": False,
        "rows": 0,
        "columns": [],
        "messages": [],
    }

    df = fallback_df.copy() if fallback_df is not None else pd.DataFrame()

    # 1. STS Sync
    if modules["STSLiveSyncPatch"] is not None:
        try:
            df, sync_status = modules["STSLiveSyncPatch"]().read()
            status["sync_ok"] = bool(sync_status.ok)
            status["messages"].append(sync_status.message)
        except Exception as exc:
            status["messages"].append(f"STS sync unavailable: {exc}")
    else:
        status["messages"].append("STS Sync Patch not installed; using fallback_df.")

    # 2. Column Mapper
    if modules["normalize_sts_columns"] is not None and df is not None and not df.empty:
        try:
            df = modules["normalize_sts_columns"](df)
            status["mapper_ok"] = True
            status["messages"].append("STS columns normalized.")
        except Exception as exc:
            status["messages"].append(f"Column mapper failed: {exc}")
    else:
        status["messages"].append("STS Column Mapper Patch not installed or no data.")

    # 3. Live Price
    if enable_live_price and modules["enrich_with_live_price"] is not None and df is not None and not df.empty:
        try:
            if ticker_col not in df.columns and "ticker" in df.columns:
                ticker_col = "ticker"
            df = modules["enrich_with_live_price"](df, ticker_col=ticker_col)
            status["live_price_ok"] = True
            status["messages"].append("Live price enriched.")
        except Exception as exc:
            status["messages"].append(f"Live price failed: {exc}")
    else:
        status["messages"].append("Live Price Patch not installed, disabled, or no data.")

    if df is not None:
        status["rows"] = len(df)
        status["columns"] = list(df.columns)

    return df, status


def render_unified_pipeline_status(status: dict):
    """Render a compact status box for the unified pipeline."""
    with st.container(border=True):
        st.markdown("### 🔗 STS + Live Price Pipeline")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Rows", status.get("rows", 0))
        with c2:
            st.metric("Sync", "OK" if status.get("sync_ok") else "Check")
        with c3:
            st.metric("Mapper", "OK" if status.get("mapper_ok") else "Check")
        with c4:
            st.metric("Live Price", "OK" if status.get("live_price_ok") else "Check")

        for msg in status.get("messages", []):
            st.caption(msg)
