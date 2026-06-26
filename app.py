import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st
import yfinance as yf

APP_TITLE = "Future Leaders AI Terminal v10.0｜AI Memory Engine"
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

PORTFOLIO_FILE = DATA_DIR / "portfolio.json"
LEADERBOARD_FILE = DATA_DIR / "leaderboard_history.json"
AI_JOURNAL_FILE = DATA_DIR / "ai_investment_journal.json"
SNAPSHOT_FILE = DATA_DIR / "daily_scanner_snapshot.json"

CORE_COLUMNS = ["Ticker", "Name", "Shares", "Cost", "Status", "Advice", "Reason", "Risk"]

SCANNER_UNIVERSE = {
    "AI Infrastructure": ["NVDA", "CRDO", "VRT", "ANET", "DELL", "HPE", "CIEN", "NTAP", "PSTG", "SMCI", "AVGO", "ARM", "QCOM"],
    "Memory / Storage": ["MU", "WDC", "STX", "SNDK", "MRVL"],
    "AI Power": ["ETN", "PWR", "HUBB", "GEV", "VST", "CEG", "NXT", "FLNC", "OKLO", "SMR", "MYRG"],
    "Semicap": ["LRCX", "AMAT", "KLAC", "ONTO", "ENTG", "ACLS", "AEHR", "TER", "ASML"],
    "AI Cloud / Compute": ["NBIS", "APLD", "IREN", "CRWV", "CLS", "BE"],
    "Space & Defense": ["RKLB", "ASTS", "LUNR", "KTOS", "AVAV", "RTX", "NOC", "LHX", "HWM", "TXT", "GD"],
    "Cybersecurity / Cloud": ["DDOG", "NET", "PANW", "ZS", "FTNT", "OKTA", "S", "CRWD", "SNOW", "MDB", "FROG"],
    "Physical AI / Robotics": ["SYM", "CGNX", "ISRG", "ROK", "ZBRA", "TER"],
    "Re-Rating Industrials": ["CAT", "GLW", "DELL", "URI", "PH", "DE", "CMI", "EMR"],
    "Watchlist High Risk": ["ON", "SHOP", "SE", "SERV", "F", "T", "VZ", "KO", "PEP", "WBA"],
}

SECTOR_TAM = {
    "AI Infrastructure": 5,
    "Memory / Storage": 4,
    "AI Power": 5,
    "Semicap": 4,
    "AI Cloud / Compute": 5,
    "Space & Defense": 5,
    "Cybersecurity / Cloud": 4,
    "Physical AI / Robotics": 4,
    "Re-Rating Industrials": 4,
    "Watchlist High Risk": 1,
    "Manual Lookup": 2,
    "Portfolio": 2,
}

WINNER_DNA = {
    "CRDO": {
        "label": "AI Networking / Data Center 高成長",
        "features": ["AI Infrastructure", "Data Center Networking", "高成長", "接近新高", "資金持續流入"],
        "sector_keywords": ["AI Infrastructure", "Memory / Storage"],
    },
    "RKLB": {
        "label": "Space Infrastructure / 國防與新產業",
        "features": ["Space & Defense", "新產業", "國防訂單", "跌不下去", "連續霸榜"],
        "sector_keywords": ["Space & Defense"],
    },
    "DDOG": {
        "label": "Cloud / AI Observability 高成長軟體",
        "features": ["Cybersecurity / Cloud", "Cloud", "資料平台", "高毛利", "長期需求"],
        "sector_keywords": ["Cybersecurity / Cloud"],
    },
    "NET": {
        "label": "Edge AI / Security 網路平台",
        "features": ["Cybersecurity / Cloud", "Edge AI", "Security", "平台型公司", "成長股"],
        "sector_keywords": ["Cybersecurity / Cloud", "AI Infrastructure"],
    },
    "VRT": {
        "label": "AI Power / Data Center 電力重新評價",
        "features": ["AI Power", "Data Center Power", "Re-Rating", "工業重新評價", "AI 用電需求"],
        "sector_keywords": ["AI Power", "Re-Rating Industrials"],
    },
}

st.set_page_config(page_title=APP_TITLE, layout="wide")


def clean_ticker(x):
    if pd.isna(x):
        return ""
    return str(x).strip().upper().replace("NASDAQ:", "").replace("NYSE:", "")


def flatten_universe():
    rows = []
    seen = set()
    for sector, tickers in SCANNER_UNIVERSE.items():
        for t in tickers:
            if t not in seen:
                rows.append({"Ticker": t, "Sector": sector})
                seen.add(t)
    return pd.DataFrame(rows)


def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default
    return default


def save_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def load_portfolio():
    if PORTFOLIO_FILE.exists():
        return pd.DataFrame(load_json(PORTFOLIO_FILE, []))
    return pd.DataFrame(columns=CORE_COLUMNS)


def save_portfolio(df):
    df = df.fillna("")
    save_json(PORTFOLIO_FILE, json.loads(df.to_json(orient="records", force_ascii=False)))


def find_col(df, candidates):
    cols = {str(c).strip().lower(): c for c in df.columns}
    for c in candidates:
        if c.lower() in cols:
            return cols[c.lower()]
    for c in df.columns:
        name = str(c).lower()
        if any(k.lower() in name for k in candidates):
            return c
    return None


def read_sts_excel(uploaded, hide_sold=True):
    xls = pd.ExcelFile(uploaded)
    preferred = ["Holdings", "Portfolio", "Analysis_Pro", "Trade_Update", "Signals"]
    sheet = next((s for s in preferred if s in xls.sheet_names), xls.sheet_names[0])
    raw = pd.read_excel(uploaded, sheet_name=sheet).dropna(how="all")

    ticker_col = find_col(raw, ["股票", "Ticker", "代碼", "Symbol"])
    shares_col = find_col(raw, ["持股", "Shares", "股數"])
    cost_col = find_col(raw, ["成本", "Cost", "成本(美金)", "Avg Cost"])
    name_col = find_col(raw, ["名稱", "Name", "公司"])
    status_col = find_col(raw, ["目前等級", "訊號分類", "Status", "分級"])
    advice_col = find_col(raw, ["建議動作", "建議", "Advice"])

    if ticker_col is None:
        return pd.DataFrame(columns=CORE_COLUMNS), sheet

    df = pd.DataFrame()
    df["Ticker"] = raw[ticker_col].apply(clean_ticker)
    df = df[df["Ticker"] != ""]
    df = df[~df["Ticker"].str.contains("股票|TICKER|代碼", na=False)]
    df["Name"] = raw[name_col] if name_col else ""
    df["Shares"] = raw[shares_col] if shares_col else ""
    df["Cost"] = raw[cost_col] if cost_col else ""
    df["Status"] = raw[status_col] if status_col else ""
    df["Advice"] = raw[advice_col] if advice_col else ""
    df["Reason"] = ""
    df["Risk"] = ""
    df = df[CORE_COLUMNS].drop_duplicates("Ticker")
    df["Shares"] = pd.to_numeric(df["Shares"], errors="coerce").fillna(0)
    if hide_sold:
        df = df[df["Shares"] > 0]
    return df, sheet


@st.cache_data(ttl=300)
def get_price(ticker):
    try:
        tk = yf.Ticker(ticker)
        hist = tk.history(period="1y", prepost=True, interval="1d")
        intraday = tk.history(period="5d", interval="5m", prepost=True)
        if hist.empty:
            return None

        regular_close = float(hist["Close"].iloc[-1])
        prev_close = float(hist["Close"].iloc[-2]) if len(hist) > 2 else regular_close
        latest = regular_close
        source = "⚪ 最近收盤"
        latest_pct = ""

        if not intraday.empty and not intraday["Close"].dropna().empty:
            latest = float(intraday["Close"].dropna().iloc[-1])
            source = "🟢 最新價 / 盤前盤中可用"
            if prev_close:
                latest_pct = round((latest / prev_close - 1) * 100, 2)

        close = hist["Close"]
        high = hist["High"]
        low = hist["Low"]
        volume = hist["Volume"]

        ma20 = float(close.tail(20).mean())
        ma50 = float(close.tail(50).mean())
        ma200 = float(close.tail(200).mean())
        high5 = float(high.tail(5).max())
        high10 = float(high.tail(10).max())
        high52 = float(high.max())
        avg_vol20 = float(volume.tail(20).mean()) if not volume.tail(20).empty else 0

        change_1d = float((close.iloc[-1] / close.iloc[-2] - 1) * 100) if len(close) > 2 else 0
        change_2d = float((close.iloc[-1] / close.iloc[-3] - 1) * 100) if len(close) > 3 else 0
        change_5d = float((close.iloc[-1] / close.iloc[-6] - 1) * 100) if len(close) > 6 else 0
        change_20d = float((close.iloc[-1] / close.iloc[-21] - 1) * 100) if len(close) > 21 else 0
        change_60d = float((close.iloc[-1] / close.iloc[-61] - 1) * 100) if len(close) > 61 else 0

        return {
            "price": latest,
            "regular_close": regular_close,
            "prev_close": prev_close,
            "price_source": source,
            "latest_pct": latest_pct,
            "ma20": ma20,
            "ma50": ma50,
            "ma200": ma200,
            "high5": high5,
            "high10": high10,
            "high52": high52,
            "avg_vol20": avg_vol20,
            "change_1d": change_1d,
            "change_2d": change_2d,
            "change_5d": change_5d,
            "change_20d": change_20d,
            "change_60d": change_60d,
        }
    except Exception:
        return None


def event_note(ticker):
    ticker = ticker.upper()
    notes = {
        "NVDA": ("🟡 Event Pullback", "發債或大型資本支出消息可能引發短線獲利了結；長期 AI 主線未必改變。"),
        "CRWV": ("🟠 Event Chase Risk", "指數納入或一次性事件容易造成單日追價，事件消化後可能回落。"),
        "ON": ("🔴 Fundamental / Event Risk", "事件風險與資金撤退疑慮較高，先不要接落刀。"),
        "NBIS": ("⚪ 無重大事件", "主要觀察高檔受阻與資金是否重新接力。"),
        "WDC": ("⚪ 無重大事件", "主要觀察突破後是否能重新站回壓力區。"),
    }
    return notes.get(ticker, ("⚪ 無重大事件", "目前沒有手動標註的重大事件；仍需搭配盤前新聞觀察。"))


def technical_warning(ticker, q):
    if not q:
        return "⚪ 資料不足", "暫時無法判斷短線時機。"

    ticker = ticker.upper()
    price = q["price"]
    h5 = q["high5"]
    h10 = q["high10"]
    pct = q.get("latest_pct", "")

    if ticker == "NBIS" and h5 >= 290 and price < 285:
        return "⚠️ 高檔受阻", "連續挑戰 290–295 區間失敗後回落，今晚不追高，等重新突破或回測支撐。"

    if ticker == "WDC" and q["change_5d"] < -5 and price < h10 * 0.94:
        return "⚠️ 假突破", "突破後沒有續攻，股價跌回壓力區下方，先觀察是否重新站回。"

    if ticker == "CRWV" and (abs(q["change_1d"]) > 8 or (isinstance(pct, (int, float)) and abs(pct) > 5)):
        return "🟠 事件追價風險", "短線大漲可能來自一次性事件或資金流，追高容易買在事件高點。"

    if q["change_1d"] <= -12 or q["change_2d"] <= -20 or price < q["ma200"] * 0.9:
        return "🔪 Falling Knife", "急跌或跌破長期趨勢，先等待止跌訊號。"

    if h5 > 0 and price < h5 * 0.94 and q["change_5d"] < -6:
        return "⚠️ 動能降溫", "近期高點後快速回落，短線資金可能在獲利了結。"

    if isinstance(pct, (int, float)) and pct <= -3:
        return "🟡 盤前轉弱", "盤前明顯轉弱，先等開盤後是否承接。"

    if price > q["ma20"] and price > q["ma50"]:
        return "🟢 可留意", "短線趨勢仍在均線之上，可觀察是否延續。"

    return "🟡 等確認", "短線還不夠強，等重新站回短期均線或突破壓力。"


def score_scanner(ticker, sector, q):
    ticker = ticker.upper()
    tam = SECTOR_TAM.get(sector, 2) * 20
    smart_money = 40
    acceleration = 40
    catalyst = 50

    if q:
        if q["price"] > q["ma20"] > q["ma50"]:
            smart_money += 25
        elif q["price"] > q["ma50"]:
            smart_money += 15
        if q["price"] >= q["high52"] * 0.90:
            smart_money += 15
        if q["change_20d"] > 10:
            acceleration += 20
        if q["change_60d"] > 20:
            acceleration += 20
        if q["change_5d"] < -12:
            acceleration -= 15
        if q["price"] < q["ma200"]:
            smart_money -= 25

    catalyst_bonus = {
        "CRDO": 25, "RKLB": 25, "NBIS": 25, "NET": 20, "DDOG": 20,
        "CIEN": 22, "MYRG": 22, "QCOM": 18, "VST": 20, "GEV": 20,
        "GLW": 18, "APLD": 18, "LUNR": 16, "KTOS": 16, "AVAV": 16,
        "LHX": 16, "ANET": 18, "VRT": 22,
    }
    catalyst += catalyst_bonus.get(ticker, 0)

    if ticker in {"F", "T", "VZ", "KO", "PEP", "WBA"}:
        tam = min(tam, 25)
        catalyst = min(catalyst, 25)

    score = 0.40 * tam + 0.25 * acceleration + 0.20 * smart_money + 0.15 * catalyst
    score = max(0, min(100, round(score, 1)))
    return score, tam, acceleration, smart_money, catalyst


def stars_from_score(score):
    if score >= 82:
        return "🚀🚀🚀🚀🚀", "🟢 Next Big Winner"
    if score >= 70:
        return "🚀🚀🚀🚀", "🟡 Re-Rating / 高潛力"
    if score >= 58:
        return "🚀🚀🚀", "🔵 Emerging"
    if score >= 45:
        return "🚀🚀", "🟡 觀察"
    return "🚀", "⚠️ 低潛力"


def tonight_action(status, timing, event_status):
    danger = ["Falling", "高檔受阻", "假突破", "事件追價", "動能降溫", "盤前轉弱"]
    if any(k in timing for k in danger) or "Risk" in event_status:
        return "🚫 今晚先不要追"
    if "可留意" in timing and ("Next Big" in status or "Re-Rating" in status or "高潛力" in status):
        return "🟢 今晚可留意"
    if "等確認" in timing:
        return "🟡 等確認"
    return "🟡 觀察"


def dna_similarity(ticker, sector, score, timing, days):
    ticker = ticker.upper()
    sims = {}
    for base, dna in WINNER_DNA.items():
        sim = 35
        if sector in dna["sector_keywords"]:
            sim += 28
        if score >= 82:
            sim += 18
        elif score >= 70:
            sim += 12
        elif score >= 58:
            sim += 6
        if "可留意" in timing:
            sim += 8
        if days >= 5:
            sim += 8
        if days >= 10:
            sim += 5
        if ticker == base:
            sim = 100
        sims[base] = min(100, sim)
    best = max(sims, key=sims.get)
    return best, sims[best], sims


def update_days_on_leaderboard(scanner_df):
    history = load_json(LEADERBOARD_FILE, {})
    today = datetime.now().strftime("%Y-%m-%d")
    top = scanner_df.head(25)["Ticker"].tolist()

    for t in top:
        h = history.get(t, {"days": 0, "last_seen": ""})
        if h.get("last_seen") != today:
            h["days"] = int(h.get("days", 0)) + 1
            h["last_seen"] = today
        history[t] = h

    save_json(LEADERBOARD_FILE, history)
    return history


def update_ai_journal(scanner_df):
    journal = load_json(AI_JOURNAL_FILE, [])
    snapshot = load_json(SNAPSHOT_FILE, {})
    today = datetime.now().strftime("%Y-%m-%d")

    prev_top = set(snapshot.get("top", []))
    current_top = scanner_df.head(25)["Ticker"].tolist()
    current_set = set(current_top)

    new_entrants = [t for t in current_top if t not in prev_top][:10]
    for t in new_entrants:
        row = scanner_df[scanner_df["Ticker"] == t].iloc[0].to_dict()
        journal.append({
            "date": today,
            "ticker": t,
            "event": "🆕 New Entrant",
            "summary": f"{t} 首次進入 Top25；相似 {row.get('DNA Match')} {row.get('DNA Similarity')}%。",
        })

    upgraded = scanner_df[scanner_df["Big Winner Type"].str.contains("Next Big", na=False)].head(10)
    for _, row in upgraded.iterrows():
        t = row["Ticker"]
        if t not in prev_top:
            continue
        journal.append({
            "date": today,
            "ticker": t,
            "event": "🏆 Next Big Winner",
            "summary": f"{t} 維持高排名；6-12M 潛力 {row.get('6-12M Upside')}；相似 {row.get('DNA Match')}。",
        })

    journal = journal[-300:]
    save_json(AI_JOURNAL_FILE, journal)
    save_json(SNAPSHOT_FILE, {"date": today, "top": current_top})
    return journal


def enrich_scanner():
    uni = flatten_universe()
    rows = []
    portfolio = load_portfolio()
    held = set(portfolio["Ticker"].astype(str).str.upper()) if not portfolio.empty and "Ticker" in portfolio.columns else set()

    for _, item in uni.iterrows():
        ticker = item["Ticker"]
        sector = item["Sector"]
        q = get_price(ticker)
        score, tam, accel, smart, catalyst = score_scanner(ticker, sector, q)
        stars, big_type = stars_from_score(score)
        timing, timing_reason = technical_warning(ticker, q)
        event, event_reason = event_note(ticker)
        action = tonight_action(big_type, timing, event)

        rows.append({
            "Ticker": ticker,
            "Sector": sector,
            "Held?": "⭐ 已持股" if ticker in held else "🆕 未持有",
            "最新價": round(q["price"], 2) if q else "",
            "最新%": q.get("latest_pct", "") if q else "",
            "Scanner Score": score,
            "6-12M Upside": stars,
            "Big Winner Type": big_type,
            "Tonight Action": action,
            "Timing Warning": timing,
            "Timing Reason": timing_reason,
            "Event Status": event,
            "Event Reason": event_reason,
            "TAM": tam,
            "Acceleration": accel,
            "Smart Money": smart,
            "Catalyst": catalyst,
        })

    df = pd.DataFrame(rows).sort_values("Scanner Score", ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", range(1, len(df) + 1))
    history = update_days_on_leaderboard(df)
    df["Days on Leaderboard"] = df["Ticker"].map(lambda t: history.get(t, {}).get("days", 0))
    dna_matches = df.apply(lambda r: dna_similarity(r["Ticker"], r["Sector"], r["Scanner Score"], r["Timing Warning"], r["Days on Leaderboard"]), axis=1)
    df["DNA Match"] = [x[0] for x in dna_matches]
    df["DNA Similarity"] = [x[1] for x in dna_matches]
    update_ai_journal(df)
    return df


def enrich_portfolio(df):
    rows = []
    for _, r in df.iterrows():
        ticker = clean_ticker(r.get("Ticker", ""))
        if not ticker:
            continue
        q = get_price(ticker)
        sector = "Portfolio"
        score, tam, accel, smart, catalyst = score_scanner(ticker, sector, q)
        stars, big_type = stars_from_score(score)
        timing, timing_reason = technical_warning(ticker, q)
        event, event_reason = event_note(ticker)
        action = tonight_action(big_type, timing, event)
        best, sim, _ = dna_similarity(ticker, sector, score, timing, 0)

        price = q["price"] if q else None
        shares = pd.to_numeric(r.get("Shares", ""), errors="coerce")
        cost = pd.to_numeric(r.get("Cost", ""), errors="coerce")
        pnl = ""
        if pd.notna(shares) and pd.notna(cost) and cost > 0 and price:
            pnl = round((price - cost) / cost * 100, 2)

        rows.append({
            "Ticker": ticker,
            "Name": r.get("Name", ""),
            "Shares": r.get("Shares", ""),
            "Cost": r.get("Cost", ""),
            "最新價": round(price, 2) if price else "",
            "最新%": q.get("latest_pct", "") if q else "",
            "PnL%": pnl,
            "Scanner Score": score,
            "6-12M Upside": stars,
            "Big Winner Type": big_type,
            "Tonight Action": action,
            "Timing Warning": timing,
            "Timing Reason": timing_reason,
            "Event Status": event,
            "Event Reason": event_reason,
            "DNA Match": best,
            "DNA Similarity": sim,
        })
    return pd.DataFrame(rows)


def sticky_table(df, extra=False):
    base_cols = ["Rank", "Ticker", "Held?", "Sector", "最新價", "最新%", "Tonight Action", "6-12M Upside", "Big Winner Type", "Timing Warning", "DNA Match", "DNA Similarity", "Days on Leaderboard"]
    cols = [c for c in (df.columns if extra else base_cols) if c in df.columns]
    sub = df[cols].copy()
    html = sub.to_html(index=False, escape=False)
    st.markdown("""
    <style>
    .sticky-table-wrap { width:100%; overflow-x:auto; border:1px solid #e5e7eb; border-radius:12px; background:white; }
    .sticky-table-wrap table { border-collapse:collapse; width:max-content; min-width:100%; font-size:14px; }
    .sticky-table-wrap th, .sticky-table-wrap td { padding:8px 12px; border-bottom:1px solid #e5e7eb; white-space:nowrap; color:#111827; background:white; }
    .sticky-table-wrap th { background:#f3f4f6; font-weight:700; }
    .sticky-table-wrap th:nth-child(2), .sticky-table-wrap td:nth-child(2) {
        position:sticky; left:0; z-index:3; background:#fff7ed; font-weight:800; color:#111827; box-shadow:2px 0 4px rgba(0,0,0,0.08);
    }
    .sticky-table-wrap th:nth-child(2) { z-index:4; background:#fed7aa; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="sticky-table-wrap">{html}</div>', unsafe_allow_html=True)


def advisor_card(row):
    st.markdown(f"## {row['Ticker']}｜{row.get('Sector', row.get('Name', ''))}")
    st.markdown(f"### {row.get('Big Winner Type','')}　{row.get('Tonight Action','')}")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.info(f"📌 **今晚建議**\n\n{row.get('Tonight Action','')}")
        st.success(f"🚀 **6–12M 潛力**\n\n{row.get('6-12M Upside','')}｜{row.get('Big Winner Type','')}")
        st.warning(f"⚡ **短線時機**\n\n{row.get('Timing Warning','')}\n\n{row.get('Timing Reason','')}")
        st.warning(f"📰 **事件狀態**\n\n{row.get('Event Status','')}\n\n{row.get('Event Reason','')}")
        st.info(f"🧬 **Winner DNA**\n\n像 {row.get('DNA Match','')}：{row.get('DNA Similarity','')}%")
    with c2:
        st.metric("最新價", row.get("最新價", ""))
        st.metric("最新%", row.get("最新%", ""))
        st.metric("Scanner Score", row.get("Scanner Score", ""))
        if "Days on Leaderboard" in row:
            st.metric("霸榜天數", row.get("Days on Leaderboard", ""))
    st.divider()


def render_group(title, df, limit=20):
    st.subheader(title)
    if df.empty:
        st.write("目前沒有")
        return
    sub = df.head(limit)
    sticky_table(sub)
    for _, row in sub.iterrows():
        with st.expander(f"{row['Ticker']}｜{row.get('DNA Match','')} {row.get('DNA Similarity','')}%｜{row.get('Tonight Action','')}"):
            advisor_card(row)


st.title(APP_TITLE)

page = st.sidebar.radio(
    "功能",
    [
        "🏠 Dashboard",
        "📰 盤前指揮中心",
        "⭐ 我的持股",
        "🤖 股票分析器",
        "🌊 全市場海選",
        "🏆 Next Big Winners",
        "🆕 New Entrants",
        "🔥 Re-Rating",
        "🔵 Emerging",
        "🔪 Falling Knife",
        "🚫 Tonight Avoid",
        "🟢 Tonight Opportunities",
        "🏆 Days on Leaderboard",
        "🧠 AI Memory Engine",
        "🧬 Winner DNA",
        "🔮 Next DDOG Radar",
        "📖 AI 投資日誌",
        "🗺️ Black Horse Timeline",
        "📁 Portfolio Center",
        "⚙️ 進階模式",
    ],
)

portfolio = load_portfolio()
enriched = enrich_portfolio(portfolio) if not portfolio.empty else pd.DataFrame()

scanner_pages = {
    "🌊 全市場海選", "🏆 Next Big Winners", "🆕 New Entrants", "🔥 Re-Rating",
    "🔵 Emerging", "🔪 Falling Knife", "🚫 Tonight Avoid", "🟢 Tonight Opportunities",
    "🏆 Days on Leaderboard", "🏠 Dashboard", "📰 盤前指揮中心", "🧠 AI Memory Engine",
    "🧬 Winner DNA", "🔮 Next DDOG Radar", "📖 AI 投資日誌", "🗺️ Black Horse Timeline", "⚙️ 進階模式"
}
scanner = None
if page in scanner_pages:
    with st.spinner("正在執行 AI Memory + 全市場海選，第一次可能需要較久..."):
        scanner = enrich_scanner()

if page == "📁 Portfolio Center":
    st.header("📁 Portfolio Center｜匯入 STS Excel")
    hide_sold = st.checkbox("隱藏已賣清股票（股數 = 0）", value=True)
    uploaded = st.file_uploader("上傳 STS Excel", type=["xlsx"])
    if uploaded:
        df, sheet = read_sts_excel(uploaded, hide_sold=hide_sold)
        st.success(f"已讀取工作表：{sheet}，共匯入 {len(df)} 檔持股")
        st.dataframe(df, use_container_width=True, hide_index=True)
        if st.button("✅ 儲存為我的持股"):
            save_portfolio(df)
            st.success("已儲存 portfolio.json，請切到『我的持股』查看。")
            st.rerun()
    st.divider()
    st.subheader("目前已儲存持股")
    st.dataframe(portfolio, use_container_width=True, hide_index=True)

elif page == "🏠 Dashboard":
    st.header("🏠 今日 AI 摘要")
    if scanner is not None:
        top_future = scanner[scanner["DNA Similarity"] >= 75].head(8)
        opp = scanner[scanner["Tonight Action"].str.contains("可留意", na=False)]
        avoid = scanner[scanner["Tonight Action"].str.contains("不要追", na=False)]
        st.success("🔮 Potential Future Leaders：" + ("、".join(top_future["Ticker"].head(8).tolist()) or "無"))
        st.info("🟢 今晚可留意：" + ("、".join(opp["Ticker"].head(12).tolist()) or "無"))
        st.error("🚫 今晚先不要追：" + ("、".join(avoid["Ticker"].head(12).tolist()) or "無"))
        render_group("🔮 Next DDOG / CRDO / RKLB Radar", top_future, 8)

elif page == "📰 盤前指揮中心":
    st.header("📰 盤前指揮中心")
    render_group("🟢 今晚可留意", scanner[scanner["Tonight Action"].str.contains("可留意", na=False)], 15)
    render_group("🚫 今晚先不要追", scanner[scanner["Tonight Action"].str.contains("不要追", na=False)], 15)

elif page == "⭐ 我的持股":
    st.header("⭐ 我的持股｜Portfolio Commander")
    if enriched.empty:
        st.info("請先到 Portfolio Center 上傳 STS Excel。")
    else:
        sticky_table(enriched)
        for _, row in enriched.iterrows():
            with st.expander(f"{row['Ticker']}｜{row.get('Tonight Action','')}"):
                advisor_card(row)

elif page == "🤖 股票分析器":
    st.header("🤖 股票分析器")
    ticker = st.text_input("輸入股票代碼", "CIEN").upper().strip()
    if ticker:
        q = get_price(ticker)
        sector = "Manual Lookup"
        score, tam, accel, smart, catalyst = score_scanner(ticker, sector, q)
        stars, big_type = stars_from_score(score)
        timing, timing_reason = technical_warning(ticker, q)
        event, event_reason = event_note(ticker)
        action = tonight_action(big_type, timing, event)
        best, sim, _ = dna_similarity(ticker, sector, score, timing, 0)
        row = {
            "Ticker": ticker, "Sector": sector, "最新價": round(q["price"], 2) if q else "",
            "最新%": q.get("latest_pct", "") if q else "", "Scanner Score": score,
            "6-12M Upside": stars, "Big Winner Type": big_type, "Tonight Action": action,
            "Timing Warning": timing, "Timing Reason": timing_reason, "Event Status": event, "Event Reason": event_reason,
            "DNA Match": best, "DNA Similarity": sim,
        }
        advisor_card(row)

elif page == "🌊 全市場海選":
    st.header("🌊 全市場海選｜Market Scanner")
    render_group("🌊 全市場海選 Top 25", scanner, 25)

elif page == "🏆 Next Big Winners":
    st.header("🏆 Next Big Winners")
    render_group("🏆 Next Big Winners", scanner[scanner["Big Winner Type"].str.contains("Next Big", na=False)], 25)

elif page == "🆕 New Entrants":
    st.header("🆕 New Entrants｜未持有新黑馬")
    render_group("🆕 未持有高潛力候選", scanner[scanner["Held?"] == "🆕 未持有"].head(30), 30)

elif page == "🔥 Re-Rating":
    st.header("🔥 Re-Rating")
    render_group("🔥 Re-Rating", scanner[scanner["Big Winner Type"].str.contains("Re-Rating", na=False)], 25)

elif page == "🔵 Emerging":
    st.header("🔵 Emerging")
    render_group("🔵 Emerging", scanner[scanner["Big Winner Type"].str.contains("Emerging", na=False)], 25)

elif page == "🔪 Falling Knife":
    st.header("🔪 Falling Knife")
    render_group("🔪 Falling Knife", scanner[scanner["Timing Warning"].str.contains("Falling", na=False)], 25)

elif page == "🚫 Tonight Avoid":
    st.header("🚫 Tonight Avoid")
    render_group("🚫 今晚先不要追", scanner[scanner["Tonight Action"].str.contains("不要追", na=False)], 30)

elif page == "🟢 Tonight Opportunities":
    st.header("🟢 Tonight Opportunities")
    render_group("🟢 今晚可留意", scanner[scanner["Tonight Action"].str.contains("可留意", na=False)], 30)

elif page == "🏆 Days on Leaderboard":
    st.header("🏆 Days on Leaderboard")
    sub = scanner.sort_values(["Days on Leaderboard", "Scanner Score"], ascending=[False, False])
    render_group("🏆 連續霸榜 / 持續強勢", sub, 30)

elif page == "🧠 AI Memory Engine":
    st.header("🧠 AI Memory Engine")
    st.write("這裡記錄股票是否從 New Entrant → Emerging → Next Big Winner → 風險警示。")
    render_group("🧠 AI Memory Top Candidates", scanner[scanner["DNA Similarity"] >= 70], 30)

elif page == "🧬 Winner DNA":
    st.header("🧬 Winner DNA")
    for k, v in WINNER_DNA.items():
        st.subheader(f"{k} DNA｜{v['label']}")
        st.write("、".join(v["features"]))
    st.divider()
    render_group("🧬 最像歷史大贏家的股票", scanner.sort_values("DNA Similarity", ascending=False), 30)

elif page == "🔮 Next DDOG Radar":
    st.header("🔮 Next DDOG / CRDO / RKLB / NET Radar")
    sub = scanner[(scanner["Held?"] == "🆕 未持有") & (scanner["DNA Similarity"] >= 70)]
    render_group("🔮 Potential Future Leaders", sub.sort_values(["DNA Similarity", "Scanner Score"], ascending=False), 30)

elif page == "📖 AI 投資日誌":
    st.header("📖 AI 投資日誌")
    journal = load_json(AI_JOURNAL_FILE, [])
    if not journal:
        st.info("目前尚無日誌。重新整理幾次後會逐步累積。")
    else:
        dfj = pd.DataFrame(journal).sort_values("date", ascending=False)
        st.dataframe(dfj, use_container_width=True, hide_index=True)

elif page == "🗺️ Black Horse Timeline":
    st.header("🗺️ Black Horse Timeline")
    journal = load_json(AI_JOURNAL_FILE, [])
    if not journal:
        st.info("目前尚無 Timeline。")
    else:
        dfj = pd.DataFrame(journal)
        ticker = st.selectbox("選擇股票", sorted(dfj["ticker"].unique()))
        sub = dfj[dfj["ticker"] == ticker].sort_values("date")
        for _, r in sub.iterrows():
            st.markdown(f"### {r['date']}｜{r['event']}")
            st.write(r["summary"])

elif page == "⚙️ 進階模式":
    st.header("⚙️ 進階資料")
    if scanner is not None:
        st.subheader("Scanner")
        st.dataframe(scanner, use_container_width=True, hide_index=True)
    if not enriched.empty:
        st.subheader("Portfolio")
        st.dataframe(enriched, use_container_width=True, hide_index=True)

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
