from django.db import models
from students.models import Student


class Job(models.Model):
    company_name = models.CharField(max_length=255)

    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    branch = models.CharField(max_length=100)

    eligibility = models.TextField()

    required_skills = models.TextField(help_text="Comma separated skills")

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=[("Open", "Open"), ("Closed", "Closed")],
        default="Open"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.title}"


#  NEW TABLE
class PlacementSelection(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    match_score = models.IntegerField()
    selected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job.title} - {self.student.full_name}"