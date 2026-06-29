
from knowledge_engine import KnowledgeLoader, KnowledgeParser
from discovery_engine import DiscoveryEngine
from research_engine import ResearchCardGenerator
from decision_coach import DecisionCoach
from winner_dna import WinnerDNAMatcher
from recommendation_engine import RecommendationEngine

DEFAULT_WINNER_DATABASE = {
    "NVDA": ["AI Infrastructure", "Platform", "Ecosystem"],
    "CRDO": ["AI Infrastructure", "Connectivity", "Networking"],
    "VRT": ["AI Infrastructure", "Power", "Cooling"],
    "RKLB": ["Space Infrastructure", "Execution", "Long-term Compound Growth"],
}

class IntegratedAnalysisEngine:
    def __init__(self, repo_root="."):
        self.repo_root = repo_root
        self.loader = KnowledgeLoader(repo_root=repo_root)
        self.parser = KnowledgeParser()
        self.discovery = DiscoveryEngine()
        self.research = ResearchCardGenerator()
        self.decision = DecisionCoach()
        self.matcher = WinnerDNAMatcher()
        self.recommendation = RecommendationEngine()

    def analyze_ticker(self, ticker: str, target_dna: list[str], user_history: dict | None = None):
        sources = self.loader.load_company_sources()
        companies = self.parser.parse_companies(sources)
        company = next((c for c in companies if c.ticker.upper() == ticker.upper()), None)
        if company is None:
            raise ValueError(f"Company knowledge file not found: {ticker}")

        ranking = self.discovery.rank([company], target_dna)[0]
        winner_matches = self.matcher.match(company.dna, DEFAULT_WINNER_DATABASE)
        similar = [m.winner for m in winner_matches[:3]]

        card = self.research.generate(
            ticker=company.ticker,
            score=ranking["score"],
            reasons=ranking["reasons"] + company.why_selected,
            similar=similar,
            risks=company.risks,
        ).to_dict()

        advice = self.decision.evaluate(card, user_history=user_history).to_dict()
        recommendation = self.recommendation.recommend(card, advice, winner_matches).to_dict()

        return {
            "company": company.to_dict(),
            "ranking": ranking,
            "winner_matches": [m.to_dict() for m in winner_matches],
            "research_card": card,
            "decision_advice": advice,
            "recommendation": recommendation,
        }
