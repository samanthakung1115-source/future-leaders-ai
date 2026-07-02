def rank(items):
    return sorted(items,key=lambda x:x.get("leader_score",0), reverse=True)
