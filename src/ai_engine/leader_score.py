from dataclasses import dataclass

DEFAULT_WEIGHTS={"trend":20,"momentum":15,"fundamental":20,"narrative":15,"valuation":10,"flow":10,"decision":10}

@dataclass
class LeaderScore:
    score: float
    breakdown: dict

def calculate(metrics, weights=DEFAULT_WEIGHTS):
    total=0
    breakdown={}
    for k,w in weights.items():
        part=float(metrics.get(k,0))*w/100
        breakdown[k]=part
        total+=part
    return LeaderScore(round(total,2), breakdown)
