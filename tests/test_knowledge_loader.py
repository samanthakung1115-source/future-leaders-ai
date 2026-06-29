import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from knowledge_engine import KnowledgeLoader, KnowledgeSource


def test_loader_discovers_company_markdown():
    loader = KnowledgeLoader(repo_root=PROJECT_ROOT)
    files = loader.discover_markdown_files()

    assert any(path.name == "NVDA.md" for path in files)


def test_loader_returns_sources():
    loader = KnowledgeLoader(repo_root=PROJECT_ROOT)
    sources = loader.load_sources()

    assert sources
    assert all(isinstance(source, KnowledgeSource) for source in sources)
    assert any(source.category == "company" for source in sources)


def test_loader_company_sources_only():
    loader = KnowledgeLoader(repo_root=PROJECT_ROOT)
    companies = loader.load_company_sources()

    assert len(companies) == 1
    assert companies[0].stem == "NVDA"
    assert companies[0].category == "company"


if __name__ == "__main__":
    test_loader_discovers_company_markdown()
    test_loader_returns_sources()
    test_loader_company_sources_only()
    print("Sprint 1 Session 1 tests passed.")
