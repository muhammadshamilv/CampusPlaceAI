from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Institution
from students.models import Student
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from requests.models import CollegeRequest
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.contrib import messages


# --------------------------------------------------
# Utility: Get institution for logged-in college user
# --------------------------------------------------
def get_institution_for_user(request):
    if not request.user.is_authenticated:
        return None

    institution = Institution.objects.filter(user=request.user).first()

    # Auto-link institution by email if not linked
    if not institution:
        institution = Institution.objects.filter(email=request.user.email).first()
        if institution:
            institution.user = request.user
            institution.save()

    return institution


# --------------------------------------------------
# COLLEGE DASHBOARD
# --------------------------------------------------
@login_required
def college_dashboard(request):
    institution = get_institution_for_user(request)

    if not institution:
        return redirect("college_login")

    total_students = Student.objects.filter(institution=institution).count()

    students_with_resume = Student.objects.filter(
        institution=institution,
        resume__isnull=False
    ).count()

    context = {
        "institution": institution,
        "total_students": total_students,
        "students_with_resume": students_with_resume,
        "drives": 0
    }

    return render(request, "college/college-dashboard.html", context)


# --------------------------------------------------
# VIEW STUDENTS
# --------------------------------------------------
@login_required
def college_view_students(request):
    institution = get_institution_for_user(request)

    if not institution:
        return redirect("college_login")

    students = Student.objects.filter(
        institution=institution
    ).order_by("full_name")

    return render(request, "college/view-students.html", {
        "students": students
    })


# --------------------------------------------------
# VIEW STUDENT PROFILE
# --------------------------------------------------
@login_required
def college_view_student(request, student_id):
    institution = get_institution_for_user(request)

    if not institution:
        return redirect("college_login")

    student = get_object_or_404(
        Student,
        id=student_id,
        institution=institution
    )

    return render(request, "college/student-profile.html", {
        "student": student
    })


@login_required
@require_POST
def delete_institution_request(request, request_id):
    if request.user.role != "ADMIN":
        raise PermissionDenied

    req = get_object_or_404(CollegeRequest, id=request_id)
    req.delete()

    messages.success(request, "Institution request deleted.")
    return redirect("company_college_requests")