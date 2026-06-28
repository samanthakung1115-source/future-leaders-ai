from pathlib import Path
from knowledge_engine import KnowledgeEngine

def test_build_and_query(tmp_path: Path):
    (tmp_path / "knowledge").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "knowledge" / "ai_infra.md").write_text("# AI 基建\nNVDA, MU, VRT are AI infrastructure candidates.", encoding="utf-8")
    (tmp_path / "docs" / "constitution.md").write_text("# AI Constitution\nDiscovery Intelligence must not replace Portfolio Intelligence.", encoding="utf-8")

    engine = KnowledgeEngine(tmp_path)
    index = engine.build()
    assert index.metadata["file_count"] == 2
    assert index.metadata["chunk_count"] >= 2

    results = engine.query("AI infrastructure MU")
    assert results
    assert results[0].chunk.category in {"knowledge", "docs"}
