
from dataclasses import dataclass

@dataclass
class DailyReport:
    market_summary:str
    top_future_leaders:list[str]
    watchlist:list[str]
    portfolio_alerts:list[str]
    samantha_comment:str

class DailyReportGenerator:
    """Generate a daily summary from Samantha AI components."""

    def generate(self,
                 market_summary:str,
                 leaders:list[str],
                 watchlist:list[str],
                 alerts:list[str]):
        comment = (
            "Focus on quality leaders. Avoid chasing extended moves. "
            "Review portfolio alerts before adding new positions."
        )
        return DailyReport(
            market_summary=market_summary,
            top_future_leaders=leaders,
            watchlist=watchlist,
            portfolio_alerts=alerts,
            samantha_comment=comment,
        )
