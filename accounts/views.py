from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("admin_dashboard")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Nom d'utilisateur ou mot de passe incorrect."
            }
        )

    return render(request, "accounts/login.html")

from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    return render(request, "accounts/dashboard_admin.html")