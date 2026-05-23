from django.urls import path
from . import views
from django.core.exceptions import PermissionDenied


# 🔒 Allow only COLLEGE users
def college_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "COLLEGE":
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


urlpatterns = [
    # Dashboard
    path(
        "dashboard/",
        college_required(views.college_dashboard),
        name="college_dashboard"
    ),

    # Student list
    path(
        "students/",
        college_required(views.college_view_students),
        name="college_view_students"
    ),

    # Student profile
    path(
        "student/<int:student_id>/",
        college_required(views.college_view_student),
        name="college_view_student"
    ),

    path(
        "delete-request/<int:request_id>/",
        views.delete_institution_request,
        name="delete_institution_request"
    ),
]
