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


def branch_match(student_qualification, job_branch):

    qualification = student_qualification.lower()

    branch_keywords = {
        "cse": ["computer science", "cse"],
        "it": ["information technology", "it"],
        "ece": ["electronics", "ece"],
        "me": ["mechanical", "me"],
        "ce": ["civil", "ce"]
    }

    job_branches = [
        b.strip().lower()
        for b in job_branch.split(",")
    ]

    for branch in job_branches:

        if branch in branch_keywords:

            for keyword in branch_keywords[branch]:

                if keyword in qualification:
                    return True

    return False


# -----------------------------------------
# FINAL MATCH SCORE
# -----------------------------------------
def calculate_match_score(student, job):

    score = 0

    # --------------------------------
    # Branch Match (Mandatory)
    # --------------------------------
    if branch_match(
        student.qualification,
        job.branch
    ):
        score += 20
    else:
        return 0

    # --------------------------------
    # Skill Match (Mandatory)
    # --------------------------------
    skill_score = skill_match_score(
        student.skills,
        job.required_skills
    )

    if skill_score == 0:
        return 0

    score += skill_score

    # --------------------------------
    # CGPA Score
    # --------------------------------
    score += cgpa_score(student.cgpa)

    # --------------------------------
    # Readiness Score
    # --------------------------------
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