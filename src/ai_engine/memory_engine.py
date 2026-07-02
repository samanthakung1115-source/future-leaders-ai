
from __future__ import annotations

from pathlib import Path
from datetime import date, datetime
import json
import pandas as pd


class MemoryEngine:
    def __init__(self, path: str = "data/memory/leader_score_history.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save(self):
        self.path.write_text(json.dumps(self.db, ensure_ascii=False, indent=2), encoding="utf-8")

    def update_score(self, ticker: str, score: float, role: str = "", theme: str = ""):
        ticker = str(ticker).upper().strip()
        today = str(date.today())
        history = self.db.setdefault(ticker, [])

        # Replace same-day record instead of duplicating forever
        history = [x for x in history if x.get("date") != today]
        history.append({
            "date": today,
            "score": float(score),
            "role": role,
            "theme": theme,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        })
        self.db[ticker] = history
        self._save()

    def update_from_dataframe(self, df: pd.DataFrame):
        if df is None or df.empty:
            return 0
        count = 0
        for _, row in df.iterrows():
            ticker = row.get("ticker", "")
            score = row.get("leader_score", 0)
            role = row.get("role", "")
            theme = row.get("theme", "")
            if ticker:
                self.update_score(ticker, score, role, theme)
                count += 1
        return count

    def history(self, ticker: str) -> list[dict]:
        return self.db.get(str(ticker).upper().strip(), [])

    def score_change(self, ticker: str) -> float:
        h = self.history(ticker)
        if len(h) < 2:
            return 0.0
        return round(float(h[-1].get("score", 0)) - float(h[-2].get("score", 0)), 2)

    def latest_summary(self) -> pd.DataFrame:
        rows = []
        for ticker, hist in self.db.items():
            if not hist:
                continue
            latest = hist[-1]
            prev = hist[-2] if len(hist) >= 2 else None
            change = float(latest.get("score", 0)) - float(prev.get("score", latest.get("score", 0))) if prev else 0
            rows.append({
                "ticker": ticker,
                "latest_score": latest.get("score", 0),
                "score_change": round(change, 2),
                "role": latest.get("role", ""),
                "theme": latest.get("theme", ""),
                "days_in_memory": len(hist),
                "latest_date": latest.get("date", ""),
            })
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows).sort_values("score_change", ascending=False)
