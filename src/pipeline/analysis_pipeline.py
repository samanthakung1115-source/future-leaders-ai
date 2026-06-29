
from dataclasses import asdict

class AnalysisPipeline:
    """Connect Knowledge -> Discovery -> Research."""

    def __init__(self, parser, discovery_engine, research_generator):
        self.parser = parser
        self.discovery_engine = discovery_engine
        self.research_generator = research_generator

    def analyze(self, source, target_dna):
        company = self.parser.parse_company(source)
        ranked = self.discovery_engine.rank([company], target_dna)[0]
        card = self.research_generator.generate(
            ticker=company.ticker,
            score=ranked["score"],
            reasons=ranked["reasons"],
            similar=[],
            risks=company.risks,
        )
        return {
            "company": company.to_dict(),
            "ranking": ranked,
            "research_card": asdict(card),
        }
