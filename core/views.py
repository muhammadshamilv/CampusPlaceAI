from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate
from .models import SystemMessage

User = get_user_model()


# -----------------------
# 🔔 MESSAGE SYSTEM
# -----------------------
@login_required
def get_messages(request):
    messages = SystemMessage.objects.filter(user=request.user).order_by("-created_at")

    data = []
    for m in messages:
        data.append({
            "id": m.id,
            "title": m.title,
            "message": m.message,
            "is_read": m.is_read,
            "created_at": m.created_at.strftime("%d %b %Y %H:%M")
        })

    return JsonResponse(data, safe=False)


@login_required
def mark_read(request, msg_id):
    msg = SystemMessage.objects.get(id=msg_id, user=request.user)
    msg.is_read = True
    msg.save()
    return JsonResponse({"status": "ok"})


@login_required
def delete_message(request, msg_id):
    msg = SystemMessage.objects.get(id=msg_id, user=request.user)
    msg.delete()
    return JsonResponse({"status": "deleted"})


# -----------------------
# 🔐 GLOBAL SET PASSWORD (Correct Workflow)
# -----------------------
def setup_password(request):
    role = request.GET.get("role") or request.POST.get("role")
    email = request.GET.get("email") or request.POST.get("email")

    # Email required
    if not email:
        return render(request, "common/setup-password.html", {
            "error": "Email is required",
        })

    # Check user exists
    user = User.objects.filter(username=email).first()

    if not user:
        return render(request, "common/setup-password.html", {
            "error": "Account not found. Please contact administrator.",
            "email": email,
            "role": role
        })

    # POST → set password
    if request.method == "POST":
        p1 = request.POST.get("password")
        p2 = request.POST.get("confirm")

        if not p1 or not p2:
            return render(request, "common/setup-password.html", {
                "error": "Both password fields are required",
                "email": email,
                "role": role
            })

        if p1 != p2:
            return render(request, "common/setup-password.html", {
                "error": "Passwords do not match",
                "email": email,
                "role": role
            })

        # Set password
        user.set_password(p1)

        # Update role if provided
        if role:
            user.role = role

        user.save()

        # Authenticate
        auth_user = authenticate(username=email, password=p1)
        if not auth_user:
            return render(request, "common/setup-password.html", {
                "error": "Authentication failed",
                "email": email,
                "role": role
            })

        login(request, auth_user)

        # Redirect by role
        if user.role == "ADMIN":
            return redirect("/company/dashboard/")
        elif user.role == "COLLEGE":
            return redirect("/college/dashboard/")
        elif user.role == "STUDENT":
            return redirect("/student/dashboard/")
        else:
            return redirect("/")

    # GET request
    return render(request, "common/setup-password.html", {
        "email": email,
        "role": role
    })
