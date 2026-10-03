from django.shortcuts import render, redirect, get_object_or_404
from .models import Lawyer
from .forms import LawyerForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from dossiers.models import Dossier
from appointments.models import Appointment
from django.http import HttpResponseForbidden

@login_required
def lawyer_list(request):
    if request.user.role not in ["ADMIN", "LAWYER"]:
        return HttpResponseForbidden("Accès refusé.")

    lawyers = Lawyer.objects.all()
    return render(request, "lawyers/lawyer_list.html", {"lawyers": lawyers})


@login_required
def lawyer_create(request):
    if request.user.role != "ADMIN":
        return HttpResponseForbidden("Accès refusé.")

    if request.method == "POST":
        form = LawyerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "L'avocat a été ajouté avec succès.")
            return redirect("lawyer_list")
    else:
        form = LawyerForm()

    return render(request, "lawyers/lawyer_form.html", {"form": form})


@login_required
def lawyer_update(request, pk):
    if request.user.role != "ADMIN":
        return HttpResponseForbidden("Accès refusé.")

    lawyer = get_object_or_404(Lawyer, pk=pk)

    if request.method == "POST":
        form = LawyerForm(request.POST, request.FILES, instance=lawyer)
        if form.is_valid():
            form.save()
            messages.success(request, "L'avocat a été modifié avec succès.")
            return redirect("lawyer_list")
    else:
        form = LawyerForm(instance=lawyer)

    return render(request, "lawyers/lawyer_form.html", {"form": form})


@login_required
def lawyer_delete(request, pk):
    if request.user.role != "ADMIN":
        return HttpResponseForbidden("Accès refusé.")

    lawyer = get_object_or_404(Lawyer, pk=pk)

    if request.method == "POST":
        lawyer.delete()
        messages.success(request, "L'avocat a été supprimé avec succès.")
        return redirect("lawyer_list")

    return render(request, "lawyers/lawyer_confirm_delete.html", {"lawyer": lawyer})

@login_required
def lawyer_dashboard(request):
    if request.user.role != "LAWYER":
        return redirect("home")
    
    lawyer = getattr(request.user, "lawyer_profile", None)

    if lawyer:
        dossiers = Dossier.objects.filter(lawyer=lawyer)
    else:
        # Compte avocat pas encore relié à une fiche Lawyer :
        # on affiche tout, en attendant que le lien soit fait.
        dossiers = Dossier.objects.all()

    appointments = Appointment.objects.filter(dossier__in=dossiers)

    today = timezone.localdate()
    today_appointments = appointments.filter(
        appointment_date__date=today
    ).order_by("appointment_date")

    clients_count = dossiers.values("client").distinct().count()
    recent_dossiers = dossiers.order_by("-id")[:5]

    return render(
        request,
        "lawyers/lawyer_dashboard.html",
        {
            "lawyer": lawyer,
            "dossiers_count": dossiers.count(),
            "appointments_count": appointments.count(),
            "clients_count": clients_count,
            "recent_dossiers": recent_dossiers,
            "today_appointments": today_appointments,
        },
    )