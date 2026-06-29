
from dataclasses import dataclass, field

@dataclass
class TradeLesson:
    ticker:str
    pattern:str
    lesson:str
    outcome:str

@dataclass
class DecisionMemory:
    lessons:list[TradeLesson]=field(default_factory=list)

    def add(self,ticker,pattern,lesson,outcome):
        self.lessons.append(TradeLesson(ticker,pattern,lesson,outcome))

    def find(self,ticker):
        return [l for l in self.lessons if l.ticker.upper()==ticker.upper()]

    def summarize(self):
        return {
            "count":len(self.lessons),
            "tickers":sorted({l.ticker for l in self.lessons})
        }
