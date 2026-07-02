from pathlib import Path
import json
from datetime import date

class MemoryEngine:
    def __init__(self,path="data/leader_history.json"):
        self.path=Path(path)
        self.path.parent.mkdir(parents=True,exist_ok=True)
        if self.path.exists():
            self.db=json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self.db={}
    def update(self,ticker,score):
        today=str(date.today())
        self.db.setdefault(ticker,[]).append({"date":today,"score":score})
        self.path.write_text(json.dumps(self.db,ensure_ascii=False,indent=2),encoding="utf-8")
    def trend(self,ticker):
        h=self.db.get(ticker,[])
        if len(h)<2:return 0
        return h[-1]["score"]-h[-2]["score"]
