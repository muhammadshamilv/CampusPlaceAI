from django.db import models
from institutions.models import Institution

class CollegeRequest(models.Model):
    institution_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    contact_person = models.CharField(max_length=100)
    details = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        creating = self.pk is None
        old_status = None

        if not creating:
            old_status = CollegeRequest.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        # 🔥 Auto create Institution when approved
        if self.status == "approved" and (creating or old_status != "approved"):
            Institution.objects.get_or_create(
                email=self.email,
                defaults={
                    "name": self.institution_name,
                    "contact_person": self.contact_person,
                    "details": self.details,
                    "status": "approved"
                }
            )

    def __str__(self):
        return f"{self.institution_name} - {self.status}"
