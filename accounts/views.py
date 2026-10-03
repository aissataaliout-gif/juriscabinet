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
from django.contrib.auth.decorators import login_required
from .models import ContactMessage
from django.core.mail import send_mail

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

@login_required
def admin_dashboard(request):
    if request.user.role != "ADMIN":
        return redirect("home")
    
    clients_count = Client.objects.count()
    lawyers_count = Lawyer.objects.count()
    dossiers_count = Dossier.objects.count()
    dossiers_encours = Dossier.objects.filter(status="EN_COURS").count()
    dossiers_attente = Dossier.objects.filter(status="OUVERT").count()
    dossiers_clotures = Dossier.objects.filter(status="FERME").count()
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
        "dossiers_encours": dossiers_encours,
        "dossiers_attente": dossiers_attente,
        "dossiers_clotures": dossiers_clotures,
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
@login_required
def profile_view(request):

    if request.method == "POST":
        if request.FILES.get("profile_picture"):
            request.user.profile_picture = request.FILES["profile_picture"]

        request.user.phone = request.POST.get("phone", request.user.phone)
        request.user.save()

        messages.success(request, "Profil mis à jour.")
        return redirect("profile")

    return render(request, "accounts/profile.html")

def contact_submit(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        message_text = request.POST.get("message", "").strip()

        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message_text,
            )
            try:
                send_mail(
                    subject="Nous avons bien reçu votre message",
                    message=(
                        f"Bonjour {name},\n\n"
                        "Merci de nous avoir contactés. Votre message a bien "
                        "été reçu par notre cabinet, et un membre de notre "
                        "équipe reviendra vers vous dans les plus brefs délais.\n\n"
                        "Cordialement,\n"
                        "L'équipe JurisCabinet"
                    ),
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(
                request,
                "Votre message a bien été envoyé. Nous vous répondrons rapidement."
            )
        else:
            messages.error(
                request,
                "Merci de remplir tous les champs."
            )

    return redirect("home")