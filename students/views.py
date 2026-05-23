from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Student, StudentCorrectionRequest
from institutions.models import Institution
from jobs.models import Job
from core.models import SystemMessage
from ai_engine.resume_parser import extract_resume_text
from ai_engine.scorer import predict_resume_score, predict_readiness
from django.contrib import messages
from ai_engine.job_recommender import recommend_jobs_for_student
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied



User = get_user_model()


# -------------------
# LOGIN
# -------------------
def student_login(request):
    if request.method == "POST":
        institution_code = request.POST.get("institution_code")
        email = request.POST.get("email")
        password = request.POST.get("password")

        institution = Institution.objects.filter(
            institution_code=institution_code,
            status="approved"
        ).first()

        if not institution:
            return render(request, "student/student-login.html", {
                "error": "Invalid Institution Code"
            })

        student = Student.objects.filter(
            institution=institution,
            email=email
        ).first()

        if not student:
            return render(request, "student/student-login.html", {
                "error": "Student not found"
            })

        # Create user if not exists
        if not student.user:
            user = User.objects.create(
                username=email,
                email=email,
                role="STUDENT"
            )
            user.set_unusable_password()
            user.save()
            student.user = user
            student.save()

        # Force password setup
        if not student.user.has_usable_password():
            return redirect(f"/core/setup-password/?email={email}&role=STUDENT")

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect("student_dashboard")

        return render(request, "student/student-login.html", {
            "error": "Incorrect password"
        })

    return render(request, "student/student-login.html")


# -------------------
# DASHBOARD
# -------------------
@login_required
def student_dashboard(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return redirect("student_login")

    matched_jobs = Job.objects.filter(
        status="Open",
        branch__icontains=student.qualification
    )

    messages = SystemMessage.objects.filter(user=request.user)

    # Pending correction requests count
    pending_corrections = student.correction_requests.filter(status="Pending").count()

    return render(request, "student/student-dashboard.html", {
        "student": student,
        "matched_jobs": matched_jobs,
        "messages": messages,
        "pending_corrections": pending_corrections
    })


# -------------------
# PROFILE
# -------------------
@login_required
def student_profile(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return redirect("student_login")

    return render(request, "student/view-profile.html", {
        "student": student
    })


# ======================================================
# CORRECTION REQUEST (Improved)
# ======================================================
@login_required
def student_correction_request(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return redirect("student_login")

    if request.method == "POST":
        field = request.POST.get("field", "").strip()
        correct_value = request.POST.get("correct_value", "").strip()
        message = request.POST.get("message", "").strip()

        # Validation
        if not field or not correct_value:
            return render(request, "student/correction-request.html", {
                "error": "Field and correct value are required"
            })

        # Save request
        StudentCorrectionRequest.objects.create(
            student=student,
            field=field,
            correct_value=correct_value,
            message=message,
            status="Pending",
            is_read=False
        )

        # Notify ADMIN (Owner)
        admins = User.objects.filter(role="ADMIN")
        for admin in admins:
            SystemMessage.objects.create(
                user=admin,
                title="Student Correction Request",
                message=f"{student.full_name} ({student.institution.name}) requested correction for {field}"
            )

        return redirect("student_dashboard")

    return render(request, "student/correction-request.html")


# ======================================================
# AI RESUME ANALYSIS
# ======================================================

@login_required
def student_resume_analysis(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return redirect("student_login")

    recommended_jobs = []

    # =========================
    # When Analyze button clicked
    # =========================
    if request.method == "POST":
        print("AI Analysis Started")

        if not student.resume:
            messages.error(request, "Please upload a resume first.")
            return redirect("student_resume_analysis")

        try:
            from ai_engine.resume_parser import extract_text_from_pdf
            from ai_engine.scorer import predict_resume_score, predict_readiness

            resume_path = student.resume.path
            text = extract_text_from_pdf(resume_path)

            if not text:
                messages.error(request, "Could not read resume.")
                return redirect("student_resume_analysis")

            # Predict score
            score = predict_resume_score(text, student)
            readiness = predict_readiness(score)

            student.resume_score = score
            student.readiness = readiness
            student.save()

            messages.success(request, "Resume analyzed successfully!")

        except Exception as e:
            print("AI ERROR:", e)
            messages.error(request, f"AI Error: {str(e)}")

        return redirect("student_resume_analysis")

    # =========================
    # IMPORTANT: Show recommendations on GET
    # =========================
    if student.resume_score and student.resume_score > 0:
        recommended_jobs = recommend_jobs_for_student(student)

    return render(request, "student/resume-analysis.html", {
        "student": student,
        "recommended_jobs": recommended_jobs
    })


@login_required
@require_POST
def delete_student(request, student_id):
    if request.user.role != "ADMIN":
        raise PermissionDenied

    student = get_object_or_404(Student, id=student_id)
    student.delete()

    messages.success(request, "Student deleted successfully.")
    return redirect("company_manage_students")