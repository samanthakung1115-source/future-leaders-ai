
class DiscoveryEngine:
    def rank(self, companies, target_dna):
        target = {d.lower() for d in target_dna}
        results = []
        for company in companies:
            matched = sorted(target & {d.lower() for d in company.dna})
            score = int((len(matched) / max(len(target), 1)) * 100)
            results.append({
                "ticker": company.ticker,
                "company": company,
                "score": score,
                "reasons": [f"Matched DNA: {m}" for m in matched],
            })
        return sorted(results, key=lambda x: x["score"], reverse=True)
