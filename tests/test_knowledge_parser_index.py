import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from knowledge_engine import KnowledgeLoader, KnowledgeParser, KnowledgeIndex


def test_parser_builds_company_object():
    loader = KnowledgeLoader(repo_root=PROJECT_ROOT)
    parser = KnowledgeParser()
    companies = parser.parse_companies(loader.load_company_sources())

    nvda = next(company for company in companies if company.ticker == "NVDA")

    assert nvda.name == "NVIDIA"
    assert nvda.status == "Verified Winner"
    assert "AI Infrastructure" in nvda.dna
    assert nvda.has_dna("platform")
    assert "AI spending slowdown" in nvda.risks


def test_index_finds_by_dna_and_ticker():
    loader = KnowledgeLoader(repo_root=PROJECT_ROOT)
    parser = KnowledgeParser()
    companies = parser.parse_companies(loader.load_company_sources())
    index = KnowledgeIndex(companies)

    assert index.get_company("NVDA") is not None
    ai_infra = index.find_by_dna("AI Infrastructure")
    tickers = sorted(company.ticker for company in ai_infra)

    assert tickers == ["CRDO", "NVDA"]
    assert index.summary()["companies"] == 2


if __name__ == "__main__":
    test_parser_builds_company_object()
    test_index_finds_by_dna_and_ticker()
    print("Sprint 2 parser/index tests passed.")
