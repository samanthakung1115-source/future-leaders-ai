
from collections import Counter

def score_company(company, target_dna):
    overlap=len(set(company.dna)&set(target_dna))
    score=overlap*20
    reasons=[f"Matched DNA: {d}" for d in set(company.dna)&set(target_dna)]
    return {"score":score,"reasons":reasons}
