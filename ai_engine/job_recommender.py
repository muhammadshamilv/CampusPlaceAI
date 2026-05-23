from jobs.models import Job


def recommend_jobs_for_student(student):
    """
    Recommend jobs based on:
    - Branch match
    - Skills match
    - Only Open jobs
    """

    recommended_jobs = []

    jobs = Job.objects.filter(status="Open")

    student_skills = student.skills.lower()
    student_branch = student.qualification.lower()

    for job in jobs:
        score = 0

        # Branch match
        if job.branch.lower() in student_branch:
            score += 40

        # Skills match
        job_text = (job.description + " " + job.eligibility).lower()
        skill_matches = sum(
            1 for word in job_text.split()
            if word in student_skills
        )

        score += min(skill_matches * 2, 60)

        if score > 20:
            recommended_jobs.append((job, score))

    # Sort by score
    recommended_jobs.sort(key=lambda x: x[1], reverse=True)

    # Return only job objects (top 5)
    return [job for job, score in recommended_jobs[:5]]
