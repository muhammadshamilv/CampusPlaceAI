from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "institution",
        "cgpa",
        "resume_score",
        "readiness",
        "created_at",
    )

    search_fields = (
        "full_name",
        "email",
        "institution__name",
    )

    list_filter = (
        "institution",
        "readiness",
    )
