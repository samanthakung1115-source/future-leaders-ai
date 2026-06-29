
class DailyBriefBuilder:
    def build(self,candidates):
        return {
            "top_future_leaders":[c.ticker for c in candidates[:10]],
            "watchlist":[c.ticker for c in candidates if c.verdict=="Watch"],
            "summary":f"{len(candidates)} candidates evaluated."
        }
