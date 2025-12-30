BANNED_KEYWORDS = ["bomb", "terrorist", "kill"]

def safety_check(question: str) -> bool:
    for word in BANNED_KEYWORDS:
        if word in question.lower():
            return False
    return True
