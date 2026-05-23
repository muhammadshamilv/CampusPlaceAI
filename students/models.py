from django.db import models
from django.conf import settings
from institutions.models import Institution


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="students"
    )

    # --------------------
    # Basic Details
    # --------------------
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    dob = models.DateField(null=True, blank=True)

    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        blank=True
    )

    # --------------------
    # Academic Details
    # --------------------
    qualification = models.CharField(max_length=255)
    cgpa = models.FloatField()
    backlogs = models.IntegerField(default=0)

    # --------------------
    # Career Details
    # --------------------
    skills = models.TextField()
    courses = models.TextField(blank=True)
    internship = models.TextField(blank=True)

    # --------------------
    # Resume
    # --------------------
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)

    # --------------------
    # Placement Status
    # --------------------
    resume_score = models.IntegerField(default=0)
    readiness = models.CharField(
        max_length=20,
        choices=[
            ("Ready", "Ready"),
            ("Improving", "Improving"),
            ("Not Ready", "Not Ready")
        ],
        default="Improving"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        # Check if resume changed
        if self.pk:
            old = Student.objects.filter(pk=self.pk).first()
            if old and old.resume != self.resume:
                # Reset AI results when resume changes
                self.resume_score = 0
                self.readiness = "Improving"

        super().save(*args, **kwargs)


# =====================================================
# CORRECTION REQUEST MODEL (UPDATED – IMPORTANT)
# =====================================================
class StudentCorrectionRequest(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Read", "Read"),
        ("Resolved", "Resolved"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="correction_requests"
    )

    # What field needs correction
    field = models.CharField(max_length=100)

    # What student wants it changed to
    correct_value = models.CharField(max_length=255)

    # Optional explanation
    message = models.TextField(blank=True)

    # Admin tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    # Read indicator (for notification badge)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.field}"
