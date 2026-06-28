from pathlib import Path

from future_leaders_ai import DiscoveryEngine, KnowledgeEngine


def test_knowledge_engine_reads_existing_repo_dirs(tmp_path: Path):
    (tmp_path / "knowledge").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "knowledge" / "NVDA.md").write_text("# NVDA\nAI GPU data center growth moat", encoding="utf-8")
    (tmp_path / "docs" / "architecture.md").write_text("# AI Architecture\nDiscovery Intelligence", encoding="utf-8")

    engine = KnowledgeEngine(tmp_path)
    objects = engine.build_index()

    assert len(objects) == 2
    assert any(obj.source_dir == "knowledge" for obj in objects)
    assert engine.search("NVDA AI")


def test_discovery_engine_outputs_sts_compatible_payload(tmp_path: Path):
    (tmp_path / "companies").mkdir()
    (tmp_path / "companies" / "MU.md").write_text(
        "# MU\nHBM DRAM AI demand growth profit risk cyclical", encoding="utf-8"
    )

    knowledge = KnowledgeEngine(tmp_path)
    discovery = DiscoveryEngine(knowledge)
    report = discovery.analyze_company("MU")

    payload = report.sts_compatible_payload
    assert payload["schema"] == "samantha.discovery_signal.v11"
    assert payload["producer"] == "future-leaders-ai"
    assert payload["consumer"] == "stock-terminal-pro"
    assert payload["company"] == "MU"
    assert "consensus_score" in payload
