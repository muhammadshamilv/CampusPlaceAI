from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.student_login, name="student_login"),
    path("dashboard/", views.student_dashboard, name="student_dashboard"),
    path("profile/", views.student_profile, name="student_profile"),

    # Correction Request
    path("correction-request/", views.student_correction_request, name="student_correction_request"),

    # AI Resume Analysis
    path("resume-analysis/", views.student_resume_analysis, name="student_resume_analysis"),
    
    path("delete/<int:student_id>/", views.delete_student, name="delete_student"),
]
