from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'title',
        'location',
        'branch',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'location',
        'branch',
        'company_name'
    )

    search_fields = (
        'title',
        'company_name',
        'branch'
    )

    ordering = ('-created_at',)
