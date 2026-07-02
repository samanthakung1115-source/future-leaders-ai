
from __future__ import annotations

import pandas as pd
import streamlit as st


def _safe_import(module_name: str, attr_name: str):
    try:
        module = __import__(module_name, fromlist=[attr_name])
        return getattr(module, attr_name), ""
    except Exception as exc:
        return None, str(exc)


def _to_numeric(series):
    return pd.to_numeric(
        series.astype(str).str.replace("%", "", regex=False).str.replace(",", "", regex=False),
        errors="coerce",
    ).fillna(0)


def _metric(label, value, help_text=""):
    with st.container(border=True):
        st.metric(label, value)
        if help_text:
            st.caption(help_text)


def _filter_portfolio(df: pd.DataFrame, hide_zero_shares: bool = True) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    out = df.copy()
    if "shares" in out.columns and hide_zero_shares:
        out = out[_to_numeric(out["shares"]) > 0]
    return out


def _portfolio_summary(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {"positions": 0, "total_market_value": 0, "strong_winners": 0, "under_pressure": 0, "avg_return_pct": 0}

    out = df.copy()
    market_value = _to_numeric(out["market_value"]) if "market_value" in out.columns else pd.Series([0])
    returns = _to_numeric(out["return_pct"]) if "return_pct" in out.columns else pd.Series([0] * len(out))

    return {
        "positions": len(out),
        "total_market_value": round(float(market_value.sum()), 2),
        "strong_winners": int((returns >= 50).sum()),
        "under_pressure": int((returns <= -20).sum()),
        "avg_return_pct": round(float(returns.mean()), 2) if len(returns) else 0,
    }


def _select_columns(df: pd.DataFrame) -> list[str]:
    preferred = [
        "ticker", "shares", "cost", "market_value", "return_pct",
        "distance_from_high_pct", "ai_score", "category", "tonight_action",
        "Live Price 最新價", "Live % 今日%", "Dist High % 距前高%", "Live Action 即時行動",
    ]
    return [c for c in preferred if c in df.columns]


def render():
    st.title("📂 Portfolio Center")
    st.caption("v1.2 RC Integration 2.1")

    build_pipeline, err_pipeline = _safe_import("unified_pipeline", "build_unified_sts_live_pipeline")
    render_pipeline_status, err_status = _safe_import("unified_pipeline", "render_unified_pipeline_status")
    render_brief, err_brief = _safe_import("samantha_brief", "render_samantha_brief")

    st.subheader("🔄 STS Google Sheet 同步")

    if not build_pipeline:
        st.error(f"Unified Pipeline 尚未安裝：{err_pipeline}")
        st.info("請確認 Patch 02 / 06 / 07 / 09 已經上傳到 v11-beta。")
        return

    c0, c1, c2 = st.columns([1, 1, 2])
    with c0:
        enable_live_price = st.checkbox("Live Price", value=True)
    with c1:
        hide_zero = st.checkbox("隱藏 0 股", value=True)
    with c2:
        st.caption("資料來源：STS Google Sheet → Column Mapper → Live Price Cache")

    if st.button("🔄 同步 Portfolio"):
        with st.spinner("同步 STS 與即時價格中..."):
            df, status = build_pipeline(enable_live_price=enable_live_price)
            st.session_state["portfolio_center_df"] = df
            st.session_state["portfolio_center_status"] = status

    df = st.session_state.get("portfolio_center_df")
    status = st.session_state.get("portfolio_center_status")

    if status:
        if render_pipeline_status:
            render_pipeline_status(status)
        else:
            st.json(status)

    if df is None or df.empty:
        st.info("尚未同步資料。請按「同步 Portfolio」。")
        return

    df = _filter_portfolio(df, hide_zero_shares=hide_zero)
    summary = _portfolio_summary(df)

    st.divider()
    st.subheader("📊 Portfolio Summary")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        _metric("Positions", summary["positions"])
    with c2:
        _metric("Market Value", summary["total_market_value"])
    with c3:
        _metric("Avg Return %", summary["avg_return_pct"])
    with c4:
        _metric("Strong Winners", summary["strong_winners"], "return_pct >= 50")
    with c5:
        _metric("Under Pressure", summary["under_pressure"], "return_pct <= -20")

    st.divider()
    st.subheader("🧠 Samantha Portfolio Brief")

    if render_brief:
        render_brief(portfolio_df=df, radar_df=df)
    else:
        st.warning(f"Samantha Brief 尚未安裝：{err_brief}")

    st.divider()
    st.subheader("📋 Holdings Table")

    cols = _select_columns(df)
    st.dataframe(df[cols] if cols else df, use_container_width=True)

    if "return_pct" in df.columns:
        temp = df.copy()
        temp["_return_pct"] = _to_numeric(temp["return_pct"])

        st.divider()
        a, b = st.columns(2)

        with a:
            st.subheader("🚀 Strong Winners")
            winners = temp[temp["_return_pct"] >= 50]
            if winners.empty:
                st.caption("目前沒有 return_pct >= 50 的持股。")
            else:
                wcols = _select_columns(winners)
                st.dataframe(winners[wcols] if wcols else winners, use_container_width=True)

        with b:
            st.subheader("⚠️ Under Pressure")
            weak = temp[temp["_return_pct"] <= -20]
            if weak.empty:
                st.caption("目前沒有 return_pct <= -20 的持股。")
            else:
                wcols = _select_columns(weak)
                st.dataframe(weak[wcols] if wcols else weak, use_container_width=True)

    if "Live Action 即時行動" in df.columns:
        st.divider()
        st.subheader("👀 Live Action Watch")
        watch = df[df["Live Action 即時行動"].astype(str).str.contains("可觀察|不要追|等回落|止跌", na=False)]
        if watch.empty:
            st.caption("目前沒有特別 Live Action 提醒。")
        else:
            wcols = _select_columns(watch)
            st.dataframe(watch[wcols] if wcols else watch, use_container_width=True)
