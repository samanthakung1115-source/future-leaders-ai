"""Future Leaders AI v11 core package.

This package is intentionally small and repository-friendly: it reads the
existing docs/, knowledge/, tests/, companies/, playbooks/, prompts/ and specs/
folders instead of creating a parallel knowledge base.
"""

from .knowledge_engine import KnowledgeEngine, KnowledgeObject
from .discovery_engine import DiscoveryEngine, DiscoveryReport
from .ai_consensus import AIConsensus, ConsensusResult

__all__ = [
    "KnowledgeEngine",
    "KnowledgeObject",
    "DiscoveryEngine",
    "DiscoveryReport",
    "AIConsensus",
    "ConsensusResult",
]
