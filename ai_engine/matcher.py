from students.models import Student


# -----------------------------------------
# IMPORTANT SKILL KEYWORDS LIST
# -----------------------------------------
SKILL_KEYWORDS = [
    "python", "java", "sql", "django", "react", "node",
    "ml", "machine learning", "aws", "docker",
    "html", "css", "javascript", "spring", "devops",
    "pandas", "numpy", "excel", "power bi"
]


# -----------------------------------------
# CGPA NORMALIZATION (0–20)
# -----------------------------------------
def cgpa_score(cgpa):
    if cgpa >= 9:
        return 20
    elif cgpa >= 8:
        return 16
    elif cgpa >= 7:
        return 12
    elif cgpa >= 6:
        return 8
    return 0


# -----------------------------------------
# READINESS WEIGHT (0–20)
# -----------------------------------------
def readiness_score(readiness):
    if readiness == "Ready":
        return 20
    elif readiness == "Improving":
        return 10
    return 0


# -----------------------------------------
# SKILL MATCH SCORE (0–40)
# -----------------------------------------
def skill_match_score(student_skills, job_skills):

    student_skills = student_skills.lower()
    job_skills = job_skills.lower().split(",")

    matches = 0

    for skill in job_skills:
        skill = skill.strip()
        if skill and skill in student_skills:
            matches += 1

    return min(matches * 10, 40)


# -----------------------------------------
# FINAL MATCH SCORE
# -----------------------------------------
def calculate_match_score(student, job):

    score = 0

    # Branch Match (Strict filter weight)
    if job.branch.lower() in student.qualification.lower():
        score += 20
    else:
        return 0   # ❗ STRICT FILTER (Very Important)

    # CGPA Score
    score += cgpa_score(student.cgpa)

    # Skill Score
    score += skill_match_score(student.skills, job.required_skills)

    # Readiness Score
    score += readiness_score(student.readiness)

    return score


# -----------------------------------------
# MAIN MATCH FUNCTION
# -----------------------------------------
def match_students_for_job(job):

    students = Student.objects.filter(
        cgpa__gte=6,
        backlogs__lte=2
    )

    scored_students = []

    for student in students:

        score = calculate_match_score(student, job)

        # MINIMUM THRESHOLD FILTER
        if score >= 30:
            scored_students.append((student, score))

    # SORT BY SCORE
    scored_students.sort(key=lambda x: x[1], reverse=True)

    return [student for student, score in scored_students]