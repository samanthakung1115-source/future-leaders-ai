
from .scoring import score_company

class DiscoveryEngine:
    def rank(self, companies, target_dna):
        results=[]
        for c in companies:
            r=score_company(c,target_dna)
            results.append({"company":c,"score":r["score"],"reasons":r["reasons"]})
        return sorted(results,key=lambda x:x["score"],reverse=True)
