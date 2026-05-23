from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from ai_engine.matcher import match_students_for_job
from .models import Job
from students.models import Student
from ai_engine.matcher import calculate_match_score
from .models import PlacementSelection
from .models import PlacementSelection
from django.views.decorators.http import require_POST


# ----------------------------
# ADMIN ONLY ACCESS CHECK
# ----------------------------
def admin_only(user):
    if not user.is_authenticated or user.role != "ADMIN":
        raise PermissionDenied


# ----------------------------
# POST JOB (System Admin)
# ----------------------------
@login_required
def company_post_job(request):
    admin_only(request.user)

    if request.method == "POST":
        Job.objects.create(
            company_name=request.POST.get("company_name"),
            title=request.POST.get("title"),
            location=request.POST.get("location"),
            branch=request.POST.get("branch"),
            eligibility=request.POST.get("eligibility"),
            required_skills=request.POST.get("required_skills"),
            description=request.POST.get("description", ""),
        )
        messages.success(request, "Job posted successfully.")
        return redirect("company_view_jobs")

    return render(request, "company/post-job.html")


# ----------------------------
# VIEW JOBS (System Admin)
# ----------------------------
@login_required
def company_view_jobs(request):
    admin_only(request.user)

    jobs = Job.objects.all().order_by("-created_at")

    return render(request, "company/view-jobs.html", {
        "jobs": jobs
    })


# ----------------------------
# MATCH STUDENTS FOR JOB (AI)
# ----------------------------
@login_required
def company_match_students(request, job_id):
    admin_only(request.user)

    job = get_object_or_404(Job, id=job_id)

    matched_students = match_students_for_job(job)

    students_with_scores = []

    for student in matched_students:
        score = calculate_match_score(student, job)
        students_with_scores.append({
            "student": student,
            "score": score
        })

    if request.method == "POST":
        selected_ids = request.POST.getlist("students")

        PlacementSelection.objects.filter(job=job).delete()

        for sid in selected_ids:
            student = Student.objects.get(id=sid)
            score = calculate_match_score(student, job)

            PlacementSelection.objects.create(
                job=job,
                student=student,
                match_score=score
            )

        messages.success(request, "Selected students saved successfully.")
        return redirect("company_view_jobs")

    return render(request, "company/job-match.html", {
        "job": job,
        "students_with_scores": students_with_scores,
        "selected_ids": PlacementSelection.objects.filter(job=job)
                          .values_list("student_id", flat=True)
    })


# ----------------------------
# VIEW SELECTED STUDENTS
# ----------------------------
@login_required
def company_selected_students(request):
    admin_only(request.user)

    selections = PlacementSelection.objects.select_related("job", "student")

    jobs_map = {}

    for s in selections:
        jobs_map.setdefault(s.job, []).append(s)

    return render(request, "company/selected-students.html", {
        "jobs_map": jobs_map
    })


@login_required
@require_POST
def delete_job(request, job_id):
    admin_only(request.user)

    job = get_object_or_404(Job, id=job_id)
    job.delete()

    messages.success(request, "Job deleted successfully.")
    return redirect("company_view_jobs")


@login_required
@require_POST
def delete_selection(request, selection_id):
    admin_only(request.user)

    sel = get_object_or_404(PlacementSelection, id=selection_id)
    sel.delete()

    messages.success(request, "Selected student removed.")
    return redirect("company_selected_students")
