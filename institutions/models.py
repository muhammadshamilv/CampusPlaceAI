from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string


class Institution(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="institution"
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_person = models.CharField(max_length=255)
    details = models.TextField(blank=True)

    institution_code = models.CharField(max_length=20, unique=True, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    password_set = models.BooleanField(default=False)   # 🔥 NEW

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status == "approved" and not self.institution_code:
            base = self.name.replace(" ", "").upper()[:5]
            self.institution_code = f"{base}{get_random_string(4).upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
