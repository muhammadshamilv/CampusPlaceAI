from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from .models import Institution

User = get_user_model()


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'created_at')
    list_filter = ('status',)

    def save_model(self, request, obj, form, change):

        # When approving and no user yet → create login
        if obj.status == "approved" and obj.user is None:

            password = get_random_string(10)   # Django-6 safe

            user = User.objects.create_user(
                username=obj.email,
                email=obj.email,
                password=password,
                role="COLLEGE"
            )

            obj.user = user

            print("\n=== COLLEGE LOGIN CREATED ===")
            print("Email:", obj.email)
            print("Password:", password)
            print("============================\n")

        super().save_model(request, obj, form, change)
