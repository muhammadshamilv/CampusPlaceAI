from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # 🔐 Logins
    path("company/login/", views.company_login, name="company_login"),
    path("college/login/", views.college_login, name="college_login"),

    # 🏢 Company (Owner)
    path("company/dashboard/", views.company_dashboard, name="company_dashboard"),
    path("company/college-requests/", views.company_college_requests, name="company_college_requests"),
    path("company/approve/<int:request_id>/", views.approve_college_request, name="approve_college_request"),
    path("company/reject/<int:request_id>/", views.reject_college_request, name="reject_college_request"),
    path("company/add-student/", views.company_add_student, name="company_add_student"),
    path("company/students/", views.company_manage_students, name="company_manage_students"),
    path("company/students/<int:student_id>/", views.company_view_student, name="company_view_student"),

    # ⭐ NEW – Correction Requests
    path("company/corrections/", views.company_correction_requests, name="company_correction_requests"),
    path("company/corrections/done/<int:request_id>/", views.mark_correction_done, name="mark_correction_done"),

    # 🏫 College
    path("college/request/", views.college_request, name="college_request"),
]
