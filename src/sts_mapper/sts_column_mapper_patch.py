
from __future__ import annotations

import pandas as pd


REQUIRED_STANDARD_COLUMNS = [
    "ticker",
    "shares",
    "cost",
    "market_value",
    "return_pct",
    "distance_from_high_pct",
    "ai_score",
    "tonight_action",
    "category",
]


COLUMN_ALIASES = {
    "ticker": [
        "Ticker", "ticker", "股票", "代碼", "Symbol", "symbol",
        "Ticker 股票行情", "股票代碼", "代號"
    ],
    "shares": [
        "shares", "股數", "持股數", "Quantity", "Qty", "庫存股數"
    ],
    "cost": [
        "cost", "成本", "成本價", "平均成本", "Avg Cost", "Cost Basis"
    ],
    "market_value": [
        "market_value", "市值", "現值", "Market Value", "Position Value"
    ],
    "return_pct": [
        "return_pct", "距成本%", "報酬率%", "損益%", "未實現%", "Return %", "PnL %"
    ],
    "distance_from_high_pct": [
        "distance_from_high_pct", "距前高%", "距前高", "Dist High %", "Distance From High %"
    ],
    "ai_score": [
        "ai_score", "AI Score", "AI分數", "AI 評分", "Score", "總分"
    ],
    "tonight_action": [
        "tonight_action", "Tonight Action", "Tonight Action 今晚行動",
        "今晚行動", "今日行動", "建議動作", "Action"
    ],
    "category": [
        "category", "Category", "類別", "分類", "Sector", "產業", "Theme", "主題"
    ],
}


def detect_sts_columns(df: pd.DataFrame) -> dict[str, str | None]:
    """Detect which original STS columns map to standard column names."""
    if df is None or df.empty:
        return {key: None for key in COLUMN_ALIASES}

    mapping = {}
    existing = list(df.columns)

    for standard, aliases in COLUMN_ALIASES.items():
        found = None
        for alias in aliases:
            if alias in existing:
                found = alias
                break
        mapping[standard] = found

    return mapping


def normalize_sts_columns(df: pd.DataFrame, keep_original: bool = True) -> pd.DataFrame:
    """Normalize STS Google Sheet / CSV columns into standard fields.

    This patch is intentionally forgiving:
    - It detects common Chinese / English STS column names.
    - It creates missing standard columns with blank values.
    - It preserves original columns by default.

    Standard columns:
    - ticker
    - shares
    - cost
    - market_value
    - return_pct
    - distance_from_high_pct
    - ai_score
    - tonight_action
    - category
    """
    if df is None:
        return pd.DataFrame()

    if df.empty:
        return df.copy()

    mapping = detect_sts_columns(df)
    out = df.copy() if keep_original else pd.DataFrame(index=df.index)

    for standard in REQUIRED_STANDARD_COLUMNS:
        source_col = mapping.get(standard)
        if source_col and source_col in df.columns:
            out[standard] = df[source_col]
        elif standard not in out.columns:
            out[standard] = ""

    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()

    # Numeric cleanup where possible
    for col in ["shares", "cost", "market_value", "return_pct", "distance_from_high_pct", "ai_score"]:
        out[col] = (
            out[col]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0)

    return out


def sts_column_health(df: pd.DataFrame) -> dict:
    """Return a simple health report for STS column mapping."""
    mapping = detect_sts_columns(df)
    missing = [k for k, v in mapping.items() if v is None]
    found = {k: v for k, v in mapping.items() if v is not None}

    return {
        "ok": "ticker" not in missing,
        "found": found,
        "missing": missing,
        "message": "STS column mapping OK." if "ticker" not in missing else "Ticker column not found. Please check STS column names.",
    }
