
from __future__ import annotations

from pathlib import Path
import json
import pandas as pd

from ai_engine import calculate_leader_score, classify_role


class MarketScanner:
    REQUIRED = ["ticker"]

    def __init__(self, weights_path: str = "config/leader_score_weights.json"):
        self.weights = self._load_weights(weights_path)

    def _load_weights(self, path: str) -> dict:
        p = Path(path)
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
        return {
            "trend": 20,
            "momentum": 15,
            "fundamental": 20,
            "narrative": 15,
            "valuation": 10,
            "flow": 10,
            "decision": 10,
        }

    def scan_dataframe(self, df: pd.DataFrame, top_n: int = 100) -> pd.DataFrame:
        if df is None or df.empty:
            return pd.DataFrame()

        out = df.copy()
        if "ticker" not in out.columns:
            for c in ["Ticker", "symbol", "Symbol", "代碼", "股票"]:
                if c in out.columns:
                    out["ticker"] = out[c]
                    break

        if "ticker" not in out.columns:
            raise ValueError("MarketScanner requires a ticker column")

        scores = []
        roles = []
        black_horse = []

        for _, row in out.iterrows():
            metrics = {
                "trend": row.get("trend", 0),
                "momentum": row.get("momentum", 0),
                "fundamental": row.get("fundamental", 0),
                "narrative": row.get("narrative", 0),
                "valuation": row.get("valuation", 0),
                "flow": row.get("flow", 0),
                "decision": row.get("decision", 0),
            }
            result = calculate_leader_score(metrics, self.weights)
            score = result["leader_score"]
            scores.append(score)
            roles.append(classify_role(score))

            # Black horse: high score but not already obvious mega leader.
            black_horse.append(
                score >= 78
                and float(row.get("momentum", 0) or 0) >= 70
                and float(row.get("narrative", 0) or 0) >= 70
                and float(row.get("valuation", 0) or 0) >= 55
            )

        out["leader_score"] = scores
        out["role"] = roles
        out["black_horse"] = black_horse

        out = out.sort_values("leader_score", ascending=False)
        out["rank"] = range(1, len(out) + 1)

        return out.head(top_n)

    def scan_csv(self, path: str, top_n: int = 100) -> pd.DataFrame:
        df = pd.read_csv(path)
        return self.scan_dataframe(df, top_n=top_n)
