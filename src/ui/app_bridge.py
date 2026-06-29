
from integration import IntegratedAnalysisEngine

class AppBridge:
    def __init__(self, repo_root="."):
        self.engine = IntegratedAnalysisEngine(repo_root=repo_root)

    def analyze(self, ticker:str):
        return self.engine.analyze_ticker(
            ticker=ticker,
            target_dna=["AI Infrastructure","Platform"],
            user_history={"lessons":["Avoid chasing parabolic moves.",
                                     "Do not sell quality winners too early."]}
        )
