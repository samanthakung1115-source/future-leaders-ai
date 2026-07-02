
def classify_role(score: float) -> str:
    score = float(score or 0)
    if score >= 90:
        return "🚀 Future Leader"
    if score >= 82:
        return "⭐ Emerging Leader"
    if score >= 74:
        return "🔥 Momentum Leader"
    if score >= 65:
        return "👀 Watch List"
    if score >= 50:
        return "⚠️ High Risk / Verify"
    return "❌ Avoid"
