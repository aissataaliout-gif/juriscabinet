from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from appointments.models import Appointment
from clients.models import Client
from lawyers.models import Lawyer
from dossiers.models import Dossier
from documents.models import Document
from django.db.models.functions import TruncMonth
from django.db.models import Count
from .forms import ClientSignUpForm


def home(request):
    return render(request, "home/home.html")

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

            if user.role == "ADMIN":
                return redirect("admin_dashboard")

            elif user.role == "LAWYER":
                return redirect("lawyer_dashboard")

            elif user.role == "CLIENT":
                return redirect("client_dashboard")

            else:
                messages.error(
                    request,
                    "Rôle utilisateur non reconnu."
                )
                return redirect("login")

        else:
            return render(
                request,
                "accounts/login.html",
                {
                    "error": "Nom d’utilisateur ou mot de passe incorrect."
                }
            )

    return render(
        request,
        "accounts/login.html"
    )

from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    clients_count = Client.objects.count()
    lawyers_count = Lawyer.objects.count()
    dossiers_count = Dossier.objects.count()
    appointments_count = Appointment.objects.count()
    documents_count = Document.objects.count()

    recent_dossiers = Dossier.objects.order_by("-id")[:5]
    recent_appointments = Appointment.objects.order_by("-id")[:5]

    # Statistiques mensuelles des dossiers
    monthly_cases = (
        Dossier.objects
        .annotate(month=TruncMonth("opening_date"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    labels = []
    values = []

    for item in monthly_cases:
        labels.append(item["month"].strftime("%b"))
        values.append(item["total"])

    context = {
        "clients_count": clients_count,
        "lawyers_count": lawyers_count,
        "dossiers_count": dossiers_count,
        "appointments_count": appointments_count,
        "documents_count": documents_count,
        "recent_dossiers": recent_dossiers,
        "recent_appointments": recent_appointments,
        "chart_labels": labels,
        "chart_values": values,
    }


    context["recent_dossiers"] = Dossier.objects.order_by("-id")[:5]
    context["recent_appointments"] = Appointment.objects.order_by("-id")[:5]
    return render(request, "accounts/dashboard_admin_v3.html", context)

def register_view(request):
    if request.method == "POST":
        form = ClientSignUpForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("login")

    else:
        form = ClientSignUpForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )