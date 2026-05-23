from django.shortcuts import render, redirect, get_object_or_404
from requests.models import CollegeRequest
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from students.models import Student, StudentCorrectionRequest
from institutions.models import Institution
from jobs.models import Job
from django.db import transaction

User = get_user_model()


# -------------------
# HOME
# -------------------
def home(request):
    return render(request, "index.html")


# -------------------
# COMPANY LOGIN (Correct Old Workflow)
# -------------------
def company_login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")

        # 1. Email required
        if not email:
            return render(request, "company/company-login.html", {
                "error": "Email is required"
            })

        # 2. Check ADMIN user exists
        user = User.objects.filter(username=email, role="ADMIN").first()

        if not user:
            return render(request, "company/company-login.html", {
                "error": "Admin account not found"
            })

        # 3. If password not set → go to setup
        if not user.has_usable_password():
            return redirect(f"/core/setup-password/?email={email}&role=ADMIN")

        # 4. Password required
        if not password:
            return render(request, "company/company-login.html", {
                "error": "Password is required"
            })

        # 5. Authenticate
        auth_user = authenticate(username=email, password=password)

        if auth_user is None:
            return render(request, "company/company-login.html", {
                "error": "Incorrect password"
            })

        login(request, auth_user)
        return redirect("company_dashboard")

    return render(request, "company/company-login.html")





# -------------------
# COMPANY DASHBOARD
# -------------------
@login_required
def company_dashboard(request):
    if request.user.role != "ADMIN":
        return redirect("company_login")

    total_institutions = Institution.objects.filter(status="approved").count()
    total_students = Student.objects.count()
    total_jobs = Job.objects.count()
    pending_requests = CollegeRequest.objects.filter(status="pending").count()

    # ⭐ Correction requests
    corrections = StudentCorrectionRequest.objects.filter(status="Pending").select_related("student", "student__institution")
    correction_count = corrections.count()

    return render(request, "company/company-dashboard.html", {
        "total_institutions": total_institutions,
        "total_students": total_students,
        "total_jobs": total_jobs,
        "pending_requests": pending_requests,
        "corrections": corrections,
        "correction_count": correction_count
    })


# -------------------
# COLLEGE REQUEST
# -------------------
def college_request(request):
    if request.method == "POST":
        CollegeRequest.objects.create(
            institution_name=request.POST["institution_name"],
            email=request.POST["email"],
            contact_person=request.POST["contact_person"],
            details=request.POST["details"],
        )
        return render(request, "college/college-request.html", {"success": True})

    return render(request, "college/college-request.html")


# -------------------
# COLLEGE LOGIN
# -------------------
def college_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)
        if user and user.role == "COLLEGE":
            login(request, user)
            return redirect("/college/dashboard/")

        # If password not set → setup
        inst = Institution.objects.filter(email=email, status="approved").first()
        if inst:
            user = User.objects.filter(username=email, role="COLLEGE").first()
            if user and not user.has_usable_password():
                return redirect(f"/core/setup-password/?email={email}&role=COLLEGE")

        return render(request, "college/college-login.html", {
            "error": "Invalid email or password"
        })

    return render(request, "college/college-login.html")


# -------------------
# COLLEGE REQUEST LIST
# -------------------
@login_required
def company_college_requests(request):
    if request.user.role != "ADMIN":
        return redirect("company_login")

    requests = CollegeRequest.objects.all().order_by("-created_at")
    return render(request, "company/college-requests.html", {
        "requests": requests
    })


# -------------------
# APPROVE / REJECT COLLEGE
# -------------------
@login_required
def approve_college_request(request, request_id):
    if request.user.role != "ADMIN":
        return redirect("company_login")

    req = get_object_or_404(CollegeRequest, id=request_id)
    req.status = "approved"
    req.save()

    institution = Institution.objects.filter(email=req.email).first()

    if not institution:
        institution = Institution.objects.create(
            name=req.institution_name,
            email=req.email,
            contact_person=req.contact_person,
            details=req.details,
            status="approved"
        )
    else:
        institution.name = req.institution_name
        institution.contact_person = req.contact_person
        institution.details = req.details
        institution.status = "approved"
        institution.save()

    # Create login user for college
    user = User.objects.filter(username=req.email).first()
    if not user:
        user = User.objects.create(
            username=req.email,
            email=req.email,
            role="COLLEGE"
        )
        user.set_unusable_password()
        user.save()

    institution.user = user
    institution.save()

    return redirect("company_college_requests")


@login_required
def reject_college_request(request, request_id):
    if request.user.role != "ADMIN":
        return redirect("company_login")

    req = get_object_or_404(CollegeRequest, id=request_id)
    req.status = "rejected"
    req.save()
    return redirect("company_college_requests")


# -------------------
# ADD STUDENT
# -------------------
@login_required
def company_add_student(request):
    if request.user.role != "ADMIN":
        return redirect("company_login")

    if request.method == "POST":
        institution_code = request.POST.get("institution_code")
        email = request.POST.get("email")

        institution = Institution.objects.filter(
            institution_code=institution_code,
            status="approved"
        ).first()

        if not institution:
            return render(request, "company/add-student.html", {"error": "Invalid Institution Code"})

        if Student.objects.filter(email=email).exists():
            return render(request, "company/add-student.html", {"error": "Student already exists"})

        data = {
            "full_name": request.POST.get("full_name"),
            "phone": request.POST.get("phone"),
            "dob": request.POST.get("dob") or None,
            "gender": request.POST.get("gender"),
            "qualification": request.POST.get("qualification"),
            "cgpa": request.POST.get("cgpa"),
            "backlogs": request.POST.get("backlogs"),
            "skills": request.POST.get("skills"),
            "courses": request.POST.get("courses"),
            "internship": request.POST.get("internship"),
            "resume": request.FILES.get("resume"),
        }

        with transaction.atomic():
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    "email": email,
                    "role": "STUDENT",
                }
            )

            if created:
                user.set_unusable_password()
                user.save()

            Student.objects.create(
                user=user,
                institution=institution,
                email=email,
                resume_score=0,
                readiness="Improving",
                **data
            )

        return redirect("company_manage_students")

    return render(request, "company/add-student.html")


# -------------------
# MANAGE STUDENTS
# -------------------
@login_required
def company_manage_students(request):
    if request.user.role != "ADMIN":
        return redirect("company_login")

    students = Student.objects.select_related("institution", "user").all()
    return render(request, "company/manage-students.html", {"students": students})


# -------------------
# VIEW / EDIT STUDENT
# -------------------
@login_required
def company_view_student(request, student_id):
    if request.user.role != "ADMIN":
        return redirect("company_login")

    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        student.full_name = request.POST.get("full_name")
        student.phone = request.POST.get("phone")
        student.cgpa = request.POST.get("cgpa")
        student.backlogs = request.POST.get("backlogs")
        student.skills = request.POST.get("skills")
        student.courses = request.POST.get("courses")
        student.internship = request.POST.get("internship")

        # Keep old readiness if not provided
        readiness_value = request.POST.get("readiness")
        if readiness_value:
            student.readiness = readiness_value

        # Resume update
        if request.FILES.get("resume"):
            student.resume = request.FILES["resume"]

        student.save()

        # Mark correction requests as completed
        StudentCorrectionRequest.objects.filter(
            student=student,
            status="Pending"
        ).update(status="Completed")

        return redirect("company_view_student", student_id=student.id)

    return render(request, "company/student-profile.html", {
        "student": student
    })


# ======================================================
# STUDENT CORRECTION REQUESTS (Admin)
# ======================================================
@login_required
def company_correction_requests(request):
    if request.user.role != "ADMIN":
        return redirect("company_login")

    corrections = StudentCorrectionRequest.objects.select_related(
        "student",
        "student__institution"
    ).order_by("-created_at")

    return render(request, "company/correction-requests.html", {
        "corrections": corrections
    })


@login_required
def mark_correction_done(request, request_id):
    if request.user.role != "ADMIN":
        return redirect("company_login")

    correction = get_object_or_404(StudentCorrectionRequest, id=request_id)
    correction.status = "Completed"
    correction.is_read = True
    correction.save()

    return redirect("company_correction_requests")
