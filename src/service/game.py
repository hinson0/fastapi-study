def get_word() -> str:
    return "yangzhibing"


def calculate_score(guess: str, word: str) -> dict:
    """
    Calculate score based on the comparison between guess and actual word
    Returns a dictionary with comparison results
    """
    if len(guess) != len(word):
        return {
            "guess": guess,
            "correctPositions": 0,
            "wordLength": len(word),
            "isCorrect": False,
            "score": 0,
        }

    correct_positions = 0
    for i in range(len(word)):
        if guess[i].lower() == word[i].lower():
            correct_positions += 1

    is_correct = correct_positions == len(word)

    # Calculate score based on number of correct positions
    score = int((correct_positions / len(word)) * 100) if len(word) > 0 else 0

    return {
        "guess": guess,
        "correctPositions": correct_positions,
        "wordLength": len(word),
        "isCorrect": is_correct,
        "score": score,
    }
