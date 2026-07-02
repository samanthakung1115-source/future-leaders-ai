def classify(score):
    if score>=90:return "Future Leader"
    if score>=80:return "Emerging Leader"
    if score>=70:return "Momentum Leader"
    if score>=60:return "Watch List"
    if score>=40:return "High Risk"
    return "Avoid"
