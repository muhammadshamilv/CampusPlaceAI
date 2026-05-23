# ==========================================
# Enhanced Resume Scoring (Better Distribution)
# ==========================================

def predict_resume_score(text, student=None):
    """
    Improved scoring logic to allow high-quality resumes
    to reach 90+ scores.
    """

    score = 0

    if not text:
        return 0

    text = text.lower()

    # -------------------------
    # 1. Length Score (25)
    # -------------------------
    length = len(text)

    if length > 3500:
        score += 25
    elif length > 2500:
        score += 20
    elif length > 1500:
        score += 15
    else:
        score += 8

    # -------------------------
    # 2. Technical Skills (35)
    # -------------------------
    skill_keywords = [
        "python", "java", "c++", "django", "flask",
        "machine learning", "deep learning", "data analysis",
        "sql", "html", "css", "javascript",
        "react", "node", "git", "api", "tensorflow", "pandas", "numpy"
    ]

    skill_count = sum(1 for skill in skill_keywords if skill in text)

    # Each skill = 2.5 points
    score += min(skill_count * 2.5, 35)

    # -------------------------
    # 3. Projects Section (15)
    # -------------------------
    if "project" in text or "projects" in text:
        score += 15

    # -------------------------
    # 4. Experience / Internship (10)
    # -------------------------
    if "intern" in text or "experience" in text:
        score += 10

    # -------------------------
    # 5. Academic (15)
    # -------------------------
    if student:
        score += min(student.cgpa * 1.5, 15)
        score -= student.backlogs * 1.5

    # -------------------------
    # 6. Bonus Quality Indicators (Optional)
    # -------------------------
    bonus_keywords = [
        "certification", "achievements", "leadership",
        "hackathon", "publication", "award"
    ]

    if any(word in text for word in bonus_keywords):
        score += 5

    # Final clamp
    score = max(0, min(int(score), 100))

    return score


def predict_readiness(score):
    if score >= 80:
        return "Ready"
    elif score >= 50:
        return "Improving"
    else:
        return "Not Ready"
