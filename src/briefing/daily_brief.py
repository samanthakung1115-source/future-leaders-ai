
from dataclasses import dataclass

@dataclass
class SamanthaBrief:
    market:str
    leaders:list[str]
    portfolio:list[str]
    watchlist:list[str]
    recommendations:list[str]
    reminders:list[str]

class SamanthaDailyBrief:
    """Combine all Future Leaders AI modules into one daily briefing."""

    def build(
        self,
        market:str,
        leaders:list[str],
        portfolio:list[str],
        watchlist:list[str],
        recommendations:list[str],
        reminders:list[str],
    ) -> SamanthaBrief:
        return SamanthaBrief(
            market=market,
            leaders=leaders,
            portfolio=portfolio,
            watchlist=watchlist,
            recommendations=recommendations,
            reminders=reminders,
        )
