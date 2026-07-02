
from pathlib import Path
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ai_engine import MemoryEngine


def test_memory_engine_score_change():
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "memory.json"
        m = MemoryEngine(str(path))
        m.update_score("AAA", 80)
        m.db["AAA"].append({"date":"2099-01-02","score":85,"role":"","theme":""})
        m._save()
        assert m.score_change("AAA") == 5


if __name__ == "__main__":
    test_memory_engine_score_change()
    print("Future Leaders AI Sprint 3.4 AI Memory test passed.")
