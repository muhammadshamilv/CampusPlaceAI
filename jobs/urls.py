from django.urls import path
from . import views

urlpatterns = [
    # Company / Admin Job Management
    path("post/", views.company_post_job, name="company_post_job"),
    path("list/", views.company_view_jobs, name="company_view_jobs"),

    # Match Students (FIXED syntax)
    path("match/<int:job_id>/", views.company_match_students, name="company_match_students"),

    # Selected Students
    path("selected/", views.company_selected_students, name="company_selected_students"),
    
    path("delete/<int:job_id>/", views.delete_job, name="delete_job"),
    path("selection/delete/<int:selection_id>/", views.delete_selection, name="delete_selection"),
]
