from django.urls import path
from .views import get_messages, mark_read, delete_message, setup_password

urlpatterns = [
    path("messages/", get_messages, name="get_messages"),
    path("messages/read/<int:msg_id>/", mark_read),
    path("messages/delete/<int:msg_id>/", delete_message),

    # 🔐 Global password setup
    path("setup-password/", setup_password, name="setup_password"),
]
